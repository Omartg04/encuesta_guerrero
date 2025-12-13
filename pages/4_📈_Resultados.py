import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from io import BytesIO
from datetime import datetime
from src.auth import bloquear_acceso

st.set_page_config(page_title="Resultados Finales Dic 2025", layout="wide")
bloquear_acceso()

# ==============================================================================
# 🗄️ BASE DE DATOS MAESTRA (DICIEMBRE 2025)
# ==============================================================================

# 1. PREFERENCIA INTERNA (ESCENARIO TODOS LOS ASPIRANTES) - "LA ENCUESTA"
DATOS_INTERNA_TODOS = {
    "GUERRERO (ESTATAL)": {
        "Iván Hernández": 21.5, "Beatriz Mojica": 10.0, "Félix Salgado": 9.3, 
        "Esthela Damián": 6.9, "Abelina López": 5.8, "Javier Saldaña": 5.2, 
        "Jacinto González": 4.9, "Pablo Amílcar": 1.8, "Ninguno": 16.0
    },
    "ACAPULCO": {
        "Iván Hernández": 22.5, "Beatriz Mojica": 12.0, "Félix Salgado": 9.5,
        "Abelina López": 8.7, "Esthela Damián": 6.5, "Ninguno": 14.9
    },
    "CHILPANCINGO": {
        "Iván Hernández": 18.3, "Félix Salgado": 8.7, "Beatriz Mojica": 6.5,
        "Esthela Damián": 4.7, "Abelina López": 0.3, "Ninguno": 19.2
    },
    "IGUALA": {
        "Iván Hernández": 22.5, "Esthela Damián": 12.8, "Félix Salgado": 9.0,
        "Beatriz Mojica": 6.4, "Ninguno": 15.2
    }
}

# 2. CAREOS CONSTITUCIONALES (ELECCIÓN GENERAL)
# Comparativa: ¿Quién garantiza el triunfo?
DATOS_CAREOS_CONST = {
    "GUERRERO (ESTATAL)": {
        "Careo 1 (Félix)": {"MORENA (Félix)": 22.9, "PRI (Añorve)": 2.5, "MC (Julián)": 2.9, "PT": 4.2, "PVEM": 2.9, "Ninguno": 33.9},
        "Careo 2 (Iván)":  {"MORENA (Iván)": 34.5, "PRI (Añorve)": 2.6, "MC (Julián)": 1.8, "PT": 3.7, "PVEM": 2.2, "Ninguno": 25.8}
    },
    "ACAPULCO": {
        "Careo 1 (Félix)": {"MORENA (Félix)": 25.8, "Ninguno": 35.7, "PRI": 2.2},
        "Careo 2 (Iván)":  {"MORENA (Iván)": 37.9, "Ninguno": 27.1, "PRI": 2.5}
    },
    "CHILPANCINGO": {
        "Careo 1 (Félix)": {"MORENA (Félix)": 17.8, "Ninguno": 34.0},
        "Careo 2 (Iván)":  {"MORENA (Iván)": 26.0, "Ninguno": 25.6}
    },
    "IGUALA": {
        "Careo 1 (Félix)": {"MORENA (Félix)": 17.6, "Ninguno": 24.7},
        "Careo 2 (Iván)":  {"MORENA (Iván)": 33.1, "Ninguno": 19.4}
    }
}

