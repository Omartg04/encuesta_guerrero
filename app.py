import streamlit as st
import pandas as pd
import io
import geopandas as gpd
import folium
import numpy as np
from streamlit_folium import st_folium
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
from folium.plugins import Search, Fullscreen
import os
import time

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

MANZANAS_FILES = {
    "IGUALA": "data/processed/manzanas_optimizadas/manzanas_iguala_opt.shp",
    "CHILPANCINGO": "data/processed/manzanas_optimizadas/manzanas_chilpancingo_opt.shp",
    "ACAPULCO": "data/processed/manzanas_optimizadas/manzanas_acapulco_opt.shp"
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

@st.cache_data
def load_manzanas_optimizadas(municipio_key):
    """Carga las manzanas INEGI procesadas."""
    if municipio_key not in MANZANAS_FILES: return None
    
    path = MANZANAS_FILES[municipio_key]
    if not os.path.exists(path): return None
    
    try:
        return gpd.read_file(path)
    except Exception: return None

# --- 3. UI DASHBOARD ---

def main():
    st.title("🗳️ Tablero de Mando Logístico - Guerrero")
    # --- SELECTOR DE MODO (NUEVO) ---
    modo=st.sidebar.radio(
    "Modo de Visualización",
    ["🗺️ Planeación (Sprint 1)", "🔮 Demo Monitoreo (Sprint 2)"],
    index=0
    )

    # Lógica de desvío: Si selecciona Demo, muestra demo y DETIENE lo demás
    if modo == "🔮 Demo Monitoreo (Sprint 2)":
        render_demo_monitoreo()
        return 
    
    gdf = get_data()
    if gdf is None: st.stop()

    with st.sidebar:
        st.header("Filtros de Visualización")
        
        opciones_menu = list(MUNICIPIOS_MAP.keys()) + ["VISTA GENERAL (TODOS)"]
        seleccion = st.selectbox("Seleccionar Territorio", opciones_menu)
        
        es_global = seleccion == "VISTA GENERAL (TODOS)"

        with st.spinner(f"🛰️ Desplazando vista satelital hacia {seleccion}..."):

            time.sleep(0.7)
        
        if es_global:
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

    # CAPA DE SECCIONES (Esta es la capa base del choropleth)
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

    # ---------------------------------------------------------
    # 👇 AQUÍ INSERTA EL BLOQUE DE LA CAPA DE MANZANAS 👇
    # ---------------------------------------------------------
    if not es_global:
        st.sidebar.markdown("---")
        # Checkbox en el sidebar para activar la capa
        ver_manzanas = st.sidebar.checkbox("🏘️ Mostrar Manzanas (INEGI)", value=False)
        
        if ver_manzanas:
            with st.spinner(f"Cargando manzanas de {seleccion}..."):
                # Llamada a la función externa que definimos antes
                gdf_mz = load_manzanas_optimizadas(seleccion)
                
                if gdf_mz is not None and not gdf_mz.empty:
                    fg_manzanas = folium.FeatureGroup(name="Manzanas (INEGI)", show=True)
                    
                    folium.GeoJson(
                        gdf_mz,
                        style_function=lambda x: {
                            'fillColor': 'transparent', # Transparente para ver el color de fondo
                            'color': '#444444',         # Gris oscuro para las líneas
                            'weight': 0.7,              # Línea fina
                            'dashArray': '4, 4',        # Línea punteada
                            'opacity': 0.8
                        },
                        # Tooltip con la clave geoestadística si existe
                        tooltip=folium.GeoJsonTooltip(fields=['CVEGEO'], aliases=['Clave:'], localize=True) if 'CVEGEO' in gdf_mz.columns else None
                    ).add_to(fg_manzanas)
                    
                    fg_manzanas.add_to(m)
                else:
                    st.toast("No hay manzanas procesadas para esta zona.", icon="⚠️")
    # ---------------------------------------------------------

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
            st.info("Descargas y Reportes")
            
            # Botón 1: CSV
            csv = gdf_view[['seccion', 'nombre_municipio', 'Supervisor_Global', 'encuestas_totales']].to_csv(index=False)
            st.download_button(
                label="⬇️ Descargar Asignación (.csv)",
                data=csv,
                file_name="logistica_guerrero_final.csv",
                mime="text/csv",
                type="primary"
            )
            
            st.write("") 
            
            # Botón 2: Mapa HTML
            map_html = io.BytesIO()
            m.save(map_html, close_file=False)
            st.download_button(
                label="🌍 Descargar Mapa Interactivo (.html)",
                data=map_html.getvalue(),
                file_name=f"mapa_logistica_{seleccion}.html",
                mime="text/html"
            )
    
    # --- NOTA METODOLÓGICA ---
    st.markdown("---")
    with st.expander("ℹ️ Nota Técnica: Metodología de Agrupación (Algoritmo Balanceado)"):
        st.markdown("""
        **¿Cómo se definen los grupos de supervisores?**
        
        Este dashboard no utiliza una agrupación arbitraria. Implementa un modelo de **Optimización Combinatoria (Asignación Lineal)** diseñado para garantizar equidad laboral y eficiencia logística:
        
        1.  **⚖️ Equidad Numérica:** El sistema divide el total de secciones entre el número de supervisores. Se fuerza matemáticamente a que la diferencia entre la carga de trabajo de un supervisor y otro sea de **máximo ±1 sección**. Nadie tiene una carga desproporcionada.
        2.  **📍 Proximidad Geográfica:** Una vez definida la cantidad de secciones, el algoritmo busca que estas sean **vecinas geográficas**. Se minimiza la distancia total que debe recorrer el equipo.
        3.  **📐 Precisión:** Se utiliza la proyección cartográfica `UTM Zona 14N` para realizar cálculos precisos en metros, evitando distorsiones por la curvatura de la tierra.
        """)
# --- FUNCIÓN DEMO SPRINT 2 (DATOS SIMULADOS) ---
def render_demo_monitoreo():
    st.markdown("## 🔮 Previsualización: Módulo de Monitoreo (Sprint 2)")
    st.info("⚠️ **Modo Demostración:** Los datos mostrados a continuación son simulados para visualizar las funcionalidades futuras de control de calidad y avance.")

    # 1. GENERAR DATOS FALSOS (MOCK DATA)
    # Simulamos avance en 20 secciones aleatorias
    data_mock = []
    import random
    
    supervisores = ["Ana G.", "Carlos M.", "Luis R.", "Sofia T."]
    
    for i in range(1, 21):
        meta = random.randint(10, 40)
        hechas = random.randint(0, meta + 5) # Algunas con sobre-muestra
        avance = min(100, int((hechas/meta)*100))
        
        # Simular coordenadas para mapa de auditoría (Cerca de Iguala como ejemplo)
        lat_base = 18.35
        lon_base = -99.53
        # Ruido aleatorio
        lat = lat_base + random.uniform(-0.02, 0.02)
        lon = lon_base + random.uniform(-0.02, 0.02)
        
        # Simular validación GPS (80% validas, 20% invalidas)
        valid_gps = random.choice([True, True, True, True, False])
        
        data_mock.append({
            "Sección": f"{1000+i}",
            "Supervisor": random.choice(supervisores),
            "Encuestador": f"Encuestador {random.randint(1,10)}",
            "Meta": meta,
            "Realizadas": hechas,
            "Avance (%)": avance / 100, # Para formato de barra
            "lat": lat,
            "lon": lon,
            "Status GPS": "✅ Válida" if valid_gps else "❌ Fuera de Zona"
        })
    
    df_mock = pd.DataFrame(data_mock)

    # --- VISUALIZACIÓN 1: BARRAS DE PROGRESO ---
    st.subheader("1. Avance en Tiempo Real por Sección")
    st.dataframe(
        df_mock[["Sección", "Supervisor", "Meta", "Realizadas", "Avance (%)"]],
        use_container_width=True,
        column_config={
            "Avance (%)": st.column_config.ProgressColumn(
                "Progreso",
                help="Avance respecto a la meta",
                format="%.0f%%",
                min_value=0,
                max_value=1,
            )
        },
        hide_index=True
    )

    # --- VISUALIZACIÓN 2: AUDITORÍA GPS ---
    st.subheader("2. Auditoría de Coordenadas (GPS vs Asignación)")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Usamos st.map para rápido, pintando puntos rojos y verdes
        # Separamos validas e invalidas para color
        # Nota: st.map es limitado con colores, para el demo rápido usaremos scatter_chart o pydeck es mejor,
        # pero para HOY, usemos un truco visual simple con st.map coloreando por columna no es nativo facil.
        # Mejor usamos un mapa de folium rápido.
        
        m_audit = folium.Map(location=[18.35, -99.53], zoom_start=13)
        
        for _, row in df_mock.iterrows():
            color = "green" if row["Status GPS"] == "✅ Válida" else "red"
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                popup=f"Encuestador: {row['Encuestador']}<br>Status: {row['Status GPS']}"
            ).add_to(m_audit)
            
        st_folium(m_audit, height=400, use_container_width=True)
        
    with col2:
        st.caption("Puntos Rojos indican encuestas realizadas fuera de la manzana asignada.")
        st.metric("Encuestas Auditable", len(df_mock))
        errores = len(df_mock[df_mock["Status GPS"] == "❌ Fuera de Zona"])
        st.metric("Posibles Errores GPS", errores, delta=f"-{errores}", delta_color="inverse")

    # --- VISUALIZACIÓN 3: PRODUCTIVIDAD ---
    st.subheader("3. Productividad por Supervisor")
    prod_df = df_mock.groupby("Supervisor")["Realizadas"].sum().reset_index().sort_values("Realizadas", ascending=False)
    
    st.bar_chart(prod_df, x="Supervisor", y="Realizadas", color="#3cb44b")

if __name__ == "__main__":
    main()