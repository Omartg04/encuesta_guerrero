import streamlit as st

import folium

from streamlit_folium import st_folium

from folium.plugins import Search, Fullscreen

import io

import time

import geopandas as gpd # Importante para que no falle el filtro de manzanas



# Importaciones Modulares

from src.config import MUNICIPIOS_MAP, SUPERVISORES_CONFIG, COLORS

from src.loader import get_data, load_manzanas_optimizadas

from src.logic import balanced_cluster_optimization, procesar_todo_el_estado



# --- CONFIGURACIÓN ---

st.set_page_config(

    page_title="Logística Electoral Guerrero", 

    page_icon="🗳️",

    layout="wide"

)



# Estilos CSS

st.markdown("<style>.block-container {padding-top: 1rem; padding-bottom: 2rem;}</style>", unsafe_allow_html=True)



# --- MAIN ---

def main():

    st.title("🗳️ Tablero de Mando Logístico - Guerrero")



    # 1. CARGA DE DATOS

    gdf = get_data()

    if gdf is None: st.stop()



    # 2. SIDEBAR Y FILTROS

    with st.sidebar:

        st.header("Filtros de Visualización")

        

        # Selector de Territorio

        opciones_menu = list(MUNICIPIOS_MAP.keys()) + ["VISTA GENERAL (TODOS)"]

        seleccion = st.selectbox("Seleccionar Territorio", opciones_menu)

        es_global = seleccion == "VISTA GENERAL (TODOS)"

        

        # Procesamiento de Datos (Con transición suave)

        with st.spinner(f"🛰️ Procesando {seleccion}..."):

            time.sleep(0.5) # Pequeña latencia estética

            

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



        # Filtro por Supervisor (Solo visible si no es Global)

        supervisor_filtro = "Todos"

        if not es_global:

            st.markdown("---")

            st.subheader("👤 Filtro Operativo")

            

            if 'Supervisor_ID' in gdf_view.columns:

                lista_sups = sorted(gdf_view['Supervisor_ID'].unique())

                opciones_sup = ["Todos"] + list(lista_sups)

                

                supervisor_sel = st.selectbox("Seleccionar Supervisor", opciones_sup)

                

                if supervisor_sel != "Todos":

                    # Filtramos el dataframe para dejar solo ese supervisor

                    gdf_view = gdf_view[gdf_view['Supervisor_ID'] == supervisor_sel].copy()

                    st.success(f"Zona: Supervisor {supervisor_sel}")

                    supervisor_filtro = str(supervisor_sel)



        st.divider()

        st.metric("Total Secciones", len(gdf_view))

        st.metric("Meta Encuestas", gdf_view['encuestas_totales'].sum())



    # 3. MAPA PRINCIPAL

    # Centro dinámico del mapa

    lat = gdf_view.geometry.centroid.y.mean()

    lon = gdf_view.geometry.centroid.x.mean()

    

    # Zoom inteligente: Más cerca si estamos viendo un solo supervisor

    zoom_base = 9 if es_global else (12 if supervisor_filtro == "Todos" else 14)

    

    m = folium.Map(location=[lat, lon], zoom_start=zoom_base, tiles=None)

    

    # Capas Base

    folium.TileLayer('CartoDB positron', name="Calle").add_to(m)

    folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite').add_to(m)



    # Función para colorear grupos

    def get_color(id_val):

        try:

            if isinstance(id_val, str) and "-" in id_val: num = int(id_val.split("-")[1])

            else: num = int(id_val)

            return COLORS[(num - 1) % len(COLORS)]

        except: return "gray"



    # Capa de Secciones (Polígonos de colores)

    geo_json = folium.GeoJson(

        gdf_view,

        name="Secciones",

        style_function=lambda x: {

            'fillColor': get_color(x['properties']['Supervisor_Global']),

            'color': 'black', 

            'weight': 2 if supervisor_filtro != "Todos" else 1, # Borde grueso si es filtro individual

            'fillOpacity': 0.6

        },

        tooltip=folium.GeoJsonTooltip(fields=['seccion', 'Supervisor_Global', 'encuestas_totales'], localize=True),

        popup=folium.GeoJsonPopup(fields=['seccion'])

    ).add_to(m)



    # Capa de Manzanas (Lógica inteligente de carga)

    if not es_global:

        # Se activa por defecto si filtramos un supervisor específico

        default_manzanas = True if supervisor_filtro != "Todos" else False

        ver_manzanas = st.sidebar.checkbox("Mostrar Manzanas (INEGI)", value=default_manzanas)

        

        if ver_manzanas:

            gdf_mz = load_manzanas_optimizadas(seleccion)

            if gdf_mz is not None:

                # Filtramos las manzanas para que coincidan con la vista actual (Supervisor o Municipio entero)

                gdf_mz_filt = gpd.sjoin(gdf_mz, gdf_view[['geometry']], how='inner', predicate='intersects')

                

                if not gdf_mz_filt.empty:

                    fg = folium.FeatureGroup(name="Manzanas", show=True)

                    folium.GeoJson(

                        gdf_mz_filt,

                        style_function=lambda x: {'fillColor':'transparent','color':'#444','weight':0.7,'dashArray':'5,5'},

                        tooltip=folium.GeoJsonTooltip(fields=['CVEGEO'], aliases=['Clave:'], localize=True) if 'CVEGEO' in gdf_mz_filt.columns else None

                    ).add_to(fg)

                    fg.add_to(m)



    # Controles del Mapa

    Search(layer=geo_json, geom_type="Polygon", placeholder="Buscar Sección", collapsed=False, search_label="seccion").add_to(m)

    Fullscreen().add_to(m)

    folium.LayerControl().add_to(m)

    

    st_folium(m, height=650, use_container_width=True)



    # 4. TABLA Y DESCARGAS

    col1, col2 = st.columns([3, 1])

    

    with col1:

        titulo_tabla = f"📋 Desglose: {('Supervisor ' + supervisor_filtro) if supervisor_filtro != 'Todos' else seleccion}"

        st.subheader(titulo_tabla)

        st.dataframe(gdf_view.drop(columns='geometry'), use_container_width=True, height=300)

    

    with col2:

        st.info("Descargas")

        

        # Nombre de archivo dinámico

        nombre_archivo = f"asignacion_{seleccion}_SUP-{supervisor_filtro}.csv"

        

        # CSV

        csv = gdf_view[['seccion', 'nombre_municipio', 'Supervisor_ID', 'encuestas_totales']].to_csv(index=False)

        st.download_button("⬇️ CSV Filtrado", csv, nombre_archivo, "text/csv", type="primary")

        

        st.write("")

        

        # Mapa HTML

        map_html = io.BytesIO()

        m.save(map_html, close_file=False)

        st.download_button("🌍 Mapa HTML", map_html.getvalue(), f"mapa_{nombre_archivo}.html", "text/html")



if __name__ == "__main__":

    main()