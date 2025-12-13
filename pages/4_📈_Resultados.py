import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA (SIN LOGIN) ---
st.set_page_config(page_title="Resultados Finales 2025", layout="wide")

# ==============================================================================
# 🗄️ BASE DE DATOS MAESTRA (JUNIO REAL vs DICIEMBRE REAL)
# ==============================================================================

# 1. PROBLEMAS
DATOS_PROBLEMAS = {
    "GUERRERO (ESTATAL)": {"Inseguridad": [47.0, 63.9], "Falta de agua": [4.0, 8.4], "Corrupción": [6.0, 6.2], "Calles mal estado": [1.0, 4.0], "Bajos Salarios": [1.0, 2.9]},
    "ACAPULCO": {"Inseguridad": [56.0, 62.2], "Falta de agua": [4.0, 11.0], "Corrupción": [3.0, 7.3]},
    "CHILPANCINGO": {"Inseguridad": [61.0, 76.2], "Falta de agua": [3.0, 4.0], "Corrupción": [2.0, 3.8]},
    "IGUALA": {"Inseguridad": [59.0, 49.6], "Economía": [4.0, 8.5], "Calles mal estado": [1.0, 6.0]}
}

# 2. VOTO GOBERNADOR (PARTIDOS)
DATOS_VOTO_GOB = {
    "GUERRERO (ESTATAL)": {"MORENA": [48.0, 59.9], "PRI": [16.0, 3.8], "MC": [7.0, 2.5], "PAN": [3.0, 1.6], "PT": [2.0, 1.3], "Ninguno": [10.0, 16.1]},
    "ACAPULCO": {"MORENA": [48.0, 64.7], "PRI": [10.0, 3.4], "MC": [10.0, 2.6], "Ninguno": [11.0, 14.4]},
    "CHILPANCINGO": {"MORENA": [34.0, 46.3], "PRI": [15.0, 5.8], "Ninguno": [19.0, 22.9]},
    "IGUALA": {"MORENA": [41.0, 61.0], "PRI": [16.0, 2.2], "Ninguno": [10.0, 12.2]}
}

# 3. CONOCIMIENTO (Name ID)
DATOS_CONOCIMIENTO = {
    "GUERRERO (ESTATAL)": {"Félix Salgado": [73.0, 73.4], "Abelina López": [48.0, 68.1], "Beatriz Mojica": [44.0, 56.0], "Javier Saldaña": [0.0, 44.9], "Iván Hernández": [8.0, 38.9], "Jacinto Gonzalez": [11.0, 24.6], "Pablo Amílcar": [21.0, 21.0], "Esthela Damián": [7.0, 20.9]},
    "ACAPULCO": {"Abelina López": [89.0, 84.8], "Félix Salgado": [86.0, 74.6], "Iván Hernández": [12.0, 40.5]},
    "CHILPANCINGO": {"Félix Salgado": [83.0, 76.1], "Abelina López": [54.0, 49.2], "Iván Hernández": [17.0, 35.7]},
    "IGUALA": {"Félix Salgado": [86.0, 61.0], "Iván Hernández": [6.0, 36.8], "Abelina López": [37.0, 15.4]}
}

# 4. DATOS PARA HEATMAP (ATRIBUTOS COMPLETOS DIC)
DATOS_HEATMAP_DIC = [
    {"Aspirante": "Iván Hernández", "Honestidad": 33.6, "Cercanía": 35.3, "Der. Mujeres": 37.8, "Conoce Edo": 43.3, "Cumple": 31.9, "Buen Candidato": 65.5},
    {"Aspirante": "Esthela Damián", "Honestidad": 25.5, "Cercanía": 20.1, "Der. Mujeres": 29.5, "Conoce Edo": 21.2, "Cumple": 20.5, "Buen Candidato": 48.3},
    {"Aspirante": "Jacinto González", "Honestidad": 20.1, "Cercanía": 21.7, "Der. Mujeres": 24.0, "Conoce Edo": 27.9, "Cumple": 18.1, "Buen Candidato": 41.2},
    {"Aspirante": "Beatriz Mojica", "Honestidad": 10.1, "Cercanía": 11.3, "Der. Mujeres": 20.8, "Conoce Edo": 21.2, "Cumple": 7.9, "Buen Candidato": 38.5},
    {"Aspirante": "Javier Saldaña", "Honestidad": 7.0, "Cercanía": 11.2, "Der. Mujeres": 7.6, "Conoce Edo": 21.5, "Cumple": 6.1, "Buen Candidato": 25.1},
    {"Aspirante": "Félix Salgado", "Honestidad": 6.9, "Cercanía": 15.6, "Der. Mujeres": 6.8, "Conoce Edo": 34.3, "Cumple": 7.7, "Buen Candidato": 21.9},
    {"Aspirante": "Pablo Amílcar", "Honestidad": 6.2, "Cercanía": 5.1, "Der. Mujeres": 5.0, "Conoce Edo": 9.4, "Cumple": 1.9, "Buen Candidato": 18.8},
    {"Aspirante": "Abelina López", "Honestidad": 9.6, "Cercanía": 14.9, "Der. Mujeres": 14.8, "Conoce Edo": 17.1, "Cumple": 8.8, "Buen Candidato": 14.0}
]

