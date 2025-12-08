import streamlit as st
import streamlit_authenticator as stauth

def bloquear_acceso():
    # 1. Validar existencia de secretos
    if 'credentials' not in st.secrets:
        st.error("Error: No se configuraron secretos en el panel de Streamlit Cloud.")
        st.stop()

    # 2. Copia MANUAL de credenciales 
    # (Esto evita errores de 'recursion depth' o 'readonly' en la nube)
    secrets_usernames = st.secrets['credentials']['usernames']
    dict_credentials = {'usernames': {}}
    
    for username, data in secrets_usernames.items():
        dict_credentials['usernames'][username] = {
            'name': data['name'],
            'password': data['password']
        }
    
    # 3. Autenticador
    authenticator = stauth.Authenticate(
        dict_credentials,
        st.secrets['cookie']['name'],
        st.secrets['cookie']['key'],
        st.secrets['cookie']['expiry_days']
    )

    # 4. Login
    authenticator.login(location='main')

    # 5. Validación
    if st.session_state["authentication_status"]:
        with st.sidebar:
            st.write(f"👤 **{st.session_state['name']}**")
            authenticator.logout('Cerrar Sesión', 'sidebar')
        return True
    elif st.session_state["authentication_status"] is False:
        st.error("Usuario o contraseña incorrectos")
        st.stop()
    elif st.session_state["authentication_status"] is None:
        st.warning("🔒 Ingresa tus credenciales para ver el monitoreo.")
        st.stop()