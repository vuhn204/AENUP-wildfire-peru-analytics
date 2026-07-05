import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Wildfire Peru Analytics",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    df = pd.read_parquet("data/processed/combined_clean.parquet")
    df["acq_date"] = pd.to_datetime(df["acq_date"], errors="coerce")
    return df

st.title("🔥 Wildfire Peru Analytics")
st.markdown("Exploración interactiva de incendios detectados por MODIS y VIIRS (NASA FIRMS).")

try:
    data = load_data()
except FileNotFoundError:
    st.error("⚠️ Ejecuta `python -m src.etl` antes de abrir el dashboard.")
    st.stop()

st.sidebar.header("Filtros")
years = sorted(data["year"].dropna().unique().astype(int).tolist())
selected_year = st.sidebar.selectbox("Año", ["Todos"] + years, key="f_year")
selected_sensor = st.sidebar.selectbox("Sensor", ["Todos", "MODIS", "VIIRS"], key="f_sensor")
selected_frp = st.sidebar.selectbox(
    "Nivel FRP",
    ["Todos"] + sorted(data["frp_level"].dropna().unique().tolist()),
    key="f_frp"
)

st.session_state["data"] = data

filtered = data.copy()
if selected_year != "Todos":
    filtered = filtered[filtered["year"] == selected_year]
if selected_sensor != "Todos":
    filtered = filtered[filtered["sensor"] == selected_sensor]
if selected_frp != "Todos":
    filtered = filtered[filtered["frp_level"] == selected_frp]

st.session_state["filtered_data"] = filtered

col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Total incendios", f"{len(filtered):,}")
col2.metric("🌡️ FRP promedio (MW)", f"{filtered['frp'].mean():,.1f}" if not filtered.empty else "0")
col3.metric("☀️ Brillo promedio (K)", f"{filtered['brightness'].mean():,.1f}" if not filtered.empty else "0")
col4.metric("🚨 FRP máximo", f"{filtered['frp'].max():,.1f}" if not filtered.empty else "0")

st.markdown("---")
st.info("Usa el menú de la izquierda (páginas) para ver Tendencias, Mapas y Análisis FRP.")