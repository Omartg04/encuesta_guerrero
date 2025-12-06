import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import altair as alt # Para gráficas bonitas
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

    # --- 1. CARGA Y PREPARACIÓN DE DATOS MAESTROS ---
    with st.spinner("Sincronizando datos operativos..."):
        # A. Cargar Metas (Shapefile + Muestra)
        gdf_raw = get_data()
        if gdf_raw is None: st.stop()

        # B. Recalcular Supervisores (Para tener el filtro disponible)
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
        # Apuntamos al archivo procesado por el ETL
        path_bubble = "data/processed/bubble_clean.csv"
        
        if not os.path.exists(path_bubble):
            st.error("⚠️ No hay datos procesados. Ejecuta el ETL primero: python -m src.etl")
            st.stop()
            
        df_bubble = pd.read_csv(path_bubble)

    # --- 2. FILTROS (SIDEBAR) ---
    with st.sidebar:
        # Botón de recarga manual para limpiar caché si se actualizó el CSV
        if st.button("🔄 Recargar Datos"):
            st.cache_data.clear()
            st.rerun()
            
        st.header("Nivel de Visualización")
        
        # Filtro 1: Territorio
        opciones_terr = ["TODO EL ESTADO"] + list(MUNICIPIOS_MAP.keys())
        seleccion_terr = st.selectbox("Territorio", opciones_terr)
        
        # Filtro 2: Supervisor (Solo si hay municipio seleccionado)
        seleccion_sup = "Todos"
        if seleccion_terr != "TODO EL ESTADO":
            nombre_oficial = MUNICIPIOS_MAP[seleccion_terr]
            ids_sups = sorted(gdf_maestro[gdf_maestro['nombre_municipio'].str.upper() == nombre_oficial.upper()]['Supervisor_ID'].unique())
            opciones_sup = ["Todos"] + list(ids_sups)
            seleccion_sup = st.selectbox("Supervisor", opciones_sup)

    # --- 3. FILTRADO DE DATOS (CASCADA) ---
    
    # Paso A: Filtrar el Maestro (Metas)
    gdf_view = gdf_maestro.copy()
    if seleccion_terr != "TODO EL ESTADO":
        nombre_oficial = MUNICIPIOS_MAP[seleccion_terr]
        gdf_view = gdf_view[gdf_view['nombre_municipio'].str.upper() == nombre_oficial.upper()]
        
        if seleccion_sup != "Todos":
            gdf_view = gdf_view[gdf_view['Supervisor_ID'] == seleccion_sup]

    # Paso B: Filtrar lo Realizado (Bubble) para que coincida con la vista
    secciones_validas = gdf_view['KEY_JOIN'].astype(str).tolist()
    # Aseguramos tipos compatibles en bubble también
    df_bubble['seccion_str'] = df_bubble['seccion_electoral'].astype(str).str.replace(".0", "", regex=False)
    df_bubble_view = df_bubble[df_bubble['seccion_str'].isin(secciones_validas)].copy()

    # --- 4. CÁLCULOS SOBRE VISTA FILTRADA ---
    
    # Auditoría GPS 
    gdf_auditado = procesar_auditoria_gps(df_bubble_view, gdf_view)
    
    # Avance Global 
    df_avance = calcular_avance_global(df_bubble_view, gdf_view)

