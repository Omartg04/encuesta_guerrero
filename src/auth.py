import streamlit as st
import streamlit_authenticator as stauth

def bloquear_acceso():
    """
    Función de bloqueo segura.
    Crea una copia manual de las credenciales para evitar errores de inmutabilidad y recursión.
    """
    # 1. Validar que existan los secretos
    if 'credentials' not in st.secrets:
        st.error("Error: No se configuraron secretos (.streamlit/secrets.toml)")
        st.stop()

    # --- CORRECCIÓN DEFINITIVA (MANUAL COPY) ---
    # Extraemos los datos manualmente a un diccionario nuevo.
    # Esto rompe el vínculo con Streamlit y evita el error de recursión.
    
    secrets_usernames = st.secrets['credentials']['usernames']
    
    # Construimos un diccionario limpio y editable
    dict_credentials = {'usernames': {}}
    
    for username, data in secrets_usernames.items():
        dict_credentials['usernames'][username] = {
            'name': data['name'],
            'password': data['password']
        }
    # -------------------------------------------
    
    # 2. Inicializar Autenticador con el diccionario limpio
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
            # Ahora el logout modificará 'dict_credentials' (nuestra copia), sin romper nada
            authenticator.logout('Cerrar Sesión', 'sidebar')
        return True 
        
    elif st.session_state["authentication_status"] is False:
        st.error("Usuario o contraseña incorrectos")
        st.stop()
        
    elif st.session_state["authentication_status"] is None:
        st.warning("🔒 Esta sección es privada. Inicia sesión para ver el monitoreo.")
        st.stop()