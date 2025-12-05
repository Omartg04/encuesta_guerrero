import pandas as pd
import os

# --- CONFIGURACIÓN ---
RAW_FILE = "data/raw/bubble_sync/bubble_raw.csv"
CLEAN_FILE = "data/processed/bubble_clean.csv"

# FILTRO DE FECHA: Solo datos a partir del 5 de Diciembre
FECHA_INICIO_REAL = pd.Timestamp("2025-12-05") 

# MAPEO EXACTO: {'Nombre en tu CSV de Bubble': 'Nombre estándar del sistema'}
COLUMN_MAPPING = {
    'seccion_electoral': 'seccion_electoral',
    'id_encuestador': 'id_encuestador',
    'latitud': 'latitud',
    'longitud': 'longitud',
    'Creation Date': 'fecha_hora',  
    'municipio': 'municipio'
}

def procesar_datos_reales():
    print(f"🧹 Iniciando limpieza (Filtrando datos anteriores al {FECHA_INICIO_REAL.date()})...")
    
    if not os.path.exists(RAW_FILE):
        print(f"❌ No se encontró: {RAW_FILE}")
        return

    try:
        df = pd.read_csv(RAW_FILE)
        
        # 1. Renombrar columnas
        df_clean = df.rename(columns=COLUMN_MAPPING)
        
        # 2. Limpieza de Sección 
        df_clean['seccion_electoral'] = pd.to_numeric(df_clean['seccion_electoral'], errors='coerce').fillna(0).astype(int).astype(str)
        df_clean = df_clean[df_clean['seccion_electoral'] != '0']

        # 3. Limpieza de Fechas
        # Formato Bubble: "Dec 5, 2025 12:00 pm"
        df_clean['fecha_hora'] = pd.to_datetime(
            df_clean['fecha_hora'], 
            format='%b %d, %Y %I:%M %p', 
            errors='coerce'
        )
        
        # APLICAR EL FILTRO DE FECHA
        total_antes = len(df_clean)
        df_clean = df_clean[df_clean['fecha_hora'] >= FECHA_INICIO_REAL]
        eliminados = total_antes - len(df_clean)
        
        if eliminados > 0:
            print(f"✂️ Se eliminaron {eliminados} registros de prueba (anteriores al día 5).")

        # 4. Limpieza de Coordenadas
        df_clean['latitud'] = pd.to_numeric(df_clean['latitud'], errors='coerce')
        df_clean['longitud'] = pd.to_numeric(df_clean['longitud'], errors='coerce')
        
        df_clean['tiene_gps'] = df_clean['latitud'].notna() & df_clean['longitud'].notna()

        # 5. Guardar
        os.makedirs("data/processed", exist_ok=True)
        df_clean.to_csv(CLEAN_FILE, index=False)
        
        print(f"✅ ¡Limpieza Exitosa!")
        print(f"   Archivo generado: {CLEAN_FILE}")
        print(f"   Total registros válidos: {len(df_clean)}")

    except Exception as e:
        print(f"❌ Error crítico en ETL: {e}")

if __name__ == "__main__":
    procesar_datos_reales()