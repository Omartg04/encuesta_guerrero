import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.auth import bloquear_acceso

st.set_page_config(page_title="Resultados Electorales", layout="wide")
bloquear_acceso()

# ==============================================================================
# 🗄️ BASE DE DATOS HISTÓRICA (DATA ENTRY)
# ==============================================================================

# 1. PRINCIPALES PROBLEMAS
DATOS_PROBLEMAS = {
    "GUERRERO (ESTATAL)": {
        "Inseguridad": 47, "Violencia": 2, "Narcotráfico": 1, "Economía": 5,
        "Falta de empleos": 4, "Pobreza": 2, "Bajos salarios": 1, "Corrupción": 6,
        "Falta de agua potable": 4, "Falta vías comunicación": 2, "Calles sin pavimento": 1,
        "Calles mal estado": 1, "Mal gobierno": 3, "Ninguno": 2, "NS/NR": 11
    },
    "ACAPULCO": {"Inseguridad": 56, "Violencia": 3, "Narcotráfico": 1, "Economía": 2, "Falta empleos": 1},
    "CHILPANCINGO": {"Inseguridad": 61, "Violencia": 3, "Narcotráfico": 1, "Economía": 3, "Falta empleos": 3},
    "IGUALA": {"Inseguridad": 59, "Violencia": 2, "Narcotráfico": 1, "Economía": 4, "Falta empleos": 5}
}

# 2. CONOCIMIENTO (NAME ID)
DATOS_CONOCIMIENTO_ESTATAL = {
    "Félix Salgado Macedonio": [73, 27], "Abelina López Rodríguez": [48, 52],
    "Beatriz Mojica Morga": [44, 56], "Pablo Amílcar Sandoval": [21, 79],
    "Jacinto Gonzalez Varona": [11, 89], "Iván Hernández Díaz": [8, 92],
    "Esthela Damián Peralta": [7, 93], "Javier Saldaña Almazán": [0, 0]
}
DATOS_CONOCIMIENTO_MUNI = {
    "ACAPULCO": {"Abelina López": 89, "Félix Salgado": 86, "Beatriz Mojica": 58, "Pablo Amílcar": 33, "Iván Hernández": 12, "Jacinto Gonzalez": 12, "Esthela Damián": 9},
    "CHILPANCINGO": {"Félix Salgado": 83, "Abelina López": 54, "Beatriz Mojica": 53, "Pablo Amílcar": 28, "Jacinto Gonzalez": 21, "Iván Hernández": 17, "Esthela Damián": 13},
    "IGUALA": {"Félix Salgado": 86, "Beatriz Mojica": 46, "Abelina López": 37, "Pablo Amílcar": 21, "Esthela Damián": 13, "Jacinto Gonzalez": 9, "Iván Hernández": 6}
}

# 3. OPINIÓN (IMAGEN)
DATOS_OPINION_ESTATAL = {
    "Félix Salgado": [13, 34, 21, 5, 27], "Beatriz Mojica": [10, 23, 5, 6, 56],
    "Abelina López": [6, 16, 21, 5, 52], "Pablo Amílcar": [3, 10, 3, 5, 79],
    "Esthela Damián": [2, 3, 2, 0, 93], "Iván Hernández": [2, 4, 1, 1, 92],
    "Jacinto Gonzalez": [2, 6, 1, 2, 89]
} # Orden: Buena, Regular, Mala, NS, No Conoce

DATOS_OPINION_MUNI = {
    "ACAPULCO": {"Félix Salgado": 13, "Beatriz Mojica": 12, "Abelina López": 9, "Pablo Amílcar": 5, "Iván Hernández": 4},
    "CHILPANCINGO": {"Félix Salgado": 10, "Beatriz Mojica": 8, "Iván Hernández": 7, "Abelina López": 4, "Pablo Amílcar": 4},
    "IGUALA": {"Félix Salgado": 16, "Beatriz Mojica": 11, "Pablo Amílcar": 6, "Abelina López": 4}
}

