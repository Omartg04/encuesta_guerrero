import pandas as pd
import os

# --- CONFIGURACIÓN DE RUTAS ---
# Nombre del archivo gigante que bajas de Bubble
INPUT_FILE = "data/raw/bubble_sync/export_full.csv" 
# Nombre del archivo limpio que espera tu sistema
OUTPUT_FILE = "data/raw/bubble_sync/bubble_raw.csv"

# --- CONFIGURACIÓN DE COLUMNAS ---
# Diccionario: "Nombre en el archivo BUBBLE" : "Nombre que queremos en el SISTEMA"
# Si en Bubble se llaman igual, repite el nombre.
# Esto sirve para filtrar (solo se quedan estas) y renombrar al mismo tiempo.
COLUMNS_TO_KEEP = {
    # 'Nombre en Bubble' : 'Nombre Final'
    'seccion_electoral': 'seccion_electoral',
    'municipio': 'municipio',
    'municipio_texto': 'municipio_texto',
    
    # A veces Bubble baja 'Created By' en vez de id_encuestador, ajusta aquí si es necesario
    'id_encuestador': 'id_encuestador', 
    
    # Coordenadas
    'latitud': 'latitud',
    'longitud': 'longitud',
    
    # Fechas
    'Creation Date': 'Creation Date',
    'Modified Date': 'Modified Date'
}

def pre_procesar_export():
    print("✂️ Iniciando pre-selección de columnas...")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ No encontré el archivo de entrada: {INPUT_FILE}")
        print("   -> Guarda tu descarga completa de Bubble con el nombre 'export_full.csv'")
        return

    try:
        # 1. Cargar el archivo gigante
        df_full = pd.read_csv(INPUT_FILE)
        total_cols = len(df_full.columns)
        print(f"📥 Archivo cargado. Columnas totales: {total_cols}")

        # 2. Verificar que existan las columnas que buscamos
        missing_cols = [col for col in COLUMNS_TO_KEEP.keys() if col not in df_full.columns]
        
        if missing_cols:
            print(f"⚠️ Precaución: Las siguientes columnas no están en el archivo original:")
            print(f"   {missing_cols}")
            print("   -> El script intentará continuar con las que sí encuentre.")
        
        # 3. Filtrar y Renombrar
        # Nos quedamos solo con las columnas que existen en el diccionario
        cols_existentes = [c for c in COLUMNS_TO_KEEP.keys() if c in df_full.columns]
        
        df_reduced = df_full[cols_existentes].copy()
        df_reduced = df_reduced.rename(columns=COLUMNS_TO_KEEP)

        # 4. Guardar
        df_reduced.to_csv(OUTPUT_FILE, index=False)
        
        print(f"✅ ¡Éxito! Archivo ligero generado: {OUTPUT_FILE}")
        print(f"   Columnas finales: {len(df_reduced.columns)}")
        print(f"   (Se eliminaron {total_cols - len(df_reduced.columns)} columnas innecesarias)")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    pre_procesar_export()