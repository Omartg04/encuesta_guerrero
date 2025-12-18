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
    
    /* Efecto hover suave en botones */
    div.stButton > button:first-child {
        transition: transform 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.02);
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

# --- NOTIFICACIÓN DE ESTATUS ---
st.success("✅ **PROYECTO CONCLUIDO** • Los resultados finales están disponibles para consulta")

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 1. MÓDULO PÚBLICO (RESULTADOS) - DESTACADO
# ==============================================================================
st.markdown("### 🏆 Entregable Ejecutivo")

with st.container(border=True):
    # Banner Azul/Morado para Resultados
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; color: white; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h2 style='margin: 0; color: white;'>📈 Tablero de Resultados 2025</h2>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.95; font-size: 1.1rem;'>
                Visualización interactiva, comparativos históricos y careos.
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

# ==============================================================================
# 🚀 PROPUESTA DE EVOLUCIÓN (NUEVO MÓDULO INTELIGENCIA)
# ==============================================================================
st.divider()
st.markdown("### 🚀 Propuesta para Desarrollar (Fase 2)")

with st.container(border=True):
    # Banner Oscuro/Cian para Tecnología/Futuro
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem; position: relative; overflow: hidden;'>
            <div style='position: relative; z-index: 2;'>
                <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;'>
                    <h2 style='margin: 0; color: white; font-size: 1.5rem;'>🧠 Inteligencia Territorial & Comunicación</h2>
                    <span style='background-color: #FFD700; color: #000; padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.5px;'>PROPUESTA ADICIONAL</span>
                </div>
                <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1rem; font-style: italic;'>
                    "De la medición a la movilización: Micro-targeting activable."
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c_prop1, c_prop2 = st.columns([1.2, 1])
    
    with c_prop1:
        st.info("**Objetivo:** Transformar los datos en operaciones de tierra y de comunicación digital quirúrgicas. Este módulo permitiría perfilar secciones críticas y **conectar directamente vía SMS o Correo con el directorio de contactos recopilado en territorio**.")
        st.caption("Ideal para: Campaña de Aire y Elevar Reconocimiento.")
    
    with c_prop2:
        st.markdown("""
        **Capacidades del Demo:**
        * 🗺️ **Mapa de secciones estratégicas** (Swing/Bastiones)
        * 👤 **Perfil por sección** Sociodemográfico
        * 🔌 **Directorio de Celulares y Correos válidos** 
        * 🤖 **Alertas** Estratégicas
        """)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("✨ EXPLORAR DEMO INTERACTIVO", use_container_width=True, type="secondary"):
         st.switch_page("pages/5_🧠_Inteligencia.py")

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 3. MÓDULOS TÉCNICOS (RESPALDO)
# ==============================================================================
with st.expander("🛠️ **Documentación Metodológica** (Respaldo del Proceso)", expanded=False):
    st.caption("Consulta las fases técnicas y auditoría de datos del proyecto actual.")
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

# --- PIE DE PÁGINA ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col_footer1, col_footer2 = st.columns([3, 1])
with col_footer1:
    st.caption("🔒 Sistema de Inteligencia Estratégica • Versión Final 2.0 • Data & AI Inclusion Tech")
with col_footer2:
    st.caption("📅 Diciembre 2025")