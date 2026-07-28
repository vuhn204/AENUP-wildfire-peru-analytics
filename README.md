# AENUP Wildfire Peru Analytics 🔥🇵🇪

Un pipeline integral de análisis de datos geoespaciales y temporales diseñado para procesar, limpiar y visualizar información satelital sobre incendios forestales en Perú, con un dashboard interactivo construido en Streamlit.

---

## 📖 Marco Teórico

### El Problema de los Incendios Forestales en Perú
En Perú, los incendios forestales son un problema recurrente, especialmente durante la temporada seca (entre agosto y noviembre). La mayoría de estos incendios son de origen antrópico (causados por humanos), vinculados a prácticas agrícolas tradicionales como el "roza y quema" para limpiar terrenos agrícolas, los cuales muchas veces se salen de control y terminan afectando bosques amazónicos, ecosistemas andinos y áreas naturales protegidas.

### NASA FIRMS (Fire Information for Resource Management System)
El sistema FIRMS de la NASA distribuye datos de incendios activos en tiempo casi real (NRT - Near Real-Time). Provee las coordenadas, la hora y características físicas de las anomalías térmicas detectadas por satélites espaciales. Este proyecto utiliza los datos históricos generados por dos de los sensores más importantes del FIRMS:

#### 1. Sensor MODIS
El *Moderate Resolution Imaging Spectroradiometer* (MODIS) vuela a bordo de los satélites Terra y Aqua. Detecta anomalías térmicas con una resolución espacial de 1 km por píxel. Es un sensor clásico y altamente confiable que lleva décadas monitoreando el planeta, aunque su menor resolución puede hacer que se pierdan incendios muy pequeños.

#### 2. Sensor VIIRS
El *Visible Infrared Imaging Radiometer Suite* (VIIRS) vuela a bordo de los satélites Suomi NPP y NOAA-20. Ofrece una resolución espacial superior de 375 metros por píxel. Esto le permite detectar incendios mucho más pequeños y mapear perímetros de grandes incendios con mayor precisión, y a menudo detecta entre 3 y 4 veces más focos de calor que MODIS.

### Fire Radiative Power (FRP)
El FRP (Poder Radiativo del Fuego) es una variable crucial en nuestros datos. Se mide en Megavatios (MW) y cuantifica la energía calórica irradiada por el incendio. Un FRP alto indica un incendio muy intenso, que consume mucha biomasa de manera rápida, lo que lo correlaciona directamente con la cantidad de gases de efecto invernadero (humo, CO2) que se están emitiendo a la atmósfera.

---

## ⚙️ Documentación del Proyecto

El código está estructurado de manera modular para transformar datos satelitales crudos en información lista para toma de decisiones y reportes, servida a través de un dashboard interactivo.

### Estructura de Directorios

```text
AENUP-wildfire-peru-analytics/
│
├── app.py                    # Punto de entrada del dashboard (página principal)
├── pages/                    # Páginas adicionales del dashboard Streamlit
│   ├── 1_Tendencias.py
│   ├── 2_Mapas.py
│   ├── 3_Analisis_FRP.py
│   └── 4_Metodologia.py
│
├── data/
│   ├── raw/                  # Archivos originales de la NASA (no versionados en git)
│   └── processed/            # Dataset limpio en formato Parquet (generado automáticamente)
│
├── src/                      # Código fuente del pipeline (ETL)
│   ├── etl.py                # Orquesta la limpieza + feature engineering + exportación
│   ├── cleaning.py           # Lógica de estandarización y limpieza
│   ├── features.py           # Ingeniería de características (momentos del día, niveles de severidad)
│   └── analysis.py           # Agregaciones estadísticas
│
├── .streamlit/
│   └── config.toml           # Tema visual del dashboard
│
└── requirements.txt           # Lista de dependencias del entorno
```

> **Nota:** `data/raw/` y `data/processed/` no se versionan en git (ver .gitignore) por su peso. Los archivos originales están disponibles en este enlace de Drive (https://drive.google.com/drive/folders/1VZ9ue0YI-T_Ki3r7sU-L6a1ByHSl4lf1?usp=sharing) — colócalos en data/raw/ antes de ejecutar el pipeline.

### Funcionalidades del Pipeline
1. **Limpieza Uniforme:** Homologa la confianza (Confidence) de MODIS (numérica) y VIIRS (letras) en una única escala (`Low`, `Medium`, `High`), eliminando registros sin coordenadas.
2. **Feature Engineering:** Deriva variables de temporalidad (año, mes, momento del día) y categoriza el nivel de gravedad basándose en el FRP y el Brightness (Brillo).
3. **Exportación a Parquet:** El dataset combinado y limpio se guarda en `data/processed/combined_clean.parquet`, listo para ser consumido por el dashboard.
4. **Dashboard Interactivo:** Aplicación web multipágina construida con Streamlit, Plotly y pydeck que permite filtrar y explorar 1.4+ millones de registros visualmente — sin generar archivos estáticos.

### Instalación y Ejecución

1. Asegúrate de tener Python instalado (probado en Python 3.10+).
2. Se recomienda crear un entorno virtual:
```bash
   python -m venv .venv
```
3. Activar el entorno virtual:
   - En Windows: `.\.venv\Scripts\Activate.ps1`
   - En Mac/Linux: `source .venv/bin/activate`
4. Instalar las dependencias:
```bash
   pip install -r requirements.txt
```
5. Descarga los datos crudos (modis_archive.csv y viirs_archive.csv) desde este enlace de Google Drive (https://drive.google.com/drive/folders/1VZ9ue0YI-T_Ki3r7sU-L6a1ByHSl4lf1?usp=sharing) y colócalos dentro de data/raw/.
(Los datos provienen originalmente de NASA FIRMS, filtrados para Perú y los sensores MODIS/VIIRS.)
6. Ejecutar el pipeline (limpieza + feature engineering + exportación a Parquet):
```bash
   python -m src.etl
```

Al finalizar, verás en la terminal el conteo de registros procesados por sensor y encontrarás el dataset limpio en `data/processed/combined_clean.parquet`.

---

## 📊 Despliegue del Dashboard Interactivo

El dashboard está construido con **Streamlit**, **Plotly** y **pydeck**, organizado en múltiples páginas:

- **Página principal (`app.py`):** filtros globales (Año, Sensor, Nivel FRP) y KPIs en tiempo real.
- **📈 Tendencias:** incendios por año y por mes, comparando sensores.
- **🗺️ Mapas:** mapa de calor y mapa de puntos individuales sobre Perú, renderizados en memoria con pydeck (sin generar archivos HTML).
- **🔥 Análisis FRP:** distribución de severidad y comparación de detecciones día/noche.
- **ℹ️ Metodología:** documentación de fuentes de datos y variables.

Todas las páginas comparten los mismos filtros a través de `st.session_state`, así que cualquier cambio en la página principal se refleja automáticamente en las demás.

### ¿Cómo ejecutarlo?

Con el pipeline ya ejecutado (paso anterior) y el entorno virtual activo:

```bash
streamlit run app.py
```

> **Nota sobre el primer inicio:**
> La primera vez que ejecutes Streamlit en tu computadora, es posible que la terminal te muestre el siguiente mensaje:
> `If you'd like to receive helpful onboarding emails... Please enter your email address below.`
> **No es necesario ingresar ningún correo**. Simplemente deja el espacio en blanco, presiona la tecla **Enter** (Intro) y la aplicación continuará cargando.

Tu navegador se abrirá automáticamente (usualmente en `http://localhost:8501`) mostrando el panel de control interactivo, con el menú de páginas visible en la barra lateral.