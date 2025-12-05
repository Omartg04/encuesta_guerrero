import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Centro de Mando Electoral",
    page_icon="🗳️",
    layout="centered"
)

# Título y Bienvenida
st.title("🗳️ Centro de Mando Logístico - Guerrero")

st.markdown("""
### Bienvenido al Sistema de Inteligencia Territorial Encuesta Diciembre 2025

Selecciona un módulo en el menú lateral para comenzar:

---

#### 🗺️ 1. Planeación y Asignación
* **Objetivo:** Visualización estratégica de secciones y cargas de trabajo.
* **Funcionalidades:** * Mapa de secciones balanceado.
    * Filtro operativo por supervisor.
    * Descarga de rutas y mapas (Manzanas INEGI).

#### 📊 2. Monitoreo y Auditoría 
* **Objetivo:** Seguimiento en tiempo real del levantamiento de campo.
* **Funcionalidades:**
    * Auditoría de coordenadas GPS (Geo-Fencing).
    * Barras de avance vs Meta.
    * Productividad por encuestador.
    * Secciones críticas

---
*v2.0 - Sprint 2* Data & AI Inclusion Tech
""")

# Sidebar informativo
with st.sidebar:
    st.info("Selecciona una página arriba 👆")