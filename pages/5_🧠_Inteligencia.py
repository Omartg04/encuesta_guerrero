import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.auth import bloquear_acceso

# Configuración de página
st.set_page_config(page_title="Inteligencia Electoral", layout="wide")
bloquear_acceso()

# ==============================================================================
# 🛠️ GENERADOR DE DATOS SIMULADOS (ENRIQUECIDO)
# ==============================================================================
@st.cache_data
def generar_data_mockup():
    """Genera datos de inteligencia territorial con perfil sociodemográfico"""
    np.random.seed(42)
    n = 150
    
    data = {
        "Seccion": [f"SE-{1000+i}" for i in range(n)],
        "Lat": np.random.normal(18.3448, 0.02, n),
        "Lon": np.random.normal(-99.5397, 0.02, n),
        "Ganador_Historico": np.random.choice(["MORENA", "PRI", "PRD", "PAN"], n, p=[0.45, 0.30, 0.15, 0.10]),
        "Participacion": np.random.uniform(35, 75, n).round(1),
        "Margen_Victoria": np.random.uniform(0.5, 25, n).round(1),
        "Nivel_Digitalizacion": np.random.choice(["Alto", "Medio", "Bajo"], n, p=[0.2, 0.5, 0.3]),
        "Poblacion_Joven": np.random.uniform(15, 40, n).round(1), # % 18-29 años
        "Poblacion_AdultoMayor": np.random.uniform(10, 30, n).round(1), # % 60+
        "NSE_Predominante": np.random.choice(["C+ (Medio Alto)", "C (Medio)", "D+ (Bajo Alto)", "D (Bajo)"], n),
        "Problema_Principal": np.random.choice(["Inseguridad", "Agua Potable", "Alumbrado", "Bacheo", "Desempleo"], n),
        "Voto_Duro_Morena": np.random.uniform(100, 500, n).astype(int),
        "Celulares_Registrados": np.random.randint(50, 400, n), # Dato para el CRM
        "Emails_Registrados": np.random.randint(20, 150, n)     # Dato para el CRM
    }
    
    df = pd.DataFrame(data)
    
    # Lógica de Clasificación Estratégica
    conditions = [
        (df['Margen_Victoria'] < 5),
        (df['Ganador_Historico'] == 'MORENA') & (df['Margen_Victoria'] > 10),
        (df['Ganador_Historico'] != 'MORENA') & (df['Margen_Victoria'] > 10)
    ]
    choices = ['Swing (Competida)', 'Bastión Propio', 'Bastión Opositor']
    df['Estrategia'] = np.select(conditions, choices, default='En Disputa')
    
    return df

df_secciones = generar_data_mockup()

# ==============================================================================
# 🎨 INTERFAZ PRINCIPAL CON NARRATIVA EDUCATIVA
# ==============================================================================

st.title("🧠 Inteligencia Territorial + Comunicación Digital")
st.markdown("""
**¿Para qué sirve este módulo?** Transforma datos geográficos, sociodemográficos y electorales en acciones de campaña. Permite identificar **dónde** están los votos decisivos, valida la información recabada en territorio como correos y celulares, conecta directamente vía SMS-Correo para enviar el mensaje correcto **a la persona correcta**.
""")

# --- KPI PANEL SUPERIOR ---
col1, col2, col3, col4 = st.columns(4)

# Swing
swing_count = len(df_secciones[df_secciones["Estrategia"] == "Swing (Competida)"])
col1.metric(
    "⚔️ Secciones Swing o Competidas", 
    f"{swing_count}", 
    "Definen la elección",
    help="💡 Valor Estratégico: Son zonas donde la diferencia es menor al 5% o cambian su intención de voto. Aquí concentra el esfuerzo territorial para crear mensajes ultra-segmentados."
)

# Voto Duro
col2.metric(
    "🎯 Base de Contactos", 
    f"{df_secciones['Celulares_Registrados'].sum():,.0f}", 
    "Celulares en CRM",
    help="💡 Valor Estratégico: Total de números telefónicos válidos listos para recibir SMS en esta zona."
)

# Abstencionismo
col3.metric(
    "📉 Abstencionismo Promedio", 
    f"{100 - df_secciones['Participacion'].mean():.1f}%", 
    "Mercado Potencial",
    help="💡 Valor Estratégico: Zonas con baja participación son ideales para campañas de 'Movilización' (sacar a votar) en lugar de persuasión."
)

# Digitalización
col4.metric(
    "📡 Cobertura Digital Alta", 
    f"{len(df_secciones[df_secciones['Nivel_Digitalizacion']=='Alto'])} Secciones", 
    "Campaña Aire",
    help="💡 Valor Estratégico: Zonas donde la inversión en Pauta Digital (Meta/Google) tiene el retorno de inversión más alto."
)

st.divider()

# ==============================================================================
# 🗺️ VISOR TERRITORIAL (IZQUIERDA) Y PERFILADOR (DERECHA)
# ==============================================================================

col_mapa, col_perfil = st.columns([1.6, 1])