# 4. PREFERENCIA INTERNA MORENA
DATOS_INTERNA = {
    "GUERRERO (ESTATAL)": {
        "Félix Salgado": {"Bruta": 20, "Efectiva": 31}, "Beatriz Mojica": {"Bruta": 18, "Efectiva": 28},
        "Pablo Amílcar": {"Bruta": 6, "Efectiva": 9}, "Abelina López": {"Bruta": 6, "Efectiva": 9},
        "Esthela Damián": {"Bruta": 5, "Efectiva": 7}, "Iván Hernández": {"Bruta": 4, "Efectiva": 7},
        "Jacinto Gonzalez": {"Bruta": 3, "Efectiva": 4}, "Ninguno": {"Bruta": 20, "Efectiva": 0},
        "NS/NR": {"Bruta": 15, "Efectiva": 0}
    },
    "ACAPULCO": {"Beatriz Mojica": 22, "Félix Salgado": 15, "Pablo Amílcar": 12, "Abelina López": 7, "Esthela Damián": 5},
    "CHILPANCINGO": {"Beatriz Mojica": 16, "Iván Hernández": 12, "Félix Salgado": 11, "Esthela Damián": 8, "Abelina López": 7},
    "IGUALA": {"Félix Salgado": 24, "Beatriz Mojica": 23, "Pablo Amílcar": 9, "Abelina López": 4, "Jacinto Gonzalez": 3}
}

# 5. INTENCIÓN DE VOTO (GOBERNADOR)
DATOS_VOTO_GOB = {
    "GUERRERO (ESTATAL)": {
        "MORENA": {"Bruta": 48, "Efectiva": 60}, "PRI": {"Bruta": 16, "Efectiva": 19},
        "MC": {"Bruta": 7, "Efectiva": 9}, "PVEM": {"Bruta": 3, "Efectiva": 4},
        "PRD": {"Bruta": 3, "Efectiva": 3}, "PT": {"Bruta": 2, "Efectiva": 3},
        "PAN": {"Bruta": 3, "Efectiva": 4}, "Ninguno/NR": {"Bruta": 10, "Efectiva": 0}
    },
    "ACAPULCO": {"MORENA": 48, "PRI": 10, "MC": 10, "PVEM": 4, "PRD": 2, "PT": 3, "PAN": 2},
    "CHILPANCINGO": {"MORENA": 34, "PRI": 15, "MC": 6, "PVEM": 3, "PRD": 4, "PT": 2, "PAN": 2},
    "IGUALA": {"MORENA": 41, "PRI": 16, "MC": 8, "PVEM": 5, "PRD": 4, "PT": 2, "PAN": 1}
}

# 6. SCORECARD (DEFINICIÓN FINAL)
DATOS_SCORECARD = [
    {"Aspirante": "Félix Salgado", "Opinion_Pos": 13.4, "Honestidad": 14.3, "Mujeres": 15.2, "Cercania": 23.3, "Conoce_Edo": 41.1, "Cumple": 14.3, "Buen_Cand": 25.5, "Votaria": 32.8, "Pref_Mor": 19.8, "SCORE": 6.5},
    {"Aspirante": "Beatriz Mojica", "Opinion_Pos": 10.1, "Honestidad": 11.5, "Mujeres": 17.5, "Cercania": 11.5, "Conoce_Edo": 19.0, "Cumple": 10.6, "Buen_Cand": 26.0, "Votaria": 33.6, "Pref_Mor": 18.4, "SCORE": 3.5},
    {"Aspirante": "Pablo Amílcar", "Opinion_Pos": 2.9, "Honestidad": 3.7, "Mujeres": 4.8, "Cercania": 3.5, "Conoce_Edo": 6.6, "Cumple": 3.2, "Buen_Cand": 8.0, "Votaria": 16.2, "Pref_Mor": 6.0, "SCORE": 0.0},
    {"Aspirante": "Abelina López", "Opinion_Pos": 6.3, "Honestidad": 6.2, "Mujeres": 12.2, "Cercania": 8.7, "Conoce_Edo": 13.7, "Cumple": 6.1, "Buen_Cand": 9.7, "Votaria": 15.9, "Pref_Mor": 5.7, "SCORE": 0.0},
    {"Aspirante": "Esthela Damián", "Opinion_Pos": 2.3, "Honestidad": 1.5, "Mujeres": 2.3, "Cercania": 1.4, "Conoce_Edo": 1.8, "Cumple": 1.5, "Buen_Cand": 3.2, "Votaria": 11.3, "Pref_Mor": 4.7, "SCORE": 0.0},
    {"Aspirante": "Iván Hernández", "Opinion_Pos": 1.7, "Honestidad": 1.7, "Mujeres": 2.1, "Cercania": 2.1, "Conoce_Edo": 2.5, "Cumple": 1.4, "Buen_Cand": 3.8, "Votaria": 11.7, "Pref_Mor": 4.3, "SCORE": 0.0},
    {"Aspirante": "Jacinto Gonzalez", "Opinion_Pos": 1.9, "Honestidad": 1.9, "Mujeres": 2.5, "Cercania": 1.7, "Conoce_Edo": 3.0, "Cumple": 1.6, "Buen_Cand": 3.5, "Votaria": 10.8, "Pref_Mor": 3.1, "SCORE": 0.0}
]

