import streamlit as st
import pandas as pd
from database.conexion import conectar


def cargar_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, rol, activo, puesto
        FROM usuarios
        ORDER BY activo ASC, rol, username
    """)

    datos = cursor.fetchall()

    return pd.DataFrame(datos, columns=[
        "ID",
        "Usuario",
        "Rol",
        "Activo",
        "Puesto solicitado"
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


def eliminar_usuario(usuario_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM usuarios
        WHERE id = %s
    """, (usuario_id,))

    conn.commit()


def pagina_control_usuarios():

    st.title("👑 Control de usuarios")
    st.write("Administra empleados, roles y accesos al sistema.")

    usuarios = cargar_usuarios()

    if usuarios.empty:
        st.info("No hay usuarios registrados.")
        return

    total = len(usuarios)
    activos = len(usuarios[usuarios["Activo"] == True])
    pendientes = len(usuarios[usuarios["Activo"] == False])

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Usuarios", total)
    col2.metric("✅ Activos", activos)
    col3.metric("⏳ Pendientes", pendientes)

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
                    ["vendedor", "almacen", "repartidor", "admin", "jefe"],
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
                st.markdown(f"### 👤 {row['Usuario']}")
                st.write(f"Rol actual: **{row['Rol']}**")

                nuevo_rol = st.selectbox(
                    "Cambiar rol",
                    ["vendedor", "almacen", "repartidor", "admin", "jefe"],
                    index=["vendedor", "almacen", "repartidor", "admin", "jefe"].index(row["Rol"])
                    if row["Rol"] in ["vendedor", "almacen", "repartidor", "admin", "jefe"]
                    else 0,
                    key=f"rol_activo_{row['ID']}"
                )

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