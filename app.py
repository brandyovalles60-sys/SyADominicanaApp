import streamlit as st
from database.conexion import conectar
import bcrypt
from PIL import Image

# IMPORTAR MÓDULOS
from modules.clientes import mostrar_clientes
from modules.inventario import pagina_inventario
from modules.ordenes import pagina_ordenes
from modules.distribucion import pagina_distribucion
from modules.almacen import pagina_almacen
from modules.degustacion import pagina_degustacion
from modules.dashboard import pagina_dashboard
from modules.mapa_clientes import pagina_mapa
from modules.control_usuarios import pagina_control_usuarios
from modules.documentos import pagina_documentos
from modules.configuracion import pagina_configuracion
from modules.registro_empleados import pagina_registro_empleados
from utils.estilos import cargar_estilos
from modules.bloc_diario import pagina_bloc_diario
from modules.calendario import pagina_calendario
from modules.finanzas import pagina_finanzas
from modules.historial_clientes import pagina_historial_clientes
from modules.idiomas import IDIOMAS
from modules.auditoria import pagina_auditoria


# CONFIGURACIÓN
st.set_page_config(page_title="SyA Dominicana", layout="wide")
cargar_estilos()


# CONEXIÓN
conn = conectar()




# LOGIN
def login():

    st.markdown("""
    <style>
    header {visibility:hidden;}

    .block-container {
        padding-top: 0 !important;
        max-width: 720px !important;
    }

    .stApp {
        background-image:
            linear-gradient(rgba(0,0,0,0.50), rgba(0,0,0,0.78)),
            url("https://raw.githubusercontent.com/brandyovalles60-sys/SyADominicanaApp/main/assets/login-bg.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .login-panel {
        max-width: 520px;
        margin: 10vh auto 25px auto;
        padding: 32px;
        border-radius: 28px;
        background: rgba(5, 8, 15, 0.82);
        border: 1px solid rgba(160, 20, 20, 0.45);
        box-shadow: 0 0 45px rgba(160, 20, 20, 0.28);
        backdrop-filter: blur(14px);
        text-align: center;
    }

    .login-logo img {
        width: 170px;
        margin-bottom: 22px;
        filter: drop-shadow(0 0 18px rgba(180,0,0,0.45));
        animation: logoFloat 4s ease-in-out infinite;
    }

    @keyframes logoFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }

    .login-title {
        color: white;
        font-size: 34px;
        font-weight: 900;
        margin-bottom: 6px;
    }

    .login-small {
        color: #d1d5db;
        font-size: 16px;
    }

    div[data-testid="stTextInput"] {
        max-width: 520px;
        margin: auto;
    }

    div[data-testid="stTextInput"] input {
        background: rgba(8, 12, 20, 0.88) !important;
        border: 1px solid rgba(120, 120, 140, 0.35) !important;
        border-radius: 14px !important;
        color: white !important;
        height: 48px !important;
    }

    .stButton {
        max-width: 520px;
        margin: auto;
    }

    .stButton > button {
        background: rgba(8, 12, 20, 0.88) !important;
        color: white !important;
        border: 1px solid rgba(180, 40, 40, 0.45) !important;
        border-radius: 14px !important;
        height: 46px !important;
        font-weight: 800 !important;
        transition: all .25s ease-in-out;
    }

    .stButton > button:hover {
        background: rgba(90, 10, 10, 0.92) !important;
        transform: translateY(-2px);
        box-shadow: 0 0 22px rgba(180, 40, 40, 0.35) !important;
    }
    </style>

    <div class="login-panel">
        <div class="login-logo">
            <img src="https://raw.githubusercontent.com/brandyovalles60-sys/SyADominicanaApp/main/assets/sya-logo-premium.png">
        </div>
        <div class="login-title">Iniciar sesión</div>
        <div class="login-small">Sistema profesional de distribución de vinos</div>
    </div>
    """, unsafe_allow_html=True)

    usuario = st.text_input("Usuario", autocomplete="username")
    password = st.text_input("Contraseña", type="password", autocomplete="current-password")

    if st.button("🚀 Entrar al sistema", width="stretch"):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT username, password, rol, activo
            FROM usuarios
            WHERE username = %s
        """, (usuario,))

        user = cursor.fetchone()

        if user:
            activo = user[3]
            db_rol = user[2]

            if not activo and db_rol not in ["admin", "jefe"]:
                st.error("Tu cuenta todavía no ha sido aprobada.")
                return

            if bcrypt.checkpw(password.encode(), user[1].encode()):
                st.session_state["login"] = True
                st.session_state["usuario"] = str(user[0]).strip()
                st.session_state["rol"] = str(user[2]).strip().lower()
                st.success("Bienvenido al sistema")
                st.rerun()
            else:
                st.error("Contraseña incorrecta")

    if st.button("📝 Registrarme como empleado", width="stretch"):
        st.session_state["modo_registro"] = True
        st.rerun()


    

   
    


    

if "modo_registro" not in st.session_state:
    st.session_state["modo_registro"] = False



if st.session_state["modo_registro"]:
    pagina_registro_empleados()

    if st.button("⬅️ Volver al login"):
        st.session_state["modo_registro"] = False
        st.rerun()

    st.stop()


# CONTROL DE SESIÓN
if "login" not in st.session_state:
    st.session_state["login"] = False

if not st.session_state["login"]:
    login()
    st.stop()


# TÍTULO PRINCIPAL
st.title("🍷 SyA Dominicana")
st.write("Sistema de gestión de distribución de vinos")

idioma_actual = st.session_state.get("idioma", "Español")

TXT = IDIOMAS[idioma_actual]


# ROLES Y MENÚ
rol = st.session_state["rol"]

if rol == "admin" or rol == "jefe":

    menu = [

        TXT["clientes"],
        TXT["inventario"],
        TXT["ordenes"],
        TXT["preparar_pedidos"],
        TXT["distribucion"],
        TXT["degustacion"],
        TXT["dashboard"],
        TXT["mapa"],
        TXT["control_usuarios"],
        TXT["documentos"],
        TXT["configuracion"],
        TXT["bloc"],
        TXT["calendario"],
        TXT["finanzas"],
        TXT["historial_clientes"],
        TXT["auditoria"]

    ]

elif rol == "vendedor":

    menu = [
        TXT["clientes"],
        TXT["ordenes"],
        TXT["bloc"],
        TXT["calendario"]
    ]

elif rol == "almacen":

    menu = [
        TXT["inventario"],
        "Preparar pedidos"
    ]

elif rol == "repartidor":

    menu = [
        TXT["distribucion"]
    ]


# SELECTOR DE MENÚ
st.sidebar.markdown("### 📌 Módulos")

if "opcion_menu" not in st.session_state:
    st.session_state["opcion_menu"] = menu[0]

for item in menu:
    if item != TXT["configuracion"]:
        if st.sidebar.button(item, width="stretch"):
            st.session_state["opcion_menu"] = item

st.sidebar.divider()

with st.sidebar.expander("☰ Opciones"):
    if st.button("⚙️ Configuración", width="stretch"):
        st.session_state["opcion_menu"] = TXT["configuracion"]

    if st.button("🚪 Cerrar sesión", width="stretch"):
        st.session_state["login"] = False
        st.session_state["usuario"] = ""
        st.session_state["rol"] = ""
        st.session_state["modo_registro"] = False
        st.rerun()

opcion = st.session_state["opcion_menu"]


# NAVEGACIÓN
if opcion == TXT["clientes"]:
    mostrar_clientes(conn)

elif opcion == TXT["inventario"]:
    pagina_inventario()

elif opcion == TXT["ordenes"]:
    pagina_ordenes()

elif opcion == TXT["distribucion"]:
    pagina_distribucion()

elif opcion == TXT["degustacion"]:
    pagina_degustacion()

elif opcion == TXT["dashboard"]:
    pagina_dashboard()

elif opcion == TXT["documentos"]:
    pagina_documentos()

elif opcion == TXT["configuracion"]:
    pagina_configuracion()

elif opcion == TXT["bloc"]:
    pagina_bloc_diario()

elif opcion == TXT["calendario"]:
    pagina_calendario()

elif opcion == TXT["finanzas"]:
    pagina_finanzas()

elif opcion == TXT["historial_clientes"]:
    pagina_historial_clientes()

elif opcion == TXT["preparar_pedidos"]:
    pagina_almacen()

elif opcion == TXT["mapa"]:
    pagina_mapa()

elif opcion == TXT["control_usuarios"]:
    pagina_control_usuarios()

elif opcion == TXT["auditoria"]:
    pagina_auditoria()