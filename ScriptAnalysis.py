import pandas as pd
import re
import csv

def extraer_tablas_y_sentencias(texto_sql):
    # 1. Limpieza rápida: normalizamos espacios y saltos de línea para que el regex sea más simple
    texto_sql = re.sub(r'\s+', ' ', texto_sql)

    hallazgos = []

    # Patrones para INSERT, UPDATE y DELETE (normalmente afectan a una tabla principal)
    # Agregamos el ":" al set de caracteres permitidos [a-zA-Z0-9_.:]
    patrones_directos = {
        'INSERT': r'\bINSERT\s+INTO\s+([a-zA-Z0-9_.:"]+)',
        'UPDATE': r'\bUPDATE\s+([a-zA-Z0-9_.:"]+)',
        'DELETE': r'\bDELETE\s+FROM\s+([a-zA-Z0-9_.:"]+)'
    }

    for sentencia, patron in patrones_directos.items():
        matches = re.findall(patron, texto_sql, re.IGNORECASE)
        for tabla in matches:
            hallazgos.append((sentencia, tabla.strip()))

    # --- Lógica especial para SELECT (soporta comas y alias) ---
    # Buscamos desde 'FROM' hasta que encontremos una palabra que indique el fin de la lista de tablas
    # o el fin de la sentencia (WHERE, GROUP, ORDER, INTO, etc.)
    patron_from = r'\bFROM\s+(.+?)(?=\s+WHERE\b|\s+GROUP\b|\s+ORDER\b|\s+HAVING\b|\s+INTO\b|\s+UNION\b|$|;)'

    bloques_from = re.findall(patron_from, texto_sql, re.IGNORECASE)

    for bloque in bloques_from:
        # El bloque puede ser: "tabla1, tabla2, bd:tabla3 r"
        segmentos = bloque.split(',')
        for seg in segmentos:
            seg = seg.strip()
            if seg:
                # Si hay un alias (ej: "bdinteg:si_fechavalor r"), el nombre real es la primera palabra
                nombre_entidad = seg.split(' ')[0]
                # Limpiamos posibles caracteres residuales
                nombre_entidad = re.sub(r'[^a-zA-Z0-9_.:"]', '', nombre_entidad)
                if nombre_entidad:
                    hallazgos.append(('SELECT', nombre_entidad))
    # print(id_SP, nombre_SP, hallazgos)
    return hallazgos

# 1. Supongamos que df_final es el resultado del paso anterior
# Vamos a crear una lista para expandir los resultados
df_final = pd.read_csv("./resources/mainserver_procedures_code.csv")
resultados_inventario = []

for index, fila in df_final.iterrows():
    procid = fila['procid']
    proc_name = fila['procname']
    codigo = str(fila['data'])

    tablas_encontradas = extraer_tablas_y_sentencias(codigo)

    for sentencia, tabla in tablas_encontradas:
        resultados_inventario.append({
            'id': procid,
            'procedimiento': proc_name,
            'sentencia': sentencia,
            'tabla': tabla
        })

# Escribir en csv
with open('./resources/afectaciones_SP.csv', 'w', encoding='utf-8', newline='') as file:
    fieldnames = ['id', 'procedimiento', 'sentencia', 'tabla']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    try:
        writer.writerows(resultados_inventario)
    except ValueError:
        print(resultados_inventario, "no tiene sentencias encontradas")
    print("Archivo guardado.")
