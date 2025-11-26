import pandas as pd

# Cargar el CSV
df = pd.read_csv("data/raw/muestra.csv")

# 1. Contar filas totales vs valores únicos
total_filas = len(df)
secciones_unicas = df['seccion'].nunique()

print(f"📊 Filas totales en el archivo: {total_filas}")
print(f"🔢 Secciones únicas reales:     {secciones_unicas}")

# 2. Buscar duplicados
if total_filas > secciones_unicas:
    print("\n⚠️ ¡ALERTA! Se encontraron secciones duplicadas:")
    # Buscamos las filas donde la sección se repite
    duplicados = df[df.duplicated(subset=['seccion'], keep=False)]
    
    # Mostramos los datos de las filas duplicadas
    print(duplicados[['seccion', 'Nombre_municipio', 'encuestas_totales']])
    
    print("\n👉 ACCIÓN: Abre tu CSV y elimina una de estas filas para tener las 189 únicas (si te falta agregar una distinta) o quedarte con 188.")
else:
    print("\n✅ No hay duplicados. Si te faltan secciones para llegar a 189, es que faltan filas en el archivo.")