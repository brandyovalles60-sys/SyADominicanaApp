import streamlit as st
import pandas as pd
import os
from datetime import datetime
from database.conexion import conectar


archivo_documentos = "data/documentos.csv"


def cargar_documentos():
    if os.path.exists(archivo_documentos):
        df = pd.read_csv(archivo_documentos)

        columnas = [
            "Fecha",
            "Tipo",
            "Cliente",
            "Descripcion",
            "Archivo",
            "Subido_por",
            "Vendedor",
            "Monto"
        ]

        for col in columnas:
            if col not in df.columns:
                df[col] = ""

        df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce").fillna(0)
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

        return df

    return pd.DataFrame(columns=[
        "Fecha",
        "Tipo",
        "Cliente",
        "Descripcion",
        "Archivo",
        "Subido_por",
        "Vendedor",
        "Monto"
    ])


def cargar_info_cliente(nombre_cliente):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nombre, telefono, direccion, rnc
        FROM clientes
        WHERE nombre = %s
        LIMIT 1
    """, (nombre_cliente,))

    dato = cursor.fetchone()

    if dato:
        return {
            "Nombre": dato[0],
            "Telefono": dato[1],
            "Direccion": dato[2],
            "RNC": dato[3]
        }

    return None

def tarjeta_documento(row, i):
    tipo = row["Tipo"]

    if tipo == "Factura":
        color = "#064e3b"
        icono = "💵"
        estado = "PAGO / FACTURA"
    elif tipo == "Consignación":
        color = "#78350f"
        icono = "⏳"
        estado = "A PLAZO / CONSIGNACIÓN"
    else:
        color = "#111827"
        icono = "📄"
        estado = "DOCUMENTO"

    fecha = row["Fecha"]

    fecha_texto = fecha.strftime("%Y-%m-%d") if pd.notnull(fecha) else "Sin fecha"

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color}, #111827);
        border: 1px solid rgba(220,38,38,0.35);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(220,38,38,0.18);
        animation: fadeIn .5s ease-in-out;
    ">
        <h3 style="color:white;">{icono} {estado}</h3>
        <p style="color:#fca5a5;">Fecha: {fecha_texto}</p>
        <p style="color:white;font-size:18px;">Monto: RD$ {row['Monto']:,.2f}</p>
        <p style="color:#d1d5db;">Vendedor: {row.get('Vendedor', 'No registrado')}</p>
        <p style="color:#d1d5db;">Nota: {row.get('Descripcion', '')}</p>
    </div>
    """, unsafe_allow_html=True)

    archivo = row.get("Archivo", "")

    if archivo and os.path.exists(archivo):
        with open(archivo, "rb") as file:
            st.download_button(
                "⬇️ Descargar documento PDF",
                data=file,
                file_name=os.path.basename(archivo),
                mime="application/pdf",
                key=f"descargar_doc_cliente_{i}",
                width="stretch"
            )
    else:
        st.warning("PDF no encontrado o no registrado.")


