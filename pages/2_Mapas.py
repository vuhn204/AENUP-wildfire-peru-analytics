import streamlit as st
import pydeck as pdk

st.title("🗺️ Mapa geoespacial")

if "filtered_data" not in st.session_state:
    st.warning("Ve primero a la página principal (app.py) para cargar los datos.")
    st.stop()

df = st.session_state["filtered_data"].dropna(subset=["latitude", "longitude"])

tipo_mapa = st.radio("Tipo de mapa", ["Mapa de calor", "Puntos individuales"], horizontal=True)

if len(df) > 100_000:
    st.caption(f"Mostrando muestra de 100,000 de {len(df):,} puntos filtrados para fluidez.")
    df = df.sample(n=100_000, random_state=42)

view_state = pdk.ViewState(latitude=-9.19, longitude=-75.015, zoom=4.5)

if tipo_mapa == "Mapa de calor":
    layer = pdk.Layer(
        "HeatmapLayer",
        data=df,
        get_position=["longitude", "latitude"],
        get_weight="frp",
        radiusPixels=40,
    )
    tooltip = None
else:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["longitude", "latitude"],
        get_radius=800,
        get_fill_color=[255, 80, 0, 140],
        pickable=True,
    )
    tooltip = {"text": "FRP: {frp}\nSensor: {sensor}\nFecha: {acq_date}"}

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
))