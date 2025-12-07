import bcrypt

# TU CONTRASEÑA REAL
password_plana = "My#is43"

print(f"🔐 Generando hash para: {password_plana} ...")

try:
    # Generar el hash seguro
    # 1. Convertimos la contraseña a bytes (.encode)
    # 2. Generamos una 'sal' aleatoria (gensalt)
    # 3. Encriptamos
    hashed_bytes = bcrypt.hashpw(password_plana.encode('utf-8'), bcrypt.gensalt())
    
    # Convertimos de bytes a texto para que lo puedas copiar
    hashed_texto = hashed_bytes.decode('utf-8')
    
    print("\n✅ ¡ÉXITO! COPIA EL SIGUIENTE CÓDIGO:")
    print("-" * 60)
    print(hashed_texto)
    print("-" * 60)
    print("Pégalo en tu secrets.toml dentro de las comillas de password.")

except Exception as e:
    print(f"❌ Error: {e}")