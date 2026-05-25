import streamlit as st
import pandas as pd
import os
from datetime import datetime

from modules.clientes import cargar_clientes
from modules.inventario import cargar_inventario
from modules.calendario import agregar_evento

archivo_degustacion = "data/degustacion.csv"


def cargar_degustacion():
    os.makedirs("data", exist_ok=True)

    if os.path.exists(archivo_degustacion):
        df = pd.read_csv(archivo_degustacion)

        columnas = [
            "Cliente",
            "Fecha",
            "Vino",
            "Botellas_usadas",
            "Tipo_diseno",
            "Notas"
        ]

        for col in columnas:
            if col not in df.columns:
                df[col] = ""

        df["Botellas_usadas"] = pd.to_numeric(
            df["Botellas_usadas"],
            errors="coerce"
        ).fillna(0).astype(int)

        return df

    return pd.DataFrame(columns=[
        "Cliente",
        "Fecha",
        "Vino",
        "Botellas_usadas",
        "Tipo_diseno",
        "Notas"
    ])


def guardar_degustacion(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(archivo_degustacion, index=False)


def pagina_degustacion():

    st.markdown("""
    <style>
    .deg-card {
        background: #111827;
        border: 1px solid #2d3748;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0px 4px 18px rgba(0,0,0,0.25);
    }

    .deg-title {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .deg-sub {
        color: #d1d5db;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🍷 Degustaciones")
    st.write("Registra botellas usadas, diseños realizados y notas comerciales.")

    clientes = cargar_clientes()
    inventario = cargar_inventario()
    df = cargar_degustacion()

    total_degustaciones = len(df)
    total_botellas = int(df["Botellas_usadas"].sum()) if not df.empty else 0
    total_clientes = df["Cliente"].nunique() if not df.empty else 0

    col_m1, col_m2, col_m3 = st.columns(3)

    col_m1.metric("🍷 Degustaciones", total_degustaciones)
    col_m2.metric("📦 Botellas usadas", total_botellas)
    col_m3.metric("👥 Clientes impactados", total_clientes)

    st.divider()

    if clientes.empty:
        st.warning("No hay clientes registrados.")
        return

    if inventario.empty:
        st.warning("No hay vinos en inventario.")
        return

    st.markdown("""
    <div class="deg-card">
        <div class="deg-title">➕ Registrar degustación</div>
        <div class="deg-sub">
            Guarda el consumo de botellas, diseño aplicado y observaciones del cliente.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        cliente = st.selectbox("Cliente", clientes["Nombre"].tolist())
        vino = st.selectbox("Vino", inventario["Vino"].tolist())

    with col2:
        botellas = st.number_input(
            "Botellas usadas",
            min_value=1,
            step=1
        )

        tipo = st.selectbox(
            "Tipo de diseño",
            [
                "Menú",
                "Evento",
                "Promoción",
                "Carta de vinos",
                "Branding",
                "Otro"
            ]
        )

    notas = st.text_area(
        "Notas / resultado de la degustación",
        placeholder="Ej: El cliente mostró interés en Royal Malbec para carta premium..."
    )

    fecha_evento = st.date_input("Fecha de la degustación")

    foto_evento = st.file_uploader(
        "Subir imagen del evento",
        type=["png", "jpg", "jpeg"]
    )

    diseno_canva = st.file_uploader(
        "Subir diseño creado en Canva",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if st.button("💾 Guardar degustación", width="stretch"):

        ruta_foto = ""
        ruta_diseno = ""

        os.makedirs("archivos/eventos", exist_ok=True)
        os.makedirs("archivos/disenos", exist_ok=True)

        if foto_evento is not None:
            ruta_foto = f"archivos/eventos/{cliente}_{foto_evento.name}".replace(" ", "_")

            with open(ruta_foto, "wb") as f:
                f.write(foto_evento.getbuffer())

        if diseno_canva is not None:
            ruta_diseno = f"archivos/disenos/{cliente}_{diseno_canva.name}".replace(" ", "_")

            with open(ruta_diseno, "wb") as f:
                f.write(diseno_canva.getbuffer())

        nueva = {
            "Cliente": cliente,
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Fecha_evento": fecha_evento.strftime("%Y-%m-%d"),
            "Vino": vino,
            "Botellas_usadas": botellas,
            "Tipo_diseno": tipo,
            "Notas": notas,
            "Foto_evento": ruta_foto,
            "Diseno_canva": ruta_diseno
        }

        df = pd.concat([df, pd.DataFrame([nueva])], ignore_index=True)
        guardar_degustacion(df)

        agregar_evento(
            fecha_evento.strftime("%Y-%m-%d"),
            "Degustación",
            f"Degustación con {cliente}",
            cliente,
            f"Vino: {vino} | Botellas usadas: {botellas}"
        )

        st.success("Degustación guardada correctamente.")
        st.rerun()
        ruta_foto = ""
        ruta_diseno = ""

        os.makedirs("archivos/eventos", exist_ok=True)
        os.makedirs("archivos/disenos", exist_ok=True)

        if foto_evento is not None:
            ruta_foto = f"archivos/eventos/{cliente}_{foto_evento.name}".replace(" ", "_")
            with open(ruta_foto, "wb") as f:
                f.write(foto_evento.getbuffer())

        if diseno_canva is not None:
            ruta_diseno = f"archivos/disenos/{cliente}_{diseno_canva.name}".replace(" ", "_")
            with open(ruta_diseno, "wb") as f:
                f.write(diseno_canva.getbuffer())

    st.divider()

    st.subheader("📊 Historial de degustaciones")

    if df.empty:
        st.info("No hay degustaciones registradas todavía.")
    else:
        st.dataframe(
            df.sort_values(by="Fecha", ascending=False),
            width="stretch",
            hide_index=True
        )

        st.download_button(
            "⬇️ Descargar historial",
            df.to_csv(index=False),
            file_name="historial_degustaciones.csv",
            mime="text/csv",
            width="stretch"
        )