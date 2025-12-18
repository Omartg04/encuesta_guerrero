import bcrypt

# Lista de usuarios y sus contraseñas planas
usuarios_a_crear = {
    "admin": "admin123",
    "ivanhd": "ivan2025",
    "ilich": "ilich2025",
    "cesarn": "cesar2025",
    "omartg": "My#is43"  # Agrego el del primer script por si acaso
}

print("COPIA ESTE DICCIONARIO Y PÉGALO EN src/auth.py:\n")
print("CREDENCIALES_HASH = {")

for usuario, password in usuarios_a_crear.items():
    # Generar hash
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_final = hashed_bytes.decode('utf-8')
    print(f'    "{usuario}": "{hashed_final}",')

print("}")