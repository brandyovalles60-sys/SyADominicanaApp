import streamlit as st
import pandas as pd
import os
from datetime import datetime

# IMPORTAR FUNCIONES
from modules.clientes import cargar_clientes
from modules.inventario import cargar_inventario


archivo_degustacion = "data/degustacion.csv"


def cargar_degustacion():
    if os.path.exists(archivo_degustacion):
        return pd.read_csv(archivo_degustacion)
    else:
        return pd.DataFrame(columns=[
            "Cliente",
            "Fecha",
            "Vino",
            "Botellas_usadas",
            "Tipo_diseno",
            "Notas"
        ])


def pagina_degustacion():

    # 🎨 ESTILO BONITO
    st.markdown("""
        <style>
        .main {
            background-color: #0E1117;
        }
        .card {
            background-color: #1C1F26;
            padding: 25px;
            border-radius: 15px;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color:#D32F2F;'>🍷 Degustaciones</h1>", unsafe_allow_html=True)

    # Crear carpeta si no existe
    os.makedirs("data", exist_ok=True)

    clientes = cargar_clientes()
    inventario = cargar_inventario()
    df = cargar_degustacion()

    # VALIDACIONES
    if clientes.empty:
        st.warning("⚠️ No hay clientes registrados")
        return

    if inventario.empty:
        st.warning("⚠️ No hay vinos en inventario")
        return

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    # FORMULARIO
    col1, col2 = st.columns(2)

    with col1:
        cliente = st.selectbox("Cliente", clientes["Nombre"])
        vino = st.selectbox("Vino", inventario["Vino"])

    with col2:
        botellas = st.number_input("Botellas usadas", min_value=1, step=1)
        tipo = st.selectbox("Tipo diseño", ["Menú", "Evento", "Promoción"])

    notas = st.text_area("Notas")

    # BOTÓN GUARDAR
    if st.button("💾 Guardar degustación"):

        nueva = {
            "Cliente": cliente,
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Vino": vino,
            "Botellas_usadas": botellas,
            "Tipo_diseno": tipo,
            "Notas": notas
        }

        df = pd.concat([df, pd.DataFrame([nueva])], ignore_index=True)
        df.to_csv(archivo_degustacion, index=False)

        st.success("✅ Guardado correctamente")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # HISTORIAL
    st.markdown("## 📊 Historial de degustaciones")

    if df.empty:
        st.info("No hay registros aún")
    else:
        st.dataframe(
            df.sort_values(by="Fecha", ascending=False),
            use_container_width=True
        )

        # DESCARGA
        st.download_button(
            "⬇️ Descargar historial",
            df.to_csv(index=False),
            file_name="degustaciones.csv",
            mime="text/csv"
        )