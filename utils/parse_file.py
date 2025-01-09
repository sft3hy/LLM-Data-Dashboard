import pandas as pd
import json
import geopandas as gpd
from xml.etree import ElementTree as ET
import shapefile  # pyshp
import zipfile
import pandas as pd
import json
import geopandas as gpd
import xml.etree.ElementTree as ET
import shapefile

def extract_file_snippet(file_path, rows=5):
    """
    Extracts a raw text representation of the columns, a few rows, 
    and their data types from various file types.
    
    Parameters:
        file_path (str): Path to the file.
        rows (int): Number of rows to display (default is 5).
    
    Returns:
        str: Text snippet describing columns, data types, and a few rows.
    """
    file_type = file_path.split('.')[-1].lower()
    try:
        if file_type == "csv":
            # Read CSV and return preview with data types
            df = pd.read_csv(file_path)
            return _describe_dataframe(df, rows)
        
        elif file_type == "json":
            # Parse JSON and convert to DataFrame if tabular
            with open(file_path, "r") as f:
                data = json.load(f)
            if isinstance(data, list):  # Array of objects
                df = pd.DataFrame(data)
                return _describe_dataframe(df, rows)
            else:  # Nested JSON
                return json.dumps(data, indent=2)[:1000]  # Return snippet of raw JSON
        
        elif file_type == "geojson":
            # Read GeoJSON into GeoDataFrame
            gdf = gpd.read_file(file_path)
            return _describe_dataframe(gdf, rows)
        
        elif file_type == "kml":
            # Parse KML and extract placemarks
            tree = ET.parse(file_path)
            root = tree.getroot()
            namespace = {"kml": "http://www.opengis.net/kml/2.2"}
            placemarks = root.findall(".//kml:Placemark", namespaces=namespace)
            rows_data = [{"name": pm.find("kml:name", namespaces=namespace).text if pm.find("kml:name", namespaces=namespace) is not None else "Unnamed"} for pm in placemarks]
            df = pd.DataFrame(rows_data)
            return _describe_dataframe(df, rows)
        
        elif file_type == "shapefile":
            # Read shapefile using PyShp
            sf = shapefile.Reader(file_path)
            fields = [field[0] for field in sf.fields[1:]]  # Skip deletion flag
            records = sf.records()
            rows_data = [dict(zip(fields, rec)) for rec in records[:rows]]
            df = pd.DataFrame(rows_data)
            return _describe_dataframe(df, rows)
        
        else:
            return "Unsupported file type."
    
    except Exception as e:
        return f"Error processing file: {e}"

def _describe_dataframe(df, rows):
    """
    Helper function to describe a DataFrame with refined data types and a preview of rows.
    
    Parameters:
        df (DataFrame): Pandas DataFrame to describe.
        rows (int): Number of rows to preview.
    
    Returns:
        str: Description of columns, refined data types, and rows.
    """
    def infer_type(series):
        """Infer refined data type based on patterns and pandas dtype."""
        series_length = series.size
        series = series.dropna().head(int(series_length/10))
        # print(series)
        if pd.api.types.is_integer_dtype(series):
            return "int"
        elif pd.api.types.is_float_dtype(series):
            return "float"
        elif pd.api.types.is_bool_dtype(series):
            return "boolean"
        elif pd.api.types.is_datetime64_any_dtype(series):
            return "date"
        elif series.str.match(r"(-?\d\.\d{14}\s+){3}\S", na=False).all():  # Latitude/Longitude
            return "coordinate"
        elif series.str.match(r"^-?\d+(\.\d+)?[NS]?, *-?\d+(\.\d+)?[EW]?$", na=False).all():  # Coordinate pair
            return "coordinate_pair"
        elif series.str.contains(r"\d{4}-\d{2}-\d{2}", na=False).all():  # Date in ISO format
            return "date"
        elif series.nunique() < 5:  # Potential categorical column
            return "categorical"
        else:
            return "string"

    # print(df.describe())

    description = "Columns and Data Types:\n"
    for col in df.columns:
        if df[col].dtype == 'object':
            dtype = infer_type(df[col].astype(str))  # Convert to string for pattern matching
        else:
            dtype = df[col].dtype
        description += f"  - {col}: {dtype}\n"
    description += "\nPreview of Rows:\n"
    description += df.head(rows).to_string(index=False)
    return description

# print(extract_file_snippet("user_uploaded_files/02-24-2022_THROUGH_09-04-2024_Vehicle_Losses.csv"))

def preview_file(file_path):
    """Extract a preview snippet of the file based on its type."""
    file_type = file_path.split('.')[-1]
    try:
        if file_type == "csv":
            df = pd.read_csv(file_path)
            return {"columns": list(df.columns), "num_rows": len(df)}

        elif file_type == "json":
            with open(file_path, "r") as f:
                data = json.load(f)
                
            if isinstance(data, list):  # Array of objects (tabular)
                df = pd.DataFrame(data)
                columns = list(df.columns)
                num_rows = len(df)
                return {"columns": columns, "num_rows": num_rows}
            
            elif isinstance(data, dict):  # Nested JSON (non-tabular)
                # Extract top-level keys for nested JSON
                top_level_keys = list(data.keys())
                num_rows = len(data)  # Number of top-level keys
                return {"columns": top_level_keys, "num_rows": num_rows}
            
            else:
                return {"error": "Unsupported JSON format"}
        elif file_type == 'geojson':
            gdf = gpd.read_file(file_path)
            return {"columns": list(gdf.columns), "num_rows": len(gdf)}

        elif file_type == 'kml':
            gdf = gpd.read_file(file_path, driver="KML")
            return {"columns": list(gdf.columns), "num_rows": len(gdf)}

        elif file_type == 'zip':
            with zipfile.ZipFile(file_path, 'r') as z:
                file_list = z.namelist()
                return {"columns": None, "num_rows": None, "content": file_list}

        else:
            return {"error": "Unsupported file format"}

    except Exception as e:
        return {"error": str(e)}