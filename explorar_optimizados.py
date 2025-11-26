import geopandas as gpd
import matplotlib.pyplot as plt
import os

# Ruta donde el script anterior debió guardar los archivos
PATH_OPTIMIZADOS = "data/processed/manzanas_optimizadas"

print(f"🔬 Explorando archivos en: {PATH_OPTIMIZADOS}\n")

if not os.path.exists(PATH_OPTIMIZADOS):
    print("❌ La carpeta no existe. ¿Ejecutaste el script 'optimizar_manzanas.py' primero?")
    exit()

archivos = [f for f in os.listdir(PATH_OPTIMIZADOS) if f.endswith('.shp')]

if not archivos:
    print("❌ No hay archivos .shp optimizados.")
else:
    for archivo in archivos:
        ruta = os.path.join(PATH_OPTIMIZADOS, archivo)
        try:
            print(f"📂 Archivo: {archivo}")
            
            # Cargar archivo
            gdf = gpd.read_file(ruta)
            
            # Métricas
            filas = len(gdf)
            crs = gdf.crs
            peso_kb = os.path.getsize(ruta) / 1024
            
            print(f"   📉 Manzanas: {filas:,}")
            print(f"   💾 Peso: {peso_kb:.2f} KB") # Ahora debería ser en KB, no MB
            print(f"   🌐 Proyección: {crs}")
            
            # Validación de Proyección
            if str(crs) == "EPSG:4326":
                print("   ✅ Proyección correcta (Lat/Lon). Listo para Folium.")
            else:
                print(f"   ❌ ALERTA: Proyección incorrecta ({crs}). No se verá en el mapa.")
            
            # Muestra de datos
            print("   📋 Ejemplo de datos (Primeras 2 filas):")
            print(gdf[['CVEGEO', 'geometry']].head(2))
            
            print("-" * 40)
            
            # Visualización Rápida (Estática)
            # Esto abrirá una ventanita con el dibujo del mapa para confirmar visualmente
            print(f"   🎨 Generando vista previa de {archivo}...")
            gdf.plot(edgecolor='blue', linewidth=0.5, alpha=0.5)
            plt.title(f"Vista Previa: {archivo} ({filas} manzanas)")
            plt.xlabel("Longitud")
            plt.ylabel("Latitud")
            plt.show() # Cierra la ventana que se abre para continuar con el siguiente archivo

        except Exception as e:
            print(f"   ❌ Error: {e}")