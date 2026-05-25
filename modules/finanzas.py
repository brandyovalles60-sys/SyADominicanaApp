import streamlit as st
import pandas as pd
import os
from datetime import datetime




archivo_documentos = "data/documentos.csv"


def cargar_documentos():
    if os.path.exists(archivo_documentos):
        df = pd.read_csv(archivo_documentos)

        for col in ["Fecha", "Tipo", "Cliente", "Monto", "Vendedor"]:
            if col not in df.columns:
                df[col] = ""

        df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce").fillna(0)
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

        return df

    return pd.DataFrame(columns=["Fecha", "Tipo", "Cliente", "Monto", "Vendedor"])


def pagina_finanzas():


    rol_actual = str(st.session_state.get("rol", "")).strip().lower()

    if rol_actual not in ["admin", "jefe"]:
        st.error("No tienes permiso para acceder a Finanzas.")
        st.stop()

    st.title("💰 Finanzas General")
    st.write("Control financiero de facturas pagadas y consignaciones a plazo.")

    df = cargar_documentos()

    if df.empty:
        st.info("No hay documentos financieros registrados.")
        return

    facturas = df[df["Tipo"] == "Factura"]
    consignaciones = df[df["Tipo"] == "Consignación"]

    total_facturas = facturas["Monto"].sum()
    total_consignaciones = consignaciones["Monto"].sum()
    total_general = total_facturas + total_consignaciones

    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Total facturas", f"RD$ {total_facturas:,.2f}")
    col2.metric("⏳ Total consignaciones", f"RD$ {total_consignaciones:,.2f}")
    col3.metric("📊 Total general", f"RD$ {total_general:,.2f}")

    st.divider()

    st.subheader("📊 Resumen financiero")

    resumen = pd.DataFrame({
        "Tipo": ["Factura", "Consignación"],
        "Total": [total_facturas, total_consignaciones]
    })

    st.bar_chart(
        resumen,
        x="Tipo",
        y="Total"
    )

    st.divider()

    st.subheader("🏆 Empleado que más vendió")

    if "Vendedor" in df.columns and not df.empty:

        ventas_empleado = (
            df.groupby("Vendedor")["Monto"]
            .sum()
            .reset_index()
            .sort_values(by="Monto", ascending=False)
        )

        st.dataframe(
            ventas_empleado,
            width="stretch",
            hide_index=True
        )

    st.divider()

    st.subheader("🚨 Alertas de consignaciones")

    hoy = pd.Timestamp(datetime.now().date())

    if consignaciones.empty:
        st.success("No hay consignaciones pendientes.")
    else:
        consignaciones = consignaciones.copy()
        consignaciones["Dias"] = (hoy - consignaciones["Fecha"]).dt.days

        for _, row in consignaciones.iterrows():

            dias = row["Dias"]

            if dias >= 60:
                color = "#450a0a"
                mensaje = "🚨 VENCIDA"
            elif dias >= 50:
                color = "#7f1d1d"
                mensaje = "⚠️ Casi vence"
            elif dias >= 40:
                color = "#78350f"
                mensaje = "🟡 Revisar pronto"
            else:
                color = "#111827"
                mensaje = "✅ Dentro del plazo"

            st.markdown(f"""
            <div style="
                background:{color};
                border:1px solid rgba(220,38,38,0.45);
                border-radius:18px;
                padding:20px;
                margin-bottom:15px;
                box-shadow:0 0 20px rgba(220,38,38,0.20);
                animation: fadeIn .5s ease-in-out;
            ">
                <h3 style="color:white;">{mensaje} - {row['Cliente']}</h3>
                <p style="color:#fca5a5;">Monto: RD$ {row['Monto']:,.2f}</p>
                <p style="color:white;">Días transcurridos: {dias}</p>
                <p style="color:#d1d5db;">Vendedor: {row.get('Vendedor', 'No registrado')}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.subheader("📚 Historial financiero")

    st.dataframe(
        df.sort_values(by="Fecha", ascending=False),
        width="stretch",
        hide_index=True
    )