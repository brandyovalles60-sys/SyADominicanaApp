import streamlit as st
import pandas as pd
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
            "Estado",
            "Vendedor",
            "Tipo_documento",
            "PDF_documento",
            "PDF_salida_almacen",
            "Preparado_por"
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
        "Estado",
        "Vendedor",
        "Tipo_documento",
        "PDF_documento",
        "PDF_salida_almacen",
        "Preparado_por"
    ])


def guardar_ordenes(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(archivo_ordenes, index=False)


def pagina_almacen():

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.title("🏪 Almacén / Preparar pedidos")
    st.write("Confirma las órdenes listas para entregar.")

    ordenes = cargar_ordenes()

    if ordenes.empty:
        st.info("No hay órdenes registradas.")
        return

    pendientes = ordenes[ordenes["Estado"] == "Pendiente"]

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total órdenes", len(ordenes))
    col2.metric("⏳ Pendientes", len(pendientes))
    col3.metric("🚚 Listas", len(ordenes[ordenes["Estado"] == "Listo para entrega"]))

    st.divider()

    if pendientes.empty:
        st.success("No hay órdenes pendientes para preparar.")
        return

    st.subheader("📋 Órdenes pendientes")

    for i, row in pendientes.iterrows():

        with st.container(border=True):

            st.markdown(f"### 🧾 Orden #{i + 1}")
            st.write(f"👤 **Cliente:** {row['Cliente']}")
            st.write(f"📞 **Teléfono:** {row.get('Telefono', '')}")
            st.write(f"🍷 **Vino:** {row['Vino']}")
            st.write(f"📦 **Cantidad:** {row['Cantidad']} botellas")
            st.write(f"📍 **Dirección:** {row['Direccion_entrega']}")
            st.write(f"👨‍💼 **Vendedor:** {row.get('Vendedor', 'No registrado')}")
            st.write(f"📄 **Documento comercial:** {row.get('Tipo_documento', 'No registrado')}")
            st.write(f"📌 **Estado:** {row['Estado']}")

            if row.get("PDF_documento", ""):
                st.info(f"PDF factura/consignación: {row.get('PDF_documento')}")

            pdf_salida = st.file_uploader(
                "Subir PDF de salida de almacén",
                type=["pdf"],
                key=f"salida_{i}"
            )

            col_a, col_b = st.columns(2)

            with col_a:
                if st.button("✅ Confirmar para distribución", key=f"confirmar_{i}"):

                    if pdf_salida is None:
                        st.error("Debes subir la salida de almacén en PDF antes de confirmar.")
                        return

                    os.makedirs("documentos/salidas_almacen", exist_ok=True)

                    nombre_pdf = f"salida_{row['Cliente']}_{row['Vino']}.pdf".replace(" ", "_")
                    ruta_pdf = os.path.join("documentos/salidas_almacen", nombre_pdf)

                    with open(ruta_pdf, "wb") as f:
                        f.write(pdf_salida.getbuffer())

                    ordenes.at[i, "PDF_salida_almacen"] = ruta_pdf
                    ordenes.at[i, "Preparado_por"] = st.session_state.get("usuario", "Desconocido")
                    ordenes.at[i, "Estado"] = "Listo para entrega"

                    guardar_ordenes(ordenes)

                    registrar_accion(
                        "Almacén",
                        "Confirmar salida",
                        f"Cliente: {row['Cliente']} | Vino: {row['Vino']} | Cantidad: {row['Cantidad']}"
                    )

                    st.success("Orden confirmada y enviada a distribución.")
                    st.rerun()

            with col_b:
                if st.button("❌ Cancelar orden", key=f"cancelar_{i}"):

                    ordenes.at[i, "Estado"] = "Cancelada"
                    guardar_ordenes(ordenes)

                    registrar_accion(
                        "Almacén",
                        "Cancelar orden",
                        f"Cliente: {row['Cliente']} | Vino: {row['Vino']}"
                    )

                    st.warning("Orden cancelada.")
                    st.rerun()