import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import os
from src.loader import get_data
from src.audit_advanced import auditar_fechas, auditar_tiempos, etiquetar_gps
from src.preprocessor import load_and_standardize
from src.auth import bloquear_acceso

st.set_page_config(page_title="Auditoría y Estandarización", layout="wide")
bloquear_acceso()

def main():
    st.title("🔍 Auditoría (Base Estandarizada)")
    st.markdown("Proceso: **Carga Raw** ➡️ **Renombrado** ➡️ **Auditoría** ➡️ **Base Maestra**.")

    # --- 1. CONFIGURACIÓN ---
    INPUT_FILE = "data/raw/bubble_sync/export_full.csv"
    DICCIONARIO_FILE = "Diccionario Variables.xlsx" 
    
    # Nombres nuevos (según tu diccionario)
    COL_CREATED = "fecha_creacion"
    COL_MODIFIED = "fecha_modificacion"
    COL_LAT = "latitud"
    COL_LON = "longitud"
    COL_SECCION = "seccion_electoral"
    COL_ENCUESTADOR = "id_encuestador" 
    
    # --- 2. SIDEBAR (CONFIGURACIÓN Y DESCARGA) ---
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # MEJORA 1: Botón para descargar el Diccionario Original
        if os.path.exists(DICCIONARIO_FILE):
            with open(DICCIONARIO_FILE, "rb") as f:
                st.download_button(
                    label="📥 Bajar Diccionario de Variables",
                    data=f,
                    file_name="Diccionario_Referencia.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        else:
            st.warning("⚠️ No se encontró el archivo del diccionario.")
            
        st.divider()
        st.subheader("Reglas de Limpieza")
        fecha_corte = st.date_input("Fecha Inicio", pd.to_datetime("2025-12-05"))
        min_tiempo = st.number_input("Minutos Mínimos", 0, 60, 2)
        buffer_mts = st.slider("Tolerancia GPS (m)", 0, 300, 50)
        
        st.divider()
        if st.button("🔄 RECALCULAR", type="primary"):
            st.rerun()

    # --- 3. CARGA Y ESTANDARIZACIÓN ---
    with st.spinner("Procesando Base Maestra..."):
        try:
            # Cargamos CSV Original para comparar columnas (Mejora 3)
            df_original = pd.read_csv(INPUT_FILE)
            
            # Procesamos
            df = load_and_standardize(INPUT_FILE, DICCIONARIO_FILE)
            gdf_secciones = get_data()
            
            # GeoDataFrame
            gdf_puntos = gpd.GeoDataFrame(
                df, geometry=gpd.points_from_xy(df[COL_LON], df[COL_LAT]), crs="EPSG:4326"
            )
            
        except Exception as e:
            st.error(f"Error crítico: {e}"); st.stop()

    # --- MEJORA 3: REPORTE DE INTEGRIDAD DE COLUMNAS ---
    # Calculamos qué columnas se perdieron en el proceso
    # (Puede ser intencional, pero mejor avisar)
    cols_orig = set(df_original.columns) # Nombres viejos
    # Esta comparación es compleja porque los nombres cambian. 
    # Simplemente mostramos cuántas columnas quedaron vs originales.
    
    with st.expander(f"ℹ️ Reporte de Estructura (Columnas: {len(df_original.columns)} ➡️ {len(df.columns)})"):
        c_info1, c_info2 = st.columns(2)
        c_info1.info(f"Columnas en CSV Original: **{len(df_original.columns)}**")
        c_info2.success(f"Columnas en Base Maestra: **{len(df.columns)}** (Según tu lista ordenada)")
        st.caption("Si este número es menor al esperado, revisa que no falten variables en `COLUMNAS_ORDENADAS` (src/preprocessor.py).")

    # --- 4. AUDITORÍA ---
    total_raw = len(df)
    
    df_step1, rech_fechas = auditar_fechas(df, COL_CREATED, str(fecha_corte))
    df_step2, rech_tiempos = auditar_tiempos(df_step1, COL_CREATED, COL_MODIFIED, min_tiempo)
    
    gdf_step2 = gpd.GeoDataFrame(
        df_step2, geometry=gpd.points_from_xy(df_step2[COL_LON], df_step2[COL_LAT]), crs="EPSG:4326"
    )
    df_final = etiquetar_gps(
        gdf_step2, gdf_secciones, 
        col_seccion_puntos=COL_SECCION, col_seccion_poligonos='KEY_JOIN', 
        buffer_metros=buffer_mts
    )

    # --- 5. KPIs ---
    total_final = len(df_final)
    total_rechazados = len(rech_fechas) + len(rech_tiempos)
    
    tiempos_reales = df_final[df_final['duracion_min'] > 0]['duracion_min']
    promedio_tiempo = tiempos_reales.mean() if not tiempos_reales.empty else 0
    
    # Manejo seguro si no existe la columna encuestador
    if COL_ENCUESTADOR in df_final.columns:
        n_enc = df_final[COL_ENCUESTADOR].nunique()
        prod_prom = total_final / n_enc if n_enc > 0 else 0
    else:
        prod_prom = 0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Muestra Final", total_final, f"{total_final/total_raw:.1%} recuperada")
    k2.metric("Eliminadas", total_rechazados, delta="Filtro Duro", delta_color="inverse")
    k3.metric("Tiempo Promedio", f"{promedio_tiempo:.1f} min", delta="Objetivo: 10-15m", delta_color="off")
    k4.metric("Prod. Encuestador", f"{prod_prom:.0f} enc")

    st.divider()

    # --- 6. MEJORA 2: TABLA CON SEMÁFORO DE RECUPERACIÓN ---
    st.subheader("🏙️ Impacto Territorial (Efectividad)")
    
    catalogo = gdf_secciones[['KEY_JOIN', 'nombre_municipio']].drop_duplicates()
    catalogo['KEY_JOIN'] = catalogo['KEY_JOIN'].astype(str)
    
    df['seccion_str'] = df[COL_SECCION].astype(str).str.replace(".0", "", regex=False)
    df_final['seccion_str'] = df_final[COL_SECCION].astype(str).str.replace(".0", "", regex=False)
    
    df_raw_muni = df.merge(catalogo, left_on='seccion_str', right_on='KEY_JOIN', how='left')
    df_fin_muni = df_final.merge(catalogo, left_on='seccion_str', right_on='KEY_JOIN', how='left')
    
    count_raw = df_raw_muni['nombre_municipio'].value_counts().rename("Original")
    count_fin = df_fin_muni['nombre_municipio'].value_counts().rename("Final")
    
    tabla = pd.concat([count_raw, count_fin], axis=1).fillna(0).astype(int)
    tabla['Eliminadas'] = tabla['Original'] - tabla['Final']
    
    # Cálculo de Recuperación (0 a 1)
    tabla['Recuperacion'] = (tabla['Final'] / tabla['Original']) 
    
    st.dataframe(
        tabla.sort_values('Recuperacion', ascending=True), # Ordenar: los peores arriba
        use_container_width=True,
        column_config={
            "Original": st.column_config.NumberColumn("Muestra Bruta", format="%d"),
            "Final": st.column_config.NumberColumn("Muestra Neta", format="%d"),
            "Eliminadas": st.column_config.NumberColumn("📉 Bajas", format="%d ❌"),
            "Recuperacion": st.column_config.ProgressColumn(
                "✅ % Recuperación", # Título claro
                format="%.1f%%",
                min_value=0,
                max_value=1,
                help="Porcentaje de la muestra bruta que pasó los filtros de calidad."
            )
        }
    )

    # --- 7. VISUALES Y DESCARGAS ---
    st.write("")
    tab_mapa, tab_tiempo = st.tabs(["📍 Mapa de Calidad", "⏱️ Tiempos"])

    with tab_mapa:
        c_map, c_pie = st.columns([3, 1])
        with c_map:
            fig_map = px.scatter_mapbox(
                df_final, lat=COL_LAT, lon=COL_LON, color="GPS_STATUS",
                color_discrete_map={"✅ Válida": "#00CC96", "⚠️ Revisar": "#EF553B"},
                zoom=8, height=500, mapbox_style="carto-positron"
            )
            st.plotly_chart(fig_map, use_container_width=True)
        with c_pie:
            st.write("**Calidad GPS**")
            conteo_gps = df_final['GPS_STATUS'].value_counts().reset_index()
            fig_pie = px.pie(
                conteo_gps, values='count', names='GPS_STATUS',
                color='GPS_STATUS',
                color_discrete_map={"✅ Válida": "#00CC96", "⚠️ Revisar": "#EF553B"}
            )
            fig_pie.update_layout(showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab_tiempo:
        if not df_final.empty:
            st.caption("Línea roja: Tu filtro mínimo de tiempo.")
            fig_hist = px.histogram(
                df_final[df_final['duracion_min'] < 45], 
                x="duracion_min", nbins=30, color_discrete_sequence=['#636EFA']
            )
            fig_hist.add_vline(x=min_tiempo, line_dash="dash", line_color="red")
            st.plotly_chart(fig_hist, use_container_width=True)

    st.divider()
    st.subheader("💾 Descargar Resultados")
    
    col_d1, col_d2 = st.columns([1, 1])
    
    with col_d1:
        csv_final = df_final.drop(columns='geometry', errors='ignore').to_csv(index=False)
        st.download_button(
            label="✅ Descargar Base Maestra (.csv)", 
            data=csv_final, 
            file_name="BASE_MAESTRA_ESTANDARIZADA.csv", 
            mime="text/csv", 
            type="primary",
            use_container_width=True
        )
    
    with col_d2:
        rechazados = pd.concat([rech_fechas, rech_tiempos])
        if not rechazados.empty:
            csv_rech = rechazados.to_csv(index=False)
            st.download_button(
                label=f"🗑️ Descargar Rechazados ({len(rechazados)})", 
                data=csv_rech, 
                file_name="rechazados_auditoria.csv", 
                mime="text/csv",
                type="secondary",
                use_container_width=True
            )
        else:
            st.success("¡Base 100% limpia!")

if __name__ == "__main__":
    main()