import pandas as pd
import geopandas as gpd
import numpy as np
import random
from datetime import datetime, timedelta
import os
from src.loader import get_data

def generar_datos_bubble_simulados(n_encuestas=500):
    """
    Genera Mock Data con las columnas confirmadas:
    seccion_electoral, id_encuestador, municipio, latitud, longitud
    """
    print("🤖 Iniciando simulación (Estructura Confirmada)...")
    
    gdf_secciones = get_data()
    if gdf_secciones is None: return None

    # Lista de IDs de encuestadores
    encuestadores = [f"ENC-{i:03d}" for i in range(1, 16)] # Ej: ENC-001
    
    data = []
    
    for _ in range(n_encuestas):
        seccion_row = gdf_secciones.sample(1).iloc[0]
        seccion_id = seccion_row['KEY_JOIN']
        municipio = seccion_row['nombre_municipio']
        
        # Centroide real
        centro = seccion_row['geometry'].centroid
        lat_real = centro.y
        lon_real = centro.x
        
        # Simulación GPS (90% válidas)
        es_valida = random.random() > 0.10
        noise = 0.001 if es_valida else 0.02
        
        gps_lat = lat_real + random.uniform(-noise, noise)
        gps_lon = lon_real + random.uniform(-noise, noise)
        
        # Fecha simulada (Necesaria para gráficos de avance)
        fecha = datetime.now() - timedelta(days=random.randint(0, 3))
        
        # --- ESTRUCTURA EXACTA DE BUBBLE ---
        registro = {
            "Modified Date": fecha, # Mantenemos fecha para el monitoreo
            "seccion_electoral": seccion_id,
            "municipio": municipio,
            "id_encuestador": random.choice(encuestadores), # <--- CAMBIO
            "latitud": gps_lat,  # <--- CAMBIO
            "longitud": gps_lon  # <--- CAMBIO
        }
        data.append(registro)
        
    df = pd.DataFrame(data)
    
    os.makedirs("data/raw/bubble_sync", exist_ok=True)
    df.to_csv("data/raw/bubble_sync/bubble_mock.csv", index=False)
    
    print(f"✅ Datos generados con columnas correctas: {len(df)}")
    return df

if __name__ == "__main__":
    generar_datos_bubble_simulados()