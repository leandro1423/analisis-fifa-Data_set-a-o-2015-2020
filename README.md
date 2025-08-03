
---

## 🚀 Scripts Desarrollados

### `cargar_datasets.py`
Carga todos los datasets ubicados en la carpeta `dataset_fifa`, incluyendo archivos `.csv` y `.xlsx`. Muestra la cantidad de filas/columnas y las primeras 5 filas de cada archivo.

---

### `comparador_dataset.py`
- Compara los jugadores entre las carpetas `jugadores_agregados` y `jugadores_eliminados`.- 
- Genera archivos CSV mostrando por año los jugadores eliminados o agregados en las carpetas `jugadores_agregados` y `jugadores_eliminados`

---

### `estadisticas_jugadores.py`
- Compara jugadores eliminados y agregados por año.
- Genera estadísticas visuales:
  - Nacionalidades más agregadas por año.
  - Nacionalidades más eliminadas por año.
  - Top 5 jugadores más valiosos por año (según valor de mercado).

---


###  `generador_dataset_actualizado.py`
- Compara jugadores eliminados y agregados por año.
- Compara los jugadores entre las carpetas `jugadores_agregados` y `jugadores_eliminados`.
- Genera un archivo `jugadores_activos_2020.csv` en la carpeta `jugadores_actualizados_2020`, conteniendo solo los jugadores que **no fueron eliminados hasta 2020**.
## ▶️ Cómo ejecutar

Asegúrate de tener Python y las librerías necesarias instaladas:

```bash
pip install pandas matplotlib seaborn
