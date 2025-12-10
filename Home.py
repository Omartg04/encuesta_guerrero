import streamlit as st
from src.auth import bloquear_acceso

# Configuración de página principal
st.set_page_config(
    page_title="Sistema Electoral - Guerrero",
    page_icon="🗳️",
    layout="centered"
)

# --- AUTENTICACIÓN CENTRALIZADA ---
if bloquear_acceso():
    
    # --- UI DEL HOME ---
    st.title("🗳️ Sistema de Inteligencia Electoral")
    st.markdown("### Estado de Guerrero 2024-2025")
    st.markdown("---")

    st.info("📢 **ESTATUS ACTUAL:** Fase de Cierre y Validación de Datos.")

    # --- MENÚ DE MÓDULOS ---
    
    # 1. MONITOREO (Ahora apunta a tu archivo 2_📊_Monitoreo.py)
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("# 📊")
        with col2:
            st.subheader("Monitoreo en Tiempo Real")
            st.write("Supervisión de levantamiento, cobertura territorial y alertas.")
            # CORREGIDO: Apunta al archivo 2
            st.page_link("pages/2_📊_Monitoreo.py", label="Ir al Tablero", icon="▶️")

    # 2. PLANEACIÓN (Ahora apunta a tu archivo 1_🗺️_Planeacion.py)
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("# 🗺️")
        with col2:
            st.subheader("Planeación Logística")
            st.write("Mapas de asignación, clusters y rutas de supervisión.")
            # CORREGIDO: Apunta al archivo 1
            st.page_link("pages/1_🗺️_Planeacion.py", label="Ver Mapas", icon="▶️")

    # 3. AUDITORÍA (Apunta a tu archivo 3_🔍_Auditoria.py)
    with st.container(border=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("# 🔍")
        with col2:
            st.subheader("Auditoría y Estandarización")
            st.markdown("**¡NUEVO MÓDULO!**")
            st.write("Limpieza de datos, validación GPS y descarga de Base Maestra.")
            # CORREGIDO: Apunta al archivo 3
            st.page_link("pages/3_🔍_Auditoria.py", label="Auditar Datos", icon="✨")

    st.markdown("---")
    st.caption("Developed for Strategic Intelligence • v2.0 (Cierre)")