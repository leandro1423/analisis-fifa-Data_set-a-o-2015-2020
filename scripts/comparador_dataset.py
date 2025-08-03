import os
import pandas as pd
import re

# Rutas
ruta_datasets = os.path.join("..", "dataset_fifa")
ruta_agregados = os.path.join(ruta_datasets, "jugadores_agregados")
ruta_eliminados = os.path.join(ruta_datasets, "jugadores_eliminados")

# Crear carpetas si no existen
os.makedirs(ruta_agregados, exist_ok=True)
os.makedirs(ruta_eliminados, exist_ok=True)

columnas_por_archivo = {}
archivos_jugadores = {}

# Recorremos todos los archivos de la carpeta
for archivo in sorted(os.listdir(ruta_datasets)):
    ruta_archivo = os.path.join(ruta_datasets, archivo)

    if archivo.endswith(".xlsx") or archivo.endswith(".csv"):
        if archivo.startswith("players_"):
            try:
                df = pd.read_excel(ruta_archivo) if archivo.endswith(".xlsx") else pd.read_csv(ruta_archivo)
                columnas = set(df.columns)
                columnas_por_archivo[archivo] = columnas
                archivos_jugadores[archivo] = df
                print(f"[OK] {archivo} ({'Excel' if archivo.endswith('.xlsx') else 'CSV'}) leído con {len(columnas)} columnas.")
            except Exception as e:
                print(f"[ERROR] No se pudo leer '{archivo}': {e}")
        else:
            print(f"[IGNORADO] {archivo} no corresponde a dataset de jugadores.")
    else:
        print(f"[IGNORADO] {archivo} no es un archivo .xlsx o .csv")

# Mostrar columnas comunes
if columnas_por_archivo:
    comunes = set.intersection(*columnas_por_archivo.values())
    print("\n=== Columnas comunes entre todos los archivos de jugadores ===")
    for columna in sorted(comunes):
        print(columna)
else:
    print("⚠️ No se cargaron archivos para comparar columnas.")

# Comparar jugadores nuevos y eliminados entre archivos por año
print("\n=== Jugadores nuevos y eliminados por año ===")
archivos_ordenados = sorted(archivos_jugadores.keys())
id_anterior = set()
jugadores_agregados_por_anio = {}
jugadores_eliminados_por_anio = {}

for archivo in archivos_ordenados:
    df = archivos_jugadores[archivo]

    # Extraer el año desde el nombre del archivo
    match = re.search(r'players_(\d{4})', archivo)
    if match:
        anio = match.group(1)
    else:
        anio = os.path.splitext(archivo)[0].replace("players_", "")
        print(f"[⚠️] No se pudo detectar año en el archivo '{archivo}', se usará '{anio}' como identificador.")

    if 'sofifa_id' not in df.columns:
        print(f"[ADVERTENCIA] El archivo {archivo} no tiene la columna 'sofifa_id'")
        continue

    ids_actuales = set(df['sofifa_id'].dropna().astype(int))

    if id_anterior:
        nuevos = ids_actuales - id_anterior
        eliminados = id_anterior - ids_actuales

        print(f"{archivo} ({anio}):")
        print(f" ➕ {len(nuevos)} jugadores nuevos")
        print(f" ➖ {len(eliminados)} jugadores eliminados")

        # 🔄 Incluir todas las columnas del jugador
        jugadores_nuevos = df[df['sofifa_id'].isin(nuevos)].drop_duplicates(subset='sofifa_id')
        jugadores_agregados_por_anio[anio] = jugadores_nuevos

        df_anterior = archivos_jugadores[archivo_anterior]
        jugadores_eliminados = df_anterior[df_anterior['sofifa_id'].isin(eliminados)].drop_duplicates(subset='sofifa_id')
        jugadores_eliminados_por_anio[anio] = jugadores_eliminados

        # Guardar CSVs
        if not jugadores_nuevos.empty:
            ruta_csv_nuevos = os.path.join(ruta_agregados, f"jugadores_agregados_{anio}.csv")
            jugadores_nuevos.to_csv(ruta_csv_nuevos, index=False)
            print(f"  [CSV] Guardados jugadores agregados en: {ruta_csv_nuevos}")

        if not jugadores_eliminados.empty:
            ruta_csv_eliminados = os.path.join(ruta_eliminados, f"jugadores_eliminados_{anio}.csv")
            jugadores_eliminados.to_csv(ruta_csv_eliminados, index=False)
            print(f"  [CSV] Guardados jugadores eliminados en: {ruta_csv_eliminados}")

    else:
        print(f"{archivo} ({anio}): primer año cargado, no hay comparación.")
        jugadores_agregados_por_anio[anio] = pd.DataFrame(columns=df.columns)
        jugadores_eliminados_por_anio[anio] = pd.DataFrame(columns=df.columns)

    id_anterior = ids_actuales
    archivo_anterior = archivo

# Mostrar resumen final
print("\n=== Resumen: Año en que se agregaron jugadores ===")
for anio, df_nuevos in jugadores_agregados_por_anio.items():
    if df_nuevos.empty:
        print(f"{anio}: sin jugadores nuevos registrados.")
    else:
        print(f"\nAño {anio}: {len(df_nuevos)} jugadores agregados")
        print(df_nuevos[['sofifa_id', 'short_name']].to_string(index=False))

print("\n=== Resumen: Año en que se eliminaron jugadores ===")
for anio, df_eliminados in jugadores_eliminados_por_anio.items():
    if df_eliminados.empty:
        print(f"{anio}: sin jugadores eliminados.")
    else:
        print(f"\nAño {anio}: {len(df_eliminados)} jugadores eliminados")
        print(df_eliminados[['sofifa_id', 'short_name']].to_string(index=False))