# 7. EVALUACIÓN DE AUTORIDADES
# Detalle Estatal
DATOS_AUTORIDAD_ESTATAL = {
    "Claudia Sheinbaum": {"Aprueba Mucho": 27, "Aprueba": 53, "Desaprueba Poco": 13, "Desaprueba Mucho": 3, "NS/NC": 4},
    "Evelyn Salgado":    {"Aprueba Mucho": 8, "Aprueba": 42, "Desaprueba Poco": 29, "Desaprueba Mucho": 9, "NS/NC": 13}
}
# Resumen Municipal (Aprueba Total vs Desaprueba Total)
DATOS_AUTORIDAD_MUNI = {
    "ACAPULCO": [
        {"Autoridad": "Presidenta (Claudia S.)", "Aprueba": 86, "Desaprueba": 13, "NS": 1},
        {"Autoridad": "Gobernadora (Evelyn S.)", "Aprueba": 52, "Desaprueba": 43, "NS": 5},
        {"Autoridad": "Alcaldesa (Abelina López)", "Aprueba": 24, "Desaprueba": 71, "NS": 5}
    ],
    "CHILPANCINGO": [
        {"Autoridad": "Presidenta (Claudia S.)", "Aprueba": 73, "Desaprueba": 23, "NS": 4},
        {"Autoridad": "Gobernadora (Evelyn S.)", "Aprueba": 34, "Desaprueba": 58, "NS": 8},
        {"Autoridad": "Alcalde (Gustavo Alarcón)", "Aprueba": 37, "Desaprueba": 52, "NS": 11}
    ],
    "IGUALA": [
        {"Autoridad": "Presidenta (Claudia S.)", "Aprueba": 77, "Desaprueba": 19, "NS": 4},
        {"Autoridad": "Gobernadora (Evelyn S.)", "Aprueba": 50, "Desaprueba": 42, "NS": 8},
        {"Autoridad": "Alcalde (Erik Catalán)", "Aprueba": 39, "Desaprueba": 21, "NS": 10}
    ]
}

# 8. DEMOGRÁFICOS
DATOS_DEMO = {
    "Sexo": {"Mujeres": 53, "Hombres": 47},
    "Edad": {"18-24": 16, "25-34": 23, "35-44": 18, "45-54": 16, "55-64": 12, "65+": 15}
}

# ==============================================================================
# 🚀 APLICACIÓN STREAMLIT
# ==============================================================================