# 3. ATRIBUTOS CUALITATIVOS (RESUMEN ESTATAL)
# Iván destaca en Honestidad y Bajo Rechazo.
DATOS_ATRIBUTOS_RESUMEN = [
    {"Aspirante": "Iván Hernández", "Honestidad": 33.6, "Cercania": 35.3, "Der_Mujer": 37.8, "Conoce_Edo": 43.3, "Cumple": 31.9, "Buen_Cand": 65.5, "Votaria": 35.5, "Rechazo": 27.4},
    {"Aspirante": "Esthela Damián", "Honestidad": 25.5, "Cercania": 20.1, "Der_Mujer": 29.5, "Conoce_Edo": 21.2, "Cumple": 20.5, "Buen_Cand": 48.3, "Votaria": 16.4, "Rechazo": 43.8},
    {"Aspirante": "Jacinto González", "Honestidad": 20.1, "Cercania": 21.7, "Der_Mujer": 24.0, "Conoce_Edo": 27.9, "Cumple": 18.1, "Buen_Cand": 41.2, "Votaria": 18.6, "Rechazo": 41.2},
    {"Aspirante": "Beatriz Mojica", "Honestidad": 10.1, "Cercania": 11.3, "Der_Mujer": 20.8, "Conoce_Edo": 21.2, "Cumple": 7.9, "Buen_Cand": 38.5, "Votaria": 26.8, "Rechazo": 41.4},
    {"Aspirante": "Javier Saldaña", "Honestidad": 7.0, "Cercania": 11.2, "Der_Mujer": 7.6, "Conoce_Edo": 21.5, "Cumple": 6.1, "Buen_Cand": 25.1, "Votaria": 17.8, "Rechazo": 51.1},
    {"Aspirante": "Félix Salgado", "Honestidad": 6.9, "Cercania": 15.6, "Der_Mujer": 6.8, "Conoce_Edo": 34.3, "Cumple": 7.7, "Buen_Cand": 21.9, "Votaria": 22.1, "Rechazo": 56.2},
    {"Aspirante": "Pablo Amílcar", "Honestidad": 6.2, "Cercania": 5.1, "Der_Mujer": 5.0, "Conoce_Edo": 9.4, "Cumple": 1.9, "Buen_Cand": 18.8, "Votaria": 8.8, "Rechazo": 50.3},
    {"Aspirante": "Abelina López", "Honestidad": 9.6, "Cercania": 14.9, "Der_Mujer": 14.8, "Conoce_Edo": 17.1, "Cumple": 8.8, "Buen_Cand": 14.0, "Votaria": 12.5, "Rechazo": 66.5}
]

# 4. EVOLUCIÓN CONOCIMIENTO (JUN VS DIC)
DATOS_CONOCIMIENTO = {
    "GUERRERO (ESTATAL)": {"Félix Salgado": [73.0, 73.4], "Abelina López": [48.0, 68.1], "Beatriz Mojica": [44.0, 56.0], "Javier Saldaña": [0.0, 44.9], "Iván Hernández": [8.0, 38.9], "Jacinto Gonzalez": [11.0, 24.6], "Pablo Amílcar": [21.0, 21.0], "Esthela Damián": [7.0, 20.9]},
    "ACAPULCO": {"Abelina López": [89.0, 84.8], "Félix Salgado": [86.0, 74.6], "Iván Hernández": [12.0, 40.5]},
    "CHILPANCINGO": {"Félix Salgado": [83.0, 76.1], "Abelina López": [54.0, 49.2], "Iván Hernández": [17.0, 35.7]},
    "IGUALA": {"Félix Salgado": [86.0, 61.0], "Iván Hernández": [6.0, 36.8], "Abelina López": [37.0, 15.4]}
}

# 5. CONTEXTO: PROBLEMAS
DATOS_PROBLEMAS = {
    "GUERRERO (ESTATAL)": {"Inseguridad": [47.0, 63.9], "Falta de agua": [4.0, 8.4], "Corrupción": [6.0, 6.2], "Calles mal estado": [1.0, 4.0], "Bajos Salarios": [1.0, 2.9]},
    "ACAPULCO": {"Inseguridad": [56.0, 62.2], "Falta de agua": [4.0, 11.0], "Corrupción": [3.0, 7.3]},
    "CHILPANCINGO": {"Inseguridad": [61.0, 76.2], "Falta de agua": [3.0, 4.0], "Corrupción": [2.0, 3.8]},
    "IGUALA": {"Inseguridad": [59.0, 49.6], "Economía": [4.0, 8.5], "Calles mal estado": [1.0, 6.0]}
}

