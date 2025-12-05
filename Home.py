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
### Bienvenido al Sistema de Inteligencia Territorial

Selecciona un módulo en el menú lateral para comenzar:

---

#### 🗺️ 1. Planeación y Asignación
* **Objetivo:** Visualización estratégica de secciones y cargas de trabajo.
* **Funcionalidades:** * Mapa de secciones balanceado.
    * Filtro operativo por supervisor.
    * Descarga de rutas y mapas (Manzanas INEGI).

#### 📊 2. Monitoreo y Auditoría (En Construcción)
* **Objetivo:** Seguimiento en tiempo real del levantamiento de campo.
* **Funcionalidades (Próximamente):**
    * Auditoría de coordenadas GPS (Geo-Fencing).
    * Barras de avance vs Meta.
    * Productividad por encuestador.

---
*v1.0 - Sprint 2*
""")

# Sidebar informativo
with st.sidebar:
    st.info("Selecciona una página arriba 👆")