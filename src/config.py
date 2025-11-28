# src/config.py

# Diccionarios de Configuración
MUNICIPIOS_MAP = {
    "IGUALA": "IGUALA DE LA INDEPENDENCIA",
    "CHILPANCINGO": "CHILPANCINGO DE LOS BRAVO", 
    "ACAPULCO": "ACAPULCO DE JUAREZ"
}

SUPERVISORES_CONFIG = {
    "IGUALA": 6,
    "CHILPANCINGO": 6,
    "ACAPULCO": 8
}

# Rutas de Manzanas
MANZANAS_FILES = {
    "IGUALA": "data/processed/manzanas_optimizadas/manzanas_iguala_opt.shp",
    "CHILPANCINGO": "data/processed/manzanas_optimizadas/manzanas_chilpancingo_opt.shp",
    "ACAPULCO": "data/processed/manzanas_optimizadas/manzanas_acapulco_opt.shp"
}

# Paleta de colores consistente
COLORS = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe']