import streamlit as st
from database.conexion import conectar
from modules.idiomas import IDIOMAS


def cargar_config():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT stock_minimo,
               alertas_activas,
               nombre_empresa,
               color_principal
        FROM configuracion
        LIMIT 1
    """)

    return cursor.fetchone()


def guardar_config(stock, alertas, nombre, color):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE configuracion
        SET stock_minimo = %s,
            alertas_activas = %s,
            nombre_empresa = %s,
            color_principal = %s
    """, (
        stock,
        alertas,
        nombre,
        color
    ))

    conn.commit()


def pagina_configuracion():

    st.title("⚙️ Configuración")

    st.divider()

    st.subheader("🌍 Idioma del sistema")

    idioma = st.selectbox(
        "Seleccionar idioma",
        list(IDIOMAS.keys()),
        index=list(IDIOMAS.keys()).index(
            st.session_state.get("idioma", "Español")
        )
    )

    st.session_state["idioma"] = idioma
    st.success(f"Idioma actual: {idioma}")

    datos = cargar_config()

    stock_minimo = datos[0]
    alertas = datos[1]
    nombre_empresa = datos[2]
    color = datos[3]

    st.divider()

    st.subheader("📦 Inventario")

    nuevo_stock = st.number_input(
        "Stock mínimo para alertas",
        min_value=1,
        value=stock_minimo
    )

    activar_alertas = st.toggle(
        "Activar alertas automáticas",
        value=alertas
    )

    st.divider()

    st.subheader("🏢 Empresa")

    nuevo_nombre = st.text_input(
        "Nombre empresa",
        value=nombre_empresa
    )

    nuevo_color = st.color_picker(
        "Color principal",
        value=color
    )

    st.divider()

    if st.button("💾 Guardar configuración", width="stretch"):

        guardar_config(
            nuevo_stock,
            activar_alertas,
            nuevo_nombre,
            nuevo_color
        )

        st.success("Configuración guardada correctamente.")