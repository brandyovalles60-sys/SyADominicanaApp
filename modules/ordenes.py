import streamlit as st
import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from database.conexion import conectar
from modules.auditoria import registrar_accion

archivo_inventario = "data/inventario.csv"
archivo_ordenes = "data/ordenes.csv"


def cargar_inventario():
    if os.path.exists(archivo_inventario):
        return pd.read_csv(archivo_inventario)
    return pd.DataFrame(columns=["Vino", "Tipo", "Stock"])


def cargar_ordenes():
    if os.path.exists(archivo_ordenes):
        return pd.read_csv(archivo_ordenes)
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


def cargar_clientes_bd():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, telefono, direccion
        FROM clientes
        ORDER BY nombre ASC
    """)

    datos = cursor.fetchall()

    return pd.DataFrame(datos, columns=[
        "id",
        "Nombre",
        "Telefono",
        "Direccion"
    ])


def generar_pdf(cliente, vino, cantidad, direccion):
    os.makedirs("pdf", exist_ok=True)

    nombre_archivo = f"pdf/orden_{cliente}_{vino}.pdf".replace(" ", "_")

    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)

    c.drawString(200, 750, "SyA Dominicana")
    c.drawString(170, 725, "Orden de salida de almacén")

    c.setFont("Helvetica", 12)
    c.drawString(100, 670, f"Cliente: {cliente}")
    c.drawString(100, 640, f"Dirección: {direccion}")
    c.drawString(100, 600, f"Vino: {vino}")
    c.drawString(100, 570, f"Cantidad de botellas: {cantidad}")

    c.drawString(100, 510, "Firma vendedor: ____________________")
    c.drawString(100, 470, "Firma encargado almacén: ____________________")

    c.save()

    return nombre_archivo


def pagina_ordenes():

    st.markdown("""
    <style>
    .orden-card {
        background: #111827;
        border: 1px solid #2d3748;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 18px rgba(0,0,0,0.25);
    }

    .orden-title {
        font-size: 24px;
        font-weight: bold;
        color: white;
        margin-bottom: 8px;
    }

    .orden-sub {
        color: #d1d5db;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.title("📦 Orden de salida de almacén")
    st.write("Crea órdenes para que almacén prepare el pedido y distribución lo entregue.")

    clientes = cargar_clientes_bd()
    inventario = cargar_inventario()
    ordenes = cargar_ordenes()

    if clientes.empty:
        st.info("Aún no tienes clientes registrados en la base de datos.")
        return

    if inventario.empty:
        st.warning("No hay vinos en inventario.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Clientes", len(clientes))
    col2.metric("🍷 Vinos", len(inventario))
    col3.metric("📦 Órdenes", len(ordenes))

    st.divider()

    st.markdown("""
    <div class="orden-card">
        <div class="orden-title">➕ Crear nueva orden</div>
        <div class="orden-sub">Selecciona cliente, vino y cantidad vendida.</div>
    </div>
    """, unsafe_allow_html=True)

    cliente_nombre = st.selectbox(
        "Seleccionar cliente",
        clientes["Nombre"].tolist()
    )

    cliente_data = clientes[clientes["Nombre"] == cliente_nombre].iloc[0]

    telefono = cliente_data["Telefono"]
    direccion_cliente = cliente_data["Direccion"]

    col_a, col_b = st.columns(2)

    with col_a:
        st.text_input("Teléfono", value=telefono if telefono else "", disabled=True)

    with col_b:
        direccion = st.text_input(
            "Dirección de entrega",
            value=direccion_cliente if direccion_cliente else ""
        )

    vino = st.selectbox(
        "Seleccionar vino",
        inventario["Vino"].tolist()
    )

    stock_actual = int(inventario.loc[inventario["Vino"] == vino, "Stock"].values[0])

    st.info(f"Stock disponible de {vino}: {stock_actual} botellas")

    cantidad = st.number_input(
        "Cantidad de botellas",
        min_value=1,
        step=1
    )

    tipo_documento = st.selectbox(
        "Documento comercial",
        ["Factura", "Consignación"]
    )

    pdf_documento = st.file_uploader(
        "Subir PDF de factura o consignación",
        type=["pdf"]
    )

    if st.button("✅ Crear orden", width="stretch"):

        if cantidad > stock_actual:
            st.error("No hay suficiente inventario disponible.")
            return
        
        ruta_pdf = ""

        if pdf_documento is not None:
            os.makedirs("documentos/ordenes", exist_ok=True)

            nombre_pdf = f"{tipo_documento}_{cliente_nombre}_{vino}.pdf".replace(" ", "_")
            ruta_pdf = os.path.join("documentos/ordenes", nombre_pdf)

            with open(ruta_pdf, "wb") as f:
                f.write(pdf_documento.getbuffer())

        nueva_orden = {
            "Cliente": cliente_nombre,
            "Telefono": telefono,
            "Vino": vino,
            "Cantidad": cantidad,
            "Direccion_entrega": direccion,
            "Estado": "Pendiente",
            "Vendedor": st.session_state.get("usuario", "Desconocido"),
            "Tipo_documento": tipo_documento,
            "PDF_documento": ruta_pdf,
        }

        ordenes = pd.concat(
            [ordenes, pd.DataFrame([nueva_orden])],
            ignore_index=True
        )

        guardar_ordenes(ordenes)

        pdf = generar_pdf(cliente_nombre, vino, cantidad, direccion)

        registrar_accion(
            "Órdenes",
            "Crear orden",
            f"Cliente: {cliente_nombre} | Vino: {vino} | Cantidad: {cantidad}"
        )

        st.success("Orden creada correctamente. Ahora debe pasar por almacén.")
        st.info(f"PDF generado: {pdf}")
        st.rerun()

    st.divider()

    st.subheader("📋 Órdenes registradas")

    if ordenes.empty:
        st.info("No hay órdenes creadas todavía.")
    else:
        st.dataframe(
            ordenes.sort_values(by="Estado"),
            width="stretch",
            hide_index=True
        )

    