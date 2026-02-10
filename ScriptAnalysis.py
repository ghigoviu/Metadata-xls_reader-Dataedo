import pandas as pd
import re


def extraer_tablas_y_sentencias(texto_sql):
    # Definimos los patrones Regex para cada sentencia
    # El patrón busca la palabra clave e intenta capturar el primer nombre de tabla válido
    patrones = {
        'SELECT': r'\bSELECT\b.*?\bFROM\s+([a-zA-Z0-9_.]+)',
        'INSERT': r'\bINSERT\s+INTO\s+([a-zA-Z0-9_.]+)',
        'UPDATE': r'\bUPDATE\s+([a-zA-Z0-9_.]+)',
        'DELETE': r'\bDELETE\s+FROM\s+([a-zA-Z0-9_.]+)'
    }

    hallazgos = []

    # Buscamos cada tipo de sentencia en el bloque de código
    for sentencia, patron in patrones.items():
        # re.IGNORECASE para que no importe si es SELECT o select
        # re.DOTALL para que el .* incluya saltos de línea
        matches = re.findall(patron, texto_sql, re.IGNORECASE | re.DOTALL)
        for tabla in matches:
            hallazgos.append((sentencia, tabla.strip()))

    return hallazgos

# 1. Supongamos que df_final es el resultado del paso anterior
# Vamos a crear una lista para expandir los resultados
df_final = extraer_tablas_y_sentencias("TEXTSQL")
resultados_inventario = []

for index, fila in df_final.iterrows():
    proc_name = fila['procname']
    codigo = str(fila['data'])

    tablas_encontradas = extraer_tablas_y_sentencias(codigo)

    for sentencia, tabla in tablas_encontradas:
        resultados_inventario.append({
            'procedimiento': proc_name,
            'sentencia': sentencia,
            'tabla': tabla
        })

# 2. Convertir a un nuevo DataFrame de análisis
df_analisis = pd.DataFrame(resultados_inventario)

# 3. Limpieza: Eliminar duplicados si una tabla aparece 10 veces en el mismo proc
df_analisis = df_analisis.drop_duplicates()

print(df_analisis.head(20))

# 4. Guardar el inventario
df_analisis.to_csv('inventario_tablas_sql.csv', index=False)