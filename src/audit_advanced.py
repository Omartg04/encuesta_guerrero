import pandas as pd
import geopandas as gpd

# Definimos el formato global para que coincida con "Dec 2, 2025 1:11 pm"
FMT_INGLES = "%b %d, %Y %I:%M %p"

def auditar_fechas(df, col_fecha, fecha_corte="2024-12-05"):
    """
    Filtro Duro: Elimina registros previos a la fecha de arranque.
    CORREGIDO: Usa formato explícito en inglés para evitar errores de lectura.
    """
    # 1. Conversión forzada usando el formato de tu CSV
    df[col_fecha] = pd.to_datetime(df[col_fecha], format=FMT_INGLES, errors='coerce')
    
    # 2. Convertimos la fecha de corte (que viene del selector de Streamlit)
    fecha_corte_dt = pd.to_datetime(fecha_corte)
    
    # 3. Validación de seguridad
    # Si la fecha de corte es nula (error de usuario), no filtramos nada para no romper
    if pd.isna(fecha_corte_dt):
        return df.copy(), pd.DataFrame()

    # 4. MASK: La fecha del registro debe ser MAYOR O IGUAL al corte
    # Y además no debe ser NaT (error de lectura)
    mask = (df[col_fecha] >= fecha_corte_dt) & (df[col_fecha].notna())
    
    return df[mask].copy(), df[~mask].copy()

def auditar_tiempos(df, col_inicio, col_fin, min_minutos=2):
    """
    Filtro Duro: Elimina encuestas muy rápidas.
    """
    # 1. Conversión explícita con el formato inglés
    df[col_inicio] = pd.to_datetime(df[col_inicio], format=FMT_INGLES, errors='coerce')
    df[col_fin] = pd.to_datetime(df[col_fin], format=FMT_INGLES, errors='coerce')

    # 2. Si Modified es NaT (vacío), asumimos que es igual a Creation (duración 0)
    df[col_fin] = df[col_fin].fillna(df[col_inicio])
    
    # 3. Cálculo de duración en minutos
    df['duracion_min'] = (df[col_fin] - df[col_inicio]).dt.total_seconds() / 60
    
    # 4. Filtro (Tú decides con el slider si min_minutos es 0 o 2)
    mask = (df['duracion_min'] >= min_minutos)
    
    return df[mask].copy(), df[~mask].copy()

def etiquetar_gps(df_puntos, gdf_poligonos, col_seccion_puntos, col_seccion_poligonos, buffer_metros=50):
    """
    Filtro Suave: Agrega columnas de validación (GPS_STATUS).
    """
    # 1. Proyectar a Metros
    gdf_puntos_utm = df_puntos.to_crs(epsg=32614)
    gdf_poligonos_utm = gdf_poligonos.to_crs(epsg=32614)
    
    # 2. Crear Buffer
    gdf_poligonos_utm['geometry'] = gdf_poligonos_utm.geometry.buffer(buffer_metros)
    
    # 3. Cruce Espacial
    join = gpd.sjoin(
        gdf_puntos_utm, 
        gdf_poligonos_utm[[col_seccion_poligonos, 'geometry']], 
        how="left", 
        predicate="within"
    )
    
    # 4. Detección dinámica de columna
    posible_nombre = f"{col_seccion_poligonos}_right"
    if posible_nombre in join.columns:
        col_geom = posible_nombre
    elif col_seccion_poligonos in join.columns:
        col_geom = col_seccion_poligonos
    else:
        col_geom = "index_right"

    # 5. Lógica de Coincidencia (Manejo de Duplicados de Buffer)
    sec_reportada = join[col_seccion_puntos].astype(str).str.replace(".0", "", regex=False)
    sec_detectada = join[col_geom].astype(str).str.replace(".0", "", regex=False).fillna("SIN_COINCIDENCIA")
    
    join['is_match'] = sec_reportada == sec_detectada
    
    # Agrupamos por índice para resolver duplicados
    resultados_agrupados = join.groupby(join.index)['is_match'].any()
    secciones_detectadas = join.groupby(join.index)[col_geom].first()

    # 6. Asignación
    df_final = df_puntos.copy()
    df_final['GPS_STATUS'] = resultados_agrupados.map({True: "✅ Válida", False: "⚠️ Revisar"})
    df_final['GPS_STATUS'] = df_final['GPS_STATUS'].fillna("⚠️ Revisar")
    df_final['SECCION_GPS_DETECTADA'] = secciones_detectadas

    return df_final