# Datos Evolutivos (Radar)
DATOS_RADAR_EVO = {
    "Iván Hernández": {"Honestidad": [1.7, 33.6], "Der. Mujeres": [2.1, 37.8], "Cercanía": [2.1, 35.3], "Conoce Edo": [2.5, 43.3], "Cumple": [1.4, 31.9]},
    "Félix Salgado": {"Honestidad": [14.3, 6.9], "Der. Mujeres": [15.2, 6.8], "Cercanía": [23.3, 15.6], "Conoce Edo": [41.1, 34.3], "Cumple": [14.3, 7.7]}
}

# 5. CANDIDATO INTERNO (Evolución Preferencia)
DATOS_PREFERENCIA_EVOLUCION = [
    {"Aspirante": "Iván Hernández", "Junio": 4.3, "Dic": 21.5},
    {"Aspirante": "Félix Salgado", "Junio": 19.8, "Dic": 9.3},
    {"Aspirante": "Beatriz Mojica", "Junio": 18.4, "Dic": 10.0},
    {"Aspirante": "Abelina López", "Junio": 5.7, "Dic": 5.8},
    {"Aspirante": "Pablo Amílcar", "Junio": 6.0, "Dic": 1.8},
    {"Aspirante": "Esthela Damián", "Junio": 4.7, "Dic": 6.9}
]

# Foto Final Diciembre
DATOS_INTERNA_TODOS = {
    "GUERRERO (ESTATAL)": {"Iván Hernández": 21.5, "Beatriz Mojica": 10.0, "Félix Salgado": 9.3, "Esthela Damián": 6.9, "Abelina López": 5.8, "Javier Saldaña": 5.2, "Jacinto González": 4.9, "Pablo Amílcar": 1.8, "Ninguno": 16.0},
    "ACAPULCO": {"Iván Hernández": 22.5, "Beatriz Mojica": 12.0, "Félix Salgado": 9.5, "Abelina López": 8.7, "Esthela Damián": 6.5, "Ninguno": 14.9},
    "CHILPANCINGO": {"Iván Hernández": 18.3, "Félix Salgado": 8.7, "Beatriz Mojica": 6.5, "Esthela Damián": 4.7, "Abelina López": 0.3, "Ninguno": 19.2},
    "IGUALA": {"Iván Hernández": 22.5, "Esthela Damián": 12.8, "Félix Salgado": 9.0, "Beatriz Mojica": 6.4, "Ninguno": 15.2}
}

# 6. CAREOS
DATOS_CAREOS_CONST = {
    "GUERRERO (ESTATAL)": {
        "Careo 1 (Félix)": {"MORENA (Félix)": 22.9, "PRI (Añorve)": 2.5, "MC (Julián)": 2.9, "PT": 4.2, "Ninguno": 33.9},
        "Careo 2 (Iván)":  {"MORENA (Iván)": 34.5, "PRI (Añorve)": 2.6, "MC (Julián)": 1.8, "PT": 3.7, "Ninguno": 25.8}
    },
    "ACAPULCO": {
        "Careo 1 (Félix)": {"MORENA (Félix)": 25.8, "Ninguno": 35.7},
        "Careo 2 (Iván)":  {"MORENA (Iván)": 37.9, "Ninguno": 27.1}
    }
}

# ==============================================================================
# 🛠️ FUNCIONES AUXILIARES
# ==============================================================================
def generar_excel_completo():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pd.DataFrame(DATOS_INTERNA_TODOS["GUERRERO (ESTATAL)"].items(), columns=["Candidato", "%"]).to_excel(writer, sheet_name='Interna', index=False)
        pd.DataFrame(DATOS_HEATMAP_DIC).to_excel(writer, sheet_name='Atributos_Heatmap', index=False)
    return output.getvalue()

