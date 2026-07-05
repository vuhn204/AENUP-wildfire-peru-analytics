import streamlit as st

st.title("ℹ️ Metodología y fuentes de datos")

st.markdown("""
### Fuente de datos
Los datos provienen del sistema **FIRMS (Fire Information for Resource Management System)**
de la NASA, que combina detecciones de dos sensores satelitales:

- **MODIS** (Terra y Aqua): resolución ~1 km, disponible desde el año 2000.
- **VIIRS** (Suomi NPP / NOAA-20): resolución ~375 m, mayor precisión espacial.

### Variables clave
- **FRP (Fire Radiative Power)**: energía radiativa del incendio, en megavatios (MW).
  Es el mejor indicador de intensidad instantánea del fuego.
- **Brightness**: temperatura de brillo del píxel detectado, en grados Kelvin.
- **Confidence**: nivel de confianza de la detección (numérico en MODIS, categórico
  L/N/H en VIIRS), normalizado aquí a Low/Medium/High.

### Limitaciones conocidas
- La cobertura satelital no detecta incendios bajo nubosidad densa.
- MODIS y VIIRS tienen resoluciones distintas, por lo que comparar conteos absolutos
  entre sensores debe hacerse con cuidado (VIIRS detecta más incendios pequeños).
- Este dashboard no distingue causa del incendio (natural vs. antrópico).
""")