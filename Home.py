import streamlit as st
from src.auth import bloquear_acceso

# Configuración de página principal
st.set_page_config(
    page_title="Sistema Electoral - Guerrero",
    page_icon="🗳️",
    layout="centered"
)

# --- AUTENTICACIÓN CENTRALIZADA ---
# Si el usuario no está logueado, esto detiene la ejecución aquí mismo.
if bloquear_acceso():
    
    # --- UI DEL HOME ---
    st.title("🗳️ Sistema de Inteligencia Electoral")
    st.markdown("### Estado de Guerrero 2024-2025")
    st.markdown("---")

    st.info("📢 **ESTATUS ACTUAL:** Fase de Cierre y Validación de Datos.")

    # --- MENÚ DE MÓDULOS ---
    
    # 1. MONITOREO (Fase Operativa)
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("# 📊")
        with col2:
            st.subheader("Monitoreo en Tiempo Real")
            st.write("Supervisión de levantamiento, cobertura territorial y alertas.")
            # Ajusta el nombre del archivo si es distinto (ej. 1_Monitoreo.py)
            st.page_link("pages/1_📊_Monitoreo.py", label="Ir al Tablero", icon="▶️")

    # 2. PLANEACIÓN (Fase Logística)
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("# 🗺️")
        with col2:
            st.subheader("Planeación Logística")
            st.write("Mapas de asignación, clusters y rutas de supervisión.")
            # Ajusta el nombre del archivo si es distinto
            st.page_link("pages/2_🗺️_Planeacion.py", label="Ver Mapas", icon="▶️")

    # 3. AUDITORÍA (Fase de Calidad - ¡NUEVO!)
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("# 🔍")
        with col2:
            st.subheader("Auditoría y Estandarización")
            st.markdown("**¡NUEVO MÓDULO!**")
            st.write("Limpieza de datos, validación GPS, renombrado de variables y descarga de Base Maestra.")
            st.page_link("pages/3_🔍_Auditoria.py", label="Auditar Datos", icon="✨")

    st.markdown("---")
    st.caption("Developed for Strategic Intelligence • v2.0 (Cierre)")