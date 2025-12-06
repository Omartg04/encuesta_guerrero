import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import altair as alt 
from streamlit_folium import st_folium
import os

# Imports modulares
from src.config import MUNICIPIOS_MAP, SUPERVISORES_CONFIG, COLORS
from src.loader import get_data
from src.logic import balanced_cluster_optimization
from src.audit import procesar_auditoria_gps, calcular_avance_global

st.set_page_config(page_title="Monitoreo de Campo", layout="wide")

def main():
    st.title("📊 Centro de Monitoreo y Auditoría")

    # --- 1. CARGA Y PREPARACIÓN ---
    with st.spinner("Sincronizando datos operativos..."):
        # A. Cargar Metas
        gdf_raw = get_data()
        if gdf_raw is None: st.stop()

        # B. Recalcular Supervisores para filtros
        gdf_list = []
        for muni, nombre_oficial in MUNICIPIOS_MAP.items():
            temp = gdf_raw[gdf_raw['nombre_municipio'].str.upper() == nombre_oficial.upper()].copy()
            if not temp.empty:
                temp = balanced_cluster_optimization(temp, SUPERVISORES_CONFIG[muni])
                temp['Supervisor_Label'] = f"{muni[:3]}-{temp['Supervisor_ID']}" 
                gdf_list.append(temp)
        
        if not gdf_list: st.error("No hay datos maestros"); st.stop()
        gdf_maestro = pd.concat(gdf_list) 

        # C. Cargar Datos de Campo (Bubble Limpio)
        path_bubble = "data/processed/bubble_clean.csv"
        
        if not os.path.exists(path_bubble):
            st.error("⚠️ No hay datos procesados. Ejecuta el ETL primero: python -m src.etl")
            st.stop()
            
        df_bubble = pd.read_csv(path_bubble)

    # --- 2. FILTROS SIDEBAR ---
    with st.sidebar:
        if st.button("🔄 Recargar Datos"):
            st.cache_data.clear()
            st.rerun()
            
        st.header("Nivel de Visualización")
        
        opciones_terr = ["TODO EL ESTADO"] + list(MUNICIPIOS_MAP.keys())
        seleccion_terr = st.selectbox("Territorio", opciones_terr)
        
        seleccion_sup = "Todos"
        if seleccion_terr != "TODO EL ESTADO":
            nombre_oficial = MUNICIPIOS_MAP[seleccion_terr]
            ids_sups = sorted(gdf_maestro[gdf_maestro['nombre_municipio'].str.upper() == nombre_oficial.upper()]['Supervisor_ID'].unique())
            opciones_sup = ["Todos"] + list(ids_sups)
            seleccion_sup = st.selectbox("Supervisor", opciones_sup)

    # --- 3. FILTRADO DE DATOS ---
    
    # A. Filtrar Maestro
    gdf_view = gdf_maestro.copy()
    if seleccion_terr != "TODO EL ESTADO":
        nombre_oficial = MUNICIPIOS_MAP[seleccion_terr]
        gdf_view = gdf_view[gdf_view['nombre_municipio'].str.upper() == nombre_oficial.upper()]
        
        if seleccion_sup != "Todos":
            gdf_view = gdf_view[gdf_view['Supervisor_ID'] == seleccion_sup]

    # B. Filtrar Realizado
    secciones_validas = gdf_view['KEY_JOIN'].astype(str).tolist()
    df_bubble['seccion_str'] = df_bubble['seccion_electoral'].astype(str).str.replace(".0", "", regex=False)
    df_bubble_view = df_bubble[df_bubble['seccion_str'].isin(secciones_validas)].copy()

    # --- 4. CÁLCULOS ---
    
    gdf_auditado = procesar_auditoria_gps(df_bubble_view, gdf_view)
    df_avance = calcular_avance_global(df_bubble_view, gdf_view)

    # --- 5. KPIs ---
    total_meta = df_avance['encuestas_totales'].sum()
    total_real = len(df_bubble_view)
    pct_global = (total_real / total_meta) if total_meta > 0 else 0
    
    # Estatus Seccional
    sec_iniciadas = len(df_avance[df_avance['realizadas'] > 0])
    # Consideramos completa si realizadas >= totales
    sec_completas = len(df_avance[df_avance['realizadas'] >= df_avance['encuestas_totales']])
    sec_pendientes = len(df_avance) - sec_completas

    # Calidad GPS
    sin_gps = len(gdf_auditado[gdf_auditado['auditoria'] == "⚠️ Sin GPS"])
    fuera_zona = len(gdf_auditado[gdf_auditado['auditoria'] == "❌ Fuera de Zona"])
    con_gps = total_real - sin_gps

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Avance Encuestas", f"{total_real} / {total_meta}", f"{pct_global:.1%}")
    k2.metric("Secciones Terminadas", f"{sec_completas} / {len(df_avance)}", f"-{sec_pendientes} pendientes", delta_color="normal")
    k3.metric("Alertas GPS", fuera_zona, delta="Revisar" if fuera_zona > 0 else "OK", delta_color="inverse")
    
    n_enc = df_bubble_view['id_encuestador'].nunique()
    prom = int(total_real / n_enc) if n_enc > 0 else 0
    k4.metric("Fuerza de Tarea", f"{n_enc} activos", f"~{prom} enc/prom")

    st.divider()

    # --- 6. GRÁFICAS Y MAPAS ---
    
    col_grafica, col_mapa = st.columns([1, 1])

    with col_grafica:
        st.subheader("📈 Desglose de Avance")
        
        if seleccion_terr == "TODO EL ESTADO":
            dim = 'nombre_municipio'; tit = "Municipio"
        elif seleccion_sup == "Todos":
            dim = 'Supervisor_Label'; tit = "Grupo Supervisor"
        else:
            dim = 'seccion'; tit = "Sección Electoral"

        chart_data = df_avance.groupby(dim).agg({'realizadas': 'sum', 'encuestas_totales': 'sum'}).reset_index()
        chart_data['Avance %'] = chart_data['realizadas'] / chart_data['encuestas_totales']

        base = alt.Chart(chart_data).encode(
            y=alt.Y(f'{dim}:N', sort='-x', title=tit),
            tooltip=[dim, 'realizadas', 'encuestas_totales', alt.Tooltip('Avance %', format='.1%')]
        )
        barras = base.mark_bar(color='#eee').encode(x='encuestas_totales:Q') + \
                 base.mark_bar(color='#3cb44b').encode(x='realizadas:Q')
        texto = base.mark_text(align='left', dx=2).encode(x='realizadas:Q', text=alt.Text('Avance %', format='.0%'))

        st.altair_chart((barras + texto), use_container_width=True)

        with st.expander("🏆 Ranking de Encuestadores"):
            ranking = df_bubble_view['id_encuestador'].value_counts().reset_index()
            ranking.columns = ['ID', 'Encuestas']
            st.dataframe(ranking, use_container_width=True, height=200)

    with col_mapa:
        st.subheader("📍 Auditoría Geoespacial")
        ver_errores = st.toggle("Ver solo errores GPS", value=False)
        
        if ver_errores:
            puntos_mapa = gdf_auditado[gdf_auditado['auditoria'] == "❌ Fuera de Zona"]
        else:
            puntos_mapa = gdf_auditado[gdf_auditado['auditoria'].isin(["✅ Válida", "❌ Fuera de Zona"])]

        # FILTRO DE SEGURIDAD PARA FOLIUM (Evita error NaNs)
        puntos_mapa = puntos_mapa.dropna(subset=['latitud', 'longitud'])

        lat = gdf_view.geometry.centroid.y.mean()
        lon = gdf_view.geometry.centroid.x.mean()
        zoom = 9 if seleccion_terr == "TODO EL ESTADO" else (12 if seleccion_sup == "Todos" else 14)

        m = folium.Map([lat, lon], zoom_start=zoom, tiles="CartoDB positron")

        folium.GeoJson(
            gdf_view,
            style_function=lambda x: {'fillColor': '#999', 'color': '#666', 'weight': 1, 'fillOpacity': 0.1},
            tooltip=folium.GeoJsonTooltip(['seccion'])
        ).add_to(m)

        limit = 2000
        if len(puntos_mapa) > limit:
            st.caption(f"⚠️ Mostrando últimos {limit} puntos.")
            puntos_mapa = puntos_mapa.head(limit)

        for _, row in puntos_mapa.iterrows():
            c = "red" if row['auditoria'] == "❌ Fuera de Zona" else "#00c853"
            folium.CircleMarker(
                [row['latitud'], row['longitud']],
                radius=4, color=c, fill=True, fill_color=c, fill_opacity=0.8, weight=0,
                tooltip=f"{row['id_encuestador']} ({row['auditoria']})"
            ).add_to(m)

        st_folium(m, height=550, use_container_width=True)

