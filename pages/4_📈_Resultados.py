import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Resultados Finales 2025", layout="wide")

# ==============================================================================
# 🗄️ BASE DE DATOS MAESTRA
# ==============================================================================

# 1. PROBLEMAS
DATOS_PROBLEMAS = {
    "GUERRERO (ESTATAL)": {"Inseguridad": [47.0, 63.9], "Falta de agua": [4.0, 8.4], "Corrupción": [6.0, 6.2], "Calles mal estado": [1.0, 4.0], "Bajos Salarios": [1.0, 2.9]},
    "ACAPULCO": {"Inseguridad": [56.0, 62.2], "Falta de agua": [4.0, 11.0], "Corrupción": [3.0, 7.3]},
    "CHILPANCINGO": {"Inseguridad": [61.0, 76.2], "Falta de agua": [3.0, 4.0], "Corrupción": [2.0, 3.8]},
    "IGUALA": {"Inseguridad": [59.0, 49.6], "Economía": [4.0, 8.5], "Calles mal estado": [1.0, 6.0]}
}

# 2. PARTIDOS (COMPLETO)
DATOS_VOTO_GOB = {
    "GUERRERO (ESTATAL)": {"PAN": [2.0, 2.0], "PRI": [16.0, 4.0], "PT": [2.0, 1.0], "PVEM": [3.0, 1.0], "MC": [7.0, 2.0], "MORENA": [48.0, 60.0], "PRD": [3.0, 1.0], "Ninguno": [9.0, 16.0], "No sabe": [10.0, 13.0]},
    "ACAPULCO": {"PAN": [2.0, 1.0], "PRI": [10.0, 3.0], "PT": [3.0, 1.0], "PVEM": [4.0, 1.0], "MC": [10.0, 3.0], "MORENA": [48.0, 65.0], "PRD": [2.0, 0.0], "Ninguno": [9.0, 14.0], "No sabe": [10.0, 11.0]},
    "CHILPANCINGO": {"PAN": [1.0, 1.0], "PRI": [15.0, 6.0], "PT": [2.0, 2.0], "PVEM": [3.0, 2.0], "MC": [6.0, 2.0], "MORENA": [34.0, 46.0], "PRD": [4.0, 1.0], "Ninguno": [19.0, 23.0], "No sabe": [15.0, 16.0]},
    "IGUALA": {"PAN": [1.0, 4.0], "PRI": [16.0, 2.0], "PT": [2.0, 1.0], "PVEM": [5.0, 1.0], "MC": [8.0, 2.0], "MORENA": [41.0, 61.0], "PRD": [4.0, 2.0], "Ninguno": [10.0, 12.0], "No sabe": [13.0, 15.0]}
}

# 3. CONOCIMIENTO (COMPLETO)
DATOS_CONOCIMIENTO = {
    "GUERRERO (ESTATAL)": {"Félix Salgado": [73.0, 73.4], "Abelina López": [48.0, 68.1], "Beatriz Mojica": [44.0, 56.0], "Javier Saldaña": [0.0, 44.9], "Iván Hernández": [8.0, 38.9], "Jacinto González": [11.0, 24.6], "Pablo Amílcar": [21.0, 21.0], "Esthela Damián": [7.0, 20.9]},
    "ACAPULCO": {"Abelina López": [86.0, 85.0], "Félix Salgado": [86.0, 75.0], "Beatriz Mojica": [58.0, 62.0], "Iván Hernández": [12.0, 41.0], "Javier Saldaña": [0.0, 45.0], "Pablo Amílcar": [33.0, 23.0], "Jacinto González": [12.0, 24.0], "Esthela Damián": [9.0, 21.0]},
    "CHILPANCINGO": {"Félix Salgado": [83.0, 76.1], "Beatriz Mojica": [53.0, 53.3], "Javier Saldaña": [0.0, 51.9], "Abelina López": [54.0, 49.2], "Iván Hernández": [17.0, 35.7], "Jacinto González": [21.0, 31.8], "Pablo Amílcar": [28.0, 20.8], "Esthela Damián": [13.0, 15.3]},
    "IGUALA": {"Félix Salgado": [86.0, 61.0], "Beatriz Mojica": [46.0, 31.2], "Iván Hernández": [6.0, 36.8], "Esthela Damián": [10.0, 29.6], "Javier Saldaña": [0.0, 27.6], "Abelina López": [37.0, 15.4], "Pablo Amílcar": [21.0, 12.7], "Jacinto González": [9.0, 10.0]}
}

