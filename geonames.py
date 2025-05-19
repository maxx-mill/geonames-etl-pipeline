import os
import requests
import zipfile
import io
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# ---------- Configuration ----------
GEONAMES_URL = "https://download.geonames.org/export/dump/allCountries.zip"
DATA_DIR = "data"
TXT_FILE = os.path.join(DATA_DIR, "allCountries.txt")
OUTPUT_DIR = "output"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- Download GeoNames Dataset ----------
def download_geonames():
    if not os.path.exists(TXT_FILE):
        print("Downloading GeoNames allCountries.zip...")
        response = requests.get(GEONAMES_URL)
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                z.extractall(DATA_DIR)
                print("Extracted:", z.namelist())
        else:
            raise Exception("Download failed with status:", response.status_code)
    else:
        print("allCountries.txt already downloaded.")

# ---------- Load and Filter Dataset ----------
def load_filtered_geonames(country_code, feature_code=None):
    columns = [
        "geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude",
        "feature_class", "feature_code", "country_code", "cc2", "admin1_code",
        "admin2_code", "admin3_code", "admin4_code", "population", "elevation",
        "dem", "timezone", "modification_date"
    ]

    print("Reading GeoNames data...")
    df = pd.read_csv(TXT_FILE, sep="\t", names=columns, dtype={"elevation": "str"}, low_memory=False)

    print(f"Filtering for Country: {country_code}" + (f" and Feature Code: {feature_code}" if feature_code else " (all features)..."))
    filtered = df[df["country_code"] == country_code]
    if feature_code:
        filtered = filtered[filtered["feature_code"] == feature_code]

    geometry = [Point(xy) for xy in zip(filtered["longitude"], filtered["latitude"])]
    gdf = gpd.GeoDataFrame(filtered, geometry=geometry, crs="EPSG:4326")

    return gdf

# ---------- Save to Selected Format ----------
def save_output(gdf, country_code, feature_code, file_format):
    suffix = feature_code if feature_code else "ALL"
    base_name = f"{country_code}_{suffix}_geonames"

    if file_format == "geojson":
        out_path = os.path.join(OUTPUT_DIR, base_name + ".geojson")
        gdf.to_file(out_path, driver="GeoJSON")
    elif file_format == "gpkg":
        out_path = os.path.join(OUTPUT_DIR, base_name + ".gpkg")
        gdf.to_file(out_path, driver="GPKG", layer="geonames")
    elif file_format == "shp":
        out_path = os.path.join(OUTPUT_DIR, base_name + ".shp")
        gdf.to_file(out_path, driver="ESRI Shapefile")
    elif file_format == "kml":
        out_path = os.path.join(OUTPUT_DIR, base_name + ".kml")
        gdf.to_file(out_path, driver="KML")
    else:
        raise ValueError("Unsupported format. Choose from: geojson, gpkg, shp, kml")

    print(f"Saved {file_format.upper()} to {out_path}")

# ---------- Main Pipeline ----------
def run_pipeline(country_code, feature_code, file_format):
    download_geonames()
    gdf = load_filtered_geonames(country_code, feature_code)
    save_output(gdf, country_code, feature_code, file_format.lower())

# ---------- Command Line Interface ----------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download and convert GeoNames data to various formats.")
    parser.add_argument("--country", required=True, help="ISO country code (e.g., 'ZA')")
    parser.add_argument("--feature", required=False, help="GeoNames feature code (e.g., 'PPL' for populated places)")
    parser.add_argument("--format", default="geojson", choices=["geojson", "gpkg", "shp", "kml"],
                        help="Output format (geojson, gpkg, shp, kml) [default: geojson]")

    args = parser.parse_args()
    run_pipeline(args.country.upper(), args.feature.upper() if args.feature else None, args.format)
