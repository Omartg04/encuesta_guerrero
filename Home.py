import streamlit as st

# Configuración de página principal
st.set_page_config(
    page_title="Sistema Electoral - Guerrero",
    page_icon="🗳️",
    layout="centered"
)

# --- ENCABEZADO ---
st.title("🗳️ Sistema de Inteligencia Electoral")
st.markdown("### Estado de Guerrero | Cierre 2025")
st.markdown("---")

# --- NOTIFICACIÓN DE ESTATUS ---
st.success("✅ **PROYECTO CONCLUIDO:** Los resultados finales ya están disponibles para su consulta.")

# ==============================================================================
# 1. MÓDULO PÚBLICO (RESULTADOS) - DESTACADO
# ==============================================================================
st.markdown("#### 🏆 Fase Final: Entregable Ejecutivo")

with st.container(border=True):
    col_icon, col_text = st.columns([1, 5])
    
    with col_icon:
        st.markdown("# 📈") 
    
    with col_text:
        st.subheader("Tablero de Resultados 2025")
        st.write(
            "Visualización interactiva de la encuesta de cierre. Incluye comparativos "
            "**Junio vs. Diciembre**, análisis de atributos, escenarios constitucionales (Careos) "
            "y descarga de reportes."
        )
        st.page_link("pages/4_📈_Resultados.py", label="Ir al Tablero Final", icon="🚀")

st.divider()

# ==============================================================================
# 2. MÓDULOS TÉCNICOS (PROCESO)
# ==============================================================================
st.markdown("#### 🛠️ Respaldo Metodológico (Proceso)")

# Card 1: Planeación
with st.container(border=True):
    c1, c2 = st.columns([1, 5])
    with c1:
        st.markdown("### 🗺️")
    with c2:
        st.markdown("**1. Planeación Logística**")
        st.caption("Diseño muestral, cartografía digital y asignación de rutas de levantamiento.")
        st.page_link("pages/1_🗺️_Planeacion.py", label="Ver Mapas", icon="▶️")

# Card 2: Monitoreo
with st.container(border=True):
    c1, c2 = st.columns([1, 5])
    with c1:
        st.markdown("### 📊")
    with c2:
        st.markdown("**2. Monitoreo en Campo**")
        st.caption("Supervisión en tiempo real del levantamiento de encuestas y cobertura GPS.")
        st.page_link("pages/2_📊_Monitoreo.py", label="Ver Avance", icon="▶️")

# Card 3: Auditoría
with st.container(border=True):
    c1, c2 = st.columns([1, 5])
    with c1:
        st.markdown("### 🔍")
    with c2:
        st.markdown("**3. Auditoría de Datos**")
        st.caption("Procesos de validación, limpieza de base de datos y control de calidad.")
        st.page_link("pages/3_🔍_Auditoria.py", label="Ver Auditoría", icon="▶️")

st.markdown("---")
st.caption("Sistema de Inteligencia Estratégica • Versión Final 2.0 (Producción)")