# 4. OPINIÓN
DATOS_OPINION_ESTATAL = {
    "Abelina López": {"Buena": [6, 12], "Regular": [16, 20], "Mala": [21, 63]},
    "Beatriz Mojica": {"Buena": [10, 18], "Regular": [23, 48], "Mala": [5, 19]},
    "Esthela Damián": {"Buena": [2, 35], "Regular": [3, 38], "Mala": [0, 11]},
    "Félix Salgado": {"Buena": [13, 13], "Regular": [34, 36], "Mala": [21, 46]},
    "Iván Hernández": {"Buena": [2, 51], "Regular": [4, 35], "Mala": [1, 6]},
    "Javier Saldaña": {"Buena": [0, 13], "Regular": [0, 46], "Mala": [0, 32]},
    "Jacinto González": {"Buena": [2, 31], "Regular": [6, 41], "Mala": [1, 11]},
    "Pablo Amílcar": {"Buena": [3, 11], "Regular": [10, 48], "Mala": [3, 20]}
}

DATOS_OPINION_MUNICIPAL = {
    "ACAPULCO": {"Abelina López": [9, 15.0], "Beatriz Mojica": [12, 20.4], "Esthela Damián": [3, 30.1], "Félix Salgado": [13, 13.3], "Iván Hernández": [4, 52.2], "Javier Saldaña": [0, 13.3], "Jacinto González": [2, 36.5], "Pablo Amílcar": [5, 12.2]},
    "CHILPANCINGO": {"Abelina López": [4, 2.1], "Beatriz Mojica": [8, 9.9], "Esthela Damián": [4, 17.0], "Félix Salgado": [10, 9.4], "Iván Hernández": [7, 40.3], "Javier Saldaña": [0, 11.4], "Jacinto González": [2, 21.4], "Pablo Amílcar": [4, 8.9]},
    "IGUALA": {"Abelina López": [4, 7.2], "Beatriz Mojica": [11, 24.0], "Esthela Damián": [1, 66.7], "Félix Salgado": [16, 16.3], "Iván Hernández": [1, 65.2], "Javier Saldaña": [0, 18.6], "Jacinto González": [2, 29.8], "Pablo Amílcar": [6, 12.9]}
}

# 5. ATRIBUTOS
DATOS_ATRIBUTOS_JUN = [
    {"Aspirante": "Félix Salgado", "Honestidad": 14.3, "Der. Mujeres": 15.2, "Cercanía": 23.3, "Conoce Edo": 41.1, "Cumple": 14.3, "Buen Candidato": 25.5, "Disposición Voto": 32.8},
    {"Aspirante": "Beatriz Mojica", "Honestidad": 11.5, "Der. Mujeres": 17.5, "Cercanía": 11.5, "Conoce Edo": 19.0, "Cumple": 10.6, "Buen Candidato": 26.0, "Disposición Voto": 33.6},
    {"Aspirante": "Pablo Amílcar", "Honestidad": 3.7, "Der. Mujeres": 4.8, "Cercanía": 3.5, "Conoce Edo": 6.6, "Cumple": 3.2, "Buen Candidato": 8.0, "Disposición Voto": 16.2},
    {"Aspirante": "Abelina López", "Honestidad": 6.2, "Der. Mujeres": 12.2, "Cercanía": 8.7, "Conoce Edo": 13.7, "Cumple": 6.1, "Buen Candidato": 9.7, "Disposición Voto": 15.9},
    {"Aspirante": "Esthela Damián", "Honestidad": 1.5, "Der. Mujeres": 2.3, "Cercanía": 1.4, "Conoce Edo": 1.8, "Cumple": 1.5, "Buen Candidato": 3.2, "Disposición Voto": 11.3},
    {"Aspirante": "Iván Hernández", "Honestidad": 1.7, "Der. Mujeres": 2.1, "Cercanía": 2.1, "Conoce Edo": 2.5, "Cumple": 1.4, "Buen Candidato": 3.8, "Disposición Voto": 11.7},
    {"Aspirante": "Jacinto González", "Honestidad": 1.9, "Der. Mujeres": 2.5, "Cercanía": 1.7, "Conoce Edo": 3.0, "Cumple": 1.6, "Buen Candidato": 3.5, "Disposición Voto": 10.8},
    {"Aspirante": "Javier Saldaña", "Honestidad": 0.0, "Der. Mujeres": 0.0, "Cercanía": 0.0, "Conoce Edo": 0.0, "Cumple": 0.0, "Buen Candidato": 0.0, "Disposición Voto": 0.0}
]

