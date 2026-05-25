import streamlit as st
import pandas as pd
import os
from datetime import datetime

archivo_bloc = "data/bloc_diario.csv"


def cargar_bloc():
    os.makedirs("data", exist_ok=True)

    if os.path.exists(archivo_bloc):
        return pd.read_csv(archivo_bloc)

    return pd.DataFrame(columns=[
        "Fecha",
        "Usuario",
        "Titulo",
        "Nota",
        "Importancia"
    ])


def guardar_bloc(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(archivo_bloc, index=False)


def pagina_bloc_diario():

    st.title("📝 Bloc Diario")
    st.write("Notas importantes de reuniones, clientes y seguimiento comercial.")

    df = cargar_bloc()

    with st.container(border=True):
        st.subheader("➕ Nueva nota")

        titulo = st.text_input("Título de la nota")
        nota = st.text_area("Escribe la nota de la reunión")
        importancia = st.selectbox(
            "Importancia",
            ["Normal", "Importante", "Urgente"]
        )

        if st.button("💾 Guardar nota", width="stretch"):

            if titulo.strip() == "" or nota.strip() == "":
                st.error("Debes llenar título y nota.")
                return

            nueva = {
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Usuario": st.session_state.get("usuario", "Desconocido"),
                "Titulo": titulo,
                "Nota": nota,
                "Importancia": importancia
            }

            df = pd.concat([df, pd.DataFrame([nueva])], ignore_index=True)
            guardar_bloc(df)

            st.success("Nota guardada correctamente.")
            st.rerun()

    st.divider()

    st.subheader("📚 Historial de notas")

    if df.empty:
        st.info("No hay notas registradas.")
        return

    filtro = st.selectbox(
        "Filtrar por importancia",
        ["Todas", "Normal", "Importante", "Urgente"]
    )

    df_filtrado = df.copy()

    if filtro != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Importancia"] == filtro]

    for _, row in df_filtrado.sort_values(by="Fecha", ascending=False).iterrows():

        color = "#111827"

        if row["Importancia"] == "Importante":
            color = "#78350f"

        if row["Importancia"] == "Urgente":
            color = "#450a0a"

        st.markdown(f"""
        <div style="
            background:{color};
            border:1px solid rgba(220,38,38,0.35);
            border-radius:18px;
            padding:20px;
            margin-bottom:15px;
            box-shadow:0 0 18px rgba(220,38,38,0.18);
        ">
            <h3 style="color:white;">📝 {row['Titulo']}</h3>
            <p style="color:#9ca3af;">📅 {row['Fecha']} | 👤 {row['Usuario']} | 📌 {row['Importancia']}</p>
            <p style="color:white;font-size:16px;">{row['Nota']}</p>
        </div>
        """, unsafe_allow_html=True)