def main():
    st.title("📊 Resultados del Ejercicio Anterior")
    st.markdown("Visualización integral de los datos históricos para comparación.")

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("📍 Filtro Territorial")
        opciones_geo = ["GUERRERO (ESTATAL)", "ACAPULCO", "CHILPANCINGO", "IGUALA"]
        seleccion = st.selectbox("Seleccionar Vista:", opciones_geo)
        st.info(f"Visualizando: **{seleccion}**")

    # --- TABS (ORDEN LÓGICO DE REPORTE) ---
    tabs = st.tabs([
        "🚨 Problemas", 
        "🧠 Conocimiento/Opinión", 
        "🗳️ Preferencia Interna",
        "⚖️ Voto Gobernador",
        "🏆 Estimación Final",
        "📊 Autoridades",
        "👥 Demográficos"
    ])

    # 1. PROBLEMAS
    with tabs[0]:
        st.subheader(f"Principales Problemas - {seleccion}")
        data = DATOS_PROBLEMAS.get(seleccion, {})
        df = pd.DataFrame(list(data.items()), columns=["Problema", "%"]).sort_values("%", ascending=True)
        colors = ['#B71C1C' if 'Inseguridad' in x else '#1f77b4' for x in df['Problema']]
        fig = px.bar(df, x="%", y="Problema", orientation='h', text_auto=True, height=600 if len(df)>10 else 400)
        fig.update_traces(marker_color=colors)
        st.plotly_chart(fig, use_container_width=True)

    # 2. CONOCIMIENTO / OPINIÓN
    with tabs[1]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Conocimiento")
            if seleccion == "GUERRERO (ESTATAL)":
                df = pd.DataFrame.from_dict(DATOS_CONOCIMIENTO_ESTATAL, orient='index', columns=['SÍ', 'NO']).reset_index().rename(columns={'index':'Aspirante'}).sort_values("SÍ", ascending=True)
                fig = px.bar(df, y="Aspirante", x=["SÍ", "NO"], orientation='h', text_auto=True, color_discrete_map={"SÍ": "#2E86C1", "NO": "#EAEDED"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                data = DATOS_CONOCIMIENTO_MUNI.get(seleccion, {})
                df = pd.DataFrame(list(data.items()), columns=["Aspirante", "SÍ"]).sort_values("SÍ", ascending=True)
                st.plotly_chart(px.bar(df, x="SÍ", y="Aspirante", orientation='h', text_auto=True), use_container_width=True)
        
        with c2:
            st.markdown("##### Opinión (Positiva)")
            if seleccion == "GUERRERO (ESTATAL)":
                df = pd.DataFrame.from_dict(DATOS_OPINION_ESTATAL, orient='index', columns=['Buena', 'Reg', 'Mala', 'NS', 'NoC']).reset_index().rename(columns={'index':'Aspirante'}).sort_values("Buena", ascending=True)
                fig = px.bar(df, y="Aspirante", x=['Buena', 'Reg', 'Mala'], orientation='h', text_auto=True, color_discrete_map={"Buena": "#2ECC71", "Reg": "#F1C40F", "Mala": "#E74C3C"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                data = DATOS_OPINION_MUNI.get(seleccion, {})
                df = pd.DataFrame(list(data.items()), columns=["Aspirante", "Buena"]).sort_values("Buena", ascending=True)
                st.plotly_chart(px.bar(df, x="Buena", y="Aspirante", orientation='h', text_auto=True, color_discrete_sequence=['#2ECC71']), use_container_width=True)

    # 3. INTERNA MORENA
    with tabs[2]:
        st.subheader(f"Preferencia Interna - {seleccion}")
        data = DATOS_INTERNA.get(seleccion, {})
        if seleccion == "GUERRERO (ESTATAL)":
            df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Aspirante'}).sort_values("Bruta", ascending=True)
            df_melt = df.melt(id_vars="Aspirante", value_vars=["Bruta", "Efectiva"], var_name="Tipo", value_name="%")
            fig = px.bar(df_melt, y="Aspirante", x="%", color="Tipo", barmode="group", orientation='h', text_auto=True, color_discrete_map={"Bruta": "#BDBDBD", "Efectiva": "#880E4F"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            df = pd.DataFrame(list(data.items()), columns=["Aspirante", "Bruta"]).sort_values("Bruta", ascending=True)
            st.plotly_chart(px.bar(df, x="Bruta", y="Aspirante", orientation='h', text_auto=True, color_discrete_sequence=['#880E4F']), use_container_width=True)

    # 4. VOTO GOBERNADOR
    with tabs[3]:
        st.subheader(f"Voto Partido - {seleccion}")
        data = DATOS_VOTO_GOB.get(seleccion, {})
        if seleccion == "GUERRERO (ESTATAL)":
            df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index':'Partido'}).sort_values("Bruta", ascending=True)
            df_melt = df.melt(id_vars="Partido", value_vars=["Bruta", "Efectiva"], var_name="Tipo", value_name="%")
            fig = px.bar(df_melt, y="Partido", x="%", color="Tipo", barmode="group", orientation='h', text_auto=True, color_discrete_map={"Bruta": "#9E9E9E", "Efectiva": "#D32F2F"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            df = pd.DataFrame(list(data.items()), columns=["Partido", "Bruta"]).sort_values("Bruta", ascending=True)
            st.plotly_chart(px.bar(df, x="Bruta", y="Partido", orientation='h', text_auto=True, color_discrete_sequence=['#D32F2F']), use_container_width=True)

    # 5. SCORECARD FINAL
    with tabs[4]:
        st.subheader("🏆 Ranking Final Ponderado (Score 0-10)")
        df_score = pd.DataFrame(DATOS_SCORECARD).sort_values("SCORE", ascending=True)
        
        c_graf, c_kpi = st.columns([2, 1])
        with c_graf:
            fig = px.bar(df_score, x="SCORE", y="Aspirante", orientation='h', text_auto=True, color="SCORE", color_continuous_scale="Reds", range_x=[0,10])
            st.plotly_chart(fig, use_container_width=True)
        with c_kpi:
            top = df_score.iloc[-1]
            st.success(f"**PUNTERO:** {top['Aspirante']}")
            st.metric("Puntaje", f"{top['SCORE']} pts")
        
        st.markdown("#### Desglose de Dimensiones (%)")
        st.dataframe(
            df_score.sort_values("SCORE", ascending=False).style.background_gradient(subset=["SCORE"], cmap="Reds"),
            use_container_width=True,
            column_config={"SCORE": st.column_config.ProgressColumn("Puntaje Final", min_value=0, max_value=10)}
        )

    # 6. AUTORIDADES
    with tabs[5]:
        st.subheader(f"Aprobación de Autoridades - {seleccion}")
        if seleccion == "GUERRERO (ESTATAL)":
            df = pd.DataFrame.from_dict(DATOS_AUTORIDAD_ESTATAL, orient='index').reset_index().rename(columns={'index':'Autoridad'})
            # Stacked Bar 100% logic visual
            df_melt = df.melt(id_vars="Autoridad", var_name="Evaluación", value_name="%")
            fig = px.bar(
                df_melt, x="%", y="Autoridad", color="Evaluación", orientation='h', text_auto=True,
                color_discrete_map={"Aprueba Mucho": "#145A32", "Aprueba": "#2ECC71", "Desaprueba Poco": "#F1C40F", "Desaprueba Mucho": "#E74C3C", "NS/NC": "#BDC3C7"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            data = DATOS_AUTORIDAD_MUNI.get(seleccion, [])
            df = pd.DataFrame(data)
            # Grouped Bar comparando Aprueba vs Desaprueba
            df_melt = df.melt(id_vars="Autoridad", value_vars=["Aprueba", "Desaprueba", "NS"], var_name="Evaluación", value_name="%")
            fig = px.bar(
                df_melt, x="%", y="Autoridad", color="Evaluación", barmode="group", orientation='h', text_auto=True,
                color_discrete_map={"Aprueba": "#2ECC71", "Desaprueba": "#E74C3C", "NS": "#BDC3C7"}
            )
            st.plotly_chart(fig, use_container_width=True)

    # 7. DEMOGRÁFICOS
    with tabs[6]:
        st.subheader("Perfil de la Muestra")
        c1, c2 = st.columns(2)
        with c1:
            df_sex = pd.DataFrame(list(DATOS_DEMO["Sexo"].items()), columns=["Sexo", "%"])
            st.plotly_chart(px.pie(df_sex, names="Sexo", values="%", title="Sexo", color="Sexo", color_discrete_map={"Mujeres": "#E91E63", "Hombres": "#3498DB"}), use_container_width=True)
        with c2:
            df_edad = pd.DataFrame(list(DATOS_DEMO["Edad"].items()), columns=["Rango", "%"])
            st.plotly_chart(px.bar(df_edad, x="Rango", y="%", title="Edad", text_auto=True), use_container_width=True)

if __name__ == "__main__":
    main()