# ==============================================================================
# 🛠️ FUNCIONES DE EXPORTACIÓN
# ==============================================================================
def generar_excel_completo():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pd.DataFrame(DATOS_INTERNA_TODOS["GUERRERO (ESTATAL)"].items(), columns=["Candidato", "%"]).to_excel(writer, sheet_name='Encuesta_Interna', index=False)
        pd.DataFrame(DATOS_ATRIBUTOS_RESUMEN).to_excel(writer, sheet_name='Atributos', index=False)
        # Careos
        careo_rows = []
        for careo, data in DATOS_CAREOS_CONST["GUERRERO (ESTATAL)"].items():
            for k, v in data.items(): careo_rows.append({"Escenario": careo, "Partido": k, "%": v})
        pd.DataFrame(careo_rows).to_excel(writer, sheet_name='Careos_Constitucionales', index=False)
    return output.getvalue()

def generar_html_reporte(municipio):
    now = datetime.now().strftime("%d/%m/%Y")
    data_int = DATOS_INTERNA_TODOS.get(municipio, {})
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            h1, h2 {{ color: #880E4F; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .highlight {{ background-color: #f8d7da; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Reporte de Resultados: {municipio}</h1>
        <p>Fecha: {now} | <strong>Cierre de Evaluación 2025</strong></p>
        <hr>
        <h2>1. Encuesta Interna (Todos los Aspirantes)</h2>
        <table>
            <tr><th>Aspirante</th><th>% Preferencia</th></tr>
            {''.join([f"<tr style='{'background-color:#E8F8F5; font-weight:bold;' if 'Iván' in k else ''}'><td>{k}</td><td>{v}%</td></tr>" for k,v in data_int.items()])}
        </table>
        <h2>2. Conclusiones</h2>
        <p>Iván Hernández muestra la mayor competitividad tanto en la encuesta interna como en los careos constitucionales frente a la oposición.</p>
        <script>window.print()</script>
    </body>
    </html>
    """
    return html

# ==============================================================================
# 🚀 APP STREAMLIT (DASHBOARD)
# ==============================================================================
def main():
    st.title("🗳️ Resultados: Definición de Candidatura 2025")
    st.markdown("### Análisis de Posicionamiento, Competitividad y Escenarios")

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("📍 Filtro Territorial")
        seleccion = st.selectbox("Seleccionar Vista:", ["GUERRERO (ESTATAL)", "ACAPULCO", "CHILPANCINGO", "IGUALA"])
        
        st.divider()
        st.info("💡 **Nota Metodológica:** Datos correspondientes al levantamiento de Diciembre 2025.")
        
        st.subheader("📥 Descargas")
        st.download_button("📊 Reporte Excel Completo", data=generar_excel_completo(), file_name="Resultados_Finales_2025.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        
        html_rep = generar_html_reporte(seleccion)
        b64 = base64.b64encode(html_rep.encode()).decode()
        st.markdown(f'<a href="data:text/html;base64,{b64}" download="Reporte_{seleccion}.html" style="text-decoration:none;"><button style="width:100%; margin-top:5px; padding:10px; background:#FFFFFF; border:1px solid #ccc; border-radius:5px; cursor:pointer;">📄 Reporte PDF</button></a>', unsafe_allow_html=True)

    # --- KPI HEADER ---
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    if seleccion == "GUERRERO (ESTATAL)":
        col_kpi1.metric("Líder Encuesta Interna", "Iván Hernández", "21.5%")
        col_kpi2.metric("Ventaja vs 2do Lugar", "+11.5 pts", delta_color="normal")
        col_kpi3.metric("Potencial Voto (Techo)", "35.5%", "Mayor crecimiento")
    else:
        lider = max(DATOS_INTERNA_TODOS.get(seleccion, {}), key=DATOS_INTERNA_TODOS.get(seleccion, {}).get)
        val = DATOS_INTERNA_TODOS.get(seleccion, {})[lider]
        col_kpi1.metric(f"Líder en {seleccion}", lider, f"{val}%")

    # --- TABS ---
    tabs = st.tabs(["🏆 Definición Candidato", "🧠 Atributos & Diagnóstico", "📊 Evolución Conocimiento", "🚨 Contexto"])

    # TAB 1: DEFINICIÓN (LA ENCUESTA Y LOS CAREOS)
    with tabs[0]:
        st.markdown(f"#### 1. Preferencia Interna: Todos los Aspirantes ({seleccion})")
        st.caption("Pregunta: De la siguiente lista, ¿quién prefiere que sea el candidato de MORENA?")
        
        # Gráfica Interna
        data_int = DATOS_INTERNA_TODOS.get(seleccion, {})
        df_int = pd.DataFrame(list(data_int.items()), columns=["Aspirante", "%"]).sort_values("%", ascending=True)
        colors_int = ['#880E4F' if 'Iván' in x else '#90A4AE' for x in df_int['Aspirante']]
        
        fig_int = px.bar(df_int, x="%", y="Aspirante", orientation='h', text_auto=True, title="Preferencia Bruta")
        fig_int.update_traces(marker_color=colors_int, textfont_size=14)
        fig_int.update_layout(height=450, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_int, use_container_width=True)

        st.divider()
        st.markdown(f"#### 2. Competitividad Constitucional: Careo 1 vs Careo 2")
        st.caption("Comparativo: ¿Quién garantiza mejor el triunfo frente a la oposición?")

        # Datos Careos
        data_careos = DATOS_CAREOS_CONST.get(seleccion, {})
        
        c1, c2 = st.columns(2)
        
        # Careo 1: Félix
        with c1:
            st.markdown("**Escenario A: Félix Salgado**")
            df_c1 = pd.DataFrame(list(data_careos["Careo 1 (Félix)"].items()), columns=["Partido", "%"])
            color_map1 = {"MORENA (Félix)": "#BDBDBD", "PRI (Añorve)": "#E74C3C", "MC (Julián)": "#F39C12", "Ninguno": "#5D6D7E", "PT": "#E74C3C", "PVEM": "#2ECC71"}
            fig_c1 = px.pie(df_c1, names="Partido", values="%", color="Partido", color_discrete_map=color_map1, hole=0.4)
            fig_c1.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=250)
            st.plotly_chart(fig_c1, use_container_width=True)
            st.metric("Intención MORENA", f"{data_careos['Careo 1 (Félix)']['MORENA (Félix)']}%", delta="- Alto Rechazo", delta_color="inverse")

        # Careo 2: Iván
        with c2:
            st.markdown("**Escenario B: Iván Hernández**")
            df_c2 = pd.DataFrame(list(data_careos["Careo 2 (Iván)"].items()), columns=["Partido", "%"])
            color_map2 = {"MORENA (Iván)": "#880E4F", "PRI (Añorve)": "#E74C3C", "MC (Julián)": "#F39C12", "Ninguno": "#5D6D7E", "PT": "#E74C3C", "PVEM": "#2ECC71"}
            fig_c2 = px.pie(df_c2, names="Partido", values="%", color="Partido", color_discrete_map=color_map2, hole=0.4)
            fig_c2.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=250)
            st.plotly_chart(fig_c2, use_container_width=True)
            
            # Calculo diferencial
            voto_ivan = data_careos['Careo 2 (Iván)']['MORENA (Iván)']
            voto_felix = data_careos['Careo 1 (Félix)']['MORENA (Félix)']
            dif = round(voto_ivan - voto_felix, 1)
            
            st.metric("Intención MORENA", f"{voto_ivan}%", delta=f"+{dif} pts vs Escenario A")

        st.success(f"💡 **CONCLUSIÓN:** Iván Hernández aporta **{dif} puntos adicionales** a la marca MORENA comparado con el escenario de Félix Salgado. Además, reduce el voto 'Ninguno' significativamente.")

    # TAB 2: ATRIBUTOS
    with tabs[1]:
        st.subheader("Diagnóstico Cualitativo (Estatal)")
        
        df_attr = pd.DataFrame(DATOS_ATRIBUTOS_RESUMEN).set_index("Aspirante")
        df_attr = df_attr.sort_values("Buen_Cand", ascending=False)
        
        # Heatmap
        st.markdown("##### 🚦 Semáforo de Calidad")
        fig_heat = px.imshow(
            df_attr.drop(columns=["Rechazo"]), 
            text_auto=True, aspect="auto", color_continuous_scale="Greens",
            title="Matriz de Fortalezas (% Opinión 'Mucho'/'Sí')"
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
        col_atr1, col_atr2 = st.columns(2)
        with col_atr1:
            st.markdown("##### 🌟 Honestidad (Diferencial)")
            fig_hon = px.bar(df_attr.sort_values("Honestidad", ascending=True), x="Honestidad", y=df_attr.index, orientation='h', text_auto=True, color_discrete_sequence=['#2ECC71'])
            fig_hon.update_layout(height=400)
            st.plotly_chart(fig_hon, use_container_width=True)
            
        with col_atr2:
            st.markdown("##### 📉 Rechazo (Nunca Votaría)")
            fig_rej = px.bar(df_attr.sort_values("Rechazo", ascending=True), x="Rechazo", y=df_attr.index, orientation='h', text_auto=True, color_discrete_sequence=['#E74C3C'])
            fig_rej.update_layout(height=400)
            st.plotly_chart(fig_rej, use_container_width=True)

    # TAB 3: EVOLUCIÓN
    with tabs[2]:
        st.subheader(f"Evolución de Conocimiento (Name ID) - {seleccion}")
        data_c = DATOS_CONOCIMIENTO.get(seleccion, {}) if seleccion in DATOS_CONOCIMIENTO else DATOS_CONOCIMIENTO["GUERRERO (ESTATAL)"]
        
        df_c = pd.DataFrame([{"Aspirante": k, "Junio": v[0], "Dic": v[1]} for k,v in data_c.items()]).sort_values("Dic", ascending=True)
        
        fig_slope = go.Figure()
        for i, row in df_c.iterrows():
            color = "#880E4F" if "Iván" in row["Aspirante"] else "gray"
            width = 4 if "Iván" in row["Aspirante"] else 1
            opacity = 1 if "Iván" in row["Aspirante"] else 0.5
            
            fig_slope.add_shape(type="line", x0=0, y0=row["Junio"], x1=1, y1=row["Dic"], 
                                line=dict(color=color, width=width), opacity=opacity)
            
            # Puntos extremos
            fig_slope.add_trace(go.Scatter(x=[0, 1], y=[row["Junio"], row["Dic"]], mode="markers+text",
                                           text=[f"{row['Aspirante']} {row['Junio']}%", f"{row['Dic']}% {row['Aspirante']}"],
                                           textposition=["middle left", "middle right"],
                                           marker=dict(color=color, size=8), showlegend=False))

        fig_slope.update_layout(
            title="Crecimiento Junio vs Diciembre",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=True, tickvals=[0, 1], ticktext=["Junio '25", "Dic '25"]),
            yaxis=dict(showgrid=True, showticklabels=False),
            height=600, margin=dict(l=150, r=150)
        )
        st.plotly_chart(fig_slope, use_container_width=True)

    # TAB 4: CONTEXTO
    with tabs[3]:
        st.subheader(f"Agenda Pública: Principales Problemas - {seleccion}")
        data_p = DATOS_PROBLEMAS.get(seleccion, {})
        df_p = pd.DataFrame([{"Problema": k, "Junio": v[0], "Dic": v[1]} for k,v in data_p.items()])
        df_melt_p = df_p.melt(id_vars="Problema", var_name="Mes", value_name="%")
        
        fig_p = px.bar(df_melt_p.sort_values("%", ascending=True), x="%", y="Problema", color="Mes", barmode="group", orientation='h', text_auto=True, color_discrete_map={"Junio": "#90A4AE", "Dic": "#D81B60"})
        st.plotly_chart(fig_p, use_container_width=True)

if __name__ == "__main__":
    main()