# src/loader.py
import streamlit as st
import geopandas as gpd
import pandas as pd
import os
from src.config import MANZANAS_FILES

@st.cache_data
def get_data():
    """Carga de datos optimizada (Secciones + Muestra)."""
    shp_dir = "data/raw/secciones_guerrero"
    try:
        shp_file = [f for f in os.listdir(shp_dir) if f.endswith('.shp')][0]
    except IndexError:
        st.error("❌ Falta Shapefile"); return None
        
    path_shp = os.path.join(shp_dir, shp_file)
    path_csv = "data/raw/muestra.csv"

    try:
        gdf = gpd.read_file(path_shp)
        df = pd.read_csv(path_csv)
        df.columns = [c.lower() for c in df.columns] 
        col_seccion_shp = [c for c in gdf.columns if 'seccion' in c.lower()][0]
        
        gdf['KEY_JOIN'] = gdf[col_seccion_shp].astype(int).astype(str)
        df['KEY_JOIN'] = df['seccion'].astype(int).astype(str)

        gdf_final = gdf.merge(df, on='KEY_JOIN', how='inner')
        if gdf_final.crs != "EPSG:4326":
            gdf_final = gdf_final.to_crs("EPSG:4326")
        return gdf_final
    except Exception as e:
        st.error(f"Error: {e}"); return None

@st.cache_data
def load_manzanas_optimizadas(municipio_key):
    """Carga las manzanas INEGI procesadas."""
    if municipio_key not in MANZANAS_FILES: return None
    
    path = MANZANAS_FILES[municipio_key]
    if not os.path.exists(path): return None
    
    try:
        return gpd.read_file(path)
    except Exception: return None