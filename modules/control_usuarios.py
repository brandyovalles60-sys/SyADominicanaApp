import streamlit as st
import pandas as pd
from database.conexion import conectar
import bcrypt


ROLES = ["vendedor", "almacen", "repartidor", "admin", "jefe"]


def cargar_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, rol, activo, puesto, pin_hash
        FROM usuarios
        ORDER BY activo ASC, rol, username
    """)

    datos = cursor.fetchall()
    cursor.close()
    conn.close()

    return pd.DataFrame(datos, columns=[
        "ID",
        "Usuario",
        "Rol",
        "Activo",
        "Puesto solicitado",
        "Pin Hash"
    ])


def actualizar_usuario(usuario_id, rol, activo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET rol = %s, activo = %s
        WHERE id = %s
    """, (rol, activo, usuario_id))

    conn.commit()
    cursor.close()
    conn.close()


def eliminar_usuario(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM usuarios
        WHERE id = %s
    """, (usuario_id,))

    conn.commit()
    cursor.close()
    conn.close()


def guardar_pin_usuario(usuario_id, username, pin):
    if not pin:
        st.error("Debes escribir un PIN.")
        return False

    if not pin.isdigit():
        st.error("El PIN debe tener solo números.")
        return False

    if len(pin) < 4:
        st.error("El PIN debe tener mínimo 4 números.")
        return False

    pin_hash = bcrypt.hashpw(
        pin.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET pin_hash = %s
        WHERE id = %s
    """, (pin_hash, usuario_id))

    conn.commit()
    cursor.close()
    conn.close()

    st.success(f"PIN asignado correctamente a {username}")
    return True


def pagina_control_usuarios():

    st.title("👑 Control de usuarios")
    st.write("Administra empleados, roles, accesos y PIN de seguridad.")

    usuarios = cargar_usuarios()

    if usuarios.empty:
        st.info("No hay usuarios registrados.")
        return

    total = len(usuarios)
    activos = len(usuarios[usuarios["Activo"] == True])
    pendientes = len(usuarios[usuarios["Activo"] == False])
    con_pin = len(usuarios[
        (usuarios["Activo"] == True) &
        (usuarios["Pin Hash"].notna())
    ])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Usuarios", total)
    col2.metric("✅ Activos", activos)
    col3.metric("⏳ Pendientes", pendientes)
    col4.metric("🔐 Con PIN", con_pin)

    st.divider()

    st.subheader("⏳ Usuarios pendientes de aprobación")

    pendientes_df = usuarios[usuarios["Activo"] == False]

    if pendientes_df.empty:
        st.success("No hay usuarios pendientes.")
    else:
        for _, row in pendientes_df.iterrows():

            with st.container(border=True):
                st.markdown(f"### 👤 {row['Usuario']}")
                st.write(f"📌 Puesto solicitado: **{row['Puesto solicitado']}**")

                rol_aprobado = st.selectbox(
                    "Asignar rol",
                    ROLES,
                    index=0,
                    key=f"rol_pendiente_{row['ID']}"
                )

                col_a, col_b = st.columns(2)

                with col_a:
                    if st.button("✅ Aprobar usuario", key=f"aprobar_{row['ID']}"):
                        actualizar_usuario(row["ID"], rol_aprobado, True)
                        st.success("Usuario aprobado correctamente.")
                        st.rerun()

                with col_b:
                    if st.button("🗑️ Eliminar solicitud", key=f"eliminar_pendiente_{row['ID']}"):
                        eliminar_usuario(row["ID"])
                        st.warning("Solicitud eliminada.")
                        st.rerun()

    st.divider()

    st.subheader("👥 Usuarios activos")

    activos_df = usuarios[usuarios["Activo"] == True]

    if activos_df.empty:
        st.info("No hay usuarios activos.")
    else:
        for _, row in activos_df.iterrows():

            with st.container(border=True):
                col_info, col_pin = st.columns([2, 1])

                with col_info:
                    st.markdown(f"### 👤 {row['Usuario']}")
                    st.write(f"Rol actual: **{row['Rol']}**")

                    if pd.notna(row["Pin Hash"]) and row["Pin Hash"]:
                        st.success("🔐 PIN configurado")
                    else:
                        st.warning("⚠️ PIN pendiente")

                    nuevo_rol = st.selectbox(
                        "Cambiar rol",
                        ROLES,
                        index=ROLES.index(row["Rol"]) if row["Rol"] in ROLES else 0,
                        key=f"rol_activo_{row['ID']}"
                    )

                with col_pin:
                    st.markdown("### 🔐 PIN")
                    pin_nuevo = st.text_input(
                        "Nuevo PIN",
                        type="password",
                        key=f"pin_{row['ID']}"
                    )

                    if st.button("💾 Guardar PIN", key=f"guardar_pin_{row['ID']}"):
                        if guardar_pin_usuario(row["ID"], row["Usuario"], pin_nuevo):
                            st.rerun()

                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    if st.button("💾 Guardar cambios", key=f"guardar_{row['ID']}"):
                        actualizar_usuario(row["ID"], nuevo_rol, True)
                        st.success("Usuario actualizado.")
                        st.rerun()

                with col_b:
                    if st.button("🚫 Desactivar", key=f"desactivar_{row['ID']}"):
                        actualizar_usuario(row["ID"], row["Rol"], False)
                        st.warning("Usuario desactivado.")
                        st.rerun()

                with col_c:
                    if st.button("🗑️ Eliminar", key=f"eliminar_{row['ID']}"):
                        eliminar_usuario(row["ID"])
                        st.error("Usuario eliminado.")
                        st.rerun()