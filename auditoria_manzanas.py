import geopandas as gpd
import os

# Ruta donde pusiste tus archivos
DIR_MANZANAS = "data/raw/inegi_capas_manzana"

print(f"🕵️‍♂️ Iniciando auditoría en: {DIR_MANZANAS}\n")

archivos = [f for f in os.listdir(DIR_MANZANAS) if f.endswith('.shp')]

if not archivos:
    print("❌ No se encontraron archivos .shp en la carpeta.")
else:
    for archivo in archivos:
        path = os.path.join(DIR_MANZANAS, archivo)
        try:
            print(f"📂 Analizando: {archivo} ...")
            
            # Carga ligera (solo geometría para ser rápido)
            gdf = gpd.read_file(path, ignore_geometry=False)
            
            peso_mb = os.path.getsize(path) / (1024 * 1024)
            crs = gdf.crs
            cols = list(gdf.columns)
            filas = len(gdf)
            
            print(f"   ⚖️  Peso: {peso_mb:.2f} MB")
            print(f"   🔢  Polígonos (Manzanas): {filas:,}")
            print(f"   🌐  Proyección (CRS): {crs}")
            
            # Evaluación rápida
            if filas > 5000:
                print("   ⚠️  ADVERTENCIA: Son muchos polígonos. Recomiendo filtrar o usar caché.")
            if str(crs) != "EPSG:4326":
                print("   ℹ️  NOTA: No está en Lat/Lon. Se deberá reproyectar en el código.")
            
            # Buscar clave de manzana
            posibles_claves = [c for c in cols if "CVE" in c or "MANZ" in c]
            print(f"   🔑  Posibles claves: {posibles_claves}")
            print("-" * 40)

        except Exception as e:
            print(f"   ❌ Error leyendo {archivo}: {e}")