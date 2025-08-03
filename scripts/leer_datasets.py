import os
import pandas as pd

# Ruta base al directorio de datasets
ruta_datasets = os.path.join("..", "dataset_fifa")
dataframes = {}

# Verifica si la ruta realmente existe
if not os.path.exists(ruta_datasets):
    print(f"[ERROR] La ruta '{ruta_datasets}' no existe. Revisa la ubicación del script.")
else:
    print(f"[INFO] Cargando archivos desde: {os.path.abspath(ruta_datasets)}\n")

    # Recorremos todas las carpetas y subcarpetas
    for raiz, carpetas, archivos in os.walk(ruta_datasets):
        for archivo in archivos:
            if archivo.endswith((".xlsx", ".csv")):
                ruta_archivo = os.path.join(raiz, archivo)
                nombre_base = os.path.splitext(archivo)[0]

                try:
                    if archivo.endswith(".xlsx"):
                        df = pd.read_excel(ruta_archivo)
                    else:
                        df = pd.read_csv(ruta_archivo, encoding='utf-8')

                    # Guardar usando la carpeta como prefijo (si hay subcarpetas)
                    carpeta_relativa = os.path.relpath(raiz, ruta_datasets)
                    clave_df = os.path.join(carpeta_relativa, nombre_base) if carpeta_relativa != "." else nombre_base
                    dataframes[clave_df] = df

                    print(f"[OK] '{archivo}' cargado desde '{carpeta_relativa}'. Filas: {df.shape[0]}, Columnas: {df.shape[1]}\n")
                    print(f"--- Primeras 5 filas de '{archivo}' ---")
                    print(df.head(), "\n")

                except Exception as e:
                    print(f"[ERROR] No se pudo leer '{archivo}': {e}\n")
            else:
                print(f"[IGNORADO] {archivo} no es .xlsx ni .csv\n")