# --- 7. SEMÁFORO DE REZAGO (AL FINAL) ---
    st.markdown("---")
    st.subheader("🚨 Semáforo de Rezago Seccional")
    
    df_rezago = df_avance.copy()
    
    # --- PARCHE DE SEGURIDAD DE ESCALA ---
    if df_rezago['porcentaje'].mean() < 5:
        df_rezago['porcentaje'] = df_rezago['porcentaje'] * 100

    # --- NUEVO: GARANTÍA DE ETIQUETA DE SUPERVISOR ---
    # Creamos una columna limpia 'Supervisor' combinando Municipio y ID
    # Esto asegura que siempre diga "IGU-1" en lugar de solo "1" o datos raros
    try:
        df_rezago['Supervisor'] = df_rezago.apply(
            lambda x: f"{str(x['nombre_municipio'])[:3].upper()}-{int(x['Supervisor_ID'])}", 
            axis=1
        )
    except:
        # Fallback por si algo raro pasa con los datos
        df_rezago['Supervisor'] = "N/A"

    # Clasificación de Status
    def clasificar_status(row):
        val = row['porcentaje']
        if row['realizadas'] == 0: return "🔴 Sin Iniciar"
        if val < 30: return "🟠 Rezago Crítico"
        if val < 100: return "🟡 En Proceso"
        return "🟢 Completada"

    df_rezago['Estatus'] = df_rezago.apply(clasificar_status, axis=1)
    
    # COLUMNAS FINALES LIMPIAS
    cols_mostrar = ['nombre_municipio', 'Supervisor', 'seccion', 'encuestas_totales', 'realizadas', 'porcentaje', 'Estatus']
    
    # Ordenar: Prioridad a las vacías y las lentas
    df_rezago = df_rezago.sort_values(by=['porcentaje', 'realizadas'], ascending=[True, True])

    # Métricas de Alerta
    cero = len(df_rezago[df_rezago['realizadas'] == 0])
    lento = len(df_rezago[(df_rezago['porcentaje'] < 30) & (df_rezago['realizadas'] > 0)])
    
    c1, c2, c3 = st.columns([1, 1, 2])
    c1.metric("🔴 En Cero", cero)
    c2.metric("🟠 Lentos (<30%)", lento)
    
    with c3:
        st.write("")
        
        # FILTRO PARA DESCARGA: Solo pendientes (<100%)
        df_pendientes = df_rezago[df_rezago['porcentaje'] < 100].copy()
        
        csv = df_pendientes[cols_mostrar].to_csv(index=False)
        st.download_button(
            label=f"⬇️ Descargar Pendientes ({len(df_pendientes)} secciones)", 
            data=csv, 
            file_name="reporte_rezago_operativo.csv", 
            mime="text/csv", 
            type="primary",
            help="Descarga solo las secciones que no han llegado a la meta."
        )

    # Tabla Visual
    st.dataframe(
        df_rezago[cols_mostrar].head(100),
        use_container_width=True,
        column_config={
            "nombre_municipio": "Municipio",
            "Supervisor": "Supervisor", # Ahora usamos la columna limpia creada arriba
            "seccion": "Sección",
            "encuestas_totales": "Meta",
            "realizadas": "Hechas",
            "porcentaje": st.column_config.ProgressColumn(
                "Avance %",
                format="%.1f%%",
                min_value=0,
                max_value=100,
            ),
            "Estatus": st.column_config.TextColumn("Estado")
        },
        hide_index=True
    )
if __name__ == "__main__":
    main()