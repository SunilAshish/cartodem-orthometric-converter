# CartoDEM Orthometric Converter

Small Python CLI to convert CartoDEM GeoTIFF DEMs from WGS84 ellipsoidal heights to orthometric heights using `gdalwarp` and a geoid grid such as `egm96_15.gtx`.

This repository is designed to be simple, reproducible, and portfolio-friendly. It wraps the GDAL workflow into a script you can run on a single DEM or a whole folder of CartoDEM tiles.

## Why this repository exists

CartoDEM and related Cartosat DEM workflows are often shared as terminal commands in articles or forum posts. This repository turns that workflow into:

- a documented Python script
- a reproducible command-line workflow
- a clean GitHub project you can show on your profile

## Method and references

This repository is based on the workflow described in:

- Ujaval Gandhi, "Convert between Orthometric and Ellipsoidal Elevations using GDAL", Spatial Thoughts, 2019.  
  https://spatialthoughts.com/2019/10/26/convert-between-orthometric-and-ellipsoidal-elevations-using-gdal/

Supporting documentation:

- GDAL `gdalwarp` documentation  
  https://gdal.org/en/stable/programs/gdalwarp.html
- PROJ resource and grid documentation  
  https://proj.org/en/stable/resource_files.html

## Important note

This script assumes the source DEM heights are ellipsoidal and converts them to orthometric heights using a geoid grid. Before using the results in production, confirm the source vertical reference from the official product specification for your dataset.

## Repository structure

```text
cartodem-orthometric-converter/
  README.md
  .gitignore
  LICENSE
  convert_cartodem.py
  CITATION.cff
```

## Requirements

- Python 3.9+
- GDAL command-line tools available on `PATH`
- `gdalwarp`
- PROJ grid file such as `egm96_15.gtx`, or `PROJ_NETWORK=ON`

Check GDAL:

```powershell
gdalwarp --version
```

## Usage

### 1. Convert one DEM

```powershell
python convert_cartodem.py `
  --input "data\sample_tile\P5_PAN_CD_N28_250_E076_875_DEM.tif"
```

### 2. Convert all CartoDEM tiles in a folder

```powershell
python convert_cartodem.py `
  --input "data" `
  --recursive `
  --proj-network
```

### 3. Use a local geoid grid file

```powershell
python convert_cartodem.py `
  --input "data" `
  --recursive `
  --grid "C:\path\to\egm96_15.gtx"
```

### 4. Dry run first

```powershell
python convert_cartodem.py `
  --input "data" `
  --recursive `
  --proj-network `
  --dry-run
```

## What the script runs

The script builds a GDAL command equivalent to:

```powershell
gdalwarp -overwrite -r bilinear `
  -s_srs "+proj=longlat +datum=WGS84 +no_defs" `
  -t_srs "+proj=longlat +datum=WGS84 +no_defs +geoidgrids=egm96_15.gtx" `
  input_dem.tif output_dem_orthometric.tif
```
## Example Path based Script
python convert_cartodem.py --input "F:\Work\Topography\Cartosat_Raw_Data\254559911\P5_PAN_CD_625_DEM.tif" --proj-network

python convert_cartodem.py --input "G:\carto_data_cartosat" --recursive --proj-network

## Output naming

- Single file input: `name_orthometric.tif`
- Folder input: creates outputs in `orthometric_output/`

## Suggested GitHub repository description

`Python + GDAL workflow to convert CartoDEM GeoTIFF DEMs from ellipsoidal to orthometric heights using EGM96 geoid grids.`

## How to create the GitHub repository

### Option A: Create on github.com

1. Sign in to GitHub.
2. Click `New repository`.
3. Repository name: `cartodem-orthometric-converter`
4. Add a short description.
5. Keep it `Public`.
6. Do not initialize with another README, because this folder already has one.
7. Click `Create repository`.

### Option B: Push this local folder after creating the empty repo online

From inside this folder:

```powershell
git init
git add .
git commit -m "Initial commit: CartoDEM orthometric conversion CLI"
git branch -M main
git remote add origin https://github.com/SunilAshish/cartodem-orthometric-converter.git
git push -u origin main
```

If GitHub asks for authentication, use GitHub Desktop, Git Credential Manager, or a personal access token.

## How to make this project stronger for your profile

- Add a screenshot of the DEM before and after conversion in QGIS
- Add one sample notebook or figure comparing CartoDEM and SRTM
- Add a short "Why this matters" section for hydrology, flood, and terrain workflows
- Add a release tag such as `v0.1.0`
- Share the project on LinkedIn with one image and one paragraph of explanation

## Career note

A strong profile is built by showing clear, useful, reproducible work. Small technical repositories like this are valuable because they show:

- problem framing
- geospatial tooling
- automation
- documentation
- open technical communication

That combination helps both academic and industry applications.
