import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def procesar_auditoria_gps(df_bubble, gdf_secciones):
    """
    Cruza coordenadas contra polígonos. Maneja casos sin GPS.
    """
    # 1. BLINDAJE DE TIPOS: Aseguramos que la sección sea string
    df_bubble = df_bubble.copy()
    # Convertimos a string y quitamos decimales (.0) si existen
    df_bubble['seccion_electoral'] = df_bubble['seccion_electoral'].astype(str).str.replace(r'\.0$', '', regex=True)
    
    # 2. Aseguramos que las secciones del mapa también sean string
    # (Usamos .copy() para no afectar el dataframe original fuera de la función)
    gdf_secciones = gdf_secciones.copy()
    gdf_secciones['KEY_JOIN'] = gdf_secciones['KEY_JOIN'].astype(str)
    
    resultados = []
    
    # Preparamos el diccionario de geometrías
    secciones_dict = gdf_secciones.set_index('KEY_JOIN')['geometry'].to_dict()

    for idx, row in df_bubble.iterrows():
        # CASO 1: Sin GPS
        if pd.isna(row['latitud']) or pd.isna(row['longitud']):
            resultados.append("⚠️ Sin GPS")
            continue
            
        # CASO 2: Con GPS -> Validar
        sec_id = str(row['seccion_electoral'])
        
        # Validación de coordenadas numéricas
        try:
            punto = Point(float(row['longitud']), float(row['latitud']))
        except (ValueError, TypeError):
            resultados.append("⚠️ Error Coords")
            continue
        
        if sec_id in secciones_dict:
            poligono = secciones_dict[sec_id]
            if poligono.contains(punto):
                resultados.append("✅ Válida")
            else:
                resultados.append("❌ Fuera de Zona")
        else:
            resultados.append("❓ Sección Desconocida")

    df_bubble['auditoria'] = resultados
    return df_bubble

def calcular_avance_global(df_bubble, gdf_metas):
    """
    Suma TODAS las encuestas y calcula porcentaje en escala 0-100.
    """
    # 1. Asegurar Strings
    df_bubble = df_bubble.copy()
    df_bubble['seccion_electoral'] = df_bubble['seccion_electoral'].astype(str).str.replace(r'\.0$', '', regex=True)
    
    gdf_metas = gdf_metas.copy()
    gdf_metas['KEY_JOIN'] = gdf_metas['KEY_JOIN'].astype(str)
    
    # 2. Agrupar
    conteo = df_bubble.groupby('seccion_electoral').size().reset_index(name='realizadas')
    
    # 3. Merge
    df_avance = gdf_metas.merge(
        conteo, 
        left_on='KEY_JOIN', 
        right_on='seccion_electoral', 
        how='left'
    )
    
    # 4. Cálculos
    df_avance['realizadas'] = df_avance['realizadas'].fillna(0)
    df_avance['encuestas_totales'] = df_avance['encuestas_totales'].fillna(1) 
    
    # --- CORRECCIÓN CRÍTICA: Multiplicar por 100 ---
    # Esto convierte 1.16 en 116.6
    df_avance['porcentaje'] = (df_avance['realizadas'] / df_avance['encuestas_totales']) * 100
    
    return df_avance