import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Resultados Finales 2025", 
    layout="wide",
    page_icon="📊"
)

# CSS PERSONALIZADO PARA MEJORAR LA ESTÉTICA
st.markdown("""
<style>
    /* Mejor espaciado general */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Mejora las tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    /* Mejora las métricas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Cards con sombra */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* Mejora el sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Headers con estilo */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🗄️ BASE DE DATOS [MANTIENE TUS DATOS ORIGINALES]
# ==============================================================================

DATOS_PROBLEMAS = {
    "GUERRERO (ESTATAL)": {"Inseguridad": [47.0, 63.9], "Falta de agua": [4.0, 8.4], "Corrupción": [6.0, 6.2], "Calles mal estado": [1.0, 4.0], "Bajos Salarios": [1.0, 2.9]},
    "ACAPULCO": {"Inseguridad": [56.0, 62.2], "Falta de agua": [4.0, 11.0], "Corrupción": [3.0, 7.3]},
    "CHILPANCINGO": {"Inseguridad": [61.0, 76.2], "Falta de agua": [3.0, 4.0], "Corrupción": [2.0, 3.8]},
    "IGUALA": {"Inseguridad": [59.0, 49.6], "Economía": [4.0, 8.5], "Calles mal estado": [1.0, 6.0]}
}

DATOS_VOTO_GOB = {
    "GUERRERO (ESTATAL)": {"MORENA": [48.0, 59.9], "PRI": [16.0, 3.8], "MC": [7.0, 2.5], "PAN": [3.0, 1.6], "PT": [2.0, 1.3], "Ninguno": [10.0, 16.1]},
    "ACAPULCO": {"MORENA": [48.0, 64.7], "PRI": [10.0, 3.4], "MC": [10.0, 2.6], "Ninguno": [11.0, 14.4]},
    "CHILPANCINGO": {"MORENA": [34.0, 46.3], "PRI": [15.0, 5.8], "Ninguno": [19.0, 22.9]},
    "IGUALA": {"MORENA": [41.0, 61.0], "PRI": [16.0, 2.2], "Ninguno": [10.0, 12.2]}
}

DATOS_CONOCIMIENTO = {
    "GUERRERO (ESTATAL)": {"Félix Salgado": [73.0, 73.4], "Abelina López": [48.0, 68.1], "Beatriz Mojica": [44.0, 56.0], "Javier Saldaña": [0.0, 44.9], "Iván Hernández": [8.0, 38.9], "Jacinto Gonzalez": [11.0, 24.6], "Pablo Amílcar": [21.0, 21.0], "Esthela Damián": [7.0, 20.9]},
    "ACAPULCO": {"Abelina López": [89.0, 84.8], "Félix Salgado": [86.0, 74.6], "Iván Hernández": [12.0, 40.5]},
    "CHILPANCINGO": {"Félix Salgado": [83.0, 76.1], "Abelina López": [54.0, 49.2], "Iván Hernández": [17.0, 35.7]},
    "IGUALA": {"Félix Salgado": [86.0, 61.0], "Iván Hernández": [6.0, 36.8], "Abelina López": [37.0, 15.4]}
}

DATOS_HEATMAP_DIC = [
    {"Aspirante": "Iván Hernández", "Honestidad": 33.6, "Cercanía": 35.3, "Der. Mujeres": 37.8, "Conoce Edo": 43.3, "Cumple": 31.9, "Buen Candidato": 65.5},
    {"Aspirante": "Esthela Damián", "Honestidad": 25.5, "Cercanía": 20.1, "Der. Mujeres": 29.5, "Conoce Edo": 21.2, "Cumple": 20.5, "Buen Candidato": 48.3},
    {"Aspirante": "Jacinto González", "Honestidad": 20.1, "Cercanía": 21.7, "Der. Mujeres": 24.0, "Conoce Edo": 27.9, "Cumple": 18.1, "Buen Candidato": 41.2},
    {"Aspirante": "Beatriz Mojica", "Honestidad": 10.1, "Cercanía": 11.3, "Der. Mujeres": 20.8, "Conoce Edo": 21.2, "Cumple": 7.9, "Buen Candidato": 38.5},
    {"Aspirante": "Javier Saldaña", "Honestidad": 7.0, "Cercanía": 11.2, "Der. Mujeres": 7.6, "Conoce Edo": 21.5, "Cumple": 6.1, "Buen Candidato": 25.1},
    {"Aspirante": "Félix Salgado", "Honestidad": 6.9, "Cercanía": 15.6, "Der. Mujeres": 6.8, "Conoce Edo": 34.3, "Cumple": 7.7, "Buen Candidato": 21.9},
    {"Aspirante": "Pablo Amílcar", "Honestidad": 6.2, "Cercanía": 5.1, "Der. Mujeres": 5.0, "Conoce Edo": 9.4, "Cumple": 1.9, "Buen Candidato": 18.8},
    {"Aspirante": "Abelina López", "Honestidad": 9.6, "Cercanía": 14.9, "Der. Mujeres": 14.8, "Conoce Edo": 17.1, "Cumple": 8.8, "Buen Candidato": 14.0}
]

DATOS_RADAR_EVO = {
    "Iván Hernández": {"Honestidad": [1.7, 33.6], "Der. Mujeres": [2.1, 37.8], "Cercanía": [2.1, 35.3], "Conoce Edo": [2.5, 43.3], "Cumple": [1.4, 31.9]},
    "Félix Salgado": {"Honestidad": [14.3, 6.9], "Der. Mujeres": [15.2, 6.8], "Cercanía": [23.3, 15.6], "Conoce Edo": [41.1, 34.3], "Cumple": [14.3, 7.7]}
}

DATOS_PREFERENCIA_EVOLUCION = [
    {"Aspirante": "Iván Hernández", "Junio": 4.3, "Dic": 21.5},
    {"Aspirante": "Félix Salgado", "Junio": 19.8, "Dic": 9.3},
    {"Aspirante": "Beatriz Mojica", "Junio": 18.4, "Dic": 10.0},
    {"Aspirante": "Abelina López", "Junio": 5.7, "Dic": 5.8},
    {"Aspirante": "Pablo Amílcar", "Junio": 6.0, "Dic": 1.8},
    {"Aspirante": "Esthela Damián", "Junio": 4.7, "Dic": 6.9}
]

DATOS_INTERNA_TODOS = {
    "GUERRERO (ESTATAL)": {"Iván Hernández": 21.5, "Beatriz Mojica": 10.0, "Félix Salgado": 9.3, "Esthela Damián": 6.9, "Abelina López": 5.8, "Javier Saldaña": 5.2, "Jacinto González": 4.9, "Pablo Amílcar": 1.8, "Ninguno": 16.0},
    "ACAPULCO": {"Iván Hernández": 22.5, "Beatriz Mojica": 12.0, "Félix Salgado": 9.5, "Abelina López": 8.7, "Esthela Damián": 6.5, "Ninguno": 14.9},
    "CHILPANCINGO": {"Iván Hernández": 18.3, "Félix Salgado": 8.7, "Beatriz Mojica": 6.5, "Esthela Damián": 4.7, "Abelina López": 0.3, "Ninguno": 19.2},
    "IGUALA": {"Iván Hernández": 22.5, "Esthela Damián": 12.8, "Félix Salgado": 9.0, "Beatriz Mojica": 6.4, "Ninguno": 15.2}
}

DATOS_CAREOS_CONST = {
    "GUERRERO (ESTATAL)": {
        "Careo 1 (Félix)": {"MORENA (Félix)": 22.9, "PRI (Añorve)": 2.5, "MC (Julián)": 2.9, "PT": 4.2, "Ninguno": 33.9},
        "Careo 2 (Iván)":  {"MORENA (Iván)": 34.5, "PRI (Añorve)": 2.6, "MC (Julián)": 1.8, "PT": 3.7, "Ninguno": 25.8}
    },
    "ACAPULCO": {
        "Careo 1 (Félix)": {"MORENA (Félix)": 25.8, "Ninguno": 35.7},
        "Careo 2 (Iván)":  {"MORENA (Iván)": 37.9, "Ninguno": 27.1}
    }
}

# ==============================================================================
# 🛠️ FUNCIONES AUXILIARES
# ==============================================================================
def generar_excel_completo():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pd.DataFrame(DATOS_INTERNA_TODOS["GUERRERO (ESTATAL)"].items(), columns=["Candidato", "%"]).to_excel(writer, sheet_name='Interna', index=False)
        pd.DataFrame(DATOS_HEATMAP_DIC).to_excel(writer, sheet_name='Atributos_Heatmap', index=False)
    return output.getvalue()

# ==============================================================================
# 🚀 APP PRINCIPAL
# ==============================================================================
def main():
    # --- HEADER MEJORADO ---
    st.markdown("""
        <div class='header-container'>
            <h1 style='margin: 0; color: white;'>📊 Resultados Finales: Guerrero 2025</h1>
            <p style='margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.95;'>
                Tablero de Control Estratégico | Análisis Comparativo Jun-Dic
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- SIDEBAR MEJORADO ---
    with st.sidebar:
        st.markdown("### 📍 Configuración")
        
        seleccion = st.selectbox(
            "Territorio:",
            ["GUERRERO (ESTATAL)", "ACAPULCO", "CHILPANCINGO", "IGUALA"],
            index=0
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Métricas resumen rápido
        with st.container():
            st.markdown("#### 📊 Vista Rápida")
            if seleccion in DATOS_VOTO_GOB:
                morena_dic = DATOS_VOTO_GOB[seleccion].get("MORENA", [0, 0])[1]
                st.metric("MORENA", f"{morena_dic}%", delta="Diciembre")
            
            if seleccion in DATOS_INTERNA_TODOS:
                ivan_pref = DATOS_INTERNA_TODOS[seleccion].get("Iván Hernández", 0)
                st.metric("Iván H. (Interna)", f"{ivan_pref}%")
        
        st.divider()
        
        # Botón de descarga destacado
        st.markdown("#### 💾 Exportar Datos")
        st.download_button(
            "📥 Descargar Excel Completo",
            data=generar_excel_completo(),
            file_name=f"Resultados_Cierre_2025_{seleccion.replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary"
        )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption("🔄 Última actualización: Diciembre 2025")

    # --- TABS CON MEJOR ORGANIZACIÓN ---
    tabs = st.tabs([
        "🚨 Problemas", 
        "🏁 Partidos", 
        "🧠 Conocimiento", 
        "✨ Atributos", 
        "🗳️ Candidato Interno", 
        "🥊 Careos"
    ])

    # ==================== TAB 1: PROBLEMAS ====================
    with tabs[0]:
        st.markdown(f"### 🚨 Agenda Pública: Principales Problemas")
        st.caption(f"Región: **{seleccion}** | Comparativo Junio vs Diciembre")
        
        data_p = DATOS_PROBLEMAS.get(seleccion, {})
        if data_p:
            df_p = pd.DataFrame([{"Problema": k, "Junio": v[0], "Dic": v[1]} for k,v in data_p.items()])
            df_melt_p = df_p.melt(id_vars="Problema", var_name="Mes", value_name="%")
            
            fig_p = px.bar(
                df_melt_p.sort_values("%", ascending=True), 
                x="%", y="Problema", color="Mes", barmode="group", 
                orientation='h', text_auto='.1f',
                color_discrete_map={"Junio": "#90A4AE", "Dic": "#D81B60"},
                height=400
            )
            fig_p.update_traces(textfont_size=12, textposition="outside")
            fig_p.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_p, use_container_width=True)
            
            # Insight automático
            max_prob = df_p.loc[df_p['Dic'].idxmax()]
            with st.expander("💡 Insight Clave"):
                st.info(f"**{max_prob['Problema']}** es el problema más mencionado en Diciembre con **{max_prob['Dic']}%** (cambio desde Junio: {max_prob['Dic'] - max_prob['Junio']:+.1f} pts)")

    # ==================== TAB 2: PARTIDOS ====================
    with tabs[1]:
        st.markdown(f"### 🏁 Preferencias Partidistas (Marca Electoral)")
        st.caption(f"Región: **{seleccion}** | Evolución del Voto")
        
        data_v = DATOS_VOTO_GOB.get(seleccion, {})
        if data_v:
            df_v = pd.DataFrame([{"Partido": k, "Junio": v[0], "Dic": v[1]} for k,v in data_v.items()])
            df_melt = df_v.melt(id_vars="Partido", var_name="Mes", value_name="%")
            
            fig_v = px.bar(
                df_melt, x="%", y="Partido", color="Mes", barmode="group", 
                orientation='h', text_auto='.1f',
                color_discrete_map={"Junio": "#90A4AE", "Dic": "#880E4F"},
                height=450
            )
            fig_v.update_traces(textfont_size=13, textposition="outside")
            fig_v.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_v, use_container_width=True)
            
            # Métricas destacadas
            col1, col2, col3 = st.columns(3)
            morena_jun, morena_dic = data_v.get("MORENA", [0, 0])
            ninguno_jun, ninguno_dic = data_v.get("Ninguno", [0, 0])
            
            with col1:
                st.metric("MORENA (Dic)", f"{morena_dic}%", delta=f"{morena_dic - morena_jun:+.1f} pts")
            with col2:
                st.metric("Ninguno (Dic)", f"{ninguno_dic}%", delta=f"{ninguno_dic - ninguno_jun:+.1f} pts")
            with col3:
                if "PRI" in data_v:
                    pri_jun, pri_dic = data_v["PRI"]
                    st.metric("PRI (Dic)", f"{pri_dic}%", delta=f"{pri_dic - pri_jun:+.1f} pts")

    # ==================== TAB 3: CONOCIMIENTO ====================
    with tabs[2]:
        st.markdown(f"### 🧠 Evolución de Conocimiento (Name ID)")
        st.caption(f"Región: **{seleccion}** | Comparativo de Recordación")
        
        data_c = DATOS_CONOCIMIENTO.get(seleccion, DATOS_CONOCIMIENTO["GUERRERO (ESTATAL)"])
        
        df_c = pd.DataFrame([{"Aspirante": k, "Junio": v[0], "Diciembre": v[1]} for k,v in data_c.items()])
        df_melt_c = df_c.melt(id_vars="Aspirante", var_name="Mes", value_name="%")
        
        order = df_c.sort_values("Diciembre", ascending=True)["Aspirante"].tolist()
        
        fig_bar_c = px.bar(
            df_melt_c, x="%", y="Aspirante", color="Mes", barmode="group", 
            orientation='h', text_auto='.1f',
            category_orders={"Aspirante": order},
            color_discrete_map={"Junio": "#90A4AE", "Diciembre": "#880E4F"},
            height=600
        )
        fig_bar_c.update_traces(textfont_size=12)
        fig_bar_c.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_bar_c, use_container_width=True)
        
        # Top 3 con mayor crecimiento
        df_c['Crecimiento'] = df_c['Diciembre'] - df_c['Junio']
        top3 = df_c.nlargest(3, 'Crecimiento')
        
        st.markdown("##### 📈 Top 3 Mayor Crecimiento")
        cols = st.columns(3)
        for idx, (i, row) in enumerate(top3.iterrows()):
            with cols[idx]:
                st.metric(
                    row['Aspirante'], 
                    f"{row['Diciembre']:.1f}%",
                    delta=f"+{row['Crecimiento']:.1f} pts"
                )

    # ==================== TAB 4: ATRIBUTOS ====================
    with tabs[3]:
        st.markdown("### ✨ Diagnóstico Cualitativo (Estatal)")
        
        # HEATMAP
        st.markdown("#### 🚦 Semáforo de Atributos (Diciembre)")
        st.caption("Intensidad: Verde oscuro = Mayor % Positivo | Todos los aspirantes")
        
        df_heat = pd.DataFrame(DATOS_HEATMAP_DIC).set_index("Aspirante")
        df_heat = df_heat.sort_values("Buen Candidato", ascending=False)
        
        fig_heat = px.imshow(
            df_heat, text_auto='.1f', aspect="auto",
            color_continuous_scale="Greens", origin="lower",
            height=500
        )
        fig_heat.update_xaxes(side="top")
        st.plotly_chart(fig_heat, use_container_width=True)
        
        st.divider()
        
        # RADAR COMPARATIVO
        st.markdown("#### 🕸️ Evolución Estructural: El Contraste (Jun vs Dic)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📈 Crecimiento: Iván Hernández")
            d_ivan = DATOS_RADAR_EVO["Iván Hernández"]
            categories = list(d_ivan.keys())
            
            fig_rad = go.Figure()
            fig_rad.add_trace(go.Scatterpolar(
                r=[v[0] for v in d_ivan.values()], 
                theta=categories, fill='toself', 
                name='Junio', line_color='#B0BEC5', fillcolor='rgba(176, 190, 197, 0.3)'
            ))
            fig_rad.add_trace(go.Scatterpolar(
                r=[v[1] for v in d_ivan.values()], 
                theta=categories, fill='toself', 
                name='Diciembre', line_color='#880E4F', fillcolor='rgba(136, 14, 79, 0.3)'
            ))
            fig_rad.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 50])), 
                showlegend=True, height=450,
                font=dict(size=11)
            )
            st.plotly_chart(fig_rad, use_container_width=True)
            
            # Métrica de mejora promedio
            avg_jun = sum([v[0] for v in d_ivan.values()]) / len(d_ivan)
            avg_dic = sum([v[1] for v in d_ivan.values()]) / len(d_ivan)
            st.metric("Promedio Atributos", f"{avg_dic:.1f}%", delta=f"+{avg_dic - avg_jun:.1f} pts")

        with col2:
            st.markdown("##### 📉 Desgaste: Félix Salgado")
            d_felix = DATOS_RADAR_EVO["Félix Salgado"]
            
            fig_rad2 = go.Figure()
            fig_rad2.add_trace(go.Scatterpolar(
                r=[v[0] for v in d_felix.values()], 
                theta=categories, fill='toself', 
                name='Junio', line_color='#B0BEC5', fillcolor='rgba(176, 190, 197, 0.3)'
            ))
            fig_rad2.add_trace(go.Scatterpolar(
                r=[v[1] for v in d_felix.values()], 
                theta=categories, fill='toself', 
                name='Diciembre', line_color='#C0392B', fillcolor='rgba(192, 57, 43, 0.3)'
            ))
            fig_rad2.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 50])), 
                showlegend=True, height=450,
                font=dict(size=11)
            )
            st.plotly_chart(fig_rad2, use_container_width=True)
            
            # Métrica de caída promedio
            avg_jun_f = sum([v[0] for v in d_felix.values()]) / len(d_felix)
            avg_dic_f = sum([v[1] for v in d_felix.values()]) / len(d_felix)
            st.metric("Promedio Atributos", f"{avg_dic_f:.1f}%", delta=f"{avg_dic_f - avg_jun_f:.1f} pts")

    # ==================== TAB 5: CANDIDATO INTERNO ====================
    with tabs[4]:
        st.markdown(f"### 🗳️ Definición Candidatura: Encuesta Interna")
        st.caption(f"Región: **{seleccion}**")
        
        col_evo, col_foto = st.columns([1, 1])
        
        with col_evo:
            st.markdown("#### 📊 Evolución Preferencia (Estatal)")
            df_evo = pd.DataFrame(DATOS_PREFERENCIA_EVOLUCION).sort_values("Dic", ascending=False)
            
            fig_slope = go.Figure()
            for i, row in df_evo.iterrows():
                if "Iván" in row["Aspirante"]:
                    color, width = "#880E4F", 4
                elif "Félix" in row["Aspirante"]:
                    color, width = "#C0392B", 3
                else:
                    color, width = "#90A4AE", 2
                
                fig_slope.add_trace(go.Scatter(
                    x=["Jun", "Dic"], y=[row["Junio"], row["Dic"]], 
                    mode="lines+markers+text", name=row["Aspirante"],
                    line=dict(color=color, width=width),
                    marker=dict(size=10),
                    text=["", f"{row['Dic']:.1f}%"],
                    textposition="middle right"
                ))
            
            fig_slope.update_layout(
                height=450, showlegend=True,
                legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.05),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=100, t=40, b=20)
            )
            st.plotly_chart(fig_slope, use_container_width=True)

        with col_foto:
            st.markdown(f"#### 📸 Foto Final Diciembre")
            data_int = DATOS_INTERNA_TODOS.get(seleccion, {})
            df_int = pd.DataFrame(list(data_int.items()), columns=["Aspirante", "%"]).sort_values("%", ascending=True)
            
            colors_int = ['#880E4F' if 'Iván' in x else ('#C0392B' if 'Félix' in x else '#90A4AE') for x in df_int['Aspirante']]
            
            fig_int = px.bar(
                df_int, x="%", y="Aspirante", orientation='h', 
                text_auto='.1f', height=450
            )
            fig_int.update_traces(marker_color=colors_int, textfont_size=13, textposition="outside")
            fig_int.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_int, use_container_width=True)
        
        # Destacar al ganador
        ganador = df_int.loc[df_int['%'].idxmax()]
        st.success(f"🏆 **Liderazgo:** {ganador['Aspirante']} con **{ganador['%']:.1f}%** de preferencia")

    # ==================== TAB 6: CAREOS ====================
    with tabs[5]:
        st.markdown("### 🥊 Competitividad Constitucional (Escenarios)")
        st.caption("Simulación de enfrentamientos con partidos de oposición")
        
        data_careos = DATOS_CAREOS_CONST.get(seleccion, DATOS_CAREOS_CONST.get("GUERRERO (ESTATAL)", {}))
        
        if data_careos:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Escenario A: Félix Salgado")
                df_c1 = pd.DataFrame(list(data_careos["Careo 1 (Félix)"].items()), columns=["Partido", "%"])
                
                fig_c1 = px.pie(
                    df_c1, names="Partido", values="%", hole=0.5,
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    height=400
                )
                fig_c1.update_traces(textposition='outside', textinfo='percent+label')
                st.plotly_chart(fig_c1, use_container_width=True)
                
                morena_felix = data_careos['Careo 1 (Félix)'].get('MORENA (Félix)', 0)
                ninguno_felix = data_careos['Careo 1 (Félix)'].get('Ninguno', 0)
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Voto MORENA", f"{morena_felix}%")
                with metric_col2:
                    st.metric("Ninguno", f"{ninguno_felix}%")
                
            with col2:
                st.markdown("#### Escenario B: Iván Hernández")
                df_c2 = pd.DataFrame(list(data_careos["Careo 2 (Iván)"].items()), columns=["Partido", "%"])
                
                fig_c2 = px.pie(
                    df_c2, names="Partido", values="%", hole=0.5,
                    color_discrete_sequence=px.colors.qualitative.Bold,
                    height=400
                )
                fig_c2.update_traces(textposition='outside', textinfo='percent+label')
                st.plotly_chart(fig_c2, use_container_width=True)
                
                morena_ivan = data_careos['Careo 2 (Iván)'].get('MORENA (Iván)', 0)
                ninguno_ivan = data_careos['Careo 2 (Iván)'].get('Ninguno', 0)
                diferencia = morena_ivan - morena_felix
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Voto MORENA", f"{morena_ivan}%", delta=f"+{diferencia:.1f} pts vs Félix")
                with metric_col2:
                    st.metric("Ninguno", f"{ninguno_ivan}%")
            
            # Comparativa final
            st.divider()
            st.markdown("#### 📊 Comparativa de Ventaja")
            
            comp_data = pd.DataFrame({
                'Escenario': ['Félix Salgado', 'Iván Hernández'],
                'MORENA': [morena_felix, morena_ivan],
                'Ninguno': [ninguno_felix, ninguno_ivan]
            })
            
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(name='MORENA', x=comp_data['Escenario'], y=comp_data['MORENA'], text=comp_data['MORENA'], texttemplate='%{text:.1f}%', marker_color='#880E4F'))
            fig_comp.add_trace(go.Bar(name='Ninguno', x=comp_data['Escenario'], y=comp_data['Ninguno'], text=comp_data['Ninguno'], texttemplate='%{text:.1f}%', marker_color='#BDBDBD'))
            
            fig_comp.update_layout(barmode='group', height=350, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_comp, use_container_width=True)
            
            # Insight final
            if diferencia > 5:
                st.success(f"✅ **Iván Hernández** muestra una ventaja competitiva de **+{diferencia:.1f} puntos** sobre Félix Salgado")
            else:
                st.info(f"ℹ️ Ambos escenarios muestran desempeños similares (diferencia de {diferencia:.1f} pts)")

if __name__ == "__main__":
    main()