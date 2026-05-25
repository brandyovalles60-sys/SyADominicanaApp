import streamlit as st
import pandas as pd
import os

archivo_pedidos = "data/pedidos.csv"
archivo_clientes = "data/clientes.csv"  # si usas CSV

def cargar_pedidos():
    if os.path.exists(archivo_pedidos):
        return pd.read_csv(archivo_pedidos)
    else:
        return pd.DataFrame(columns=["Cliente", "Vino", "Cantidad", "Lat", "Lon", "Estado"])

def guardar_pedidos(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(archivo_pedidos, index=False)

def pagina_pedidos():

    st.title("🧾 Crear Pedido")

    df = cargar_pedidos()

    # 🔥 AQUÍ puedes cambiar luego por DB si quieres
    cliente = st.text_input("Nombre del cliente")

    vino = st.selectbox("Vino", [
        "Callejon Comunero",
        "Descariado",
        "Royal Cabernet",
        "Royal Malbec",
        "Finca Buenaventura",
        "Aureo Ruta 90",
        "Aureo Chardonnay",
        "Aureo Petit Verdot"
    ])

    cantidad = st.number_input("Cantidad", min_value=1)

    lat = st.number_input("Latitud", value=18.48)
    lon = st.number_input("Longitud", value=-69.93)

    if st.button("Crear pedido"):

        nuevo = {
            "Cliente": cliente,
            "Vino": vino,
            "Cantidad": cantidad,
            "Lat": lat,
            "Lon": lon,
            "Estado": "Pendiente"
        }

        df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)

        guardar_pedidos(df)

        st.success("Pedido creado")