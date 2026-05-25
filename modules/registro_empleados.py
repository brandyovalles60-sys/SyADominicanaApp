import streamlit as st
import bcrypt
from database.conexion import conectar


def pagina_registro_empleados():

    st.title("📝 Registro de empleados")
    st.write("Crea tu usuario. El jefe o admin debe aprobar tu acceso.")

    nombre = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")

    puesto = st.selectbox(
        "Puesto solicitado",
        ["vendedor", "almacen", "repartidor"]
    )

    if st.button("Crear cuenta", width="stretch"):

        if nombre.strip() == "" or password.strip() == "":
            st.error("Debes llenar usuario y contraseña.")
            return

        password_hash = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO usuarios (username, password, rol, activo, puesto)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                nombre,
                password_hash,
                "pendiente",
                False,
                puesto
            ))

            conn.commit()
            st.success("Cuenta creada. Espera aprobación del jefe/admin.")

        except Exception as e:
            conn.rollback()
            st.error(f"Error creando usuario: {e}")