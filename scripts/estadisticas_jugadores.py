import os
import pandas as pd
import matplotlib.pyplot as plt

# Ruta base al dataset
ruta_base = os.path.join("..", "dataset_fifa")
ruta_agregados = os.path.join(ruta_base, "jugadores_agregados")
ruta_eliminados = os.path.join(ruta_base, "jugadores_eliminados")

# Crear diccionarios para guardar dataframes por año
agregados_por_anio = {}
eliminados_por_anio = {}

# Función para cargar todos los archivos CSV desde una carpeta
def cargar_archivos_por_anio(ruta_carpeta):
    data = {}
    for archivo in os.listdir(ruta_carpeta):
        if archivo.endswith(".csv"):
            anio = archivo.split('_')[-1].split('.')[0]
            ruta = os.path.join(ruta_carpeta, archivo)
            try:
                df = pd.read_csv(ruta, encoding='utf-8')
                data[anio] = df
            except Exception as e:
                print(f"[ERROR] Cargando {archivo}: {e}")
    return data

# Cargar los datasets
agregados_por_anio = cargar_archivos_por_anio(ruta_agregados)
eliminados_por_anio = cargar_archivos_por_anio(ruta_eliminados)

# Crear carpeta para gráficas
ruta_graficas = os.path.join(ruta_base, "estadisticas")
os.makedirs(ruta_graficas, exist_ok=True)

# ---------- ESTADÍSTICAS ----------

for anio in sorted(agregados_por_anio.keys()):
    df_ag = agregados_por_anio.get(anio, pd.DataFrame())
    df_el = eliminados_por_anio.get(anio, pd.DataFrame())

    # ---------- 1. Nacionalidades más agregadas ----------
    if not df_ag.empty and 'nationality' in df_ag.columns:
        top_nacionalidades_ag = df_ag['nationality'].value_counts().head(5)
        plt.figure(figsize=(8,5))
        top_nacionalidades_ag.plot(kind='bar', color='green')
        plt.title(f"Nacionalidades más agregadas en {anio}")
        plt.xlabel("Nacionalidad")
        plt.ylabel("Cantidad")
        plt.tight_layout()
        plt.savefig(os.path.join(ruta_graficas, f"nacionalidades_agregadas_{anio}.png"))
        plt.close()

    # ---------- 2. Nacionalidades más eliminadas ----------
    if not df_el.empty and 'nationality' in df_el.columns:
        top_nacionalidades_el = df_el['nationality'].value_counts().head(5)
        plt.figure(figsize=(8,5))
        top_nacionalidades_el.plot(kind='bar', color='red')
        plt.title(f"Nacionalidades más eliminadas en {anio}")
        plt.xlabel("Nacionalidad")
        plt.ylabel("Cantidad")
        plt.tight_layout()
        plt.savefig(os.path.join(ruta_graficas, f"nacionalidades_eliminadas_{anio}.png"))
        plt.close()

    # ---------- 3. Top 5 jugadores más valiosos ----------
    for df, tipo in zip([df_ag, df_el], ['agregados', 'eliminados']):
        if not df.empty and 'value_eur' in df.columns and 'short_name' in df.columns:
            top_valiosos = df[['short_name', 'value_eur']].sort_values(by='value_eur', ascending=False).head(5)
            plt.figure(figsize=(8,5))
            plt.bar(top_valiosos['short_name'], top_valiosos['value_eur'], color='blue' if tipo == 'agregados' else 'gray')
            plt.title(f"Top 5 jugadores más valiosos ({tipo}) en {anio}")
            plt.xlabel("Jugador")
            plt.ylabel("Valor en EUR")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(ruta_graficas, f"top5_valiosos_{tipo}_{anio}.png"))
            plt.close()

print("[FINALIZADO] Gráficas guardadas en la carpeta 'estadisticas'")


# ---------- NOTA ----------
# Asegúrate de que los archivos CSV tengan las columnas
# 'national
# Si alguna columna no existe, se omitirá esa parte del análisis.
# Puedes ajustar los nombres de las columnas según tu dataset.
# Además, verifica que las rutas sean correctas según tu estructura de carpetas.
# Si encuentras algún error, revisa los nombres de los archivos y las columnas.
# Las gráficas se guardarán en la carpeta 'estadisticas' dentro de 'dataset_f

# fifa'.
# Puedes personalizar los colores y estilos de las gráficas según tus preferencias.
# Si necesitas más análisis o estadísticas, puedes agregar más secciones al script.
# Si deseas realizar un análisis más detallado, considera agregar más columnas
# o métricas a los dataframes antes de generar las gráficas.
# También puedes explorar otras visualizaciones como gráficos de líneas o dispersión
# para analizar tendencias a lo largo de los años.
# Recuerda que este script es un punto de partida y puedes adaptarlo a tus necesidades.


# Si tienes alguna duda o necesitas ayuda adicional, no dudes en preguntar.
# ¡Buena suerte con tu análisis de jugadores de FIFA!
