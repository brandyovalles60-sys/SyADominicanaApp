import streamlit as st
import pandas as pd
import os
import calendar
from datetime import datetime, date

archivo_calendario = "data/calendario.csv"


def cargar_calendario():
    os.makedirs("data", exist_ok=True)

    if os.path.exists(archivo_calendario):
        return pd.read_csv(archivo_calendario)

    return pd.DataFrame(columns=[
        "Fecha",
        "Tipo",
        "Titulo",
        "Cliente",
        "Descripcion",
        "Creado_por"
    ])


def guardar_calendario(df):
    os.makedirs("data", exist_ok=True)
    df.to_csv(archivo_calendario, index=False)


def agregar_evento(fecha, tipo, titulo, cliente, descripcion):
    df = cargar_calendario()

    nuevo = {
        "Fecha": fecha,
        "Tipo": tipo,
        "Titulo": titulo,
        "Cliente": cliente,
        "Descripcion": descripcion,
        "Creado_por": st.session_state.get("usuario", "Desconocido")
    }

    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    guardar_calendario(df)


def color_tipo(tipo):
    colores = {
        "Reunión": "#7c2d12",
        "Degustación": "#7f1d1d",
        "Entrega": "#064e3b",
        "Tarea": "#312e81"
    }
    return colores.get(tipo, "#111827")


def pagina_calendario():

    st.title("📅 Calendario Comercial")
    st.write("Agenda visual de degustaciones, reuniones, entregas y tareas.")

    st.markdown("""
    <style>
    .cal-card {
        background: rgba(17,24,39,0.92);
        border: 1px solid rgba(220,38,38,0.35);
        border-radius: 18px;
        padding: 16px;
        min-height: 135px;
        box-shadow: 0 0 18px rgba(220,38,38,0.15);
        transition: all .25s ease-in-out;
        animation: fadeIn .5s ease-in-out;
    }

    .cal-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 0 28px rgba(220,38,38,0.35);
        border-color: rgba(220,38,38,0.75);
    }

    .cal-day {
        color: white;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .event-pill {
        color: white;
        padding: 7px 10px;
        border-radius: 12px;
        margin-bottom: 7px;
        font-size: 13px;
        font-weight: 700;
    }

    .history-card {
        background: rgba(17,24,39,0.94);
        border: 1px solid rgba(220,38,38,0.35);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 0 18px rgba(220,38,38,0.18);
        animation: fadeIn .5s ease-in-out;
    }

    @keyframes fadeIn {
        from {opacity:0; transform:translateY(15px);}
        to {opacity:1; transform:translateY(0);}
    }
    </style>
    """, unsafe_allow_html=True)

    df = cargar_calendario()

    # -------------------------
    # FORMULARIO
    # -------------------------
    with st.container(border=True):
        st.subheader("➕ Agregar fecha importante")

        col1, col2 = st.columns(2)

        with col1:
            fecha = st.date_input("Fecha")
            tipo = st.selectbox("Tipo", ["Reunión", "Degustación", "Entrega", "Tarea"])

        with col2:
            titulo = st.text_input("Título")
            cliente = st.text_input("Cliente")

        descripcion = st.text_area("Descripción")

        if st.button("💾 Guardar evento", width="stretch"):

            if titulo.strip() == "":
                st.error("Debes escribir un título.")
                return

            agregar_evento(
                fecha.strftime("%Y-%m-%d"),
                tipo,
                titulo,
                cliente,
                descripcion
            )

            st.success("Evento guardado correctamente.")
            st.rerun()

    st.divider()

    # -------------------------
    # CALENDARIO VISUAL
    # -------------------------
    st.subheader("🗓️ Calendario mensual")

    hoy = date.today()

    col_mes, col_ano = st.columns(2)

    with col_mes:
        mes = st.selectbox(
            "Mes",
            list(range(1, 13)),
            index=hoy.month - 1,
            format_func=lambda x: calendar.month_name[x]
        )

    with col_ano:
        ano = st.number_input("Año", min_value=2024, max_value=2035, value=hoy.year)

    df_eventos = df.copy()

    if not df_eventos.empty:
        df_eventos["Fecha"] = pd.to_datetime(df_eventos["Fecha"], errors="coerce")

    cal = calendar.Calendar(firstweekday=0)
    semanas = cal.monthdatescalendar(int(ano), int(mes))

    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

    cols = st.columns(7)
    for i, d in enumerate(dias):
        cols[i].markdown(f"### {d}")

    for semana in semanas:
        cols = st.columns(7)

        for i, dia in enumerate(semana):

            eventos_dia = pd.DataFrame()

            if not df_eventos.empty:
                eventos_dia = df_eventos[
                    df_eventos["Fecha"].dt.date == dia
                ]

            contenido = f"""
            <div class="cal-card">
                <div class="cal-day">{dia.day}</div>
            """

            if dia.month != mes:
                contenido += "<p style='color:#6b7280;'>Fuera de mes</p>"
            else:
                if eventos_dia.empty:
                    contenido += "<p style='color:#6b7280;'>Sin eventos</p>"
                else:
                    for _, ev in eventos_dia.iterrows():
                        color = color_tipo(ev["Tipo"])
                        contenido += f"""
                        <div class="event-pill" style="background:{color};">
                            {ev["Tipo"]}: {ev["Titulo"]}
                        </div>
                        """

            contenido += "</div>"

            cols[i].markdown(contenido, unsafe_allow_html=True)

    st.divider()

    # -------------------------
    # HISTORIAL PREMIUM
    # -------------------------
    st.subheader("📚 Historial de eventos")

    if df.empty:
        st.info("No hay eventos registrados.")
        return

    filtro = st.selectbox(
        "Filtrar historial",
        ["Todos", "Reunión", "Degustación", "Entrega", "Tarea"]
    )

    historial = df.copy()

    if filtro != "Todos":
        historial = historial[historial["Tipo"] == filtro]

    historial["Fecha"] = pd.to_datetime(historial["Fecha"], errors="coerce")
    historial = historial.sort_values(by="Fecha", ascending=True)

    for _, row in historial.iterrows():

        color = color_tipo(row["Tipo"])

        st.markdown(f"""
        <div class="history-card">
            <h3 style="color:white;">📌 {row['Titulo']}</h3>
            <p style="color:#fca5a5;">
                {row['Tipo']} | {row['Fecha'].strftime('%Y-%m-%d')}
            </p>
            <p style="color:white;">👤 Cliente: {row['Cliente']}</p>
            <p style="color:#d1d5db;">📝 {row['Descripcion']}</p>
            <p style="color:#9ca3af;">Creado por: {row['Creado_por']}</p>
        </div>
        """, unsafe_allow_html=True)