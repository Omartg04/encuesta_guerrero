import geopandas as gpd
import pandas as pd
import os

# CONFIGURACIÓN
PATH_SECCIONES = "data/raw/secciones_guerrero"
PATH_RAW_MANZANAS = "data/raw/inegi_capas_manzana"
PATH_OUTPUT = "data/processed/manzanas_optimizadas"

# Diccionario de archivos crudos
ARCHIVOS_MANZANAS = {
    "IGUALA": "manzanas_iguala.shp",
    "CHILPANCINGO": "manzanas_chilpancingo.shp",
    "ACAPULCO": "manzanas_acapulco.shp"
}

os.makedirs(PATH_OUTPUT, exist_ok=True)

print("🚀 Iniciando optimización de manzanas...")

# 1. Cargar Secciones (El molde de galletas)
shp_sec = [f for f in os.listdir(PATH_SECCIONES) if f.endswith('.shp')][0]
gdf_secciones = gpd.read_file(os.path.join(PATH_SECCIONES, shp_sec))

# Cargar tu CSV de muestra para saber cuáles son las 189 secciones OBJETIVO
df_muestra = pd.read_csv("data/raw/muestra.csv")
# Estandarizar columna seccion
col_sec_shp = [c for c in gdf_secciones.columns if 'seccion' in c.lower()][0]
gdf_secciones['KEY'] = gdf_secciones[col_sec_shp].astype(int).astype(str)
df_muestra['KEY'] = df_muestra['seccion'].astype(int).astype(str)

# FILTRAR: Solo nos interesan las geometrías de las 189 secciones del proyecto
gdf_secciones_objetivo = gdf_secciones[gdf_secciones['KEY'].isin(df_muestra['KEY'])].copy()

# Asegurar WGS84
if gdf_secciones_objetivo.crs != "EPSG:4326":
    gdf_secciones_objetivo = gdf_secciones_objetivo.to_crs("EPSG:4326")

print(f"🎯 Filtro maestro: Se usarán las {len(gdf_secciones_objetivo)} secciones del proyecto para recortar.")

# 2. Procesar cada municipio
for municipio, archivo in ARCHIVOS_MANZANAS.items():
    ruta_completa = os.path.join(PATH_RAW_MANZANAS, archivo)
    if not os.path.exists(ruta_completa):
        print(f"⚠️ No encontrado: {archivo}")
        continue

    print(f"\n🛠️  Procesando {municipio} ({archivo})...")
    
    try:
        # Cargar Manzanas
        gdf_m = gpd.read_file(ruta_completa)
        total_orig = len(gdf_m)
        
        # REPROYECCIÓN OBLIGATORIA (De ITRF a Lat/Lon)
        # Esto soluciona la advertencia de tu auditoría
        if gdf_m.crs != "EPSG:4326":
            gdf_m = gdf_m.to_crs("EPSG:4326")
            
        # RECORTE ESPACIAL (Spatial Join)
        # "Quédate solo con manzanas que tocan mis secciones objetivo"
        gdf_opt = gpd.sjoin(gdf_m, gdf_secciones_objetivo[['geometry']], how='inner', predicate='intersects')
        
        # Limpieza de columnas (para bajar peso)
        cols_keep = ['geometry', 'CVEGEO', 'CVE_MZA'] # Ajusta si necesitas más datos
        # Si las columnas existen, las mantenemos
        cols_final = [c for c in cols_keep if c in gdf_opt.columns]
        gdf_opt = gdf_opt[cols_final]

        total_final = len(gdf_opt)
        
        # Guardar
        out_name = f"manzanas_{municipio.lower()}_opt.shp"
        gdf_opt.to_file(os.path.join(PATH_OUTPUT, out_name))
        
        print(f"✅ Terminado: De {total_orig} -> {total_final} manzanas.")
        
    except Exception as e:
        print(f"❌ Error en {municipio}: {e}")

print("\n✨ Proceso finalizado. Archivos listos en data/processed/manzanas_optimizadas")