DATOS_ATRIBUTOS_DIC = [
    {"Aspirante": "Iván Hernández", "Honestidad": 33.6, "Der. Mujeres": 37.8, "Cercanía": 35.3, "Conoce Edo": 43.3, "Cumple": 31.9, "Buen Candidato": 65.5, "Disposición Voto": 35.5},
    {"Aspirante": "Esthela Damián", "Honestidad": 25.5, "Der. Mujeres": 29.5, "Cercanía": 20.1, "Conoce Edo": 21.2, "Cumple": 20.5, "Buen Candidato": 48.3, "Disposición Voto": 16.4},
    {"Aspirante": "Jacinto González", "Honestidad": 20.1, "Der. Mujeres": 24.0, "Cercanía": 21.7, "Conoce Edo": 27.9, "Cumple": 18.1, "Buen Candidato": 41.2, "Disposición Voto": 18.6},
    {"Aspirante": "Beatriz Mojica", "Honestidad": 10.1, "Der. Mujeres": 20.8, "Cercanía": 11.3, "Conoce Edo": 21.2, "Cumple": 7.9, "Buen Candidato": 38.5, "Disposición Voto": 26.8},
    {"Aspirante": "Javier Saldaña", "Honestidad": 7.0, "Der. Mujeres": 7.6, "Cercanía": 11.2, "Conoce Edo": 21.5, "Cumple": 6.1, "Buen Candidato": 25.1, "Disposición Voto": 17.8},
    {"Aspirante": "Félix Salgado", "Honestidad": 6.9, "Der. Mujeres": 6.8, "Cercanía": 15.6, "Conoce Edo": 34.3, "Cumple": 7.7, "Buen Candidato": 21.9, "Disposición Voto": 22.1},
    {"Aspirante": "Pablo Amílcar", "Honestidad": 6.2, "Der. Mujeres": 5.0, "Cercanía": 5.1, "Conoce Edo": 9.4, "Cumple": 1.9, "Buen Candidato": 18.8, "Disposición Voto": 8.8},
    {"Aspirante": "Abelina López", "Honestidad": 9.6, "Der. Mujeres": 14.8, "Cercanía": 14.9, "Conoce Edo": 17.1, "Cumple": 8.8, "Buen Candidato": 14.0, "Disposición Voto": 12.5}
]

DATOS_RADAR_EVO = {
    "Iván Hernández": {"Honestidad": [1.7, 33.6], "Der. Mujeres": [2.1, 37.8], "Cercanía": [2.1, 35.3], "Conoce Edo": [2.5, 43.3], "Cumple": [1.4, 31.9]},
    "Félix Salgado": {"Honestidad": [14.3, 6.9], "Der. Mujeres": [15.2, 6.8], "Cercanía": [23.3, 15.6], "Conoce Edo": [41.1, 34.3], "Cumple": [14.3, 7.7]}
}

# 6. CANDIDATO INTERNO
DATOS_INTERNA = {
    "GUERRERO (ESTATAL)": {
        "Abelina López": [6, 6], "Beatriz Mojica": [18, 10], "Esthela Damián": [5, 7], "Félix Salgado": [20, 9],
        "Iván Hernández": [4, 21], "Javier Saldaña": [0, 5], "Jacinto González": [3, 5], "Pablo Amílcar": [6, 2],
        "Ninguno": [20, 16], "No sabe": [15, 19]
    },
    "ACAPULCO": {
        "Abelina López": [7, 9], "Beatriz Mojica": [22, 12], "Esthela Damián": [5, 6], "Félix Salgado": [15, 10],
        "Iván Hernández": [5, 22], "Javier Saldaña": [0, 5], "Jacinto González": [5, 5], "Pablo Amílcar": [12, 2],
        "Ninguno": [18, 15], "No sabe": [8, 14]
    },
    "CHILPANCINGO": {
        "Abelina López": [4, 0], "Beatriz Mojica": [16, 6], "Esthela Damián": [8, 5], "Félix Salgado": [11, 9],
        "Iván Hernández": [12, 18], "Javier Saldaña": [0, 6], "Jacinto González": [4, 6], "Pablo Amílcar": [6, 2],
        "Ninguno": [22, 19], "No sabe": [12, 28]
    },
    "IGUALA": {
        "Abelina López": [4, 1], "Beatriz Mojica": [23, 6], "Esthela Damián": [3, 13], "Félix Salgado": [24, 9],
        "Iván Hernández": [2, 22], "Javier Saldaña": [0, 4], "Jacinto González": [3, 2], "Pablo Amílcar": [9, 1],
        "Ninguno": [20, 15], "No sabe": [8, 27]
    }
}

