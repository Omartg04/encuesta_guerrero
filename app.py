import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Search, Fullscreen
import io
import time
import geopandas as gpd  # <--- ¡AGREGA ESTA LÍNEA!

# Importaciones Modulares
from src.config import MUNICIPIOS_MAP, SUPERVISORES_CONFIG, COLORS
from src.loader import get_data, load_manzanas_optimizadas
from src.logic import balanced_cluster_optimization, procesar_todo_el_estado

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Logística Electoral Guerrero", layout="wide")
st.markdown("<style>.block-container {padding-top: 1rem; padding-bottom: 2rem;}</style>", unsafe_allow_html=True)

# --- FUNCIÓN DEMO SPRINT 2 (Simplificada para mantener funcionalidad) ---
def render_demo_monitoreo():
    st.info("🔮 Módulo Demo disponible en código fuente (Oculto por refactorización)")

# --- MAIN ---
def main():
    st.title("🗳️ Tablero de Mando Logístico - Guerrero")

    # Selector de Modo
    modo = st.sidebar.radio("Modo", ["🗺️ Planeación (Sprint 1)", "🔮 Demo Monitoreo (Sprint 2)"], index=0)
    if modo == "🔮 Demo Monitoreo (Sprint 2)":
        render_demo_monitoreo(); return

    # Carga de datos
    gdf = get_data()
    if gdf is None: st.stop()

    with st.sidebar:
        st.header("Filtros")
        opciones_menu = list(MUNICIPIOS_MAP.keys()) + ["VISTA GENERAL (TODOS)"]
        seleccion = st.selectbox("Seleccionar Territorio", opciones_menu)
        es_global = seleccion == "VISTA GENERAL (TODOS)"
        
        # --- PROCESAMIENTO ---
        with st.spinner(f"🛰️ Procesando {seleccion}..."):
            time.sleep(0.5)
            if es_global:
                gdf_view = procesar_todo_el_estado(gdf)
                total_supervisores = sum(SUPERVISORES_CONFIG.values())
            else:
                nombre_oficial = MUNICIPIOS_MAP[seleccion]
                gdf_view = gdf[gdf['nombre_municipio'].str.upper() == nombre_oficial.upper()].copy()
                total_supervisores = SUPERVISORES_CONFIG[seleccion]
                gdf_view = balanced_cluster_optimization(gdf_view, total_supervisores)
                gdf_view['Supervisor_Global'] = gdf_view['Supervisor_ID']

        if gdf_view.empty: st.warning("Sin datos"); st.stop()

        # --- NUEVA FUNCIONALIDAD: FILTRO POR SUPERVISOR ---
        supervisor_filtro = "Todos"
        if not es_global:
            st.markdown("---")
            st.subheader("👤 Filtro Operativo")
            # Obtenemos lista única de supervisores
            lista_sups = sorted(gdf_view['Supervisor_ID'].unique())
            # Creamos opciones: [Todos, 1, 2, 3...]
            opciones_sup = ["Todos"] + list(lista_sups)
            
            supervisor_sel = st.selectbox("Seleccionar Supervisor", opciones_sup)
            
            if supervisor_sel != "Todos":
                # FILTRADO DEL DATAFRAME
                gdf_view = gdf_view[gdf_view['Supervisor_ID'] == supervisor_sel].copy()
                st.success(f"Mostrando zona del Supervisor {supervisor_sel}")
                supervisor_filtro = str(supervisor_sel)

        st.divider()
        st.metric("Total Secciones", len(gdf_view))
        st.metric("Meta Encuestas", gdf_view['encuestas_totales'].sum())

    # --- MAPA ---
    lat = gdf_view.geometry.centroid.y.mean()
    lon = gdf_view.geometry.centroid.x.mean()
    # Ajuste de zoom: Si filtramos un supervisor, hacemos zoom in
    zoom_base = 9 if es_global else (12 if supervisor_filtro == "Todos" else 14)
    
    m = folium.Map(location=[lat, lon], zoom_start=zoom_base, tiles=None)
    folium.TileLayer('CartoDB positron', name="Calle").add_to(m)
    folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite').add_to(m)

    # Función de color
    def get_color(id_val):
        try:
            if isinstance(id_val, str) and "-" in id_val: num = int(id_val.split("-")[1])
            else: num = int(id_val)
            return COLORS[(num - 1) % len(COLORS)]
        except: return "gray"

    # Capa Secciones
    geo_json = folium.GeoJson(
        gdf_view,
        name="Secciones",
        style_function=lambda x: {
            'fillColor': get_color(x['properties']['Supervisor_Global']),
            'color': 'black', 'weight': 2 if supervisor_filtro != "Todos" else 1, # Borde más grueso si es filtro individual
            'fillOpacity': 0.6
        },
        tooltip=folium.GeoJsonTooltip(fields=['seccion', 'Supervisor_Global', 'encuestas_totales'], localize=True),
        popup=folium.GeoJsonPopup(fields=['seccion'])
    ).add_to(m)

    # Capa Manzanas (Solo si no es global y hay filtro o checkbox)
    if not es_global:
        # Si seleccionamos un supervisor, activamos manzanas por defecto para ayudarle
        default_manzanas = True if supervisor_filtro != "Todos" else False
        ver_manzanas = st.sidebar.checkbox("Mostrar Manzanas", value=default_manzanas)
        
        if ver_manzanas:
            gdf_mz = load_manzanas_optimizadas(seleccion)
            if gdf_mz is not None:
                # IMPORTANTE: Filtrar también las manzanas para ese supervisor
                # Spatial Join rápido: manzanas que tocan las secciones del supervisor filtrado
                gdf_mz_filt = gpd.sjoin(gdf_mz, gdf_view[['geometry']], how='inner', predicate='intersects')
                
                if not gdf_mz_filt.empty:
                    fg = folium.FeatureGroup(name="Manzanas", show=True)
                    folium.GeoJson(
                        gdf_mz_filt,
                        style_function=lambda x: {'fillColor':'transparent','color':'#444','weight':0.7,'dashArray':'5,5'},
                        tooltip=folium.GeoJsonTooltip(fields=['CVEGEO'], aliases=['Clave:'], localize=True) if 'CVEGEO' in gdf_mz_filt.columns else None
                    ).add_to(fg)
                    fg.add_to(m)

    Search(layer=geo_json, geom_type="Polygon", placeholder="Buscar Sección", collapsed=False, search_label="seccion").add_to(m)
    Fullscreen().add_to(m)
    folium.LayerControl().add_to(m)
    st_folium(m, height=650, use_container_width=True)

    # --- DESCARGAS ---
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"📋 Desglose: {('Supervisor ' + supervisor_filtro) if supervisor_filtro != 'Todos' else seleccion}")
        st.dataframe(gdf_view.drop(columns='geometry'), use_container_width=True, height=300)
    
    with col2:
        st.info("Descargas")
        # El CSV ahora descargará SOLO lo que esté filtrado (ej. solo Supervisor 1)
        nombre_archivo = f"asignacion_{seleccion}_SUP-{supervisor_filtro}.csv"
        csv = gdf_view[['seccion', 'nombre_municipio', 'Supervisor_ID', 'encuestas_totales']].to_csv(index=False)
        st.download_button("⬇️ CSV Filtrado", csv, nombre_archivo, "text/csv", type="primary")
        
        map_html = io.BytesIO(); m.save(map_html, close_file=False)
        st.download_button("🌍 Mapa HTML", map_html.getvalue(), f"mapa_{nombre_archivo}.html", "text/html")

if __name__ == "__main__":
    main()