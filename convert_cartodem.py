from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_SOURCE_SRS = "+proj=longlat +datum=WGS84 +no_defs"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert CartoDEM DEM GeoTIFFs from WGS84 ellipsoidal heights "
            "to orthometric heights using gdalwarp and a geoid grid."
        )
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to a single DEM GeoTIFF or a directory containing CartoDEM tiles.",
    )
    parser.add_argument(
        "--output-dir",
        help="Optional output directory for converted files. Used for directory mode.",
    )
    parser.add_argument(
        "--grid",
        default="egm96_15.gtx",
        help="Geoid grid filename or full path. Default: egm96_15.gtx",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search for DEM tiles recursively when input is a directory.",
    )
    parser.add_argument(
        "--pattern",
        default="*_DEM.tif",
        help="Glob pattern used in directory mode. Default: *_DEM.tif",
    )
    parser.add_argument(
        "--proj-network",
        action="store_true",
        help="Set PROJ_NETWORK=ON for this process so grids can be fetched if supported.",
    )
    parser.add_argument(
        "--resampling",
        default="bilinear",
        choices=["near", "bilinear", "cubic", "cubicspline", "lanczos"],
        help="Resampling method passed to gdalwarp. Default: bilinear",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing them.",
    )
    return parser.parse_args()


def ensure_gdalwarp() -> None:
    if shutil.which("gdalwarp") is None:
        sys.exit("Error: gdalwarp was not found on PATH.")


def build_target_srs(grid: str) -> str:
    return f"+proj=longlat +datum=WGS84 +no_defs +geoidgrids={grid}"


def find_inputs(input_path: Path, recursive: bool, pattern: str) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    if not input_path.is_dir():
        sys.exit(f"Error: input path does not exist: {input_path}")

    matches = input_path.rglob(pattern) if recursive else input_path.glob(pattern)
    files = sorted(p for p in matches if p.is_file())
    if not files:
        sys.exit(f"Error: no files matched pattern '{pattern}' in {input_path}")
    return files


def output_path_for(src: Path, input_root: Path, output_dir: Path | None) -> Path:
    if input_root.is_file():
        return src.with_name(f"{src.stem}_orthometric{src.suffix}")

    base_output_dir = output_dir if output_dir else input_root / "orthometric_output"
    relative_parent = src.parent.relative_to(input_root)
    final_dir = base_output_dir / relative_parent
    final_dir.mkdir(parents=True, exist_ok=True)
    return final_dir / f"{src.stem}_orthometric{src.suffix}"


def run_conversion(
    src: Path,
    dst: Path,
    source_srs: str,
    target_srs: str,
    resampling: str,
    dry_run: bool,
    env: dict[str, str],
) -> int:
    command = [
        "gdalwarp",
        "-overwrite",
        "-r",
        resampling,
        "-s_srs",
        source_srs,
        "-t_srs",
        target_srs,
        str(src),
        str(dst),
    ]

    print("Running:")
    print(" ".join(f'"{item}"' if " " in item else item for item in command))

    if dry_run:
        return 0

    result = subprocess.run(command, env=env, check=False)
    return result.returncode


def main() -> int:
    args = parse_args()
    ensure_gdalwarp()

    input_path = Path(args.input).resolve()
    files = find_inputs(input_path, args.recursive, args.pattern)

    output_dir = Path(args.output_dir).resolve() if args.output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    if args.proj_network:
        env["PROJ_NETWORK"] = "ON"

    target_srs = build_target_srs(args.grid)

    failures = 0
    for src in files:
        dst = output_path_for(src, input_path, output_dir)
        code = run_conversion(
            src=src,
            dst=dst,
            source_srs=DEFAULT_SOURCE_SRS,
            target_srs=target_srs,
            resampling=args.resampling,
            dry_run=args.dry_run,
            env=env,
        )
        if code != 0:
            failures += 1
            print(f"Failed: {src}", file=sys.stderr)

    if failures:
        print(f"Completed with {failures} failure(s).", file=sys.stderr)
        return 1

    print(f"Completed successfully for {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
