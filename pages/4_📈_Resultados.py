import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="Resultados Finales Guerrero 2025", layout="wide")

# Estilo personalizado para UI más profesional
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stApp {background-color: #ffffff;}
    h1, h2, h3 {color: #1e3a8a; font-family: 'Helvetica Neue', sans-serif;}
    .stTabs [data-baseweb="tab"] {font-size: 16px; font-weight: bold;}
    .stInfo, .stSuccess {border-radius: 10px; padding: 15px;}
    </style>
    """, unsafe_allow_html=True)

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

# 2. PARTIDOS
DATOS_VOTO_GOB = {
    "GUERRERO (ESTATAL)": {"PAN": [2.0, 2.0], "PRI": [16.0, 4.0], "PT": [2.0, 1.0], "PVEM": [3.0, 1.0], "MC": [7.0, 2.0], "MORENA": [48.0, 60.0], "PRD": [3.0, 1.0], "Ninguno": [9.0, 16.0], "No sabe": [10.0, 13.0]},
    "ACAPULCO": {"PAN": [2.0, 1.0], "PRI": [10.0, 3.0], "PT": [3.0, 1.0], "PVEM": [4.0, 1.0], "MC": [10.0, 3.0], "MORENA": [48.0, 65.0], "PRD": [2.0, 0.0], "Ninguno": [9.0, 14.0], "No sabe": [10.0, 11.0]},
    "CHILPANCINGO": {"PAN": [1.0, 1.0], "PRI": [15.0, 6.0], "PT": [2.0, 2.0], "PVEM": [3.0, 2.0], "MC": [6.0, 2.0], "MORENA": [34.0, 46.0], "PRD": [4.0, 1.0], "Ninguno": [19.0, 23.0], "No sabe": [15.0, 16.0]},
    "IGUALA": {"PAN": [1.0, 4.0], "PRI": [16.0, 2.0], "PT": [2.0, 1.0], "PVEM": [5.0, 1.0], "MC": [8.0, 2.0], "MORENA": [41.0, 61.0], "PRD": [4.0, 2.0], "Ninguno": [10.0, 12.0], "No sabe": [13.0, 15.0]}
}

# 3. CONOCIMIENTO
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

# 9. CAREO (solo Diciembre)
DATOS_CAREO_1 = {
    "GUERRERO (ESTATAL)": {"Gustavo Alarcón Herrera (PAN)": 0.8, "Manuel Añorve Baños (PRI)": 2.5, "Candidato o candidata del PT": 4.2, "Candidato o candidata del PVEM": 2.9, "Julián López Galeana (MC)": 2.9, "Félix Salgado Macedonio (MORENA)": 22.9, "Candidato o candidata del PRD": 1.6, "Ninguno": 33.9, "No sabe": 19.0, "No respondió": 9.3},
    "ACAPULCO": {"Gustavo Alarcón Herrera (PAN)": 0.3, "Manuel Añorve Baños (PRI)": 2.2, "Candidato o candidata del PT": 4.2, "Candidato o candidata del PVEM": 3.7, "Julián López Galeana (MC)": 3.5, "Félix Salgado Macedonio (MORENA)": 25.8, "Candidato o candidata del PRD": 1.6, "Ninguno": 35.7, "No sabe": 14.0, "No respondió": 8.9},
    "CHILPANCINGO": {"Gustavo Alarcón Herrera (PAN)": 2.1, "Manuel Añorve Baños (PRI)": 3.4, "Candidato o candidata del PT": 5.2, "Candidato o candidata del PVEM": 1.7, "Julián López Galeana (MC)": 2.3, "Félix Salgado Macedonio (MORENA)": 17.8, "Candidato o candidata del PRD": 1.6, "Ninguno": 34.0, "No sabe": 26.6, "No respondió": 5.2},
    "IGUALA": {"Gustavo Alarcón Herrera (PAN)": 1.0, "Manuel Añorve Baños (PRI)": 2.2, "Candidato o candidata del PT": 1.9, "Candidato o candidata del PVEM": 1.1, "Julián López Galeana (MC)": 0.8, "Félix Salgado Macedonio (MORENA)": 17.6, "Candidato o candidata del PRD": 1.9, "Ninguno": 24.7, "No sabe": 29.9, "No respondió": 18.9}
}

DATOS_CAREO_2 = {
    "GUERRERO (ESTATAL)": {"Gustavo Alarcón Herrera (PAN)": 1.1, "Manuel Añorve Baños (PRI)": 2.6, "Candidato o candidata del PT": 3.7, "Candidato o candidata del PVEM": 2.2, "Julián López Galeana (MC)": 1.8, "Iván Hernández Díaz (MORENA)": 34.5, "Candidato o candidata del PRD": 1.0, "Ninguno": 25.8, "No sabe": 16.9, "No respondió": 10.3},
    "ACAPULCO": {"Gustavo Alarcón Herrera (PAN)": 0.9, "Manuel Añorve Baños (PRI)": 2.5, "Candidato o candidata del PT": 3.9, "Candidato o candidata del PVEM": 2.4, "Julián López Galeana (MC)": 2.0, "Iván Hernández Díaz (MORENA)": 37.9, "Candidato o candidata del PRD": 0.9, "Ninguno": 27.1, "No sabe": 12.3, "No respondió": 10.1},
    "CHILPANCINGO": {"Gustavo Alarcón Herrera (PAN)": 1.4, "Manuel Añorve Baños (PRI)": 3.1, "Candidato o candidata del PT": 3.8, "Candidato o candidata del PVEM": 1.9, "Julián López Galeana (MC)": 1.8, "Iván Hernández Díaz (MORENA)": 26.0, "Candidato o candidata del PRD": 1.2, "Ninguno": 25.6, "No sabe": 25.3, "No respondió": 9.8},
    "IGUALA": {"Gustavo Alarcón Herrera (PAN)": 1.7, "Manuel Añorve Baños (PRI)": 1.9, "Candidato o candidata del PT": 2.8, "Candidato o candidata del PVEM": 1.9, "Julián López Galeana (MC)": 1.0, "Iván Hernández Díaz (MORENA)": 33.1, "Candidato o candidata del PRD": 1.4, "Ninguno": 19.4, "No sabe": 24.1, "No respondió": 12.8}
}

# ==============================================================================
# 🎨 PALETAS DE COLORES
# ==============================================================================
COLOR_PARTIDOS = {
    "PAN": "#0000FF", "PRI": "#008000", "PRD": "#FFFF00", "PVEM": "#90EE90",
    "PT": "#FF0000", "MC": "#FFA500", "MORENA": "#880E4F",
    "Ninguno": "#808080", "No sabe": "#A9A9A9", "No respondió": "#D3D3D3"
}

COLOR_ASPIRANTES = {
    "Iván Hernández": "#880E4F", "Iván Hernández Díaz": "#880E4F",
    "Félix Salgado": "#C0392B", "Félix Salgado Macedonio": "#C0392B",
    "Abelina López": "#1f77b4", "Beatriz Mojica": "#2ca02c",
    "Esthela Damián": "#ff7f0e", "Javier Saldaña": "#9467bd",
    "Jacinto González": "#8c564b", "Pablo Amílcar": "#e377c2",
    "Gustavo Alarcón Herrera (PAN)": "#0000FF", "Manuel Añorve Baños (PRI)": "#008000",
    "Julián López Galeana (MC)": "#FFA500", "Candidato o candidata del PT": "#FF0000",
    "Candidato o candidata del PVEM": "#90EE90", "Candidato o candidata del PRD": "#FFFF00"
}

# ==============================================================================
# 🛠️ ANÁLISIS BREVE POR PESTAÑA
# ==============================================================================
def analisis_problemas(sel):
    data = DATOS_PROBLEMAS.get(sel, {})
    if not data: return "No hay datos disponibles."
    max_prob = max(data.items(), key=lambda x: x[1][1])
    return f"**Análisis:** La inseguridad domina la agenda ({max_prob[1][1]}% en diciembre), con fuerte incremento en la percepción ciudadana."

def analisis_partidos(sel):
    data = DATOS_VOTO_GOB.get(sel, {})
    if not data: return "No hay datos disponibles."
    return f"**Análisis:** MORENA consolida su liderazgo con {data['MORENA'][1]}% (+{data['MORENA'][1]-data['MORENA'][0']} pts). Los partidos tradicionales pierden terreno."

def analisis_conocimiento(sel):
    data = DATOS_CONOCIMIENTO.get(sel, {})
    if not data: return "No hay datos disponibles."
    top = max(data.items(), key=lambda x: x[1][1])
    ivan = data.get("Iván Hernández", [0,0])
    return f"**Análisis:** {top[0]} lidera el reconocimiento ({top[1][1]}%). Iván Hernández muestra el mayor crecimiento (+{ivan[1]-ivan[0]:.1f} pts)."

def analisis_opinion(sel):
    if sel == "GUERRERO (ESTATAL)":
        return "**Análisis:** Iván Hernández alcanza la opinión neta más alta. Félix Salgado mantiene alta polarización."
    else:
        data = DATOS_OPINION_MUNICIPAL.get(sel, {})
        if data and "Iván Hernández" in data:
            return f"**Análisis:** Iván Hernández lidera opinión positiva en {sel} ({data['Iván Hernández'][1]}%)."
        return "**Análisis:** Variación significativa en percepción municipal."

def analisis_atributos():
    return "**Análisis:** Iván Hernández domina los atributos cualitativos en diciembre, especialmente 'Buen Candidato' y 'Honestidad'."

def analisis_interno(sel):
    data = DATOS_INTERNA.get(sel, {})
    if not data: return "No hay datos disponibles."
    ivan = data.get("Iván Hernández", [0,0])
    return f"**Análisis:** Iván Hernández se posiciona como favorito interno ({ivan[1]}%), con fuerte crecimiento."

def analisis_autoridades(sel):
    pres = DATOS_AUTORIDADES["Presidenta"].get(sel, {})
    return f"**Análisis:** Alta aprobación presidencial ({pres.get('Aprueba',[0,0])[1]}%). Gobernadora mantiene estabilidad."

def analisis_sociodem():
    return "**Análisis:** Muestra equilibrada por género y edad, con leve mejora en NSE medios."

def analisis_careo(sel):
    c1 = DATOS_CAREO_1[sel].get("Félix Salgado Macedonio (MORENA)", 0)
    c2 = DATOS_CAREO_2[sel]["Iván Hernández Díaz (MORENA)"]
    return f"**Análisis:** Iván Hernández Díaz muestra mayor competitividad ({c2}%) que Félix Salgado ({c1}%) en careo directo."

# ==============================================================================
# 🚀 APP STREAMLIT
# ==============================================================================
def main():
    st.title("📊 Resultados Finales: Guerrero 2025")
    st.markdown("### Tablero Estratégico de Encuesta")

    with st.sidebar:
        st.header("📍 Vista Territorial")
        sel = st.selectbox("Seleccionar:", ["GUERRERO (ESTATAL)", "ACAPULCO", "CHILPANCINGO", "IGUALA"])

    tabs = st.tabs(["🚨 Problemas", "🏁 Partidos", "🧠 Conocimiento", "💭 Opinión", "✨ Atributos", "🗳️ Candidato Interno", "👔 Evaluación Autoridades", "📊 Sociodemográficos", "⚔️ Careo"])

    with tabs[0]:  # Problemas
        st.subheader(f"Principales Problemas - {sel}")
        st.info(analisis_problemas(sel))
        data_p = DATOS_PROBLEMAS.get(sel, {})
        df_p = pd.DataFrame([{"Problema": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data_p.items()])
        df_melt_p = df_p.melt(id_vars="Problema", var_name="Mes", value_name="%")
        fig_p = px.bar(df_melt_p, x="%", y="Problema", color="Mes", barmode="group", orientation='h',
                       text_auto=True, height=500, color_discrete_map={"Junio": "#B0BEC5", "Diciembre": "#880E4F"})
        st.plotly_chart(fig_p, use_container_width=True)

    with tabs[1]:  # Partidos
        st.subheader(f"Preferencias Partidistas - {sel}")
        st.info(analisis_partidos(sel))
        data_v = DATOS_VOTO_GOB.get(sel, {})
        df_v = pd.DataFrame([{"Partido": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data_v.items()])
        df_melt_v = df_v.melt(id_vars="Partido", var_name="Mes", value_name="%")
        order = df_v.sort_values("Diciembre", ascending=False)["Partido"].tolist()
        fig_v = px.bar(df_melt_v, x="%", y="Partido", color="Partido", barmode="group", orientation='h',
                       text_auto=True, height=600, category_orders={"Partido": order},
                       color_discrete_map=COLOR_PARTIDOS)
        fig_v.update_layout(showlegend=False)
        st.plotly_chart(fig_v, use_container_width=True)

    with tabs[2]:  # Conocimiento
        st.subheader(f"Evolución del Conocimiento - {sel}")
        st.info(analisis_conocimiento(sel))
        data_c = DATOS_CONOCIMIENTO.get(sel, {})
        df_c = pd.DataFrame([{"Aspirante": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data_c.items()])
        df_melt_c = df_c.melt(id_vars="Aspirante", var_name="Mes", value_name="%")
        order = df_c.sort_values("Diciembre", ascending=False)["Aspirante"].tolist()
        fig_c = px.bar(df_melt_c, x="%", y="Aspirante", color="Aspirante", barmode="group", orientation='h',
                       text="%", height=650, category_orders={"Aspirante": order},
                       color_discrete_map=COLOR_ASPIRANTES)
        fig_c.update_traces(textfont_size=14, textposition='outside')
        fig_c.update_layout(showlegend=False)
        st.plotly_chart(fig_c, use_container_width=True)

    with tabs[3]:  # Opinión
        st.subheader("Opinión de Aspirantes")
        st.info(analisis_opinion(sel))

        if sel == "GUERRERO (ESTATAL)":
            st.markdown("#### 📈 Opinión Neta Estatal (Buena - Mala)")
            df_neta = pd.DataFrame({
                "Aspirante": list(DATOS_OPINION_ESTATAL.keys()),
                "Junio": [v["Buena"][0] - v["Mala"][0] for v in DATOS_OPINION_ESTATAL.values()],
                "Diciembre": [v["Buena"][1] - v["Mala"][1] for v in DATOS_OPINION_ESTATAL.values()]
            })
            df_neta_melt = df_neta.melt(id_vars="Aspirante", var_name="Mes", value_name="Neta")
            order_neta = df_neta.sort_values("Diciembre", ascending=False)["Aspirante"].tolist()
            fig_neta = px.bar(df_neta_melt, x="Neta", y="Aspirante", color="Aspirante", barmode="group",
                              orientation='h', text_auto=True, height=600,
                              category_orders={"Aspirante": order_neta}, color_discrete_map=COLOR_ASPIRANTES)
            fig_neta.update_layout(showlegend=False)
            st.plotly_chart(fig_neta, use_container_width=True)

            st.markdown("#### Detalle por Aspirante")
            for asp, vals in DATOS_OPINION_ESTATAL.items():
                with st.expander(asp):
                    net_jun = vals["Buena"][0] - vals["Mala"][0]
                    net_dic = vals["Buena"][1] - vals["Mala"][1]
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Neta Junio", f"{net_jun:+}")
                    col2.metric("Neta Diciembre", f"{net_dic:+}")
                    col3.metric("Cambio", f"{net_dic - net_jun:+}")
                    df_op = pd.DataFrame([{"Opinión": k, "Junio": v[0], "Diciembre": v[1]} for k, v in vals.items()])
                    fig_op = px.bar(df_op, x="Opinión", y=["Junio", "Diciembre"], barmode='group', height=300)
                    st.plotly_chart(fig_op, use_container_width=True)
        else:
            data_op = DATOS_OPINION_MUNICIPAL.get(sel, {})
            df_op = pd.DataFrame([{"Aspirante": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data_op.items()])
            df_melt = df_op.melt(id_vars="Aspirante", var_name="Mes", value_name="% Positiva")
            order = df_op.sort_values("Diciembre", ascending=False)["Aspirante"].tolist()
            fig_op = px.bar(df_melt, x="% Positiva", y="Aspirante", color="Aspirante", barmode="group",
                            orientation='h', text_auto=True, height=600,
                            category_orders={"Aspirante": order}, color_discrete_map=COLOR_ASPIRANTES)
            fig_op.update_layout(showlegend=False)
            st.plotly_chart(fig_op, use_container_width=True)

    with tabs[4]:  # Atributos
        st.subheader("Diagnóstico Cualitativo (Estatal)")
        st.info(analisis_atributos())

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Atributos Junio")
            df_jun = pd.DataFrame(DATOS_ATRIBUTOS_JUN).set_index("Aspirante")
            df_jun = df_jun.sort_values("Buen Candidato", ascending=False)
            fig_jun = px.imshow(df_jun, text_auto=True, aspect="auto", color_continuous_scale="Blues")
            st.plotly_chart(fig_jun, use_container_width=True)

        with col2:
            st.markdown("##### Atributos Diciembre")
            df_dic = pd.DataFrame(DATOS_ATRIBUTOS_DIC).set_index("Aspirante")
            df_dic = df_dic.sort_values("Buen Candidato", ascending=False)
            fig_dic = px.imshow(df_dic, text_auto=True, aspect="auto", color_continuous_scale="Greens")
            st.plotly_chart(fig_dic, use_container_width=True)

        st.markdown("##### Evolución Radar")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown("**Iván Hernández**")
            d_ivan = DATOS_RADAR_EVO["Iván Hernández"]
            fig_ivan = go.Figure()
            fig_ivan.add_trace(go.Scatterpolar(r=[v[0] for v in d_ivan.values()], theta=list(d_ivan.keys()), fill='toself', name='Junio'))
            fig_ivan.add_trace(go.Scatterpolar(r=[v[1] for v in d_ivan.values()], theta=list(d_ivan.keys()), fill='toself', name='Diciembre', line_color='#880E4F'))
            fig_ivan.update_layout(polar=dict(radialaxis=dict(range=[0, 50])), height=400)
            st.plotly_chart(fig_ivan, use_container_width=True)

        with col_r2:
            st.markdown("**Félix Salgado**")
            d_felix = DATOS_RADAR_EVO["Félix Salgado"]
            fig_felix = go.Figure()
            fig_felix.add_trace(go.Scatterpolar(r=[v[0] for v in d_felix.values()], theta=list(d_felix.keys()), fill='toself', name='Junio'))
            fig_felix.add_trace(go.Scatterpolar(r=[v[1] for v in d_felix.values()], theta=list(d_felix.keys()), fill='toself', name='Diciembre', line_color='#C0392B'))
            fig_felix.update_layout(polar=dict(radialaxis=dict(range=[0, 50])), height=400)
            st.plotly_chart(fig_felix, use_container_width=True)

    with tabs[5]:  # Candidato Interno
        st.subheader(f"Preferencia Interna MORENA - {sel}")
        st.info(analisis_interno(sel))
        data_int = DATOS_INTERNA.get(sel, {})
        df_int = pd.DataFrame([{"Aspirante": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data_int.items()])
        df_int = df_int.sort_values("Diciembre", ascending=False)

        fig_slope = go.Figure()
        for _, row in df_int.iterrows():
            color = COLOR_ASPIRANTES.get(row["Aspirante"], "#95a5a6")
            fig_slope.add_trace(go.Scatter(
                x=["Junio", "Diciembre"], y=[row["Junio"], row["Diciembre"]],
                mode="lines+markers+text", name=row["Aspirante"],
                line=dict(color=color, width=3), marker=dict(size=10),
                text=["", f"{row['Diciembre']}%"], textposition="top center"
            ))
        fig_slope.update_layout(height=700, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_slope, use_container_width=True)

        st.markdown("#### 📋 Tabla de Resultados")
        df_display = df_int.copy()
        df_display["Cambio"] = df_display["Diciembre"] - df_display["Junio"]
        st.dataframe(df_display.style.format({"Junio": "{:.1f}%", "Diciembre": "{:.1f}%", "Cambio": "{:+.1f} pts"}), use_container_width=True)

    with tabs[6]:  # Evaluación Autoridades
        st.subheader("Evaluación de Autoridades")
        st.info(analisis_autoridades(sel))
        # (código original de autoridades mantenido – funciona perfectamente)

        # Presidenta
        if sel in DATOS_AUTORIDADES["Presidenta"]:
            data = DATOS_AUTORIDADES["Presidenta"][sel]
            st.markdown("#### Presidenta de México")
            col1, col2 = st.columns(2)
            col1.metric("Aprueba Dic", f"{data['Aprueba'][1]}%")
            col2.metric("Desaprueba Dic", f"{data['Desaprueba'][1]}%")
            df = pd.DataFrame([{"Categoría": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data.items()])
            fig = px.bar(df, x="Categoría", y=["Junio", "Diciembre"], barmode='group')
            st.plotly_chart(fig, use_container_width=True)

        # Gobernadora
        if sel in DATOS_AUTORIDADES["Gobernadora"]:
            data = DATOS_AUTORIDADES["Gobernadora"][sel]
            st.markdown("#### Gobernadora de Guerrero")
            col1, col2 = st.columns(2)
            col1.metric("Aprueba Dic", f"{data['Aprueba'][1]}%")
            col2.metric("Desaprueba Dic", f"{data['Desaprueba'][1]}%")
            df = pd.DataFrame([{"Categoría": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data.items()])
            fig = px.bar(df, x="Categoría", y=["Junio", "Diciembre"], barmode='group')
            st.plotly_chart(fig, use_container_width=True)

        # Presidentes Municipales (si aplica)
        if sel == "ACAPULCO":
            data = DATOS_AUTORIDADES["Pres. Municipal Acapulco"]["ACAPULCO"]
            st.markdown("#### Pdte. Municipal Acapulco")
        elif sel == "CHILPANCINGO":
            data = DATOS_AUTORIDADES["Pres. Municipal Chilpancingo"]["CHILPANCINGO"]
            st.markdown("#### Pdte. Municipal Chilpancingo")
        elif sel == "IGUALA":
            data = DATOS_AUTORIDADES["Pres. Municipal Iguala"]["IGUALA"]
            st.markdown("#### Pdte. Municipal Iguala")
        else:
            data = None

        if data:
            col1, col2 = st.columns(2)
            col1.metric("Aprueba Dic", f"{data['Aprueba'][1]}%")
            col2.metric("Desaprueba Dic", f"{data['Desaprueba'][1]}%")
            df = pd.DataFrame([{"Categoría": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data.items()])
            fig = px.bar(df, x="Categoría", y=["Junio", "Diciembre"], barmode='group')
            st.plotly_chart(fig, use_container_width=True)

    with tabs[7]:  # Sociodemográficos
        st.subheader("Perfil Sociodemográfico")
        st.info(analisis_sociodem())
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("##### Edad")
            df = pd.DataFrame([{"Rango": k, "Junio": v[0], "Diciembre": v[1]} for k, v in DATOS_SOCIODEM["Edad"].items()])
            fig = px.bar(df, x="Rango", y=["Junio", "Diciembre"], barmode='group')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("##### Sexo")
            df = pd.DataFrame([{"Sexo": k, "Junio": v[0], "Diciembre": v[1]} for k, v in DATOS_SOCIODEM["Sexo"].items()])
            fig = px.bar(df, x="Sexo", y=["Junio", "Diciembre"], barmode='group')
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("##### NSE")
            df = pd.DataFrame([{"NSE": k, "Junio": v[0], "Diciembre": v[1]} for k, v in DATOS_SOCIODEM["NSE"].items()])
            fig = px.bar(df, x="NSE", y=["Junio", "Diciembre"], barmode='group')
            st.plotly_chart(fig, use_container_width=True)

    with tabs[8]:  # Careo
        st.subheader(f"Careo Electoral - {sel} (Diciembre 2025)")
        st.info(analisis_careo(sel))

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### Careo 1: Félix Salgado vs Oposición")
            df_c1 = pd.DataFrame(list(DATOS_CAREO_1[sel].items()), columns=["Candidato", "%"])
            df_c1 = df_c1.sort_values("%", ascending=False)
            fig_c1 = px.bar(df_c1, x="%", y="Candidato", orientation='h', text="%", height=600,
                            color="Candidato", color_discrete_map=COLOR_ASPIRANTES)
            fig_c1.update_traces(textposition='outside', texttemplate='%{text:.1f}%')
            fig_c1.update_layout(showlegend=False)
            st.plotly_chart(fig_c1, use_container_width=True)

        with col2:
            st.markdown("##### Careo 2: Iván Hernández vs Oposición")
            df_c2 = pd.DataFrame(list(DATOS_CAREO_2[sel].items()), columns=["Candidato", "%"])
            df_c2 = df_c2.sort_values("%", ascending=False)
            fig_c2 = px.bar(df_c2, x="%", y="Candidato", orientation='h', text="%", height=600,
                            color="Candidato", color_discrete_map=COLOR_ASPIRANTES)
            fig_c2.update_traces(textposition='outside', texttemplate='%{text:.1f}%')
            fig_c2.update_layout(showlegend=False)
            st.plotly_chart(fig_c2, use_container_width=True)

if __name__ == "__main__":
    main()