with col_mapa:
    st.subheader("1. Identificación Territorial")
    st.info("💡 **Uso:** Filtra el mapa para encontrar 'secciones' de oportunidad. Por ejemplo, busca zonas 'Swing' con 'Inseguridad' como problema principal.")
    
    c_filt1, c_filt2 = st.columns(2)
    with c_filt1:
        filtro_capa = st.selectbox("Capa de Análisis:", ["Estrategia (Competitividad)", "Nivel Socioeconómico", "Problema Principal", "Participación"])
    with c_filt2:
        # Filtro rápido para limpiar mapa
        ver_solo_swing = st.checkbox("Ver solo Zonas Swing (Prioridad)", value=False)

    # Lógica de filtrado visual
    df_view = df_secciones.copy()
    if ver_solo_swing:
        df_view = df_view[df_view["Estrategia"] == "Swing (Competida)"]

    # Configuración dinámica de colores
    if filtro_capa == "Estrategia (Competitividad)":
        color_col = "Estrategia"
        colors = {"Bastión Propio": "#2ECC71", "Bastión Opositor": "#E74C3C", "Swing (Competida)": "#F1C40F", "En Disputa": "#BDC3C7"}
    elif filtro_capa == "Problema Principal":
        color_col = "Problema_Principal"
        colors = px.colors.qualitative.Plotly
    elif filtro_capa == "Nivel Socioeconómico":
        color_col = "NSE_Predominante"
        colors = {"C+ (Medio Alto)": "#3498DB", "C (Medio)": "#9B59B6", "D+ (Bajo Alto)": "#E67E22", "D (Bajo)": "#E74C3C"}
    else:
        color_col = "Participacion"
        colors = "inferno"

    fig_map = px.scatter_mapbox(
        df_view, lat="Lat", lon="Lon", color=color_col, size="Voto_Duro_Morena",
        # 🛠️ CORRECCIÓN AQUÍ: Usamos "Problema_Principal" con guion bajo
        hover_name="Seccion", hover_data=["Margen_Victoria", "Participacion", "Problema_Principal"],
        color_discrete_map=colors if isinstance(colors, dict) else None,
        color_continuous_scale=colors if isinstance(colors, str) else None,
        zoom=11.5, height=600
    )
    fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with col_perfil:
    st.subheader("2. Micro-Targeting y Acción")
    
    # Simulación de selección
    secciones_clave = df_secciones[df_secciones["Estrategia"] == "Swing (Competida)"]["Seccion"].tolist()
    seccion_sel = st.selectbox("🔍 Seleccionar Sección (Simulación Clic):", secciones_clave)
    
    # Obtener datos de la sección seleccionada
    data_sec = df_secciones[df_secciones["Seccion"] == seccion_sel].iloc[0]
    
    # --- FICHA TÁCTICA ---
    with st.container(border=True):
        st.markdown(f"#### 📍 Ficha Técnica: {seccion_sel}")
        st.caption("Resumen estratégico para toma de decisiones.")
        
        # Etiquetas
        st.markdown(f"**Dolor Principal:** :red[{data_sec['Problema_Principal']}]")
        
        # Demografía
        df_demo = pd.DataFrame({
            "Grupo": ["Jóvenes", "Adultos Mayores", "Resto"],
            "Porcentaje": [data_sec["Poblacion_Joven"], data_sec["Poblacion_AdultoMayor"], 100-(data_sec["Poblacion_Joven"]+data_sec["Poblacion_AdultoMayor"])]
        })
        fig_pie = px.pie(df_demo, values="Porcentaje", names="Grupo", hole=0.6, height=120)
        fig_pie.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        
        # --- MÓDULO DE INTEGRACIÓN CRM (NUEVO) ---
        st.markdown("#### 🔌 Integración Módulo Comunicación")
        st.info("💡 **Utilidad:** Identifica segmentos directamente desde aquí para usar la Plataforma de envíos, usando la base de datos filtrada por esta sección.")
        
        # Métricas de audiencia disponible
        c_sms, c_email = st.columns(2)
        c_sms.metric("📱 Móviles", f"{data_sec['Celulares_Registrados']}", help="Contactos con celular válido en esta sección")
        c_email.metric("📧 Correos", f"{data_sec['Emails_Registrados']}", help="Correos válidos en esta sección")
        
        # Formulario de Acción
        with st.form("crm_action"):
            st.write("**Configurar Campaña Saliente:**")
            
            # Selección inteligente de mensaje basado en el problema
            plantilla_sugerida = f"Propuesta: Solución a {data_sec['Problema_Principal']}"
            tipo_mensaje = st.selectbox("Plantilla de Mensaje:", [plantilla_sugerida, "Invitación a Mitin", "Ataque/Contraste", "Movilización (Día D)"])
            
            canal = st.radio("Canal de Envío:", ["SMS Masivo", "Email Newsletter", "WhatsApp (Bot)"], horizontal=True)
            
            submitted = st.form_submit_button(f"🚀 Disparar Campaña a {seccion_sel}", use_container_width=True)
            
            if submitted:
                st.toast(f"Conectando con API CRM...", icon="🔄")
                # Simulación de delay
                import time
                time.sleep(1)
                st.success(f"✅ ¡Éxito! Se enviaron {data_sec['Celulares_Registrados']} mensajes vía {canal} usando la plantilla: '{tipo_mensaje}'.")
                st.caption("ID Transacción CRM: #CRM-8823-XYZ")

# ==============================================================================
# 📋 TABLA DETALLADA CON TOOLTIPS
# ==============================================================================
st.markdown("---")
st.subheader("📂 Padrón de Secciones Prioritarias")
with st.expander("Ver detalle de datos y exportar"):
    st.markdown("""
    **Guía de Columnas:**
    * **Margen:** Diferencia porcentual entre 1er y 2do lugar. Menor a 5% es crítico.
    * **NSE:** Nivel Socioeconómico predominante (determina el lenguaje de la campaña).
    * **Digitalización:** Probabilidad de que el mensaje llegue vía redes sociales.
    """)
    st.dataframe(
        df_secciones.sort_values("Margen_Victoria"),
        column_config={
            "Participacion": st.column_config.ProgressColumn("Participación", format="%.1f%%", min_value=0, max_value=100),
            "Estrategia": st.column_config.TextColumn("Clasificación"),
            "Voto_Duro_Morena": st.column_config.NumberColumn("Voto Duro", help="Votos seguros estimados basados en elecciones pasadas"),
        },
        use_container_width=True
    )