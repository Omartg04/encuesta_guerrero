import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import numpy as np
from streamlit_folium import st_folium
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
from folium.plugins import Search, Fullscreen
import os

# --- 1. CONFIGURACIÓN Y ESTILOS ---
st.set_page_config(
    page_title="Logística Electoral Guerrero",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    </style>
    """, unsafe_allow_html=True)

# Constantes
MUNICIPIOS_MAP = {
    "IGUALA": "IGUALA DE LA INDEPENDENCIA",
    "CHILPANCINGO": "CHILPANCINGO DE LOS BRAVO", 
    "ACAPULCO": "ACAPULCO DE JUAREZ"
}

SUPERVISORES_CONFIG = {
    "IGUALA": 6,
    "CHILPANCINGO": 6,
    "ACAPULCO": 8
}

# --- 2. FUNCIONES DE LÓGICA ---

@st.cache_data
def get_data():
    """Carga de datos optimizada."""
    shp_dir = "data/raw/secciones_guerrero"
    try:
        shp_file = [f for f in os.listdir(shp_dir) if f.endswith('.shp')][0]
    except IndexError:
        st.error("❌ Falta Shapefile"); return None
        
    path_shp = os.path.join(shp_dir, shp_file)
    path_csv = "data/raw/muestra.csv"

    try:
        gdf = gpd.read_file(path_shp)
        df = pd.read_csv(path_csv)
        df.columns = [c.lower() for c in df.columns] 
        col_seccion_shp = [c for c in gdf.columns if 'seccion' in c.lower()][0]
        
        gdf['KEY_JOIN'] = gdf[col_seccion_shp].astype(int).astype(str)
        df['KEY_JOIN'] = df['seccion'].astype(int).astype(str)

        gdf_final = gdf.merge(df, on='KEY_JOIN', how='inner')
        if gdf_final.crs != "EPSG:4326":
            gdf_final = gdf_final.to_crs("EPSG:4326")
        return gdf_final
    except Exception as e:
        st.error(f"Error: {e}"); return None

def balanced_cluster_optimization(gdf, n_clusters):
    """Algoritmo Húngaro para balanceo de cargas."""
    if len(gdf) <= n_clusters:
        gdf = gdf.copy()
        gdf['Supervisor_ID'] = range(1, len(gdf) + 1)
        return gdf

    gdf_utm = gdf.to_crs("EPSG:32614")
    coords = np.column_stack((gdf_utm.geometry.centroid.x, gdf_utm.geometry.centroid.y))
    n_points = len(coords)

    base_size = n_points // n_clusters
    remainder = n_points % n_clusters
    
    cluster_slots = []
    for i in range(n_clusters):
        size = base_size + (1 if i < remainder else 0)
        cluster_slots.extend([i] * size)
    
    kmeans = KMeans(n_clusters=n_clusters, n_init=20, random_state=42)
    kmeans.fit(coords)
    centroids = kmeans.cluster_centers_

    target_coords = centroids[cluster_slots]
    cost_matrix = cdist(coords, target_coords)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    assigned_supervisors = [cluster_slots[c] + 1 for c in col_ind]
    final_assignment = pd.Series(data=assigned_supervisors, index=row_ind).sort_index()
    
    gdf_out = gdf.copy()
    gdf_out['Supervisor_ID'] = final_assignment.values
    return gdf_out

def procesar_todo_el_estado(gdf_global):
    """Procesamiento iterativo por municipio."""
    resultados = []
    for muni_key, nombre_oficial in MUNICIPIOS_MAP.items():
        sub_gdf = gdf_global[gdf_global['nombre_municipio'].str.upper() == nombre_oficial.upper()].copy()
        if not sub_gdf.empty:
            n_supervisores = SUPERVISORES_CONFIG[muni_key]
            sub_gdf = balanced_cluster_optimization(sub_gdf, n_supervisores)
            sub_gdf['Supervisor_Global'] = f"{muni_key[:3]}-" + sub_gdf['Supervisor_ID'].astype(str)
            resultados.append(sub_gdf)
    if resultados:
        return pd.concat(resultados)
    return gpd.GeoDataFrame()

# --- 3. UI DASHBOARD ---

def main():
    st.title("🗳️ Tablero de Mando Logístico - Guerrero")
    
    gdf = get_data()
    if gdf is None: st.stop()

    with st.sidebar:
        st.header("Filtros de Visualización")
        
        opciones_menu = list(MUNICIPIOS_MAP.keys()) + ["VISTA GENERAL (TODOS)"]
        seleccion = st.selectbox("Seleccionar Territorio", opciones_menu)
        
        es_global = seleccion == "VISTA GENERAL (TODOS)"
        
        if es_global:
            st.info("🔄 Procesando todo el estado...")
            gdf_view = procesar_todo_el_estado(gdf)
            total_supervisores = sum(SUPERVISORES_CONFIG.values())
        else:
            nombre_oficial = MUNICIPIOS_MAP[seleccion]
            gdf_view = gdf[gdf['nombre_municipio'].str.upper() == nombre_oficial.upper()].copy()
            total_supervisores = SUPERVISORES_CONFIG[seleccion]
            gdf_view = balanced_cluster_optimization(gdf_view, total_supervisores)
            gdf_view['Supervisor_Global'] = gdf_view['Supervisor_ID']
            
        if gdf_view.empty:
            st.warning("Sin datos."); st.stop()

        st.divider()
        st.metric("Total Secciones", len(gdf_view))
        st.metric("Encuestas Totales", gdf_view['encuestas_totales'].sum())
        
        # --- NUEVO: GUÍA DE USO EN SIDEBAR ---
        st.divider()
        st.markdown("### 📚 Guía Rápida")
        st.markdown("""
        1. **🔍 Buscar:** Usa la lupa en el mapa (arriba izq.) para hallar una sección (ej. '1540').
        2. **🗺️ Capas:** Alterna entre 'Calle' y 'Satélite' con el icono (arriba der.).
        3. **⬇️ Descargar:** Baja al final para obtener el CSV de asignación.
        """)

    # --- MAPA PRINCIPAL ---
    
    k1, k2, k3 = st.columns(3)
    k1.info(f"📍 **Visualizando:** {seleccion}")
    k2.success(f"🎯 **Meta Total:** {gdf_view['encuestas_totales'].sum()} encuestas")
    promedio = gdf_view['encuestas_totales'].sum() / total_supervisores
    k3.warning(f"⚖️ **Carga Promedio:** ~{int(promedio)} enc/supervisor")

    lat = gdf_view.geometry.centroid.y.mean()
    lon = gdf_view.geometry.centroid.x.mean()
    zoom = 9 if es_global else 12
    
    m = folium.Map(location=[lat, lon], zoom_start=zoom, tiles=None)

    folium.TileLayer('CartoDB positron', name="Mapa Claro (Calle)").add_to(m)
    folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Satélite (Terreno)',
    ).add_to(m)

    import branca.colormap as cm
    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe']
    
    def get_color(id_val):
        try:
            if isinstance(id_val, str) and "-" in id_val:
                num = int(id_val.split("-")[1])
            else:
                num = int(id_val)
            return colors[(num - 1) % len(colors)]
        except:
            return "gray"

    geo_json = folium.GeoJson(
        gdf_view,
        name="Secciones Electorales",
        style_function=lambda x: {
            'fillColor': get_color(x['properties']['Supervisor_Global']),
            'color': 'black', 'weight': 1, 'fillOpacity': 0.6
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['seccion', 'nombre_municipio', 'Supervisor_Global', 'encuestas_totales', 'lista_nom'],
            aliases=['Sección:', 'Municipio:', 'Supervisor:', 'Meta:', 'LN:'],
            localize=True
        ),
        popup=folium.GeoJsonPopup(fields=['seccion'])
    ).add_to(m)

    Search(
        layer=geo_json,
        geom_type="Polygon",
        placeholder="Buscar Sección (ej: 1540)",
        collapsed=False,
        search_label="seccion",
        weight=3
    ).add_to(m)

    Fullscreen().add_to(m)
    folium.LayerControl().add_to(m)

    st_folium(m, height=650, use_container_width=True)

    # --- TABLA Y DESCARGA ---
    st.markdown("### 📋 Desglose Operativo")
    
    col_t1, col_t2 = st.columns([3,1])
    with col_t1:
        agg_key = 'Supervisor_Global'
        resumen = gdf_view.groupby(['nombre_municipio', agg_key]).agg({
            'seccion': 'count',
            'encuestas_totales': 'sum',
            'lista_nom': 'sum'
        }).reset_index().rename(columns={'seccion': 'Secciones', 'encuestas_totales': 'Meta', 'lista_nom': 'Población LN'})
        
        st.dataframe(resumen, use_container_width=True, height=300)
    
    with col_t2:
        st.info("Descarga la base maestra para compartir con coordinadores.")
        csv = gdf_view[['seccion', 'nombre_municipio', 'Supervisor_Global', 'encuestas_totales']].to_csv(index=False)
        st.download_button(
            label="⬇️ Descargar CSV",
            data=csv,
            file_name="logistica_guerrero_final.csv",
            mime="text/csv",
            type="primary"
        )
    
    # --- NUEVO: NOTA METODOLÓGICA (AL PIE) ---
    st.markdown("---")
    with st.expander("ℹ️ Nota Técnica: Metodología de Agrupación (Algoritmo Balanceado)"):
        st.markdown("""
        **¿Cómo se definen los grupos de supervisores?**
        
        Este dashboard no utiliza una agrupación arbitraria. Implementa un modelo de **Optimización Combinatoria (Asignación Lineal)** diseñado para garantizar equidad laboral y eficiencia logística:
        
        1.  **⚖️ Equidad Numérica:** El sistema divide el total de secciones entre el número de supervisores. Se fuerza matemáticamente a que la diferencia entre la carga de trabajo de un supervisor y otro sea de **máximo ±1 sección**. Nadie tiene una carga desproporcionada.
        2.  **📍 Proximidad Geográfica:** Una vez definida la cantidad de secciones, el algoritmo busca que estas sean **vecinas geográficas**. Se minimiza la distancia total que debe recorrer el equipo.
        3.  **📐 Precisión:** Se utiliza la proyección cartográfica `UTM Zona 14N` para realizar cálculos precisos en metros, evitando distorsiones por la curvatura de la tierra.
        """)

if __name__ == "__main__":
    main()