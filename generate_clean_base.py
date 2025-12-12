import pandas as pd
import geopandas as gpd
import os

# Importamos nuestros módulos personalizados
from src.loader import get_data
from src.preprocessor import load_and_standardize
from src.audit_advanced import auditar_fechas, auditar_tiempos, etiquetar_gps

# --- CONFIGURACIÓN DE PARÁMETROS (DEFAULTS) ---
INPUT_RAW = "data/raw/bubble_sync/export_full.csv"
INPUT_DICT = "Diccionario Variables.xlsx"
OUTPUT_CLEAN = "BASE_MAESTRA_FINAL.csv"

# Reglas de Negocio
FECHA_INICIO = "2025-12-05"  # Todo lo anterior se borra
MIN_MINUTOS = 2            # Menos de esto se considera fraude
BUFFER_GPS = 50            # Metros de tolerancia para validar ubicación

def main():
    print("="*60)
    print("🚀 INICIANDO GENERACIÓN AUTOMÁTICA DE BASE MAESTRA")
    print("="*60)

    # 1. CARGA Y ESTANDARIZACIÓN
    print(f"\n[1/4] 📥 Procesando archivo crudo y diccionario...")
    try:
        # Esto aplica el renombrado y reordenamiento de columnas
        df = load_and_standardize(INPUT_RAW, INPUT_DICT)
        total_inicial = len(df)
        print(f"      ✓ Base cargada: {total_inicial} registros.")
        print("      ✓ Nombres de columnas estandarizados.")
    except Exception as e:
        print(f"      ❌ Error crítico: {e}")
        return

    # 2. FILTRO DE FECHAS
    print(f"\n[2/4] 📅 Aplicando filtro de fecha (Inicio: {FECHA_INICIO})...")
    # Usamos los nombres nuevos ya estandarizados ('fecha_creacion')
    df_fecha_ok, df_fecha_bad = auditar_fechas(df, "fecha_creacion", FECHA_INICIO)
    print(f"      ✓ Se conservaron: {len(df_fecha_ok)}")
    print(f"      🗑️ Se eliminaron: {len(df_fecha_bad)} (anteriores al arranque).")

    # 3. FILTRO DE TIEMPOS
    print(f"\n[3/4] ⏱️ Aplicando filtro de tiempo (Mínimo: {MIN_MINUTOS} min)...")
    df_tiempo_ok, df_tiempo_bad = auditar_tiempos(
        df_fecha_ok, "fecha_creacion", "fecha_modificacion", MIN_MINUTOS
    )
    print(f"      ✓ Se conservaron: {len(df_tiempo_ok)}")
    print(f"      🗑️ Se eliminaron: {len(df_tiempo_bad)} (llenado muy rápido).")

    # 4. VALIDACIÓN GPS (FLAG)
    print(f"\n[4/4] 📍 Validando coordenadas GPS (Tolerancia: {BUFFER_GPS}m)...")
    try:
        # Cargar shapefile de secciones
        gdf_poligonos = get_data()
        
        # Convertir encuestas a GeoDataFrame
        gdf_puntos = gpd.GeoDataFrame(
            df_tiempo_ok, 
            geometry=gpd.points_from_xy(df_tiempo_ok.longitud, df_tiempo_ok.latitud),
            crs="EPSG:4326"
        )
        
        # Etiquetar (No elimina, solo marca Status)
        df_final = etiquetar_gps(
            gdf_puntos, 
            gdf_poligonos, 
            col_seccion_puntos="seccion_electoral", 
            col_seccion_poligonos="KEY_JOIN", 
            buffer_metros=BUFFER_GPS
        )
        print("      ✓ Validación geoespacial completada.")
        
    except Exception as e:
        print(f"      ⚠️ Advertencia GPS: {e}")
        print("      Continuando sin validación GPS...")
        df_final = df_tiempo_ok

    # 5. EXPORTACIÓN
    print(f"\n💾 Guardando archivo final en: {OUTPUT_CLEAN}")
    # Quitamos la columna 'geometry' antes de guardar en CSV
    df_final.drop(columns='geometry', errors='ignore').to_csv(OUTPUT_CLEAN, index=False)
    
    # Resumen Final
    total_final = len(df_final)
    eliminados = total_inicial - total_final
    recuperacion = (total_final / total_inicial) * 100
    
    print("\n" + "="*60)
    print(f"✅ PROCESO TERMINADO CON ÉXITO")
    print(f"   - Muestra Original: {total_inicial}")
    print(f"   - Muestra Final:    {total_final}")
    print(f"   - Eliminados:       {eliminados} ({100-recuperacion:.1f}%)")
    print(f"   - Tasa Recuperación: {recuperacion:.1f}%")
    print("="*60)

if __name__ == "__main__":
    main()