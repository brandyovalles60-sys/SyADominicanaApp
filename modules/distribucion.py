import streamlit as st
import pandas as pd
import pydeck as pdk
import os
from modules.auditoria import registrar_accion

archivo_ordenes = "data/ordenes.csv"


def cargar_ordenes():
    if os.path.exists(archivo_ordenes):
        df = pd.read_csv(archivo_ordenes)

        columnas = [
            "Cliente",
            "Telefono",
            "Vino",
            "Cantidad",
            "Direccion_entrega",
            "Estado"
        ]

        for col in columnas:
            if col not in df.columns:
                df[col] = ""

        return df

    return pd.DataFrame(columns=[
        "Cliente",
        "Telefono",
        "Vino",
        "Cantidad",
        "Direccion_entrega",
        "Estado"
    ])


def guardar_ordenes(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(archivo_ordenes, index=False)


def pagina_distribucion():

    st.title("🚚 Distribución / Repartidor")
    st.write("Pedidos confirmados por almacén y listos para entregar.")

    ordenes = cargar_ordenes()

    if ordenes.empty:
        st.info("No hay órdenes registradas.")
        return

    listas = ordenes[ordenes["Estado"] == "Listo para entrega"]

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total órdenes", len(ordenes))
    col2.metric("🚚 Listas para entrega", len(listas))
    col3.metric("✅ Entregadas", len(ordenes[ordenes["Estado"] == "Entregado"]))

    st.divider()

    if listas.empty:
        st.info("No hay pedidos listos para entregar.")
        return

    st.subheader("📦 Pedidos listos")

    for i, row in listas.iterrows():

        with st.container(border=True):

            st.markdown(f"### 🚚 Entrega #{i + 1}")
            st.write(f"👤 **Cliente:** {row['Cliente']}")
            st.write(f"📞 **Teléfono:** {row.get('Telefono', '')}")
            st.write(f"🍷 **Vino:** {row['Vino']}")
            st.write(f"📦 **Cantidad:** {row['Cantidad']} botellas")
            st.write(f"📍 **Dirección:** {row['Direccion_entrega']}")
            st.write(f"📌 **Estado:** {row['Estado']}")

            link_maps = f"https://www.google.com/maps/search/?api=1&query={row['Direccion_entrega'].replace(' ', '+')}"

            st.link_button("📍 Abrir ubicación en Google Maps", link_maps)

            if st.button("✅ Marcar como entregado", key=f"entregado_{i}"):

                ordenes.at[i, "Estado"] = "Entregado"
                ordenes.at[i, "Entregado_por"] = st.session_state.get("usuario", "Desconocido")
                guardar_ordenes(ordenes)

                registrar_accion(
                    "Distribución",
                    "Pedido entregado",
                    f"Cliente: {row['Cliente']} | Vino: {row['Vino']} | Cantidad: {row['Cantidad']}"
                )

                st.success("Pedido marcado como entregado.")
                st.rerun()