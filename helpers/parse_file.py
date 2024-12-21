import pandas as pd
import json
import geopandas as gpd
from xml.etree import ElementTree as ET
import shapefile  # pyshp
from io import StringIO

def extract_file_snippet(file_path, rows=5):
    """
    Extracts a raw text representation of the columns and a few rows from various file types.
    
    Parameters:
        file_path (str): Path to the file.
        file_type (str): File type (e.g., 'csv', 'json', 'geojson', 'kml', 'shapefile').
        rows (int): Number of rows to display (default is 5).
    
    Returns:
        str: Text snippet representing the columns and a few rows.
    """
    file_type = file_path.split('.')[-1]
    try:
        if file_type == "csv":
            # Read CSV and return preview
            df = pd.read_csv(file_path)
            return df.head(rows).to_string(index=False)
        
        elif file_type == "json":
            # Parse JSON and convert to DataFrame if it's a tabular JSON
            with open(file_path, "r") as f:
                data = json.load(f)
            if isinstance(data, list):  # Array of objects
                df = pd.DataFrame(data)
                return df.head(rows).to_string(index=False)
            else:  # Nested JSON
                return json.dumps(data, indent=2)[:1000]  # Return snippet of raw JSON

        elif file_type == "geojson":
            # Read GeoJSON into GeoDataFrame
            gdf = gpd.read_file(file_path)
            return gdf.head(rows).to_string(index=False)
        
        elif file_type == "kml":
            # Parse KML and extract placemarks
            tree = ET.parse(file_path)
            root = tree.getroot()
            namespace = {"kml": "http://www.opengis.net/kml/2.2"}
            placemarks = root.findall(".//kml:Placemark", namespaces=namespace)
            rows = [{"name": pm.find("kml:name", namespaces=namespace).text if pm.find("kml:name", namespaces=namespace) is not None else "Unnamed"} for pm in placemarks]
            return pd.DataFrame(rows).head(rows).to_string(index=False)
        
        elif file_type == "shapefile":
            # Read shapefile using PyShp
            sf = shapefile.Reader(file_path)
            fields = [field[0] for field in sf.fields[1:]]  # Skip deletion flag
            records = sf.records()
            rows_data = [dict(zip(fields, rec)) for rec in records[:rows]]
            return pd.DataFrame(rows_data).to_string(index=False)
        
        else:
            return "Unsupported file type."
    
    except Exception as e:
        return f"Error processing file: {e}"

