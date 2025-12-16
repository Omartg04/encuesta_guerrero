import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. IMPORTAR LA FUNCIÓN DE SEGURIDAD
from src.auth import bloquear_acceso 

# Configuración de página
st.set_page_config(page_title="Resultados Finales 2025", layout="wide")

# 2. ACTIVAR EL BLOQUEO (Esto pedirá usuario y contraseña antes de mostrar nada)
bloquear_acceso()

# --- CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="Resultados Finales Guerrero 2025", layout="wide", page_icon="📊")

# Estilo personalizado para UI más profesional
st.markdown("""
    <style>
    /* Tipografía y fondo general */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    .main {
        background-color: #f4f6f9;
    }
    h1, h2, h3 {
        color: #1e3a8a; 
        font-weight: 700;
    }
    
    /* Estilo para las métricas (KPIs) */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 5px 5px 0 0;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
    }
    .stTabs [aria-selected="true"] {
        background-color: #e3f2fd;
        color: #1e3a8a;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 🗄️ BASE DE DATOS MAESTRA (Intacta)
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
    "Alcaldes": {
        "ACAPULCO": {"Aprueba": [24, 22], "Desaprueba": [71, 75], "No sabe": [5, 3]},
        "CHILPANCINGO": {"Aprueba": [37, 19], "Desaprueba": [52, 74], "No sabe": [11, 8]},
        "IGUALA": {"Aprueba": [39, 30], "Desaprueba": [51, 59], "No sabe": [10, 11]}
    }
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
# 🎨 PALETAS DE COLORES (Intactas)
# ==============================================================================
COLOR_PARTIDOS = {
    "PAN": "#0066CC", 
    "PRI": "#00A650", 
    "PRD": "#FFD700", 
    "PVEM": "#90EE90",
    "PT": "#DC143C", 
    "MC": "#FF8C00", 
    "MORENA": "#880E4F",
    "Ninguno": "#808080", 
    "No sabe": "#A9A9A9", 
    "No respondió": "#D3D3D3"
}

COLOR_ASPIRANTES = {
    "Iván Hernández": "#880E4F", 
    "Iván Hernández Díaz": "#880E4F",
    "Félix Salgado": "#C0392B", 
    "Félix Salgado Macedonio": "#C0392B",
    "Abelina López": "#1f77b4", 
    "Beatriz Mojica": "#2ca02c",
    "Esthela Damián": "#ff7f0e", 
    "Javier Saldaña": "#9467bd",
    "Jacinto González": "#8c564b", 
    "Pablo Amílcar": "#e377c2",
    "Gustavo Alarcón Herrera (PAN)": "#0066CC", 
    "Manuel Añorve Baños (PRI)": "#00A650",
    "Julián López Galeana (MC)": "#FF8C00", 
    "Candidato o candidata del PT": "#DC143C",
    "Candidato o candidata del PVEM": "#90EE90", 
    "Candidato o candidata del PRD": "#FFD700",
    "Ninguno": "#808080",
    "No sabe": "#A9A9A9"
}

# ==============================================================================
# 🛠️ FUNCIONES AUXILIARES DE ESTILO
# ==============================================================================

import io

def generar_excel_maestro():
    """Genera un archivo Excel con múltiples hojas basado en los diccionarios de datos."""
    output = io.BytesIO()
    # Usamos el motor xlsxwriter que es muy compatible con Streamlit
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        
        # 1. PROBLEMAS
        rows = []
        for terr, data in DATOS_PROBLEMAS.items():
            for prob, vals in data.items():
                rows.append({"Territorio": terr, "Problema": prob, "Junio": vals[0], "Diciembre": vals[1]})
        pd.DataFrame(rows).to_excel(writer, sheet_name='Problemas', index=False)

        # 2. PARTIDOS
        rows = []
        for terr, data in DATOS_VOTO_GOB.items():
            for part, vals in data.items():
                rows.append({"Territorio": terr, "Partido": part, "Junio": vals[0], "Diciembre": vals[1]})
        pd.DataFrame(rows).to_excel(writer, sheet_name='Partidos', index=False)

        # 3. CONOCIMIENTO
        rows = []
        for terr, data in DATOS_CONOCIMIENTO.items():
            for asp, vals in data.items():
                rows.append({"Territorio": terr, "Aspirante": asp, "Junio": vals[0], "Diciembre": vals[1]})
        pd.DataFrame(rows).to_excel(writer, sheet_name='Conocimiento', index=False)

        # 4. AUTORIDADES (Incluyendo Alcaldes)
        rows = []
        for cargo, territorios in DATOS_AUTORIDADES.items():
            for terr, metricas in territorios.items():
                for metrica, vals in metricas.items():
                    rows.append({
                        "Cargo": cargo, 
                        "Territorio": terr, 
                        "Métrica": metrica, 
                        "Junio": vals[0], 
                        "Diciembre": vals[1]
                    })
        pd.DataFrame(rows).to_excel(writer, sheet_name='Evaluación Autoridades', index=False)

        # 5. ATRIBUTOS (Solo Diciembre como ejemplo)
        pd.DataFrame(DATOS_ATRIBUTOS_DIC).to_excel(writer, sheet_name='Atributos Dic', index=False)

        # 6. CAREOS
        rows = []
        for terr, data in DATOS_CAREO_1.items(): # Careo 1
            for cand, val in data.items():
                 rows.append({"Territorio": terr, "Careo": "Félix Salgado", "Candidato": cand, "Diciembre": val})
        for terr, data in DATOS_CAREO_2.items(): # Careo 2
             for cand, val in data.items():
                 rows.append({"Territorio": terr, "Careo": "Iván Hernández", "Candidato": cand, "Diciembre": val})
        pd.DataFrame(rows).to_excel(writer, sheet_name='Careos', index=False)

    return output.getvalue()

def estilo_pro(fig, height=500, show_legend=True, legend_bottom=False):
    """Aplica estilo profesional a las gráficas de Plotly"""
    
    # Configuración de leyenda
    legend_cfg = {}
    if not show_legend:
        legend_cfg = dict(showlegend=False)
    elif legend_bottom:
        legend_cfg = dict(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5
            )
        )
    else:
        # Top right por defecto
        legend_cfg = dict(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

    fig.update_layout(
        font_family="Roboto, sans-serif",
        title_font_family="Roboto, sans-serif",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(t=40, l=20, r=20, b=20 if not legend_bottom else 60), # Margen extra abajo si leyenda está abajo
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Roboto, sans-serif"
        ),
        **legend_cfg
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig

def analisis_problemas(sel):
    data = DATOS_PROBLEMAS.get(sel, {})
    if not data: return "No hay datos disponibles."
    max_prob = max(data.items(), key=lambda x: x[1][1])
    return f"La **inseguridad** domina la agenda con un **{max_prob[1][1]}%** en diciembre, mostrando un incremento crítico respecto a la medición anterior."

def analisis_partidos(sel):
    data = DATOS_VOTO_GOB.get(sel, {})
    if not data: return "No hay datos disponibles."
    return f"**MORENA** consolida su hegemonía alcanzando el **{data['MORENA'][1]}%** de preferencia efectiva, creciendo +{data['MORENA'][1]-data['MORENA'][0]} puntos."

# ==============================================================================
# 🚀 APP STREAMLIT
# ==============================================================================
def main():
    st.title("📊 Resultados Finales: Guerrero 2025")
    st.markdown("### Tablero Estratégico de Encuesta")

    with st.sidebar:
        st.header("🔍 Configuración")
        sel = st.selectbox("Seleccionar Territorio:", ["GUERRERO (ESTATAL)", "ACAPULCO", "CHILPANCINGO", "IGUALA"])
        
        st.divider()
        st.subheader("📋 Ficha Técnica")
        st.markdown("""
        **Levantamiento:** Diciembre 2025
        
        **Muestra estatal:** 1,907 casos efectivos
        * **Acapulco:** 793 casos
        * **Chilpancingo:** 665 casos
        * **Iguala:** 449 casos
        
        **Metodología:** Encuesta en vivienda
        """)
        st.info("💡 Use las pestañas superiores para navegar por los módulos.")

    with st.sidebar:
        st.header("🔍 Configuración")
        sel = st.selectbox("Seleccionar Territorio:", ["GUERRERO (ESTATAL)", "ACAPULCO", "CHILPANCINGO", "IGUALA"])
        
        st.divider()
        st.subheader("📋 Ficha Técnica")
        # ... (tu texto de ficha técnica) ...
        
        st.divider()
        
        # --- BOTÓN DE DESCARGA ---
        st.subheader("📥 Descargar Datos")
        excel_data = generar_excel_maestro()
        st.download_button(
            label="Descargar Base Maestra (XLSX)",
            data=excel_data,
            file_name="Resultados_Guerrero_2025.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            icon="💾"
        )

    tabs = st.tabs(["🚨 Problemas", "🏛️ Partidos", "🧠 Conocimiento", "💭 Opinión", "✨ Atributos", "🗳️ Interna", "👔 Autoridades", "📊 Sociodem", "⚔️ Careo"])

    # 1. PROBLEMAS ----------------------------------------------------------------
    with tabs[0]:
        st.subheader(f"Principales Problemas - {sel}")
        
        data_p = DATOS_PROBLEMAS.get(sel, {})
        if data_p:
            # KPIs
            top_prob = max(data_p.items(), key=lambda x: x[1][1])
            col1, col2, col3 = st.columns(3)
            col1.metric("Principal Problema", top_prob[0])
            col2.metric("Nivel de Mención", f"{top_prob[1][1]}%", delta=f"{top_prob[1][1]-top_prob[1][0]:.1f} pts vs Jun", delta_color="inverse")
            col3.metric("Segundo Problema", sorted(data_p.items(), key=lambda x: x[1][1], reverse=True)[1][0])

            with st.container(border=True):
                st.markdown(f"**Análisis:** {analisis_problemas(sel)}")
                df_p = pd.DataFrame([{"Problema": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data_p.items()])
                df_melt_p = df_p.melt(id_vars="Problema", var_name="Mes", value_name="%")
                fig_p = px.bar(df_melt_p, x="%", y="Problema", color="Mes", barmode="group", orientation='h',
                            text_auto=True, color_discrete_map={"Junio": "#B0BEC5", "Diciembre": "#880E4F"})
                fig_p.update_traces(textposition='outside', textfont_size=13, textfont_weight='bold')
                st.plotly_chart(estilo_pro(fig_p), use_container_width=True)

    # 2. PARTIDOS -----------------------------------------------------------------
    with tabs[1]:
        st.subheader(f"Preferencias Partidistas - {sel}")
        data_v = DATOS_VOTO_GOB.get(sel, {})
        
        if data_v:
            # KPIs
            morena_val = data_v["MORENA"][1]
            pri_val = data_v["PRI"][1]
            col1, col2, col3 = st.columns(3)
            col1.metric("Líder (MORENA)", f"{morena_val}%", delta=f"{morena_val - data_v['MORENA'][0]:.1f} pts")
            col2.metric("Seguidor (PRI)", f"{pri_val}%", delta=f"{pri_val - data_v['PRI'][0]:.1f} pts")
            col3.metric("Ventaja", f"{morena_val - pri_val:.1f} pts", delta_color="off")

            with st.container(border=True):
                st.markdown(analisis_partidos(sel))
                df_v = pd.DataFrame([{"Partido": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data_v.items()])
                
                color_map_partidos = {k: COLOR_PARTIDOS.get(k, "#ccc") for k in df_v["Partido"].unique()}
                df_melt_v = df_v.melt(id_vars="Partido", var_name="Mes", value_name="%")
                order = df_v.sort_values("Diciembre", ascending=False)["Partido"].tolist()
                
                fig_v = px.bar(df_melt_v, x="%", y="Partido", color="Partido", facet_col="Mes",
                            orientation='h', text_auto=True, category_orders={"Partido": order},
                            color_discrete_map=color_map_partidos)
                fig_v.update_traces(textposition='outside', textfont_size=12)
                fig_v.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
                # Eliminamos la leyenda porque los nombres ya están en el eje Y
                st.plotly_chart(estilo_pro(fig_v, height=600, show_legend=False), use_container_width=True)

    # 3. CONOCIMIENTO -------------------------------------------------------------
    with tabs[2]:
        st.subheader(f"Conocimiento de Aspirantes - {sel}")
        data_c = DATOS_CONOCIMIENTO.get(sel, {})
        
        if data_c:
            top_k = max(data_c.items(), key=lambda x: x[1][1])
            top_growth = max(data_c.items(), key=lambda x: x[1][1]-x[1][0])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Mayor Conocimiento", top_k[0], f"{top_k[1][1]}%")
            col2.metric("Mayor Crecimiento", top_growth[0], f"+{top_growth[1][1]-top_growth[1][0]:.1f} pts")
            col3.metric("Iván Hernández", f"{data_c.get('Iván Hernández', [0,0])[1]}%", delta=f"+{data_c.get('Iván Hernández', [0,0])[1]-data_c.get('Iván Hernández', [0,0])[0]:.1f} pts")

            with st.container(border=True):
                df_c = pd.DataFrame([{"Aspirante": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data_c.items()])
                color_map_aspirantes = {k: COLOR_ASPIRANTES.get(k, "#ccc") for k in df_c["Aspirante"].unique()}
                
                df_melt_c = df_c.melt(id_vars="Aspirante", var_name="Mes", value_name="%")
                order = df_c.sort_values("Diciembre", ascending=False)["Aspirante"].tolist()
                
                fig_c = px.bar(df_melt_c, x="%", y="Aspirante", color="Aspirante", facet_col="Mes",
                            orientation='h', text_auto=True, category_orders={"Aspirante": order},
                            color_discrete_map=color_map_aspirantes)
                fig_c.update_traces(textposition='outside')
                fig_c.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
                # Leyenda redundante (nombres en eje Y), eliminada
                st.plotly_chart(estilo_pro(fig_c, height=650, show_legend=False), use_container_width=True)

    # 4. OPINIÓN ------------------------------------------------------------------
    with tabs[3]:
        st.subheader("Balance de Opinión")
        if sel == "GUERRERO (ESTATAL)":
            col1, col2 = st.columns(2)
            col1.metric("Mejor Opinión (+)", "Iván Hernández", "51% Buena")
            col2.metric("Peor Negativo (-)", "Félix Salgado", "46% Mala", delta_color="inverse")

            with st.container(border=True):
                st.markdown("##### 📈 Comparativo de Imagen (Estatal)")
                data_opinion_comp = []
                for asp, vals in DATOS_OPINION_ESTATAL.items():
                    data_opinion_comp.append({"Aspirante": asp, "Tipo": "Positiva", "Junio": vals["Buena"][0], "Diciembre": vals["Buena"][1]})
                    data_opinion_comp.append({"Aspirante": asp, "Tipo": "Negativa", "Junio": vals["Mala"][0], "Diciembre": vals["Mala"][1]})
                
                df_opinion_comp = pd.DataFrame(data_opinion_comp)
                orden_aspirantes = df_opinion_comp[df_opinion_comp["Tipo"] == "Positiva"].sort_values("Diciembre", ascending=False)["Aspirante"].tolist()
                
                fig_comp = go.Figure()
                
                for asp in orden_aspirantes:
                    df_asp = df_opinion_comp[df_opinion_comp["Aspirante"] == asp]
                    # Positiva
                    fig_comp.add_trace(go.Bar(y=[asp], x=[df_asp[df_asp["Tipo"]=="Positiva"]["Diciembre"].values[0]], orientation='h', name="Positiva Dic", marker_color="#2E7D32", texttemplate="%{x}%", textposition="inside"))
                    # Negativa
                    fig_comp.add_trace(go.Bar(y=[asp], x=[-df_asp[df_asp["Tipo"]=="Negativa"]["Diciembre"].values[0]], orientation='h', name="Negativa Dic", marker_color="#C62828", texttemplate="%{x}%", textposition="inside"))
                
                fig_comp.update_layout(barmode='relative', title="Balance Diciembre (Positiva vs Negativa)", yaxis={'categoryorder':'array', 'categoryarray':orden_aspirantes})
                # Leyenda movida abajo para que no estorbe
                st.plotly_chart(estilo_pro(fig_comp, height=600, legend_bottom=True), use_container_width=True)

        else:
             with st.container(border=True):
                data_op = DATOS_OPINION_MUNICIPAL.get(sel, {})
                df_op = pd.DataFrame([{"Aspirante": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data_op.items()])
                color_map_op = {k: COLOR_ASPIRANTES.get(k, "#ccc") for k in df_op["Aspirante"].unique()}
                
                df_melt = df_op.melt(id_vars="Aspirante", var_name="Mes", value_name="% Positiva")
                order = df_op.sort_values("Diciembre", ascending=False)["Aspirante"].tolist()
                
                fig_op = px.bar(df_melt, x="% Positiva", y="Aspirante", color="Aspirante", facet_col="Mes",
                                orientation='h', text_auto=True, category_orders={"Aspirante": order},
                                color_discrete_map=color_map_op)
                # Leyenda redundante eliminada
                st.plotly_chart(estilo_pro(fig_op, show_legend=False), use_container_width=True)

    # 5. ATRIBUTOS ----------------------------------------------------------------
    with tabs[4]:
        st.subheader("Diagnóstico Cualitativo")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Mejor 'Buen Candidato'", "Iván Hernández", "65.5%")
        with col2:
             st.metric("Más Honesto", "Iván Hernández", "33.6%")

        with st.container(border=True):
            col_h1, col_h2 = st.columns(2)
            with col_h1:
                st.markdown("**Junio**")
                df_jun = pd.DataFrame(DATOS_ATRIBUTOS_JUN).set_index("Aspirante").sort_values("Buen Candidato", ascending=False)
                fig_jun = px.imshow(df_jun, text_auto=True, aspect="auto", color_continuous_scale="Blues")
                st.plotly_chart(estilo_pro(fig_jun, height=400, show_legend=False), use_container_width=True)
            with col_h2:
                st.markdown("**Diciembre**")
                df_dic = pd.DataFrame(DATOS_ATRIBUTOS_DIC).set_index("Aspirante").sort_values("Buen Candidato", ascending=False)
                fig_dic = px.imshow(df_dic, text_auto=True, aspect="auto", color_continuous_scale="Greens")
                st.plotly_chart(estilo_pro(fig_dic, height=400, show_legend=False), use_container_width=True)

        with st.container(border=True):
            st.markdown("#### Evolución Radar")
            col_r1, col_r2 = st.columns(2)
            # Radar Iván
            d_ivan = DATOS_RADAR_EVO["Iván Hernández"]
            fig_ivan = go.Figure()
            fig_ivan.add_trace(go.Scatterpolar(r=[v[0] for v in d_ivan.values()], theta=list(d_ivan.keys()), fill='toself', name='Junio'))
            fig_ivan.add_trace(go.Scatterpolar(r=[v[1] for v in d_ivan.values()], theta=list(d_ivan.keys()), fill='toself', name='Diciembre', line_color='#880E4F'))
            fig_ivan.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 50])), title="Iván Hernández")
            col_r1.plotly_chart(estilo_pro(fig_ivan, height=400), use_container_width=True)
            
            # Radar Félix
            d_felix = DATOS_RADAR_EVO["Félix Salgado"]
            fig_felix = go.Figure()
            fig_felix.add_trace(go.Scatterpolar(r=[v[0] for v in d_felix.values()], theta=list(d_felix.keys()), fill='toself', name='Junio'))
            fig_felix.add_trace(go.Scatterpolar(r=[v[1] for v in d_felix.values()], theta=list(d_felix.keys()), fill='toself', name='Diciembre', line_color='#C0392B'))
            fig_felix.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 50])), title="Félix Salgado")
            col_r2.plotly_chart(estilo_pro(fig_felix, height=400), use_container_width=True)

    # 6. INTERNA ------------------------------------------------------------------
    with tabs[5]:
        st.subheader(f"Interna MORENA - {sel}")
        data_int = DATOS_INTERNA.get(sel, {})
        
        if data_int:
            # KPI
            lider = max(data_int.items(), key=lambda x: x[1][1])
            col1, col2, col3 = st.columns(3)
            col1.metric("Puntero Interno", lider[0], f"{lider[1][1]}%")
            col2.metric("Crecimiento Puntero", f"{lider[1][1]-lider[1][0]:.1f} pts")
            
            with st.container(border=True):
                df_int = pd.DataFrame([{"Aspirante": k, "Junio": v[0], "Diciembre": v[1]} for k, v in data_int.items()]).sort_values("Diciembre", ascending=False)
                fig_slope = go.Figure()
                for _, row in df_int.iterrows():
                    color = COLOR_ASPIRANTES.get(row["Aspirante"], "#95a5a6")
                    opacity = 1.0 if row["Diciembre"] > 10 else 0.3
                    fig_slope.add_trace(go.Scatter(
                        x=["Junio", "Diciembre"], y=[row["Junio"], row["Diciembre"]],
                        mode="lines+markers+text", name=row["Aspirante"],
                        line=dict(color=color, width=4 if row["Diciembre"] > 15 else 2),
                        marker=dict(size=10), opacity=opacity,
                        text=["", f"{row['Diciembre']}%"], textposition="top center", textfont=dict(size=14, color=color, family="Roboto")
                    ))
                st.plotly_chart(estilo_pro(fig_slope, height=600), use_container_width=True)

# 7. AUTORIDADES --------------------------------------------------------------
    with tabs[6]:
        st.subheader("Aprobación de Autoridades")
        
        # --- SECCIÓN 1: PRESIDENTA DE MÉXICO ---
        with st.container(border=True):
            st.markdown("#### 🇲🇽 Presidenta de México")
            if sel in DATOS_AUTORIDADES["Presidenta"]:
                d = DATOS_AUTORIDADES["Presidenta"][sel]
                
                # KPIs
                apr_dic = d['Aprueba'][1]
                apr_jun = d['Aprueba'][0]
                col1, col2, col3 = st.columns(3)
                col1.metric("Aprobación (Dic)", f"{apr_dic}%", delta=f"{apr_dic - apr_jun:.1f} pts vs Jun")
                col2.metric("Desaprobación", f"{d['Desaprueba'][1]}%")
                col3.metric("No sabe", f"{d['No sabe'][1]}%")
                
                # Gráfica
                df = pd.DataFrame([{"Cat": k, "Junio": v[0], "Diciembre": v[1]} for k,v in d.items()])
                fig = go.Figure(data=[
                    go.Bar(name='Junio', x=df["Cat"], y=df["Junio"], marker_color='#B0BEC5', text=df["Junio"], textposition='auto'),
                    go.Bar(name='Diciembre', x=df["Cat"], y=df["Diciembre"], marker_color='#880E4F', text=df["Diciembre"], textposition='auto')
                ])
                fig.update_layout(barmode='group')
                st.plotly_chart(estilo_pro(fig, height=350, legend_bottom=True), use_container_width=True)

        # --- SECCIÓN 2: GOBERNADORA ---
        with st.container(border=True):
            st.markdown("#### 🏛️ Gobernadora del Estado")
            if sel in DATOS_AUTORIDADES["Gobernadora"]:
                d = DATOS_AUTORIDADES["Gobernadora"][sel]
                
                # KPIs
                apr_dic = d['Aprueba'][1]
                apr_jun = d['Aprueba'][0]
                col1, col2, col3 = st.columns(3)
                col1.metric("Aprobación (Dic)", f"{apr_dic}%", delta=f"{apr_dic - apr_jun:.1f} pts vs Jun")
                col2.metric("Desaprobación", f"{d['Desaprueba'][1]}%", delta_color="inverse")
                col3.metric("No sabe", f"{d['No sabe'][1]}%")

                # Gráfica
                df = pd.DataFrame([{"Cat": k, "Junio": v[0], "Diciembre": v[1]} for k,v in d.items()])
                fig = go.Figure(data=[
                    go.Bar(name='Junio', x=df["Cat"], y=df["Junio"], marker_color='#B0BEC5', text=df["Junio"], textposition='auto'),
                    go.Bar(name='Diciembre', x=df["Cat"], y=df["Diciembre"], marker_color='#880E4F', text=df["Diciembre"], textposition='auto')
                ])
                fig.update_layout(barmode='group')
                st.plotly_chart(estilo_pro(fig, height=350, legend_bottom=True), use_container_width=True)

        # --- SECCIÓN 3: PRESIDENTES MUNICIPALES ---
        if sel in ["ACAPULCO", "CHILPANCINGO", "IGUALA"]:
            with st.container(border=True):
                st.markdown(f"#### 🏙️ Presidente Municipal de {sel.title()}")
                
                # Obtener datos específicos del diccionario actualizado "Alcaldes"
                d_alc = DATOS_AUTORIDADES["Alcaldes"].get(sel, {})
                
                if d_alc:
                    # KPIs
                    apr_dic = d_alc['Aprueba'][1]
                    apr_jun = d_alc['Aprueba'][0]
                    des_dic = d_alc['Desaprueba'][1]
                    des_jun = d_alc['Desaprueba'][0]
                    
                    col1, col2, col3 = st.columns(3)
                    # Lógica de color para delta: si baja la aprobación es rojo (normal), si sube es verde
                    col1.metric("Aprobación (Dic)", f"{apr_dic}%", delta=f"{apr_dic - apr_jun:.1f} pts vs Jun")
                    # Lógica inversa para desaprobación: si sube es malo (rojo/inverse)
                    col2.metric("Desaprobación (Dic)", f"{des_dic}%", delta=f"{des_dic - des_jun:.1f} pts", delta_color="inverse")
                    col3.metric("No sabe / NR", f"{d_alc['No sabe'][1]}%")

                    # Gráfica
                    df_alc = pd.DataFrame([
                        {"Categoría": "Aprueba", "Junio": d_alc["Aprueba"][0], "Diciembre": d_alc["Aprueba"][1]},
                        {"Categoría": "Desaprueba", "Junio": d_alc["Desaprueba"][0], "Diciembre": d_alc["Desaprueba"][1]},
                        {"Categoría": "NS/NR", "Junio": d_alc["No sabe"][0], "Diciembre": d_alc["No sabe"][1]}
                    ])
                    
                    fig_alc = go.Figure(data=[
                        go.Bar(name='Junio', x=df_alc["Categoría"], y=df_alc["Junio"], 
                               marker_color='#B0BEC5', text=df_alc["Junio"], textposition='auto'),
                        go.Bar(name='Diciembre', x=df_alc["Categoría"], y=df_alc["Diciembre"], 
                               marker_color='#880E4F', text=df_alc["Diciembre"], textposition='auto')
                    ])
                    
                    fig_alc.update_layout(barmode='group')
                    st.plotly_chart(estilo_pro(fig_alc, height=350, legend_bottom=True), use_container_width=True)
        else:
            # Mensaje informativo si están en vista ESTATAL
            st.info("ℹ️ Para ver la evaluación específica de los Presidentes Municipales, seleccione un municipio (Acapulco, Chilpancingo o Iguala) en el menú lateral.")

    # 8. SOCIODEM -----------------------------------------------------------------
    with tabs[7]:
        st.subheader("Perfil de la Muestra")
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Edad**")
                df = pd.DataFrame([{"Rango": k, "Diciembre": v[1]} for k, v in DATOS_SOCIODEM["Edad"].items()])
                fig = px.pie(df, values="Diciembre", names="Rango", hole=0.4, color_discrete_sequence=px.colors.sequential.Blues)
                st.plotly_chart(estilo_pro(fig, height=300, show_legend=False), use_container_width=True)
            with col2:
                st.markdown("**Sexo**")
                df = pd.DataFrame([{"Sexo": k, "Diciembre": v[1]} for k, v in DATOS_SOCIODEM["Sexo"].items()])
                fig = px.pie(df, values="Diciembre", names="Sexo", hole=0.4, color_discrete_map={"Hombres": "#90CAF9", "Mujeres": "#F48FB1"})
                st.plotly_chart(estilo_pro(fig, height=300, show_legend=False), use_container_width=True)
            with col3:
                st.markdown("**NSE**")
                df = pd.DataFrame([{"NSE": k, "Diciembre": v[1]} for k, v in DATOS_SOCIODEM["NSE"].items()])
                fig = px.bar(df, x="NSE", y="Diciembre", text_auto=True, color_discrete_sequence=["#5C6BC0"])
                st.plotly_chart(estilo_pro(fig, height=300), use_container_width=True)

    # 9. CAREO --------------------------------------------------------------------
    with tabs[8]:
        st.subheader(f"Escenarios Electorales - {sel}")
        
        c1_morena = DATOS_CAREO_1[sel].get("Félix Salgado Macedonio (MORENA)", 0)
        c2_morena = DATOS_CAREO_2[sel].get("Iván Hernández Díaz (MORENA)", 0)
        
        col1, col2 = st.columns(2)
        col1.metric("Preferencia Careo Félix", f"{c1_morena}%")
        col2.metric("Preferencia Careo Iván", f"{c2_morena}%", delta=f"{c2_morena - c1_morena:.1f} pts vs Félix")

        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            with st.container(border=True):
                st.markdown("##### Careo 1: Félix Salgado")
                df_c1 = pd.DataFrame(list(DATOS_CAREO_1[sel].items()), columns=["Candidato", "%"]).sort_values("%", ascending=False)
                color_map = {k: COLOR_ASPIRANTES.get(k, "#ccc") for k in df_c1["Candidato"]}
                fig_c1 = px.bar(df_c1, x="%", y="Candidato", orientation='h', text_auto=True, color="Candidato", color_discrete_map=color_map)
                fig_c1.update_traces(textposition='outside')
                fig_c1.update_layout(showlegend=False)
                st.plotly_chart(estilo_pro(fig_c1, height=500), use_container_width=True)
        
        with col_c2:
             with st.container(border=True):
                st.markdown("##### Careo 2: Iván Hernández")
                df_c2 = pd.DataFrame(list(DATOS_CAREO_2[sel].items()), columns=["Candidato", "%"]).sort_values("%", ascending=False)
                color_map = {k: COLOR_ASPIRANTES.get(k, "#ccc") for k in df_c2["Candidato"]}
                fig_c2 = px.bar(df_c2, x="%", y="Candidato", orientation='h', text_auto=True, color="Candidato", color_discrete_map=color_map)
                fig_c2.update_traces(textposition='outside')
                fig_c2.update_layout(showlegend=False)
                st.plotly_chart(estilo_pro(fig_c2, height=500), use_container_width=True)

if __name__ == "__main__":
    main()