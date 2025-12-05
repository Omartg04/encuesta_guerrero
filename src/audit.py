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
    Suma TODAS las encuestas (con y sin GPS) para el avance.
    CORRECCIÓN: Fuerza tipos de datos str en AMBOS lados antes del merge.
    """
    # 1. Asegurar que Bubble sea String (limpiando posibles .0)
    df_bubble = df_bubble.copy()
    df_bubble['seccion_electoral'] = df_bubble['seccion_electoral'].astype(str).str.replace(r'\.0$', '', regex=True)
    
    # 2. Asegurar que Metas sea String
    gdf_metas = gdf_metas.copy()
    gdf_metas['KEY_JOIN'] = gdf_metas['KEY_JOIN'].astype(str)
    
    # 3. Agrupar conteos
    conteo = df_bubble.groupby('seccion_electoral').size().reset_index(name='realizadas')
    
    # 4. Merge seguro (String vs String)
    df_avance = gdf_metas.merge(
        conteo, 
        left_on='KEY_JOIN', 
        right_on='seccion_electoral', 
        how='left'
    )
    
    # 5. Cálculos finales
    df_avance['realizadas'] = df_avance['realizadas'].fillna(0)
    # Evitar división por cero o nulos
    df_avance['encuestas_totales'] = df_avance['encuestas_totales'].fillna(1) 
    
    df_avance['porcentaje'] = (df_avance['realizadas'] / df_avance['encuestas_totales'])
    
    return df_avance