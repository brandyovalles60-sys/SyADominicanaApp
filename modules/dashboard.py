import streamlit as st
import pandas as pd
import plotly.express as px
import os
from modules.configuracion import cargar_config


def cargar_csv(ruta):
    if os.path.exists(ruta):
        return pd.read_csv(ruta)
    return pd.DataFrame()


def pagina_dashboard():

    st.title("📊 Dashboard Ejecutivo")
    st.write("Resumen general del sistema SyA Dominicana.")

    # -------------------------
    # CARGAR DATOS
    # -------------------------
    ordenes = cargar_csv("data/ordenes.csv")
    inventario = cargar_csv("data/inventario.csv")
    degustaciones = cargar_csv("data/degustacion.csv")

    # -------------------------
    # KPIs
    # -------------------------
    total_ordenes = len(ordenes)

    total_clientes = (
        ordenes["Cliente"].nunique()
        if not ordenes.empty else 0
    )

    total_vinos = (
        inventario["Vino"].nunique()
        if not inventario.empty else 0
    )

    total_botellas = (
        ordenes["Cantidad"].sum()
        if not ordenes.empty else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📦 Órdenes", total_ordenes)
    col2.metric("👥 Clientes", total_clientes)
    col3.metric("🍷 Vinos", total_vinos)
    col4.metric("🥂 Botellas vendidas", total_botellas)

    st.divider()

    # -------------------------
    # VINOS MÁS VENDIDOS
    # -------------------------
    st.subheader("🍷 Vinos más vendidos")

    if not ordenes.empty:

        vinos = (
            ordenes.groupby("Vino")["Cantidad"]
            .sum()
            .reset_index()
            .sort_values(by="Cantidad", ascending=False)
        )

        fig = px.bar(
            vinos,
            x="Cantidad",
            y="Vino",
            orientation="h",
            text="Cantidad"
        )

        fig.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font_color="white",
            height=450
        )

        st.plotly_chart(fig, width="stretch")

    else:
        st.info("No hay ventas todavía.")

    st.divider()

    # -------------------------
    # CLIENTES TOP
    # -------------------------
    st.subheader("🏆 Clientes que más compran")

    if not ordenes.empty:

        clientes = (
            ordenes.groupby("Cliente")["Cantidad"]
            .sum()
            .reset_index()
            .sort_values(by="Cantidad", ascending=False)
        )

        fig2 = px.bar(
            clientes,
            x="Cliente",
            y="Cantidad",
            text="Cantidad"
        )

        fig2.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font_color="white",
            height=450
        )

        st.plotly_chart(fig2, width="stretch")

    else:
        st.info("No hay clientes registrados.")

    st.divider()

    # -------------------------
    # ALERTAS
    # -------------------------
    config = cargar_config()

    stock_minimo = int(config[0]) if config else 5
    alertas_activas = bool(config[1]) if config else True

    st.subheader("🚨 Alertas de inventario")

    if alertas_activas:

        if not inventario.empty:

            bajo_stock = inventario[inventario["Stock"] <= stock_minimo]

            if bajo_stock.empty:
                st.success("✅ Todo el inventario está saludable.")
            else:
                for _, row in bajo_stock.iterrows():
                    st.markdown(f"""
                        <div style="
                        background: linear-gradient(135deg, #450a0a, #111827);
                        border: 1px solid #dc2626;
                        border-radius: 18px;
                        padding: 20px;
                        margin-bottom: 15px;
                        box-shadow: 0 0 20px rgba(220,38,38,0.25);
                        animation: fadeIn 0.6s ease-in-out;
                    ">
                        <h3 style="color:#fecaca;">🚨 Stock bajo: {row['Vino']}</h3>
                        <p style="color:white;font-size:18px;">
                        Quedan <b>{row['Stock']}</b> botellas.
                        </p>
                        <p style="color:#9ca3af;">
                        Mínimo configurado: {stock_minimo} botellas.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No hay inventario cargado.")
    else:
        st.info("Las alertas están desactivadas desde configuración.")

    # -------------------------
    # ÚLTIMAS ÓRDENES
    # -------------------------
    st.divider()

    st.subheader("📋 Últimas órdenes")

    if not ordenes.empty:

        st.dataframe(
            ordenes.tail(5),
            width="stretch",
            hide_index=True
        )

    else:
        st.info("No hay órdenes.")