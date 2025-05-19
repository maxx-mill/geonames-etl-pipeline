# Geonames ETL Pipeline

This Python script provides a simple ETL (Extract, Transform, Load) pipeline for downloading and processing [GeoNames](https://www.geonames.org/) geographical data. It allows you to extract location data for specific countries and feature types and convert it to various geospatial formats.

## Features

- Downloads the complete GeoNames dataset (allCountries.zip)
- Filters data by country code and feature type
- Converts to multiple geospatial formats (GeoJSON, GeoPackage, Shapefile, KML)
- Command-line interface for easy execution

## Requirements

- Python 3.6+
- Dependencies:
  - pandas
  - geopandas
  - shapely
  - requests

## Installation

1. Clone this repository or download the script
2. Install required dependencies:

```bash
pip install pandas geopandas shapely requests
```

## Usage

The script can be executed from the command line with the following arguments:

```bash
python geonames.py --country <ISO_COUNTRY_CODE> [--feature <FEATURE_CODE>] [--format <OUTPUT_FORMAT>]
```

### Parameters

- `--country`: Required. Two-letter ISO country code (e.g., 'US', 'GB', 'ZA')
- `--feature`: Optional. GeoNames feature code (e.g., 'PPL' for populated places)
- `--format`: Optional. Output format (choices: geojson, gpkg, shp, kml, default: geojson)

### Examples

Extract all populated places in South Africa and save as GeoJSON:
```bash
python geonames.py --country ZA --feature PPL --format geojson
```

Extract all geographical features in the United States and save as a GeoPackage:
```bash
python geonames.py --country US --format gpkg
```

## Output

Files are saved to the `output` directory with naming convention:
```
<COUNTRY_CODE>_<FEATURE_CODE>_geonames.<FORMAT>
```

Example: `ZA_PPL_geonames.geojson`

## Common Feature Codes

Some commonly used feature codes:

- `PPL`: Populated place
- `PPLC`: Capital of a political entity
- `ADM1`: First-order administrative division
- `ADM2`: Second-order administrative division
- `MT`: Mountain
- `LK`: Lake
- `STM`: Stream

For a complete list of feature codes, refer to the [GeoNames Feature Codes](https://www.geonames.org/export/codes.html) documentation.

## Data Structure

The extracted data includes the following fields:

- `geonameid`: Unique identifier
- `name`: Name of the geographical entity
- `asciiname`: Name in ASCII characters
- `alternatenames`: Alternate names (comma-separated)
- `latitude` and `longitude`: Geographic coordinates
- `feature_class` and `feature_code`: Type of feature
- `country_code`: ISO country code
- `admin1_code`, `admin2_code`, etc.: Administrative division codes
- `population`: Population size (for populated places)
- `elevation`: Elevation in meters
- `timezone`: Timezone identifier
- `modification_date`: Date of last modification

## License

The GeoNames geographical database is licensed under a [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/). You are free to use, share, and adapt the data with appropriate attribution.

## Notes

- The full `allCountries.zip` file is approximately 350MB (1.5GB uncompressed)
- The script checks if the data file already exists before downloading
- Data is stored in the `data` directory
- Processed files are saved to the `output` directory