def pagina_historial_clientes():

    st.title("🏪 Historial de Clientes")
    st.write("Consulta facturas, consignaciones, deudas y actividad por restaurante.")

    df = cargar_documentos()

    if df.empty:
        st.info("No hay documentos registrados todavía.")
        return

    clientes = sorted(df["Cliente"].dropna().unique().tolist())

    if not clientes:
        st.info("No hay clientes en documentos.")
        return

    cliente = st.selectbox(
        "Buscar / seleccionar cliente",
        clientes
    )

    datos_cliente = df[df["Cliente"] == cliente].copy()


    info_cliente = cargar_info_cliente(cliente)

    if info_cliente:
        st.markdown(f"""
        <div style="
            background:rgba(17,24,39,0.92);
            border:1px solid rgba(220,38,38,0.35);
            border-radius:18px;
            padding:20px;
            margin-bottom:20px;
            box-shadow:0 0 18px rgba(220,38,38,0.18);
        ">
            <h3 style="color:white;">🏪 Información del cliente</h3>
            <p style="color:white;">📞 Teléfono: {info_cliente['Telefono']}</p>
            <p style="color:white;">📍 Dirección: {info_cliente['Direccion']}</p>
            <p style="color:white;">🧾 RNC: {info_cliente['RNC']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No se encontró información adicional del cliente en la base de datos.")

    if datos_cliente.empty:
        st.info("Este cliente no tiene documentos.")
        return

    facturas = datos_cliente[datos_cliente["Tipo"] == "Factura"]
    consignaciones = datos_cliente[datos_cliente["Tipo"] == "Consignación"]

    total_facturas = facturas["Monto"].sum()
    total_consignaciones = consignaciones["Monto"].sum()
    total_general = total_facturas + total_consignaciones

    hoy = pd.Timestamp(datetime.now().date())

    deuda_vencida = 0
    consignaciones_vencidas = pd.DataFrame()

    if not consignaciones.empty:
        consignaciones = consignaciones.copy()
        consignaciones["Dias"] = (hoy - consignaciones["Fecha"]).dt.days
        consignaciones_vencidas = consignaciones[consignaciones["Dias"] >= 60]
        deuda_vencida = consignaciones_vencidas["Monto"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Facturas", f"RD$ {total_facturas:,.2f}")
    col2.metric("⏳ Consignación", f"RD$ {total_consignaciones:,.2f}")
    col3.metric("📊 Total vendido", f"RD$ {total_general:,.2f}")


    st.divider()

    st.subheader("⏳ Estado de consignaciones")

    if consignaciones.empty:
        st.success("Este cliente no tiene consignaciones pendientes.")
    else:
        consignaciones_estado = consignaciones.copy()
        consignaciones_estado["Dias"] = (hoy - consignaciones_estado["Fecha"]).dt.days
        consignaciones_estado["Dias_faltantes"] = 60 - consignaciones_estado["Dias"]
        consignaciones_estado["Fecha_vencimiento"] = consignaciones_estado["Fecha"] + pd.to_timedelta(60, unit="D")

        for _, row in consignaciones_estado.sort_values(by="Fecha", ascending=False).iterrows():

            dias = int(row["Dias"])
            faltan = int(row["Dias_faltantes"])
            fecha_vencimiento = row["Fecha_vencimiento"].strftime("%Y-%m-%d")

            if dias >= 60:
                estado = "🚨 VENCIDA - COBRAR URGENTE"
                color = "#450a0a"
                mensaje = f"Pasaron {dias} días. Está vencida hace {dias - 60} días."
            elif dias >= 50:
                estado = "⚠️ CASI VENCE"
                color = "#7f1d1d"
                mensaje = f"Han pasado {dias} días. Faltan {faltan} días para vencer."
            elif dias >= 40:
                estado = "🟡 PREPARAR COBRO"
                color = "#78350f"
                mensaje = f"Han pasado {dias} días. Faltan {faltan} días para vencer."
            else:
                estado = "✅ DENTRO DEL PLAZO"
                color = "#111827"
                mensaje = f"Han pasado {dias} días. Faltan {faltan} días para vencer."

            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {color}, #111827);
                border: 1px solid rgba(220,38,38,0.45);
                border-radius: 18px;
                padding: 22px;
                margin-bottom: 15px;
                box-shadow: 0 0 22px rgba(220,38,38,0.22);
                animation: fadeIn .5s ease-in-out;
            ">
                <h3 style="color:white;">{estado}</h3>
                <p style="color:#fca5a5;font-size:18px;">Monto pendiente: RD$ {row['Monto']:,.2f}</p>
                <p style="color:white;">{mensaje}</p>
                <p style="color:#d1d5db;">Fecha consignación: {row['Fecha'].strftime('%Y-%m-%d')}</p>
                <p style="color:#d1d5db;">Fecha límite de pago: {fecha_vencimiento}</p>
                <p style="color:#9ca3af;">Vendedor: {row.get('Vendedor', 'No registrado')}</p>
            </div>
            """, unsafe_allow_html=True)
    

    st.divider()

    # Últimos movimientos
    st.subheader("🧾 Último movimiento")

    datos_ordenados = datos_cliente.sort_values(by="Fecha", ascending=False)

    ultimo = datos_ordenados.iloc[0]

    fecha_ultimo = ultimo["Fecha"].strftime("%Y-%m-%d") if pd.notnull(ultimo["Fecha"]) else "Sin fecha"

    st.markdown(f"""
    <div style="
        background:rgba(17,24,39,0.92);
        border:1px solid rgba(220,38,38,0.35);
        border-radius:18px;
        padding:20px;
        margin-bottom:15px;
        box-shadow:0 0 18px rgba(220,38,38,0.18);
    ">
        <h3 style="color:white;">Último documento: {ultimo['Tipo']}</h3>
        <p style="color:#fca5a5;">Fecha: {fecha_ultimo}</p>
        <p style="color:white;">Monto: RD$ {ultimo['Monto']:,.2f}</p>
        <p style="color:#d1d5db;">Vendedor: {ultimo.get('Vendedor', 'No registrado')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Aviso de deuda
    if not consignaciones.empty:

        consignaciones_actualizadas = consignaciones.copy()
        consignaciones_actualizadas["Dias"] = (hoy - consignaciones_actualizadas["Fecha"]).dt.days

        alerta = consignaciones_actualizadas[consignaciones_actualizadas["Dias"] >= 45]

        if not alerta.empty:
            st.subheader("🚨 Alertas de consignación")

            for _, row in alerta.iterrows():
                dias = row["Dias"]

                if dias >= 60:
                    mensaje = "🚨 Vencida"
                    color = "#450a0a"
                elif dias >= 50:
                    mensaje = "⚠️ Casi vence"
                    color = "#7f1d1d"
                else:
                    mensaje = "🟡 Revisar pronto"
                    color = "#78350f"

                st.markdown(f"""
                <div style="
                    background:{color};
                    border:1px solid rgba(220,38,38,0.45);
                    border-radius:18px;
                    padding:20px;
                    margin-bottom:15px;
                    box-shadow:0 0 20px rgba(220,38,38,0.2);
                ">
                    <h3 style="color:white;">{mensaje}</h3>
                    <p style="color:white;">Monto: RD$ {row['Monto']:,.2f}</p>
                    <p style="color:#fca5a5;">Días transcurridos: {dias}</p>
                    <p style="color:#d1d5db;">Fecha: {row['Fecha'].strftime('%Y-%m-%d')}</p>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # Sugerencia comercial
    st.subheader("🍷 Recomendación comercial")

    ultimo_tipo = ultimo["Tipo"]
    dias_ultimo = (hoy - ultimo["Fecha"]).days if pd.notnull(ultimo["Fecha"]) else 0

    if dias_ultimo >= 30:
        st.warning(f"Este cliente tiene {dias_ultimo} días sin movimiento. Conviene visitarlo o revisar si necesita más vino.")
    elif total_consignaciones > total_facturas:
        st.warning("Este cliente tiene más consignación que facturación. Revisar cobro antes de entregar más vino.")
    else:
        st.success("Cliente con movimiento reciente. Buen seguimiento comercial.")

    st.divider()

    tab1, tab2, tab3 = st.tabs([
        "💵 Facturas",
        "⏳ Consignaciones",
        "📚 Todo el historial"
    ])

    with tab1:
        if facturas.empty:
            st.info("Este cliente no tiene facturas.")
        else:
            for i, row in facturas.sort_values(by="Fecha", ascending=False).iterrows():
                tarjeta_documento(row, f"factura_{i}")

    with tab2:
        if consignaciones.empty:
            st.info("Este cliente no tiene consignaciones.")
        else:
            for i, row in consignaciones.sort_values(by="Fecha", ascending=False).iterrows():
                tarjeta_documento(row, f"consignacion_{i}")

    with tab3:
        for i, row in datos_cliente.sort_values(by="Fecha", ascending=False).iterrows():
            tarjeta_documento(row, f"historial_{i}")