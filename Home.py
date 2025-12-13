import streamlit as st

# Configuración de página principal
st.set_page_config(
    page_title="Sistema Electoral - Guerrero",
    page_icon="🗳️",
    layout="centered"
)

# CSS personalizado para mejorar la estética
st.markdown("""
<style>
    /* Mejora el aspecto de los contenedores */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        gap: 1rem;
    }
    
    /* Mejora el espaciado general */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Estilo para los badges de estado */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Mejora las cards de navegación */
    .nav-card {
        transition: transform 0.2s;
    }
    
    .nav-card:hover {
        transform: translateX(5px);
    }
</style>
""", unsafe_allow_html=True)

# --- ENCABEZADO MEJORADO ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🗳️ Sistema de Inteligencia Electoral")
    st.markdown("### Estado de Guerrero | Cierre 2025")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.metric("Fase", "Final", delta="100%")

st.markdown("---")

# --- NOTIFICACIÓN DE ESTATUS CON MEJOR VISIBILIDAD ---
st.success("✅ **PROYECTO CONCLUIDO** • Los resultados finales están disponibles para consulta")

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 1. MÓDULO PÚBLICO (RESULTADOS) - DESTACADO Y MEJORADO
# ==============================================================================
st.markdown("### 🏆 Entregable Ejecutivo")

with st.container(border=True):
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
            <h2 style='margin: 0; color: white;'>📈 Tablero de Resultados 2025</h2>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;'>
                Visualización interactiva completa
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**✓** Comparativo Jun-Dic")
    with col2:
        st.markdown("**✓** Análisis de Atributos")
    with col3:
        st.markdown("**✓** Escenarios Careos")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        st.page_link(
            "pages/4_📈_Resultados.py", 
            label="🚀 ACCEDER AL TABLERO FINAL",
            use_container_width=True
        )

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# ==============================================================================
# 2. MÓDULOS TÉCNICOS (PROCESO) - CON EXPANSOR OPCIONAL
# ==============================================================================
with st.expander("🛠️ **Documentación Metodológica** (Respaldo del Proceso)", expanded=False):
    st.caption("Consulta las fases técnicas del proyecto")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Card 1: Planeación
    with st.container(border=True):
        col_icon, col_content, col_action = st.columns([1, 6, 2])
        with col_icon:
            st.markdown("### 🗺️")
        with col_content:
            st.markdown("**1. Planeación Logística**")
            st.caption("Diseño muestral, cartografía digital y rutas de levantamiento")
        with col_action:
            st.page_link("pages/1_🗺️_Planeacion.py", label="Ver ▶️")
    
    # Card 2: Monitoreo
    with st.container(border=True):
        col_icon, col_content, col_action = st.columns([1, 6, 2])
        with col_icon:
            st.markdown("### 📊")
        with col_content:
            st.markdown("**2. Monitoreo en Campo**")
            st.caption("Supervisión en tiempo real del levantamiento y cobertura GPS")
        with col_action:
            st.page_link("pages/2_📊_Monitoreo.py", label="Ver ▶️")
    
    # Card 3: Auditoría
    with st.container(border=True):
        col_icon, col_content, col_action = st.columns([1, 6, 2])
        with col_icon:
            st.markdown("### 🔍")
        with col_content:
            st.markdown("**3. Auditoría de Datos**")
            st.caption("Validación, limpieza de base de datos y control de calidad")
        with col_action:
            st.page_link("pages/3_🔍_Auditoria.py", label="Ver ▶️")

# --- PIE DE PÁGINA MEJORADO ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col_footer1, col_footer2 = st.columns([3, 1])
with col_footer1:
    st.caption("🔒 Sistema de Inteligencia Estratégica • Versión Final 2.0")
with col_footer2:
    st.caption("📅 Diciembre 2025")