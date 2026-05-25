import streamlit as st
import pandas as pd
import os
from modules.auditoria import registrar_accion

st.write("Modulo inventario cargado")

archivo_inventario = "data/inventario.csv"

VINOS = [
    "Callejon Comunero",
    "Descariado",
    "Royal Cabernet",
    "Royal Malbec",
    "Finca Buenaventura",
    "Aureo Ruta 90",
    "Aureo Chardonnay",
    "Aureo Petit Verdot"
]


def cargar_inventario():
    os.makedirs("data", exist_ok=True)

    if os.path.exists(archivo_inventario):
        df = pd.read_csv(archivo_inventario)

        if "Vino" not in df.columns:
            df["Vino"] = ""
        if "Tipo" not in df.columns:
            df["Tipo"] = ""
        if "Stock" not in df.columns:
            df["Stock"] = 0

        df["Stock"] = pd.to_numeric(df["Stock"], errors="coerce").fillna(0).astype(int)

        return df

    return pd.DataFrame(columns=["Vino", "Tipo", "Stock"])


def guardar_inventario(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(archivo_inventario, index=False)


def pagina_inventario():

    st.markdown("""
    <style>
    .inv-card {
        background: #111827;
        border: 1px solid #2d3748;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0px 4px 18px rgba(0,0,0,0.25);
        margin-bottom: 18px;
    }

    .inv-title {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 10px;
    }

    .inv-sub {
        color: #d1d5db;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("📦 Inventario de Vinos")
    st.write("Control de entradas, salidas y alertas de stock.")

    df = cargar_inventario()

    total_botellas = int(df["Stock"].sum()) if not df.empty else 0
    total_vinos = len(df) if not df.empty else 0
    stock_bajo_total = len(df[df["Stock"] <= 10]) if not df.empty else 0

    col_m1, col_m2, col_m3 = st.columns(3)

    col_m1.metric("🍷 Botellas totales", total_botellas)
    col_m2.metric("📌 Vinos registrados", total_vinos)
    col_m3.metric("⚠️ Stock bajo", stock_bajo_total)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="inv-card">
            <div class="inv-title">➕ Agregar stock</div>
            <div class="inv-sub">Registra nuevas botellas al inventario.</div>
        </div>
        """, unsafe_allow_html=True)

        vino = st.selectbox("Seleccionar vino", VINOS, key="vino_entrada")

        tipo = st.selectbox(
            "Tipo",
            ["Tinto", "Blanco", "Rosado", "Espumoso"],
            key="tipo_entrada"
        )

        cantidad = st.number_input(
            "Cantidad a agregar",
            min_value=1,
            step=1,
            key="cantidad_entrada"
        )

        if st.button("✅ Guardar entrada", use_container_width=True):

            if vino in df["Vino"].values:
                df.loc[df["Vino"] == vino, "Stock"] += cantidad
                df.loc[df["Vino"] == vino, "Tipo"] = tipo
            else:
                nuevo = {
                    "Vino": vino,
                    "Tipo": tipo,
                    "Stock": cantidad
                }

                df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)

            guardar_inventario(df)

            registrar_accion(
                "Inventario",
                "Agregar stock",
                f"Vino: {vino} | Cantidad: {cantidad}"
            )

            st.success(f"Entrada registrada: {vino} +{cantidad}")
            st.rerun()

    with col2:
        st.markdown("""
        <div class="inv-card">
            <div class="inv-title">➖ Retirar stock</div>
            <div class="inv-sub">Registra salidas por venta, degustación o entrega.</div>
        </div>
        """, unsafe_allow_html=True)

        if df.empty:
            st.info("No hay inventario para retirar.")
        else:
            vino_salida = st.selectbox(
                "Seleccionar vino para salida",
                df["Vino"].tolist(),
                key="vino_salida"
            )

            cantidad_salida = st.number_input(
                "Cantidad a retirar",
                min_value=1,
                step=1,
                key="cantidad_salida"
            )

            motivo = st.selectbox(
                "Motivo de salida",
                ["Venta", "Degustación", "Entrega", "Ajuste"],
                key="motivo_salida"
            )

            if st.button("📤 Registrar salida", use_container_width=True):

                stock_actual = int(df.loc[df["Vino"] == vino_salida, "Stock"].values[0])

                if cantidad_salida > stock_actual:
                    st.error("No hay suficiente stock disponible.")
                else:
                    df.loc[df["Vino"] == vino_salida, "Stock"] -= cantidad_salida

                    guardar_inventario(df)

                    registrar_accion(
                        "Inventario",
                        "Retirar stock",
                        f"Vino: {vino_salida} | Cantidad: {cantidad_salida} | Motivo: {motivo}"
                    )

                    st.success(f"Salida registrada: {vino_salida} -{cantidad_salida} ({motivo})")
                    st.rerun()

    st.divider()


    stock_minimo = 10

    try:
        from modules.configuracion import cargar_config
        config = cargar_config()
        stock_minimo = int(config[0]) if config else 10
    except:
        stock_minimo = 10

    st.subheader("📊 Inventario actual")

    if df.empty:
        st.info("No hay inventario registrado.")
    else:
        tabla = df.sort_values(by="Stock", ascending=True).copy()

        tabla["Estado"] = tabla["Stock"].apply(
            lambda x: "🚨 Bajo" if x <= stock_minimo else "✅ OK"
        )

        st.dataframe(
        tabla,
        width="stretch",
        hide_index=True,
        column_config={
            "Vino": st.column_config.TextColumn("🍷 Vino"),
            "Tipo": st.column_config.TextColumn("🏷️ Tipo"),
            "Stock": st.column_config.NumberColumn("📦 Stock"),
            "Estado": st.column_config.TextColumn("Estado")
        }
    )
       

    st.subheader("🚨 Alertas de inventario")

    

    if df.empty:
        st.info("Sin datos de inventario.")
    else:
        stock_bajo = df[df["Stock"] <= stock_minimo]

        if stock_bajo.empty:
            st.success("✅ Todo el inventario está saludable.")
        else:
            for _, row in stock_bajo.iterrows():
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