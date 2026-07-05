import streamlit as st
import plotly.express as px

st.title("🔥 Análisis de severidad e intensidad")

if "filtered_data" not in st.session_state:
    st.warning("Ve primero a la página principal (app.py) para cargar los datos.")
    st.stop()

df = st.session_state["filtered_data"]

col1, col2 = st.columns(2)

with col1:
    frp_df = df.groupby(["sensor", "frp_level"]).size().reset_index(name="fires")
    fig = px.bar(
        frp_df, x="frp_level", y="fires", color="sensor", barmode="group",
        title="Incendios por nivel de FRP"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    dn_df = df.groupby(["sensor", "daynight"]).size().reset_index(name="fires")
    fig2 = px.bar(
        dn_df, x="daynight", y="fires", color="sensor", barmode="group",
        title="Detecciones de día vs. noche"
    )
    st.plotly_chart(fig2, use_container_width=True)