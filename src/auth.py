import streamlit as st
import streamlit_authenticator as stauth

def bloquear_acceso():
    """
    Función de bloqueo. 
    Si el usuario NO está logueado -> Muestra Login y detiene la app.
    Si el usuario SÍ está logueado -> Muestra botón Logout y deja pasar.
    """
    # 1. Cargar configuración
    if 'credentials' not in st.secrets:
        st.error("Error: No se configuraron secretos (.streamlit/secrets.toml)")
        st.stop()

    dict_credentials = dict(st.secrets['credentials'])
    
    # 2. Inicializar Autenticador
    authenticator = stauth.Authenticate(
        dict_credentials,
        st.secrets['cookie']['name'],
        st.secrets['cookie']['key'],
        st.secrets['cookie']['expiry_days']
    )

    # 3. Renderizar Widget de Login
    # (El widget maneja la UI automáticamente)
    authenticator.login()

    # 4. Verificar Estado
    if st.session_state["authentication_status"]:
        # CASO: ÉXITO
        with st.sidebar:
            st.success(f"Hola, {st.session_state['name']}")
            authenticator.logout('Cerrar Sesión', 'sidebar')
        return True # Deja pasar
        
    elif st.session_state["authentication_status"] is False:
        # CASO: CONTRASEÑA MAL
        st.error("Usuario o contraseña incorrectos")
        st.stop() # Detiene la ejecución
        
    elif st.session_state["authentication_status"] is None:
        # CASO: AÚN NO INTENTA ENTRAR
        st.warning("🔒 Esta sección es privada. Inicia sesión para ver el monitoreo.")
        st.stop() # Detiene la ejecución para que no se vea el mapa de fondo