# 7. EVALUACIÓN AUTORIDADES
DATOS_AUTORIDADES = {
    "Presidenta": {
        "GUERRERO (ESTATAL)": {"Aprueba": [80, 76], "Desaprueba": [16, 21], "No sabe": [4, 3]},
        "ACAPULCO": {"Aprueba": [86, 78], "Desaprueba": [13, 19], "No sabe": [1, 2]},
        "CHILPANCINGO": {"Aprueba": [73, 72], "Desaprueba": [23, 23], "No sabe": [4, 5]},
        "IGUALA": {"Aprueba": [77, 71], "Desaprueba": [19, 21], "No sabe": [4, 8]}
    },
    "Gobernadora": {
        "GUERRERO (ESTATAL)": {"Aprueba": [50, 50], "Desaprueba": [37, 45], "No sabe": [13, 5]},
        "ACAPULCO": {"Aprueba": [52, 57], "Desaprueba": [43, 39], "No sabe": [5, 4]},
        "CHILPANCINGO": {"Aprueba": [34, 35], "Desaprueba": [58, 59], "No sabe": [8, 6]},
        "IGUALA": {"Aprueba": [50, 41], "Desaprueba": [37, 50], "No sabe": [13, 8]}
    },
    "Pres. Municipal Acapulco": {"ACAPULCO": {"Aprueba": [24, 22], "Desaprueba": [71, 75], "No sabe": [5, 3]}},
    "Pres. Municipal Chilpancingo": {"CHILPANCINGO": {"Aprueba": [37, 19], "Desaprueba": [52, 74], "No sabe": [11, 8]}},
    "Pres. Municipal Iguala": {"IGUALA": {"Aprueba": [39, 30], "Desaprueba": [51, 59], "No sabe": [10, 11]}}
}

# 8. SOCIODEMOGRÁFICOS
DATOS_SOCIODEM = {
    "Edad": {
        "18-24": [16, 15.3], "25-34": [23, 20.1], "35-44": [18, 18.8],
        "45-54": [16, 16.9], "55-64": [12, 15.1], "65+": [15, 13.7]
    },
    "Sexo": {"Hombres": [47, 46], "Mujeres": [53, 54]},
    "NSE": {
        "A/B": [7, 7.8], "C+": [8, 15.5], "C": [14, 19.7],
        "C-": [17, 21.4], "D+": [15, 14.3], "D/E": [39, 15.3]
    }
}

# ==============================================================================
# 🛠️ FUNCIONES AUXILIARES
# ==============================================================================
def generar_hallazgo_problemas(sel):
    data = DATOS_PROBLEMAS.get(sel, {})
    if not data: return ""
    cambios = {k: v[1]-v[0] for k,v in data.items()}
    max_prob = max(data.items(), key=lambda x: x[1][1])
    mayor_crec = max(cambios.items(), key=lambda x: x[1])
    return f"**Hallazgo:** {max_prob[0]} lidera con {max_prob[1][1]}%. Mayor crecimiento: {mayor_crec[0]} (+{mayor_crec[1]:.1f} pts)"

def generar_hallazgo_partidos(sel):
    data = DATOS_VOTO_GOB.get(sel, {})
    if not data: return ""
    morena_cambio = data["MORENA"][1] - data["MORENA"][0]
    return f"**Hallazgo:** MORENA consolida pasando de {data['MORENA'][0]}% a {data['MORENA'][1]}% ({morena_cambio:+.0f} pts). Los partidos tradicionales pierden fuerza."

def generar_insight_conocimiento(sel):
    data = DATOS_CONOCIMIENTO.get(sel, {})
    if "Iván Hernández" not in data: return ""
    ivan_crec = data["Iván Hernández"][1] - data["Iván Hernández"][0]
    return f"**Insight Iván Hernández:** Crece de {data['Iván Hernández'][0]}% a {data['Iván Hernández'][1]}% (+{ivan_crec:.1f} pts), multiplicando su reconocimiento."

def generar_excel_completo():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as w:
        pd.DataFrame(DATOS_INTERNA["GUERRERO (ESTATAL)"].items(), columns=["Candidato", "Jun-Dic"]).to_excel(w, sheet_name='Interna', index=False)
        pd.DataFrame(DATOS_ATRIBUTOS_DIC).to_excel(w, sheet_name='Atributos_Dic', index=False)
        pd.DataFrame(DATOS_ATRIBUTOS_JUN).to_excel(w, sheet_name='Atributos_Jun', index=False)
    return output.getvalue()

