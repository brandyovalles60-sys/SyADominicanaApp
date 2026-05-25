import streamlit as st
import pandas as pd
import os
from datetime import datetime
from modules.auditoria import registrar_accion

CARPETAS = {
    "Factura": "documentos/facturas",
    "Consignación": "documentos/consignaciones",
    "Salida de almacén": "documentos/salidas_almacen"
}

archivo_registro = "data/documentos.csv"


def cargar_documentos():
    os.makedirs("data", exist_ok=True)

    

    if os.path.exists(archivo_registro):
        return pd.read_csv(archivo_registro)
    

    

    return pd.DataFrame(columns=[
        "Fecha",
        "Tipo",
        "Cliente",
        "Descripcion",
        "Archivo",
        "Subido_por"
    ])


   


def guardar_documentos(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(archivo_registro, index=False)


def pagina_documentos():

    st.title("📂 Centro de Documentos")
    st.write("Gestiona facturas, consignaciones y salidas de almacén.")

    for carpeta in CARPETAS.values():
        os.makedirs(carpeta, exist_ok=True)

    df = cargar_documentos()

    col1, col2, col3 = st.columns(3)
    col1.metric("📄 Documentos", len(df))
    col2.metric("🧾 Facturas", len(df[df["Tipo"] == "Factura"]) if not df.empty else 0)
    col3.metric("📦 Salidas", len(df[df["Tipo"] == "Salida de almacén"]) if not df.empty else 0)

    st.divider()

    with st.container(border=True):
        st.subheader("➕ Subir nuevo documento")

        tipo = st.selectbox(
            "Tipo de documento",
            ["Factura", "Consignación", "Salida de almacén"]
        )

        cliente = st.text_input("Cliente / Restaurante")
        descripcion = st.text_area("Descripción / Nota")

        monto = st.number_input(
            "Monto del documento RD$",
            min_value=0.0,
            step=100.0
            )

        archivo = st.file_uploader(
            "Subir PDF",
            type=["pdf"]
        )

        if st.button("💾 Guardar documento", width="stretch"):

            if archivo is None:
                st.error("Debes subir un PDF.")
                return

            if cliente.strip() == "":
                st.error("Debes escribir el cliente.")
                return

            carpeta = CARPETAS[tipo]

            fecha_archivo = datetime.now().strftime("%Y-%m-%d_%H-%M")
            nombre_archivo = f"{tipo}_{cliente}_{fecha_archivo}.pdf".replace(" ", "_")
            ruta = os.path.join(carpeta, nombre_archivo)

            with open(ruta, "wb") as f:
                f.write(archivo.getbuffer())

            nuevo = {
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Tipo": tipo,
                "Cliente": cliente,
                "Descripcion": descripcion,
                "Archivo": ruta,
                "Subido_por": st.session_state.get("usuario", "Desconocido"),
                "Vendedor": st.session_state.get("usuario", "Desconocido"),
                "Monto": monto
            }

            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            guardar_documentos(df)

            registrar_accion(
                "Documentos",
                "Subir documento",
                f"Tipo: {tipo} | Cliente: {cliente} | Monto: {monto}"
            )

            st.success("Documento guardado correctamente.")
            st.rerun()

    st.divider()

    st.subheader("📚 Historial de documentos")

    if df.empty:
        st.info("No hay documentos guardados todavía.")
        return

    filtro = st.selectbox(
        "Filtrar por tipo",
        ["Todos", "Factura", "Consignación", "Salida de almacén"]
    )

    df_filtrado = df.copy()

    if filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Tipo"] == filtro]

    for i, row in df_filtrado.sort_values(by="Fecha", ascending=False).iterrows():

        with st.container(border=True):

            st.markdown(f"### {row['Tipo']} - {row['Cliente']}")
            st.write(f"📅 **Fecha:** {row['Fecha']}")
            st.write(f"👤 **Subido por:** {row.get('Subido_por', 'No registrado')}")
            st.write(f"📝 **Descripción:** {row['Descripcion']}")

            if os.path.exists(row["Archivo"]):
                with open(row["Archivo"], "rb") as file:
                    st.download_button(
                        "⬇️ Descargar PDF",
                        data=file,
                        file_name=os.path.basename(row["Archivo"]),
                        mime="application/pdf",
                        key=f"doc_{i}",
                        width="stretch"
                    )
            else:
                st.error("Archivo no encontrado.")