# ==============================================================================
# 🚀 APP STREAMLIT
# ==============================================================================
def main():
    st.title("📊 Resultados Finales: Guerrero 2025")
    st.markdown("### Tablero de Control Estratégico")

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("📍 Filtro Territorial")
        seleccion = st.selectbox("Seleccionar Vista:", ["GUERRERO (ESTATAL)", "ACAPULCO", "CHILPANCINGO", "IGUALA"])
        st.divider()
        st.download_button("📥 Bajar Excel Completo", data=generar_excel_completo(), file_name="Resultados_Cierre_2025.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

    # --- TABS ORDENADOS ---
    tabs = st.tabs([
        "🚨 1. Problemas", 
        "🏁 2. Partidos", 
        "🧠 3. Conocimiento", 
        "✨ 4. Atributos", 
        "🗳️ 5. Candidato Interno", 
        "🥊 6. Careos"
    ])

    # TAB 1: PROBLEMAS
    with tabs[0]:
        st.subheader(f"Agenda Pública: Principales Problemas - {seleccion}")
        data_p = DATOS_PROBLEMAS.get(seleccion, {})
        df_p = pd.DataFrame([{"Problema": k, "Junio": v[0], "Dic": v[1]} for k,v in data_p.items()])
        df_melt_p = df_p.melt(id_vars="Problema", var_name="Mes", value_name="%")
        fig_p = px.bar(df_melt_p.sort_values("%", ascending=True), x="%", y="Problema", color="Mes", barmode="group", orientation='h', text_auto=True, color_discrete_map={"Junio": "#B0BEC5", "Dic": "#D81B60"})
        st.plotly_chart(fig_p, use_container_width=True)

    # TAB 2: PARTIDOS
    with tabs[1]:
        st.subheader(f"Preferencias Partidistas (Marca) - {seleccion}")
        data_v = DATOS_VOTO_GOB.get(seleccion, {})
        df_v = pd.DataFrame([{"Partido": k, "Junio": v[0], "Dic": v[1]} for k,v in data_v.items()])
        df_melt = df_v.melt(id_vars="Partido", var_name="Mes", value_name="%")
        fig_v = px.bar(df_melt, x="%", y="Partido", color="Mes", barmode="group", orientation='h', text_auto=True, color_discrete_map={"Junio": "#B0BEC5", "Dic": "#880E4F"})
        st.plotly_chart(fig_v, use_container_width=True)

    # TAB 3: CONOCIMIENTO (BARRAS AGRUPADAS)
    with tabs[2]:
        st.subheader(f"Evolución de Conocimiento (Name ID) - {seleccion}")
        st.caption("Comparativo Junio vs Diciembre (Ordenado por Conocimiento Actual)")
        
        data_c = DATOS_CONOCIMIENTO.get(seleccion, {}) if seleccion in DATOS_CONOCIMIENTO else DATOS_CONOCIMIENTO["GUERRERO (ESTATAL)"]
        
        # Preparamos DataFrame para Barras
        df_c = pd.DataFrame([{"Aspirante": k, "Junio": v[0], "Diciembre": v[1]} for k,v in data_c.items()])
        df_melt_c = df_c.melt(id_vars="Aspirante", var_name="Mes", value_name="%")
        
        # Ordenar por valor de Diciembre
        order = df_c.sort_values("Diciembre", ascending=True)["Aspirante"].tolist()
        
        fig_bar_c = px.bar(
            df_melt_c, x="%", y="Aspirante", color="Mes", barmode="group", orientation='h', 
            text_auto=True, 
            category_orders={"Aspirante": order},
            color_discrete_map={"Junio": "#B0BEC5", "Diciembre": "#880E4F"}
        )
        fig_bar_c.update_layout(height=600)
        st.plotly_chart(fig_bar_c, use_container_width=True)

    # TAB 4: ATRIBUTOS (HEATMAP + RADAR)
    with tabs[3]:
        st.subheader("Diagnóstico Cualitativo (Estatal)")
        
        # 1. HEATMAP COMPLETO (DICIEMBRE)
        st.markdown("##### 🚦 Semáforo de Atributos (Diciembre)")
        st.caption("Intensidad de Color: Verde fuerte = Mayor % Positivo")
        
        df_heat = pd.DataFrame(DATOS_HEATMAP_DIC).set_index("Aspirante")
        df_heat = df_heat.sort_values("Buen Candidato", ascending=False)
        
        fig_heat = px.imshow(
            df_heat, text_auto=True, aspect="auto", 
            color_continuous_scale="Greens", origin="lower"
        )
        fig_heat.update_layout(height=500)
        st.plotly_chart(fig_heat, use_container_width=True)
        
        st.divider()

        # 2. RADAR COMPARATIVO (EVOLUCIÓN)
        st.markdown("##### 🕸️ Evolución Estructural: El contraste (Jun vs Dic)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Crecimiento: Iván Hernández**")
            d_ivan = DATOS_RADAR_EVO["Iván Hernández"]
            categories = list(d_ivan.keys())
            
            fig_rad = go.Figure()
            fig_rad.add_trace(go.Scatterpolar(r=[v[0] for v in d_ivan.values()], theta=categories, fill='toself', name='Junio', line_color='#B0BEC5'))
            fig_rad.add_trace(go.Scatterpolar(r=[v[1] for v in d_ivan.values()], theta=categories, fill='toself', name='Diciembre', line_color='#880E4F'))
            fig_rad.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 45])), showlegend=True, height=400)
            st.plotly_chart(fig_rad, use_container_width=True)

        with col2:
            st.markdown("**Desgaste: Félix Salgado**")
            d_felix = DATOS_RADAR_EVO["Félix Salgado"]
            
            fig_rad2 = go.Figure()
            fig_rad2.add_trace(go.Scatterpolar(r=[v[0] for v in d_felix.values()], theta=categories, fill='toself', name='Junio', line_color='#B0BEC5'))
            fig_rad2.add_trace(go.Scatterpolar(r=[v[1] for v in d_felix.values()], theta=categories, fill='toself', name='Diciembre', line_color='#C0392B'))
            fig_rad2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 45])), showlegend=True, height=400)
            st.plotly_chart(fig_rad2, use_container_width=True)

    # TAB 5: CANDIDATO INTERNO
    with tabs[4]:
        st.subheader(f"Definición Candidatura: Encuesta Interna - {seleccion}")
        
        c_evo, c_foto = st.columns([2, 3])
        
        with c_evo:
            st.markdown("###### 📊 Evolución Preferencia (Estatal)")
            st.caption("Cambio porcentual Junio -> Diciembre")
            df_evo = pd.DataFrame(DATOS_PREFERENCIA_EVOLUCION).sort_values("Dic", ascending=True)
            
            fig_slope2 = go.Figure()
            for i, row in df_evo.iterrows():
                color = "#880E4F" if "Iván" in row["Aspirante"] else "#90A4AE"
                if "Félix" in row["Aspirante"]: color = "#C0392B" 
                
                fig_slope2.add_trace(go.Scatter(x=["Jun", "Dic"], y=[row["Junio"], row["Dic"]], mode="lines+markers", name=row["Aspirante"], line=dict(color=color, width=3)))
            
            fig_slope2.update_layout(height=400, showlegend=True, legend=dict(orientation="h"))
            st.plotly_chart(fig_slope2, use_container_width=True)

        with c_foto:
            st.markdown(f"###### 📸 Foto Final Diciembre - {seleccion}")
            st.caption("Preferencias 'Todos los Aspirantes'")
            data_int = DATOS_INTERNA_TODOS.get(seleccion, {})
            df_int = pd.DataFrame(list(data_int.items()), columns=["Aspirante", "%"]).sort_values("%", ascending=True)
            colors_int = ['#880E4F' if 'Iván' in x else '#90A4AE' for x in df_int['Aspirante']]
            
            fig_int = px.bar(df_int, x="%", y="Aspirante", orientation='h', text_auto=True)
            fig_int.update_traces(marker_color=colors_int, textfont_size=14)
            st.plotly_chart(fig_int, use_container_width=True)

    # TAB 6: CAREOS
    with tabs[5]:
        st.subheader("Competitividad Constitucional (Escenarios)")
        data_careos = DATOS_CAREOS_CONST.get(seleccion, {}) if seleccion in DATOS_CAREOS_CONST else DATOS_CAREOS_CONST["GUERRERO (ESTATAL)"]
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Escenario A: Félix Salgado**")
            df_c1 = pd.DataFrame(list(data_careos["Careo 1 (Félix)"].items()), columns=["Partido", "%"])
            fig_c1 = px.pie(df_c1, names="Partido", values="%", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_c1, use_container_width=True)
            st.metric("Voto MORENA", f"{data_careos['Careo 1 (Félix)']['MORENA (Félix)']}%")
            
        with c2:
            st.markdown("**Escenario B: Iván Hernández**")
            df_c2 = pd.DataFrame(list(data_careos["Careo 2 (Iván)"].items()), columns=["Partido", "%"])
            fig_c2 = px.pie(df_c2, names="Partido", values="%", hole=0.4, color_discrete_sequence=px.colors.qualitative.Bold)
            st.plotly_chart(fig_c2, use_container_width=True)
            st.metric("Voto MORENA", f"{data_careos['Careo 2 (Iván)']['MORENA (Iván)']}%", delta="+11.6 pts vs Félix")

if __name__ == "__main__":
    main()