# ==============================================================================
# 🚀 APP STREAMLIT
# ==============================================================================
def main():
    st.title("📊 Resultados Finales: Guerrero 2025")
    st.markdown("### Tablero de Control Estratégico")

    with st.sidebar:
        st.header("📍 Filtro Territorial")
        sel = st.selectbox("Seleccionar Vista:", ["GUERRERO (ESTATAL)", "ACAPULCO", "CHILPANCINGO", "IGUALA"])
        st.divider()
        st.download_button("📥 Bajar Excel", data=generar_excel_completo(), file_name="Resultados_2025.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

    tabs = st.tabs(["🚨 Problemas", "🏁 Partidos", "🧠 Conocimiento", "💭 Opinión", "✨ Atributos", "🗳️ Candidato Interno", "👔 Evaluación Autoridades", "📊 Sociodemográficos"])

    # TAB 1: PROBLEMAS
    with tabs[0]:
        st.subheader(f"Principales Problemas - {sel}")
        st.info(generar_hallazgo_problemas(sel))
        data_p = DATOS_PROBLEMAS.get(sel, {})
        df_p = pd.DataFrame([{"Problema": k, "Junio": v[0], "Dic": v[1]} for k,v in data_p.items()])
        df_melt_p = df_p.melt(id_vars="Problema", var_name="Mes", value_name="%").sort_values("%", ascending=True)
        fig_p = px.bar(df_melt_p, x="%", y="Problema", color="Mes", barmode="group", orientation='h', text_auto=True, color_discrete_map={"Junio": "#B0BEC5", "Dic": "#D81B60"})
        st.plotly_chart(fig_p, use_container_width=True)

    # TAB 2: PARTIDOS
    with tabs[1]:
        st.subheader(f"Preferencias Partidistas - {sel}")
        st.info(generar_hallazgo_partidos(sel))
        data_v = DATOS_VOTO_GOB.get(sel, {})
        df_v = pd.DataFrame([{"Partido": k, "Junio": v[0], "Dic": v[1]} for k,v in data_v.items()])
        df_melt = df_v.melt(id_vars="Partido", var_name="Mes", value_name="%").sort_values("%", ascending=True)
        fig_v = px.bar(df_melt, x="%", y="Partido", color="Mes", barmode="group", orientation='h', text_auto=True, color_discrete_map={"Junio": "#B0BEC5", "Dic": "#880E4F"})
        st.plotly_chart(fig_v, use_container_width=True)

    # TAB 3: CONOCIMIENTO
    with tabs[2]:
        st.subheader(f"Evolución Conocimiento - {sel}")
        st.info(generar_insight_conocimiento(sel))
        data_c = DATOS_CONOCIMIENTO.get(sel, {})
        df_c = pd.DataFrame([{"Aspirante": k, "Junio": v[0], "Diciembre": v[1]} for k,v in data_c.items()])
        df_melt_c = df_c.melt(id_vars="Aspirante", var_name="Mes", value_name="%")
        order = df_c.sort_values("Diciembre", ascending=True)["Aspirante"].tolist()
        fig_c = px.bar(df_melt_c, x="%", y="Aspirante", color="Mes", barmode="group", orientation='h', text_auto=True, category_orders={"Aspirante": order}, color_discrete_map={"Junio": "#B0BEC5", "Diciembre": "#880E4F"})
        fig_c.update_layout(height=600)
        st.plotly_chart(fig_c, use_container_width=True)

    # TAB 4: OPINIÓN
    with tabs[3]:
        st.subheader(f"Opinión de Aspirantes")
        
        if sel == "GUERRERO (ESTATAL)":
            st.markdown("#### Opinión Detallada (Estatal)")
            st.caption("Buena / Regular / Mala entre quienes conocen al aspirante")
            
            for asp, vals in DATOS_OPINION_ESTATAL.items():
                with st.expander(f"📊 {asp}"):
                    df_op = pd.DataFrame([
                        {"Categoría": "Buena", "Junio": vals["Buena"][0], "Dic": vals["Buena"][1]},
                        {"Categoría": "Regular", "Junio": vals["Regular"][0], "Dic": vals["Regular"][1]},
                        {"Categoría": "Mala", "Junio": vals["Mala"][0], "Dic": vals["Mala"][1]}
                    ])
                    
                    neta_jun = vals["Buena"][0] - vals["Mala"][0]
                    neta_dic = vals["Buena"][1] - vals["Mala"][1]
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Opinión Neta Jun", f"{neta_jun:+.0f} pts")
                    col2.metric("Opinión Neta Dic", f"{neta_dic:+.0f} pts")
                    col3.metric("Cambio", f"{neta_dic-neta_jun:+.0f} pts")
                    
                    fig_op = go.Figure()
                    fig_op.add_trace(go.Bar(name='Junio', x=df_op["Categoría"], y=df_op["Junio"], marker_color='#B0BEC5'))
                    fig_op.add_trace(go.Bar(name='Dic', x=df_op["Categoría"], y=df_op["Dic"], marker_color='#880E4F'))
                    fig_op.update_layout(barmode='group', height=300)
                    st.plotly_chart(fig_op, use_container_width=True)
        else:
            st.markdown(f"#### Opinión Positiva - {sel}")
            st.caption("% de opinión 'Buena' entre quienes conocen al aspirante")
            data_op_mun = DATOS_OPINION_MUNICIPAL.get(sel, {})
            df_op_mun = pd.DataFrame([{"Aspirante": k, "Junio": v[0], "Dic": v[1]} for k,v in data_op_mun.items()])
            df_melt_op = df_op_mun.melt(id_vars="Aspirante", var_name="Mes", value_name="%").sort_values("%", ascending=True)
            fig_op_mun = px.bar(df_melt_op, x="%", y="Aspirante", color="Mes", barmode="group", orientation='h', text_auto=True, color_discrete_map={"Junio": "#B0BEC5", "Dic": "#880E4F"})
            fig_op_mun.update_layout(height=600)
            st.plotly_chart(fig_op_mun, use_container_width=True)
            
            if "Iván Hernández" in data_op_mun:
                ivan_op = data_op_mun["Iván Hernández"]
                st.success(f"**Insight Iván:** Opinión positiva crece de {ivan_op[0]}% a {ivan_op[1]}% (+{ivan_op[1]-ivan_op[0]:.1f} pts)")

    # TAB 5: ATRIBUTOS
    with tabs[4]:
        st.subheader("Diagnóstico Cualitativo (Estatal)")
        
        col_heat1, col_heat2 = st.columns(2)
        
        with col_heat1:
            st.markdown("##### 🚦 Atributos JUNIO 2024")
            df_heat_jun = pd.DataFrame(DATOS_ATRIBUTOS_JUN).set_index("Aspirante")
            df_heat_jun = df_heat_jun.sort_values("Buen Candidato", ascending=False)
            fig_heat_jun = px.imshow(df_heat_jun, text_auto=True, aspect="auto", color_continuous_scale="Blues", origin="lower")
            fig_heat_jun.update_layout(height=500)
            st.plotly_chart(fig_heat_jun, use_container_width=True)
        
        with col_heat2:
            st.markdown("##### 🚦 Atributos DICIEMBRE 2025")
            df_heat_dic = pd.DataFrame(DATOS_ATRIBUTOS_DIC).set_index("Aspirante")
            df_heat_dic = df_heat_dic.sort_values("Buen Candidato", ascending=False)
            fig_heat_dic = px.imshow(df_heat_dic, text_auto=True, aspect="auto", color_continuous_scale="Greens", origin="lower")
            fig_heat_dic.update_layout(height=500)
            st.plotly_chart(fig_heat_dic, use_container_width=True)
        
        st.divider()
        st.markdown("##### 🕸️ Evolución Estructural: El Contraste")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Crecimiento: Iván Hernández**")
            d_ivan = DATOS_RADAR_EVO["Iván Hernández"]
            categories = list(d_ivan.keys())
            fig_rad = go.Figure()
            fig_rad.add_trace(go.Scatterpolar(r=[v[0] for v in d_ivan.values()], theta=categories, fill='toself', name='Junio', line_color='#B0BEC5'))
            fig_rad.add_trace(go.Scatterpolar(r=[v[1] for v in d_ivan.values()], theta=categories, fill='toself', name='Diciembre', line_color='#880E4F'))
            fig_rad.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 50])), showlegend=True, height=400)
            st.plotly_chart(fig_rad, use_container_width=True)

        with col2:
            st.markdown("**Desgaste: Félix Salgado**")
            d_felix = DATOS_RADAR_EVO["Félix Salgado"]
            fig_rad2 = go.Figure()
            fig_rad2.add_trace(go.Scatterpolar(r=[v[0] for v in d_felix.values()], theta=categories, fill='toself', name='Junio', line_color='#B0BEC5'))
            fig_rad2.add_trace(go.Scatterpolar(r=[v[1] for v in d_felix.values()], theta=categories, fill='toself', name='Diciembre', line_color='#C0392B'))
            fig_rad2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 50])), showlegend=True, height=400)
            st.plotly_chart(fig_rad2, use_container_width=True)

    # TAB 6: CANDIDATO INTERNO
    with tabs[5]:
        st.subheader(f"Encuesta Interna MORENA - {sel}")
        data_int = DATOS_INTERNA.get(sel, {})
        
        df_int = pd.DataFrame([{"Aspirante": k, "Junio": v[0], "Dic": v[1]} for k,v in data_int.items()])
        df_int = df_int.sort_values("Dic", ascending=True)
        
        fig_slope = go.Figure()
        for i, row in df_int.iterrows():
            color = "#880E4F" if "Iván" in row["Aspirante"] else "#90A4AE"
            if "Félix" in row["Aspirante"]: color = "#C0392B"
            fig_slope.add_trace(go.Scatter(x=["Junio", "Dic"], y=[row["Junio"], row["Dic"]], mode="lines+markers+text", name=row["Aspirante"], line=dict(color=color, width=2), text=["", f"{row['Dic']}%"], textposition="middle right"))
        
        fig_slope.update_layout(height=600, showlegend=True, legend=dict(orientation="v", y=0.5))
        st.plotly_chart(fig_slope, use_container_width=True)
        
        if "Iván Hernández" in data_int:
            ivan_int = data_int["Iván Hernández"]
            st.success(f"**Insight Iván:** Preferencia interna crece de {ivan_int[0]}% a {ivan_int[1]}% (+{ivan_int[1]-ivan_int[0]} pts)")

    # TAB 7: EVALUACIÓN AUTORIDADES
    with tabs[6]:
        st.subheader("Evaluación de Autoridades")
        
        # Presidenta
        st.markdown("#### 🇲🇽 Presidenta de México")
        if sel in DATOS_AUTORIDADES["Presidenta"]:
            data_pres = DATOS_AUTORIDADES["Presidenta"][sel]
            df_pres = pd.DataFrame([
                {"Categoría": "Aprueba", "Junio": data_pres["Aprueba"][0], "Dic": data_pres["Aprueba"][1]},
                {"Categoría": "Desaprueba", "Junio": data_pres["Desaprueba"][0], "Dic": data_pres["Desaprueba"][1]},
                {"Categoría": "No sabe", "Junio": data_pres["No sabe"][0], "Dic": data_pres["No sabe"][1]}
            ])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Aprueba Jun", f"{data_pres['Aprueba'][0]}%")
            col2.metric("Aprueba Dic", f"{data_pres['Aprueba'][1]}%", delta=f"{data_pres['Aprueba'][1]-data_pres['Aprueba'][0]} pts")
            col3.metric("Desaprueba Dic", f"{data_pres['Desaprueba'][1]}%")
            
            fig_pres = go.Figure()
            fig_pres.add_trace(go.Bar(name='Junio', x=df_pres["Categoría"], y=df_pres["Junio"], marker_color='#B0BEC5'))
            fig_pres.add_trace(go.Bar(name='Dic', x=df_pres["Categoría"], y=df_pres["Dic"], marker_color='#880E4F'))
            fig_pres.update_layout(barmode='group', height=300)
            st.plotly_chart(fig_pres, use_container_width=True)
        
        st.divider()
        
        # Gobernadora
        st.markdown("#### 🏛️ Gobernadora de Guerrero")
        if sel in DATOS_AUTORIDADES["Gobernadora"]:
            data_gob = DATOS_AUTORIDADES["Gobernadora"][sel]
            df_gob = pd.DataFrame([
                {"Categoría": "Aprueba", "Junio": data_gob["Aprueba"][0], "Dic": data_gob["Aprueba"][1]},
                {"Categoría": "Desaprueba", "Junio": data_gob["Desaprueba"][0], "Dic": data_gob["Desaprueba"][1]},
                {"Categoría": "No sabe", "Junio": data_gob["No sabe"][0], "Dic": data_gob["No sabe"][1]}
            ])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Aprueba Jun", f"{data_gob['Aprueba'][0]}%")
            col2.metric("Aprueba Dic", f"{data_gob['Aprueba'][1]}%", delta=f"{data_gob['Aprueba'][1]-data_gob['Aprueba'][0]} pts")
            col3.metric("Desaprueba Dic", f"{data_gob['Desaprueba'][1]}%")
            
            fig_gob = go.Figure()
            fig_gob.add_trace(go.Bar(name='Junio', x=df_gob["Categoría"], y=df_gob["Junio"], marker_color='#B0BEC5'))
            fig_gob.add_trace(go.Bar(name='Dic', x=df_gob["Categoría"], y=df_gob["Dic"], marker_color='#880E4F'))
            fig_gob.update_layout(barmode='group', height=300)
            st.plotly_chart(fig_gob, use_container_width=True)
        
        st.divider()
        
        # Presidente Municipal
        if sel == "ACAPULCO":
            st.markdown("#### 🏙️ Presidente Municipal de Acapulco")
            data_pm = DATOS_AUTORIDADES["Pres. Municipal Acapulco"]["ACAPULCO"]
        elif sel == "CHILPANCINGO":
            st.markdown("#### 🏙️ Presidente Municipal de Chilpancingo")
            data_pm = DATOS_AUTORIDADES["Pres. Municipal Chilpancingo"]["CHILPANCINGO"]
        elif sel == "IGUALA":
            st.markdown("#### 🏙️ Presidente Municipal de Iguala")
            data_pm = DATOS_AUTORIDADES["Pres. Municipal Iguala"]["IGUALA"]
        else:
            data_pm = None
        
        if data_pm:
            df_pm = pd.DataFrame([
                {"Categoría": "Aprueba", "Junio": data_pm["Aprueba"][0], "Dic": data_pm["Aprueba"][1]},
                {"Categoría": "Desaprueba", "Junio": data_pm["Desaprueba"][0], "Dic": data_pm["Desaprueba"][1]},
                {"Categoría": "No sabe", "Junio": data_pm["No sabe"][0], "Dic": data_pm["No sabe"][1]}
            ])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Aprueba Jun", f"{data_pm['Aprueba'][0]}%")
            col2.metric("Aprueba Dic", f"{data_pm['Aprueba'][1]}%", delta=f"{data_pm['Aprueba'][1]-data_pm['Aprueba'][0]} pts")
            col3.metric("Desaprueba Dic", f"{data_pm['Desaprueba'][1]}%")
            
            fig_pm = go.Figure()
            fig_pm.add_trace(go.Bar(name='Junio', x=df_pm["Categoría"], y=df_pm["Junio"], marker_color='#B0BEC5'))
            fig_pm.add_trace(go.Bar(name='Dic', x=df_pm["Categoría"], y=df_pm["Dic"], marker_color='#C0392B'))
            fig_pm.update_layout(barmode='group', height=300)
            st.plotly_chart(fig_pm, use_container_width=True)

    # TAB 8: SOCIODEMOGRÁFICOS
    with tabs[7]:
        st.subheader("Perfil Sociodemográfico de la Muestra")
        st.caption("Comparativo Junio vs Diciembre")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("##### 👥 Edad")
            df_edad = pd.DataFrame([{"Rango": k, "Junio": v[0], "Dic": v[1]} for k,v in DATOS_SOCIODEM["Edad"].items()])
            fig_edad = go.Figure()
            fig_edad.add_trace(go.Bar(name='Junio', x=df_edad["Rango"], y=df_edad["Junio"], marker_color='#B0BEC5'))
            fig_edad.add_trace(go.Bar(name='Dic', x=df_edad["Rango"], y=df_edad["Dic"], marker_color='#880E4F'))
            fig_edad.update_layout(barmode='group', height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig_edad, use_container_width=True)
        
        with col2:
            st.markdown("##### ⚧️ Sexo")
            df_sexo = pd.DataFrame([{"Categoría": k, "Junio": v[0], "Dic": v[1]} for k,v in DATOS_SOCIODEM["Sexo"].items()])
            fig_sexo = go.Figure()
            fig_sexo.add_trace(go.Bar(name='Junio', x=df_sexo["Categoría"], y=df_sexo["Junio"], marker_color='#B0BEC5'))
            fig_sexo.add_trace(go.Bar(name='Dic', x=df_sexo["Categoría"], y=df_sexo["Dic"], marker_color='#880E4F'))
            fig_sexo.update_layout(barmode='group', height=400)
            st.plotly_chart(fig_sexo, use_container_width=True)
        
        with col3:
            st.markdown("##### 💰 Nivel Socioeconómico")
            df_nse = pd.DataFrame([{"NSE": k, "Junio": v[0], "Dic": v[1]} for k,v in DATOS_SOCIODEM["NSE"].items()])
            fig_nse = go.Figure()
            fig_nse.add_trace(go.Bar(name='Junio', x=df_nse["NSE"], y=df_nse["Junio"], marker_color='#B0BEC5'))
            fig_nse.add_trace(go.Bar(name='Dic', x=df_nse["NSE"], y=df_nse["Dic"], marker_color='#880E4F'))
            fig_nse.update_layout(barmode='group', height=400)
            st.plotly_chart(fig_nse, use_container_width=True)

if __name__ == "__main__":
    main()