import streamlit as st
import plotly.express as px

st.title("📈 Tendencias temporales")

if "filtered_data" not in st.session_state:
    st.warning("Ve primero a la página principal (app.py) para cargar los datos.")
    st.stop()

df = st.session_state["filtered_data"]

yearly = df.groupby(["sensor", "year"]).size().reset_index(name="fires")
fig_year = px.line(
    yearly, x="year", y="fires", color="sensor", markers=True,
    title="Incendios por año"
)
st.plotly_chart(fig_year, use_container_width=True)

month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]
monthly = df.groupby(["sensor", "month_name"]).size().reset_index(name="fires")
fig_month = px.bar(
    monthly, x="month_name", y="fires", color="sensor", barmode="group",
    category_orders={"month_name": month_order},
    title="Incendios por mes"
)
st.plotly_chart(fig_month, use_container_width=True)