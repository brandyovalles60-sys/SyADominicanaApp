import streamlit as st
import bcrypt
import re
from database.conexion import conectar


CODIGO_EMPRESA = "SYA2026"


def password_segura(password):
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"[0-9]", password)
    )


def pagina_registro_empleados():

    st.title("📝 Registro de empleados")
    st.write("Completa tus datos. El jefe o admin debe aprobar tu acceso.")

    nombre_completo = st.text_input("Nombre completo")
    cedula = st.text_input("Cédula")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo")
    username = st.text_input("Nombre de usuario")

    puesto = st.selectbox(
        "Puesto solicitado",
        ["vendedor", "almacen", "repartidor"]
    )

    password = st.text_input("Contraseña", type="password")
    confirmar = st.text_input("Confirmar contraseña", type="password")
    codigo = st.text_input("Código de empresa", type="password")

    if st.button("Crear solicitud de acceso", width="stretch"):

        if not all([
            nombre_completo.strip(),
            cedula.strip(),
            telefono.strip(),
            correo.strip(),
            username.strip(),
            password.strip(),
            confirmar.strip(),
            codigo.strip()
        ]):
            st.error("Debes llenar todos los campos.")
            return

        if codigo != CODIGO_EMPRESA:
            st.error("Código de empresa incorrecto.")
            return

        if password != confirmar:
            st.error("Las contraseñas no coinciden.")
            return

        if not password_segura(password):
            st.error("La contraseña debe tener mínimo 8 caracteres, mayúscula, minúscula y número.")
            return

        password_hash = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO usuarios (
                    username,
                    password,
                    rol,
                    activo,
                    puesto,
                    nombre_completo,
                    cedula,
                    telefono,
                    correo
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                username.strip(),
                password_hash,
                "pendiente",
                False,
                puesto,
                nombre_completo.strip(),
                cedula.strip(),
                telefono.strip(),
                correo.strip()
            ))

            conn.commit()
            st.success("Solicitud enviada. Espera aprobación del jefe/admin.")

        except Exception as e:
            conn.rollback()
            st.error(f"Error creando solicitud: {e}")