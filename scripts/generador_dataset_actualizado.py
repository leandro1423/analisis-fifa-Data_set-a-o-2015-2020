import os
import pandas as pd

# Rutas
base_dir = os.path.join("..", "dataset_fifa")
carpeta_agregados = os.path.join(base_dir, "jugadores_agregados")
carpeta_eliminados = os.path.join(base_dir, "jugadores_eliminados")
carpeta_salida = os.path.join(base_dir, "jugadores_actualizados_2020")

# Crear carpeta de salida si no existe
os.makedirs(carpeta_salida, exist_ok=True)

# Cargar todos los archivos .csv de ambas carpetas
def cargar_jugadores(ruta_carpeta):
    jugadores = pd.DataFrame()
    for archivo in sorted(os.listdir(ruta_carpeta)):
        if archivo.endswith(".csv"):
            df = pd.read_csv(os.path.join(ruta_carpeta, archivo), encoding='utf-8')
            jugadores = pd.concat([jugadores, df], ignore_index=True)
    return jugadores

print("[INFO] Cargando jugadores agregados...")
df_agregados = cargar_jugadores(carpeta_agregados)
print(f"[INFO] Total jugadores agregados: {df_agregados.shape[0]}")

print("[INFO] Cargando jugadores eliminados...")
df_eliminados = cargar_jugadores(carpeta_eliminados)
print(f"[INFO] Total jugadores eliminados: {df_eliminados.shape[0]}")

# Verificamos que tengan columna 'short_name' o similar como identificador
if 'short_name' not in df_agregados.columns or 'short_name' not in df_eliminados.columns:
    raise Exception("No se encontró la columna 'short_name' en uno de los datasets")

# Obtener jugadores activos hasta 2020: los que NO fueron eliminados
jugadores_activos = df_agregados[~df_agregados['short_name'].isin(df_eliminados['short_name'])]

print(f"[INFO] Jugadores activos hasta 2020: {jugadores_activos.shape[0]}")

# Guardar en un CSV
ruta_salida = os.path.join(carpeta_salida, "jugadores_activos_2020.csv")
jugadores_activos.to_csv(ruta_salida, index=False, encoding='utf-8')
print(f"[OK] Archivo guardado: {ruta_salida}")
