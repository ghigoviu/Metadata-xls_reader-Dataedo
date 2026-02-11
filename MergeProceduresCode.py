import pandas as pd
import glob
import os


def extraer_nombre_bd(ruta_archivo):
    nombre_archivo = os.path.basename(ruta_archivo)
    nombre_sin_ext = nombre_archivo.replace('.csv', '')
    partes = nombre_sin_ext.split('_')
    if len(partes) > 1:
        return partes[1]
    return "desconocido"

def consolidar_procedimientos(carpeta_entrada, archivo_salida):
    # 1. Obtener la lista de todos los archivos CSV en la carpeta
    ruta_busqueda = os.path.join(carpeta_entrada, "*.csv")
    archivos = glob.glob(ruta_busqueda)

    if not archivos:
        print(f"No se encontraron archivos CSV en la carpeta: {carpeta_entrada}")
        return

    lista_df = []
    print(f"Leyendo {len(archivos)} archivos...")

    # 2. Iterar y cargar cada archivo
    for archivo in archivos:
        bd_name = extraer_nombre_bd(archivo)
        try:
            # Leemos el CSV (ajusta el separador si es necesario, ej: sep=';')
            temp_df = pd.read_csv(archivo)
            temp_df['bd_name'] = bd_name
            print(temp_df)
            # Validamos que tenga las columnas necesarias
            columnas_req = {'procid', 'procname', 'seqno', 'data', 'bd_name'}
            if columnas_req.issubset(temp_df.columns):
                lista_df.append(temp_df)
            else:
                print(f"Archivo omitido (faltan columnas): {archivo}")
        except Exception as e:
            print(f"Error al leer {archivo}: {e}")

    if not lista_df:
        print("No hay datos válidos para procesar.")
        return

    # 3. Concatenar todos los DataFrames en uno solo
    df_total = pd.concat(lista_df, ignore_index=True)

    # 4. Limpieza y ordenamiento
    # Convertimos seqno a numérico para asegurar el orden lógico del código
    df_total['seqno'] = pd.to_numeric(df_total['seqno'], errors='coerce')
    df_total = df_total.sort_values(by=['procname', 'seqno'])

    # 5. Agrupación y unión de la columna 'data'
    # Agrupamos por procname (y procid si quieres mantenerlo)
    df_final = df_total.groupby(['procid', 'procname', 'bd_name'], as_index=False).agg({
        'data': lambda x: ''.join(x.dropna().astype(str))
    })

    # 6. Exportar a un solo archivo maestro
    df_final.to_csv(archivo_salida, index=False, encoding='utf-8')
    print("-" * 30)
    print(f"PROCESO EXITOSO")
    print(f"Total de procedimientos únicos: {len(df_final)}")
    print(f"Archivo generado: {archivo_salida}")

# --- Configuración y Ejecución ---
CARPETA_MAIN = './resources/mainserver_procedures'  # Asegúrate que esta carpeta esté en la misma ruta que tu script
ARCHIVO_RESULTADO = './resources/mainserver_procedures_code.csv'

consolidar_procedimientos(CARPETA_MAIN, ARCHIVO_RESULTADO)