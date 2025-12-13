import streamlit as st

# Configuración de página principal
st.set_page_config(
    page_title="Inteligencia Electoral Guerrero",
    page_icon="🗳️",
    layout="centered"
)

# --- CABECERA DE CIERRE ---
st.title("🗳️ Sistema de Inteligencia Electoral")
st.markdown("### Estado de Guerrero | Cierre 2025")
st.divider()

# --- MENSAJE PRINCIPAL ---
st.success("✅ **REPORTE FINAL DISPONIBLE**")
st.markdown("""
El ciclo de evaluación estratégica ha concluido. Los datos procesados incluyen:
* Encuesta de Cierre (Diciembre 2025).
* Comparativo Evolutivo (Junio vs. Diciembre).
* Modelaje de Escenarios Constitucionales.
""")

# --- ACCESO DIRECTO AL MÓDULO PÚBLICO ---
with st.container(border=True):
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2921/2921222.png", width=60) # Icono genérico de gráfica
    with col2:
        st.subheader("Consultar Resultados Finales")
        st.write("Acceso directo al tablero ejecutivo, comparativos y descarga de bases de datos.")
        
        # Botón grande
        st.page_link("pages/4_📈_Resultados.py", label="Ver Tablero de Resultados 2025", icon="🚀")

st.markdown("---")

# --- ACCESO A MÓDULOS INTERNOS (OPCIONAL/RESTRINGIDO) ---
st.caption("Módulos técnicos (Requieren credenciales):")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.page_link("pages/1_🗺️_Planeacion.py", label="Planeación", icon="🔒")
with col_b:
    st.page_link("pages/2_📊_Monitoreo.py", label="Monitoreo", icon="🔒")
with col_c:
    st.page_link("pages/3_🔍_Auditoria.py", label="Auditoría", icon="🔒")

st.markdown("---")
st.caption("Sistema de Inteligencia Estratégica • Versión de Cierre 2.0")