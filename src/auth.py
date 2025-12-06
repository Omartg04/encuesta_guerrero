import streamlit as st
import streamlit_authenticator as stauth
import copy # <--- IMPORTANTE: Necesario para la solución

def bloquear_acceso():
    """
    Función de bloqueo con corrección para Logout.
    """
    # 1. Cargar configuración
    if 'credentials' not in st.secrets:
        st.error("Error: No se configuraron secretos (.streamlit/secrets.toml)")
        st.stop()

    # --- CORRECCIÓN CRÍTICA ---
    # st.secrets es inmutable (solo lectura).
    # Usamos deepcopy para crear una copia completa y editable de las credenciales.
    # Esto permite que la librería modifique el estado 'logged_in' sin error.
    try:
        dict_credentials = copy.deepcopy(dict(st.secrets['credentials']))
    except Exception as e:
        st.error(f"Error procesando credenciales: {e}")
        st.stop()
    # --------------------------
    
    # 2. Inicializar Autenticador
    authenticator = stauth.Authenticate(
        dict_credentials,
        st.secrets['cookie']['name'],
        st.secrets['cookie']['key'],
        st.secrets['cookie']['expiry_days']
    )

    # 3. Renderizar Widget de Login
    authenticator.login()

    # 4. Verificar Estado
    if st.session_state["authentication_status"]:
        with st.sidebar:
            st.write(f"👤 **{st.session_state['name']}**")
            # El botón de logout ahora modificará 'dict_credentials' (la copia), no 'st.secrets'
            authenticator.logout('Cerrar Sesión', 'sidebar')
        return True 
        
    elif st.session_state["authentication_status"] is False:
        st.error("Usuario o contraseña incorrectos")
        st.stop()
        
    elif st.session_state["authentication_status"] is None:
        st.warning("🔒 Esta sección es privada. Inicia sesión para ver el monitoreo.")
        st.stop()