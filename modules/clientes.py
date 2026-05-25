import streamlit as st
import re
from geopy.geocoders import Nominatim
import pandas as pd

geolocator = Nominatim(user_agent="sya_app")


def validar_rnc(rnc):
    if rnc == "":
        return True
    return re.match(r"^\d{9}$", rnc)


def obtener_coordenadas(direccion, ubicacion):
    try:
        query = ubicacion if ubicacion != "" else direccion

        if query == "":
            return None, None

        location = geolocator.geocode(query + ", Republica Dominicana")

        if location:
            return location.latitude, location.longitude

        return None, None

    except:
        return None, None
    

def cargar_clientes(conn=None):
    if conn is None:
        from database.conexion import conectar
        conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, telefono, rnc, direccion, ubicacion, latitud, longitud
        FROM clientes
        ORDER BY id DESC
    """)

    datos = cursor.fetchall()

    return pd.DataFrame(datos, columns=[
        "id",
        "Nombre",
        "Telefono",
        "RNC",
        "Direccion",
        "Ubicacion",
        "Latitud",
        "Longitud"
    ])


def mostrar_clientes(conn):

    st.markdown("""
    <style>
    .cliente-card {
        background: #111827;
        border: 1px solid #2d3748;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0px 4px 18px rgba(0,0,0,0.25);
    }

    .cliente-nombre {
        font-size: 22px;
        font-weight: bold;
        color: #ffffff;
    }

    .cliente-info {
        color: #d1d5db;
        font-size: 15px;
        margin-top: 6px;
    }

    .badge {
        background: #7f1d1d;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("👥 Clientes")
    st.write("Registro y gestión de restaurantes/clientes de SyA Dominicana.")

    # -----------------------------
    # FORMULARIO
    # -----------------------------
    with st.expander("➕ Agregar nuevo cliente", expanded=False):

        nombre = st.text_input("Nombre del restaurante o cliente *")
        telefono = st.text_input("Teléfono (opcional)")
        rnc = st.text_input("RNC (opcional)")
        direccion = st.text_input("Dirección (opcional)")
        ubicacion = st.text_input("Link de Google Maps (opcional)")

        if st.button("Guardar cliente"):

            if nombre.strip() == "":
                st.error("El nombre es obligatorio")
                return

            if not validar_rnc(rnc):
                st.error("El RNC debe tener 9 números")
                return

            lat, lon = obtener_coordenadas(direccion, ubicacion)

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO clientes
                (nombre, telefono, rnc, direccion, ubicacion, latitud, longitud)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (nombre, telefono, rnc, direccion, ubicacion, lat, lon))

            conn.commit()

            st.success("Cliente guardado correctamente")
            st.rerun()

    # -----------------------------
    # LISTA DE CLIENTES
    # -----------------------------
    st.subheader("📋 Lista de clientes")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, telefono, rnc, direccion, ubicacion, latitud, longitud
        FROM clientes
        ORDER BY id DESC
    """)

    datos = cursor.fetchall()

    if not datos:
        st.info("Aún no hay clientes registrados.")
        return

    for c in datos:

        cliente_id = c[0]
        nombre = c[1]
        telefono = c[2]
        rnc = c[3]
        direccion = c[4]
        ubicacion = c[5]
        lat = c[6]
        lon = c[7]

        st.markdown(f"""
        <div class="cliente-card">
            <div class="cliente-nombre">🏪 {nombre}</div>
            <div class="cliente-info">📞 Teléfono: {telefono if telefono else "No registrado"}</div>
            <div class="cliente-info">🧾 RNC: {rnc if rnc else "No registrado"}</div>
            <div class="cliente-info">📍 Dirección: {direccion if direccion else "No registrada"}</div>
            <div class="cliente-info">🌎 Lat: {lat} | Lon: {lon}</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            if ubicacion:
                st.link_button("📍 Abrir ubicación", ubicacion)

        with col2:
            if st.button("🗑️ Eliminar", key=f"eliminar_{cliente_id}"):

                cursor.execute("""
                    DELETE FROM clientes
                    WHERE id = %s
                """, (cliente_id,))

                conn.commit()

                st.success(f"Cliente eliminado: {nombre}")
                st.rerun()


        with st.expander("✏️ Editar cliente"):

            nuevo_nombre = st.text_input(
                "Nombre",
                value=nombre,
                key=f"edit_nombre_{cliente_id}"
            )

            nuevo_telefono = st.text_input(
                "Teléfono",
                value=telefono if telefono else "",
                key=f"edit_telefono_{cliente_id}"
            )

            nuevo_rnc = st.text_input(
                "RNC",
                value=rnc if rnc else "",
                key=f"edit_rnc_{cliente_id}"
            )

            nueva_direccion = st.text_input(
                "Dirección",
                value=direccion if direccion else "",
                key=f"edit_direccion_{cliente_id}"
            )

            nueva_ubicacion = st.text_input(
                "Link de Google Maps",
                value=ubicacion if ubicacion else "",
                key=f"edit_ubicacion_{cliente_id}"
            )

            if st.button("💾 Guardar cambios", key=f"guardar_cliente_{cliente_id}"):

                lat_nueva, lon_nueva = obtener_coordenadas(
                    nueva_direccion,
                    nueva_ubicacion
                )

                cursor.execute("""
                    UPDATE clientes
                    SET nombre = %s,
                        telefono = %s,
                        rnc = %s,
                        direccion = %s,
                        ubicacion = %s,
                        latitud = %s,
                        longitud = %s
                    WHERE id = %s
                """, (
                    nuevo_nombre,
                    nuevo_telefono,
                    nuevo_rnc,
                    nueva_direccion,
                    nueva_ubicacion,
                    lat_nueva,
                    lon_nueva,
                    cliente_id
                ))

                conn.commit()

                st.success("Cliente actualizado correctamente.")
                st.rerun()