# --- 5. KPIs (TOP BAR) ---
    total_meta = df_avance['encuestas_totales'].sum()
    total_real = len(df_bubble_view)
    pct_global = (total_real / total_meta) if total_meta > 0 else 0
    
    # CÁLCULOS DE ESTATUS SECCIONAL
    total_secciones = len(df_avance)
    # Secciones iniciadas (tienen al menos 1 encuesta)
    sec_iniciadas = len(df_avance[df_avance['realizadas'] > 0])
    # Secciones completas (ya llegaron o superaron su meta)
    sec_completas = len(df_avance[df_avance['realizadas'] >= df_avance['encuestas_totales']])
    
    # Calcular restantes para cerrar
    sec_pendientes = total_secciones - sec_completas

    # Métricas de Calidad
    sin_gps = len(gdf_auditado[gdf_auditado['auditoria'] == "⚠️ Sin GPS"])
    fuera_zona = len(gdf_auditado[gdf_auditado['auditoria'] == "❌ Fuera de Zona"])
    con_gps = total_real - sin_gps

    k1, k2, k3, k4 = st.columns(4)
    
    # KPI 1: Avance Global (Encuestas)
    k1.metric(
        "Avance Encuestas", 
        f"{total_real} / {total_meta}", 
        f"{pct_global:.1%}"
    )
    
    # KPI 2: SECCIONES COMPLETAS (NUEVO)
    k2.metric(
        "Secciones Terminadas", 
        f"{sec_completas} / {total_secciones}", 
        f"-{sec_pendientes} pendientes", # Delta negativo muestra cuánto falta
        delta_color="normal"
    )
    
    # KPI 3: Calidad GPS
    k3.metric(
        "Alertas GPS (Fuera Zona)", 
        fuera_zona, 
        delta="Revisar" if fuera_zona > 0 else "OK", 
        delta_color="inverse"
    )
    
    # KPI 4: Productividad
    n_encuestadores = df_bubble_view['id_encuestador'].nunique()
    prom_prod = int(total_real / n_encuestadores) if n_encuestadores > 0 else 0
    k4.metric(
        "Fuerza de Tarea", 
        f"{n_encuestadores} activos", 
        f"~{prom_prod} enc/prom"
    )

    st.divider()
    # --- 6. VISUALIZACIÓN INTELIGENTE (DRILL-DOWN) ---
    
    col_grafica, col_mapa = st.columns([1, 1])

    with col_grafica:
        st.subheader("📈 Desglose de Avance")
        
        # Lógica de Drill-down
        if seleccion_terr == "TODO EL ESTADO":
            dimension = 'nombre_municipio'
            titulo_eje = "Municipio"
        elif seleccion_sup == "Todos":
            dimension = 'Supervisor_Label' 
            titulo_eje = "Grupo Supervisor"
        else:
            dimension = 'seccion' # O KEY_JOIN
            titulo_eje = "Sección Electoral"

        # Agrupación dinámica
        chart_data = df_avance.groupby(dimension).agg({
            'realizadas': 'sum',
            'encuestas_totales': 'sum'
        }).reset_index()
        
        chart_data['Avance %'] = chart_data['realizadas'] / chart_data['encuestas_totales']

        # Gráfica Altair
        base = alt.Chart(chart_data).encode(
            y=alt.Y(f'{dimension}:N', sort='-x', title=titulo_eje),
            tooltip=[dimension, 'realizadas', 'encuestas_totales', alt.Tooltip('Avance %', format='.1%')]
        )

        barras_meta = base.mark_bar(color='#eee').encode(x='encuestas_totales:Q')
        barras_real = base.mark_bar(color='#3cb44b').encode(x='realizadas:Q')
        
        texto = base.mark_text(align='left', dx=2).encode(
            x='realizadas:Q', 
            text=alt.Text('Avance %', format='.0%')
        )

        st.altair_chart((barras_meta + barras_real + texto), use_container_width=True)

        with st.expander("🏆 Ranking de Encuestadores (En esta zona)"):
            ranking = df_bubble_view['id_encuestador'].value_counts().reset_index()
            ranking.columns = ['ID', 'Encuestas']
            st.dataframe(ranking, use_container_width=True, height=200)

    with col_mapa:
        st.subheader("📍 Auditoría Geoespacial")
        
        # Filtro de puntos visual
        ver_errores = st.toggle("Ver solo errores GPS", value=False)
        
        # PREPARAR DATOS PARA EL MAPA
        if ver_errores:
            puntos_mapa = gdf_auditado[gdf_auditado['auditoria'] == "❌ Fuera de Zona"]
        else:
            # Mostramos válidas y errores (excluyendo las que no tienen GPS)
            puntos_mapa = gdf_auditado[gdf_auditado['auditoria'].isin(["✅ Válida", "❌ Fuera de Zona"])]

        # --- FILTRO CRÍTICO ANTI-ERROR ---
        # Eliminamos filas que tengan NaN en lat/lon antes de pasarlas a Folium
        puntos_mapa = puntos_mapa.dropna(subset=['latitud', 'longitud'])
        # ---------------------------------

        # Mapa base
        lat = gdf_view.geometry.centroid.y.mean()
        lon = gdf_view.geometry.centroid.x.mean()
        zoom = 9 if seleccion_terr == "TODO EL ESTADO" else (12 if seleccion_sup == "Todos" else 14)

        m = folium.Map([lat, lon], zoom_start=zoom, tiles="CartoDB positron")

        # Capa Polígonos (Metas)
        folium.GeoJson(
            gdf_view,
            style_function=lambda x: {'fillColor': '#999', 'color': '#666', 'weight': 1, 'fillOpacity': 0.1},
            tooltip=folium.GeoJsonTooltip(['seccion', 'encuestas_totales'], aliases=['Sección:', 'Meta:'])
        ).add_to(m)

        # Capa Puntos (Realizado)
        limit_points = 2000 
        if len(puntos_mapa) > limit_points:
            st.caption(f"⚠️ Mostrando solo los últimos {limit_points} puntos con GPS.")
            puntos_mapa = puntos_mapa.head(limit_points)

        for _, row in puntos_mapa.iterrows():
            c = "red" if row['auditoria'] == "❌ Fuera de Zona" else "#00c853"
            folium.CircleMarker(
                [row['latitud'], row['longitud']],
                radius=4, color=c, fill=True, fill_color=c, fill_opacity=0.8, weight=0,
                tooltip=f"{row['id_encuestador']} ({row['auditoria']})"
            ).add_to(m)

        st_folium(m, height=550, use_container_width=True)

