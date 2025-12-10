import pandas as pd
import os

# --- LISTA MAESTRA DE COLUMNAS (ORDEN DEFINITIVO) ---
COLUMNAS_ORDENADAS = [
    # Bloque 1: Datos de captura
    'id_unico', 'fecha_creacion', 'fecha_modificacion', 'duracion_min', 'id_encuestador',
    
    # Bloque 2: Datos identificación de la vivienda
    'seccion_electoral', 'localidad', 'manzana', 'calle', 'num_exterior', 'num_interior',
    'entre_calle_1', 'entre_calle_2', 'colonia', 
    'latitud', 'longitud',  # <--- AGREGADAS AL FINAL DEL BLOQUE 2
    
    # Bloque 3: Sexo, Edad, INE
    'codigo_sexo', 'sexo', 'edad', 'codigo_rango_edad', 'rango_edad', 'codigo_ine', 'ine',
    
    # Bloque 4: Principal problema del estado
    'codigo_direccion_estado', 'direccion_estado', 'codigo_principal_problema',
    'principal_problema_estado', 'principal_problema_estado_otro', 'principal_problema_estado_opciones',
    'codigo_tipo_inseguridad', 'tipo_inseguridad', 'tipo_inseguridad_otro', 'tipo_inseguridad_opciones',
    'codigo_servicios_publicos', 'servicios_publicos', 'servicios_publicos_otro', 'servicios_publicos_opciones',
    
    # Bloque 5: Intención de voto
    'codigo_identificacion_partidaria', 'identificacion_partidaria', 'codigo_intencion_voto_principal',
    'intencion_voto_principal', 'codigo_intencion_voto_secundaria', 'intencion_voto_secundaria',
    'codigo_nunca_votaria', 'nunca_votaria',
    
    # Bloque 6: Conocimiento y opinión
    'codigo_conocimiento_abelina', 'conocimiento_abelina', 'codigo_conocimiento_beatriz', 'conocimiento_beatriz',
    'codigo_conocimiento_esthela', 'conocimiento_esthela', 'codigo_conocimiento_felix', 'conocimiento_felix',
    'codigo_conocimiento_ivan', 'conocimiento_ivan', 'codigo_conocimiento_javier', 'conocimiento_javier',
    'codigo_conocimiento_jacinto', 'conocimiento_jacinto', 'codigo_conocimiento_pablo', 'conocimiento_pablo',
    'codigo_opinion_abelina', 'opinion_abelina', 'codigo_opinion_beatriz', 'opinion_beatriz',
    'codigo_opinion_esthela', 'opinion_esthela', 'codigo_opinion_felix', 'opinion_felix',
    'codigo_opinion_ivan', 'opinion_ivan', 'codigo_opinion_javier', 'opinion_javier',
    'codigo_opinion_jacinto', 'opinion_jacinto', 'codigo_opinion_pablo', 'opinion_pablo',
    
    # Bloque 7: Evaluación de atributos
    'codigo_honestidad_abelina', 'honestidad_abelina', 'codigo_honestidad_beatriz', 'honestidad_beatriz',
    'codigo_honestidad_esthela', 'honestidad_esthela', 'codigo_honestidad_felix', 'honestidad_felix',
    'codigo_honestidad_ivan', 'honestidad_ivan', 'codigo_honestidad_javier', 'honestidad_javier',
    'codigo_honestidad_jacinto', 'honestidad_jacinto', 'codigo_honestidad_pablo', 'honestidad_pablo',
    
    'codigo_cercania_abelina', 'cercania_abelina', 'codigo_cercania_beatriz', 'cercania_beatriz',
    'codigo_cercania_esthela', 'cercania_esthela', 'codigo_cercania_felix', 'cercania_felix',
    'codigo_cercania_ivan', 'cercania_ivan', 'codigo_cercania_javier', 'cercania_javier',
    'codigo_cercania_jacinto', 'cercania_jacinto', 'codigo_cercania_pablo', 'cercania_pablo',
    
    'codigo_derecho_mujeres_abelina', 'derecho_mujeres_abelina', 'codigo_derecho_mujeres_beatriz', 'derecho_mujeres_beatriz',
    'codigo_derecho_mujeres_esthela', 'derecho_mujeres_esthela', 'codigo_derecho_mujeres_felix', 'derecho_mujeres_felix',
    'codigo_derecho_mujeres_ivan', 'derecho_mujeres_ivan', 'codigo_derecho_mujeres_javier', 'derecho_mujeres_javier',
    'codigo_derecho_mujeres_jacinto', 'derecho_mujeres_jacinto', 'codigo_derecho_mujeres_pablo', 'derecho_mujeres_pablo',
    
    'codigo_conocimiento_estado_abelina', 'conocimiento_estado_abelina', 'codigo_conocimiento_estado_beatriz', 'conocimiento_estado_beatriz',
    'codigo_conocimiento_estado_esthela', 'conocimiento_estado_esthela', 'codigo_conocimiento_estado_felix', 'conocimiento_estado_felix',
    'codigo_conocimiento_estado_ivan', 'conocimiento_estado_ivan', 'codigo_conocimiento_estado_javier', 'conocimiento_estado_javier',
    'codigo_conocimiento_estado_jacinto', 'conocimiento_estado_jacinto', 'codigo_conocimiento_estado_pablo', 'conocimiento_estado_pablo',
    
    'codigo_cumplimiento_abelina', 'cumplimiento_abelina', 'codigo_cumplimiento_beatriz', 'cumplimiento_beatriz',
    'codigo_cumplimiento_esthela', 'cumplimiento_esthela', 'codigo_cumplimiento_felix', 'cumplimiento_felix',
    'codigo_cumplimiento_ivan', 'cumplimiento_ivan', 'codigo_cumplimiento_javier', 'cumplimiento_javier',
    'codigo_cumplimiento_jacinto', 'cumplimiento_jacinto', 'codigo_cumplimiento_pablo', 'cumplimiento_pablo',
    
    'codigo_buena_candidatura_abelina', 'buena_candidatura_abelina', 'codigo_buena_candidatura_beatriz', 'buena_candidatura_beatriz',
    'codigo_buena_candidatura_esthela', 'buena_candidatura_esthela', 'codigo_buena_candidatura_felix', 'buena_candidatura_felix',
    'codigo_buena_candidatura_ivan', 'buena_candidatura_ivan', 'codigo_buena_candidatura_javier', 'buena_candidatura_javier',
    'codigo_buena_candidatura_jacinto', 'buena_candidatura_jacinto', 'codigo_buena_candidatura_pablo', 'buena_candidatura_pablo',
    
    'codigo_votar_o_no_abelina', 'votar_o_no_abelina', 'codigo_votar_o_no_beatriz', 'votar_o_no_beatriz',
    'codigo_votar_o_no_esthela', 'votar_o_no_esthela', 'codigo_votar_o_no_felix', 'votar_o_no_felix',
    'codigo_votar_o_no_ivan', 'votar_o_no_ivan', 'codigo_votar_o_no_javier', 'votar_o_no_javier',
    'codigo_votar_o_no_jacinto', 'votar_o_no_jacinto', 'codigo_votar_o_no_pablo', 'votar_o_no_pablo',
    
    # Bloque 8: Preferencia MORENA
    'codigo_preferencia_candidato_morena', 'preferencia_candidato_morena', 'codigo_preferencia_segundo_candidato_morena',
    'preferencia_segundo_candidato_morena', 'codigo_preferencia_candidata_morena', 'preferencia_candidata_morena',
    'codigo_preferencia_segunda_candidata_morena', 'preferencia_segunda_candidata_morena', 'codigo_preferencia_total_morena',
    'preferencia_total_morena', 'codigo_segunda_preferencia_total_morena', 'segunda_preferencia_total_morena',
    
    # Bloque 9: Careos
    'codigo_careo_1', 'careo_1', 'codigo_careo_2', 'careo_2',
    
    # Bloque 10: Evaluación autoridades
    'codigo_aprobacion_acapulco', 'aprobacion_acapulco', 'codigo_aprobacion_chilpancingo', 'aprobacion_chilpancingo',
    'codigo_aprobacion_iguala', 'aprobacion_iguala', 'codigo_aprobacion_gobernadora', 'aprobacion_gobernadora',
    'codigo_aprobacion_presidenta', 'aprobacion_presidenta',
    
    # Bloque 11: Medios
    'codigo_medio_comunicacion_1', 'medio_comunicacion_1', 'codigo_medio_comunicacion_2', 'medio_comunicacion_2',
    'codigo_medio_comunicacion_3', 'medio_comunicacion_3', 'codigo_medio_comunicacion_4', 'medio_comunicacion_4',
    'codigo_medio_comunicacion_5', 'medio_comunicacion_5', 'codigo_medio_comunicacion_6', 'medio_comunicacion_6',
    'codigo_medio_comunicacion_7', 'medio_comunicacion_7', 'codigo_medio_comunicacion_8', 'medio_comunicacion_8',
    'codigo_medio_comunicacion_9', 'medio_comunicacion_9', 'codigo_medio_comunicacion_96', 'medio_comunicacion_96',
    'codigo_medio_comunicacion_97', 'medio_comunicacion_97', 'codigo_medio_comunicacion_98', 'medio_comunicacion_98',
    'codigo_medio_comunicacion_99', 'medio_comunicacion_99', 'codigo_medio_comunicacion_otro', 'medio_comunicacion_otro',
    'medio_comunicacion_otro_1',
    'codigo_uso_television', 'uso_television', 'codigo_uso_radio', 'uso_radio', 'codigo_uso_periodico', 'uso_periodico',
    'codigo_uso_facebook', 'uso_facebook', 'codigo_uso_twitter', 'uso_twitter', 'codigo_uso_instagram', 'uso_instagram',
    'codigo_uso_youtube', 'uso_youtube', 'codigo_uso_whatsapp', 'uso_whatsapp', 'codigo_uso_tiktok', 'uso_tiktok',
    'codigo_recibe_programas', 'recibe_programas',
    
    # Bloque 12: Sociodemográficos
    'codigo_ocupacion', 'ocupacion', 'codigo_estado_civil', 'estado_civil', 'codigo_nivel_escolaridad',
    'puntaje_nivel_escolaridad', 'nivel_escolaridad', 'codigo_baños_completos', 'puntaje_baños_completos',
    'baños_completos', 'codigo_numero_automoviles', 'puntaje_numero_automoviles', 'numero_automoviles',
    'codigo_internet', 'puntaje_internet', 'internet', 'codigo_personas_trabajan', 'puntaje_personas_trabajan',
    'personas_trabajan', 'codigo_numero_cuartos', 'puntaje_numero_cuartos', 'numero_cuartos'
]

def load_and_standardize(csv_path, dict_path):
    """
    Carga el CSV crudo, le aplica el renombrado del diccionario Excel
    y reordena las columnas según COLUMNAS_ORDENADAS.
    Retorna: DataFrame limpio y ordenado.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No se encuentra el CSV: {csv_path}")
    if not os.path.exists(dict_path):
        raise FileNotFoundError(f"No se encuentra el diccionario: {dict_path}")
        
    df = pd.read_csv(csv_path)
    diccionario_df = pd.read_excel(dict_path)
    
    # Renombrar
    # Asumimos columnas 'nombre base' (original) y 'nombre variable' (nuevo)
    mapeo = dict(zip(diccionario_df['nombre base'], diccionario_df['nombre variable']))
    df_renamed = df.rename(columns=mapeo)
    
    # Reordenar
    columnas_disponibles = [col for col in COLUMNAS_ORDENADAS if col in df_renamed.columns]
    columnas_extra = [col for col in df_renamed.columns if col not in COLUMNAS_ORDENADAS]
    columnas_finales = columnas_disponibles + columnas_extra
    
    return df_renamed[columnas_finales]