import streamlit as st
import bcrypt

# ==============================================================================
# 🔐 CONFIGURACIÓN DE SEGURIDAD
# ==============================================================================

# PEGA AQUÍ EL DICCIONARIO QUE GENERASTE CON EL SCRIPT ANTERIOR
# Debe verse algo así: {"usuario": "$2b$12$..."}

CREDENCIALES_HASH = {
    "admin": "$2b$12$poqf/nK7F3HJScoOIEBhx.w8WY44E4rznqkLRudcdCaS3MdTivNIm",
    "ivanhd": "$2b$12$cOPiznR6ALMpDnhyG8PKROkLD0/vMG2Bji64KzzoJy/q0QlJuLxSm",
    "ilich": "$2b$12$0nx7HShCg8couG5iskwUUuO4KZN4Kt3Y5rdmbQR6ixRK7VapEfdBO",
    "cesarn": "$2b$12$D7KWoN0kOH1S7.SvyS3g1eKHbOyjHZ.lTtAmusHsSDGM0l6RevNbO",
    "omartg": "$2b$12$pcopPpGE6kl3Doq7nM020.T89oyP4PNFDE4ju7qvUnUWRnTgbIzoC",
}
def bloquear_acceso():
    """
    Verifica credenciales usando BCRYPT.
    """
    # 1. Inicializar sesión
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False
    if "usuario_actual" not in st.session_state:
        st.session_state["usuario_actual"] = None

    # 2. Si NO está autenticado, mostrar Login
    if not st.session_state["autenticado"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Acceso Restringido")
            st.info("Sistema de Inteligencia Electoral - Guerrero 2025")
            
            user_input = st.text_input("Usuario")
            pass_input = st.text_input("Contraseña", type="password")
            
            if st.button("Iniciar Sesión", type="primary", use_container_width=True):
                # Validamos si el usuario existe en el diccionario
                if user_input in CREDENCIALES_HASH:
                    hashed_password = CREDENCIALES_HASH[user_input]
                    
                    # COMPARACIÓN SEGURA: Texto plano vs Hash
                    # .encode('utf-8') convierte el texto a bytes, necesario para bcrypt
                    try:
                        if bcrypt.checkpw(pass_input.encode('utf-8'), hashed_password.encode('utf-8')):
                            st.session_state["autenticado"] = True
                            st.session_state["usuario_actual"] = user_input
                            st.toast(f"¡Bienvenido, {user_input}!", icon="👋")
                            st.rerun()
                        else:
                            st.error("❌ Contraseña incorrecta.")
                    except Exception as e:
                        st.error(f"Error de validación: {e}")
                else:
                    st.error("❌ Usuario no encontrado.")
        
        # Detener la app si no hay login
        st.stop()

    # 3. Si YA está autenticado, mostrar Sidebar con Logout
    else:
        with st.sidebar:
            st.write(f"👤 **{st.session_state['usuario_actual']}**")
            if st.button("🔒 Cerrar Sesión", use_container_width=True):
                st.session_state["autenticado"] = False
                st.session_state["usuario_actual"] = None
                st.rerun()
            st.divider()
            
    return True