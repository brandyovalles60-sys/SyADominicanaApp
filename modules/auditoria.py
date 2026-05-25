import pandas as pd
import os
from datetime import datetime
import streamlit as st

archivo_auditoria = "data/auditoria.csv"


def registrar_accion(modulo, accion, detalle=""):
    os.makedirs("data", exist_ok=True)

    nuevo = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Usuario": st.session_state.get("usuario", "Desconocido"),
        "Rol": st.session_state.get("rol", "Sin rol"),
        "Modulo": modulo,
        "Accion": accion,
        "Detalle": detalle
    }])

    if os.path.exists(archivo_auditoria):
        df = pd.read_csv(archivo_auditoria)
        df = pd.concat([df, nuevo], ignore_index=True)
    else:
        df = nuevo

    df.to_csv(archivo_auditoria, index=False)


def pagina_auditoria():
    st.title("🛡️ Auditoría del sistema")
    st.write("Historial de acciones realizadas por los usuarios.")

    if not os.path.exists(archivo_auditoria):
        st.info("Todavía no hay actividad registrada.")
        return

    df = pd.read_csv(archivo_auditoria)

    st.dataframe(
        df.sort_values(by="Fecha", ascending=False),
        width="stretch",
        hide_index=True
    )