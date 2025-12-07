import bcrypt

# TU CONTRASEÑA EXACTA
password_raw = "My#is43"

print(f"🔑 Generando clave segura para: '{password_raw}'")

# Generamos el hash usando bcrypt estándar (compatible con streamlit-authenticator)
hashed_bytes = bcrypt.hashpw(password_raw.encode('utf-8'), bcrypt.gensalt())
hashed_final = hashed_bytes.decode('utf-8')

print("\n" + "="*50)
print("COPIA LA SIGUIENTE LÍNEA EXACTA EN TU SECRETS.TOML:")
print("="*50)
print(f'usernames = {{ "omartg" = {{name = "Product Owner", password = "{hashed_final}"}} }}')
print("="*50 + "\n")