# ... (Después de st_folium y las columnas anteriores) ...

    st.markdown("---")
    st.subheader("🚨 Semáforo de Rezago Seccional")
    
    # 1. PREPARACIÓN DE DATOS
    # Filtramos columnas útiles y ordenamos por menor avance
    df_rezago = df_avance.copy()
    
    # Clasificación de Status para facilitar lectura
    def clasificar_status(row):
        if row['realizadas'] == 0: return "🔴 Sin Iniciar"
        if row['porcentaje'] < 30: return "🟠 Rezago Crítico"
        if row['porcentaje'] < 80: return "🟡 En Proceso"
        return "🟢 Completada"

    df_rezago['Estatus'] = df_rezago.apply(clasificar_status, axis=1)
    
    # Seleccionar columnas para mostrar
    cols_mostrar = ['nombre_municipio', 'seccion_electoral', 'encuestas_totales', 'realizadas', 'porcentaje', 'Estatus']
    
    # Ordenar: Primero las de 0%, luego las de menor porcentaje
    df_rezago = df_rezago.sort_values(by=['porcentaje', 'realizadas'], ascending=[True, True])

    # 2. MÉTRICAS DE ALERTA
    secciones_cero = len(df_rezago[df_rezago['realizadas'] == 0])
    secciones_criticas = len(df_rezago[(df_rezago['porcentaje'] < 30) & (df_rezago['realizadas'] > 0)])
    
    col_alerta1, col_alerta2, col_descarga = st.columns([1, 1, 2])
    col_alerta1.metric("🔴 Secciones en Cero", secciones_cero, help="No se ha levantado ninguna encuesta")
    col_alerta2.metric("🟠 Avance Lento (<30%)", secciones_criticas, help="Secciones iniciadas pero muy atrasadas")
    
    with col_descarga:
        st.write("") # Espacio para alinear
        # Botón para descargar reporte de rezago para coordinadores
        csv_rezago = df_rezago[cols_mostrar].to_csv(index=False)
        st.download_button(
            "⬇️ Descargar Reporte de Focos Rojos (.csv)",
            csv_rezago,
            "reporte_rezago_diario.csv",
            "text/csv",
            type="primary"
        )

    # 3. TABLA VISUAL DE REZAGO
    # Mostramos las top 50 peores para no saturar
    st.dataframe(
        df_rezago[cols_mostrar].head(50),
        use_container_width=True,
        column_config={
            "nombre_municipio": "Municipio",
            "seccion_electoral": "Sección",
            "encuestas_totales": "Meta",
            "realizadas": "Hechas",
            "porcentaje": st.column_config.ProgressColumn(
                "Avance %",
                format="%.1f%%",
                min_value=0,
                max_value=100, # Ajusta a 100 porque calculamos porcentaje * 100 antes, o quita el *100 en audit.py y usa max_value=1
            ),
            "Estatus": st.column_config.TextColumn(
                "Estado",
                help="🔴=0, 🟠<30%, 🟡<80%, 🟢>80%",
            )
        },
        hide_index=True
    )

if __name__ == "__main__":
    main()