import os

# Try to import heavy tools, but don't crash if they are missing
try:
    import rasterio
    import geopandas as gpd
    HAS_GEO_TOOLS = True
except ImportError:
    HAS_GEO_TOOLS = False

def validate_crs(file_path: str):
    if not os.path.exists(file_path):
        return "Error: File not found."

    # If we don't have the heavy tools installed yet
    if not HAS_GEO_TOOLS:
        return "[Simulation Mode] Tools missing. Assuming WGS 84 (EPSG:4326) for demo."

    # Real logic (only runs if installed)
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.tif', '.tiff']:
            with rasterio.open(file_path) as src:
                return src.crs.to_string()
        elif ext in ['.geojson', '.shp']:
            data = gpd.read_file(file_path)
            return data.crs.to_string()
    except Exception as e:
        return f"Error reading file: {str(e)}"
    
    return "Unsupported format."