import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("PRUEBA MAPA")

# Datos fijos (esto DEBE funcionar sí o sí)
data = pd.DataFrame([
    {"nombre": "Punto 1", "lat": 18.4861, "lon": -69.9312},
    {"nombre": "Punto 2", "lat": 18.4961, "lon": -69.9412}
])

st.write(data)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position='[lon, lat]',
    get_radius=200,
    get_color='[255, 0, 0]',
    pickable=True
)

view_state = pdk.ViewState(
    latitude=18.4861,
    longitude=-69.9312,
    zoom=12
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{nombre}"}
))