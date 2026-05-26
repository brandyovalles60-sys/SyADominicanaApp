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

    /* =========================
    OCULTAR STREAMLIT
    ========================= */

    header {
        visibility: hidden;
    }

    .block-container{
        padding:0 !important;
        max-width:100% !important;
    }

    /* =========================
    FONDO ANIMADO
    ========================= */

    .stApp{

        background-image:
            linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.82)),
            url("https://raw.githubusercontent.com/brandyovalles60-sys/SyADominicanaApp/main/assets/login-bg.png");

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;

        animation:bgMove 18s ease-in-out infinite alternate;
    }

    /* MOVIMIENTO SUAVE DEL FONDO */

    @keyframes bgMove{

        0%{
            background-position:center top;
            transform:scale(1);
        }

        50%{
            background-position:center center;
            transform:scale(1.03);
        }

        100%{
            background-position:center bottom;
            transform:scale(1.05);
        }
    }

    /* EFECTO ROJO PREMIUM */

    .stApp::before{

        content:"";
        position:fixed;
        inset:0;

        background:
            radial-gradient(circle at 20% 30%, rgba(255,0,0,0.10), transparent 35%),
            radial-gradient(circle at 80% 70%, rgba(255,0,0,0.08), transparent 35%);

        animation:glowMove 10s ease-in-out infinite alternate;

        pointer-events:none;
    }

    @keyframes glowMove{

        0%{
            transform:translateY(0px);
            opacity:.6;
        }

        100%{
            transform:translateY(-20px);
            opacity:1;
        }
    }

    /* =========================
    LOGIN PANEL
    ========================= */

    .login-panel{

        max-width:430px;

        margin:8vh auto;

        padding:38px;

        border-radius:30px;

        background:rgba(5,8,15,0.82);

        border:1px solid rgba(255,0,0,0.25);

        backdrop-filter:blur(14px);

        box-shadow:
            0 0 40px rgba(255,0,0,0.18),
            0 0 80px rgba(255,0,0,0.08);

        animation:fadeIn 1s ease;
    }

    /* =========================
    LOGO
    ========================= */

    .login-logo{

        display:flex;
        justify-content:center;

        margin-bottom:18px;
    }

    .login-logo img{

        width:170px;

        filter:
            drop-shadow(0 0 15px rgba(255,0,0,0.45))
            drop-shadow(0 0 35px rgba(255,0,0,0.20));

        animation:logoFloat 4s ease-in-out infinite;
    }

    @keyframes logoFloat{

        0%{
            transform:translateY(0px);
        }

        50%{
            transform:translateY(-6px);
        }

        100%{
            transform:translateY(0px);
        }
    }

    /* =========================
    TITULOS
    ========================= */

    .login-title{

        text-align:center;

        color:white;

        font-size:42px;

        font-weight:900;

        margin-top:10px;
    }

    .login-small{

        text-align:center;

        color:#cbd5e1;

        font-size:15px;

        margin-bottom:28px;
    }

    /* =========================
    INPUTS
    ========================= */

    .stTextInput > div > div{

        background:rgba(10,15,25,0.92);

        border:1px solid rgba(255,255,255,0.08);

        border-radius:14px;

        transition:0.3s;

        box-shadow:none;
    }

    .stTextInput > div > div:hover{

        border:1px solid rgba(255,0,0,0.30);

        box-shadow:0 0 18px rgba(255,0,0,0.10);
    }

    .stTextInput input{

        color:white !important;

        font-size:16px;
    }

    /* =========================
    BOTONES
    ========================= */

    .stButton > button{

        width:100%;

        border-radius:14px;

        height:52px;

        border:none;

        font-size:16px;

        font-weight:700;

        transition:0.3s;

        margin-top:10px;

        background:linear-gradient(135deg,#0b1220,#111827);

        color:white;

        border:1px solid rgba(255,0,0,0.20);
    }

    /* BOTON PRINCIPAL */

    .stButton > button:hover{

        transform:translateY(-2px);

        border:1px solid rgba(255,0,0,0.45);

        box-shadow:
            0 0 20px rgba(255,0,0,0.18),
            0 0 35px rgba(255,0,0,0.10);

        background:linear-gradient(135deg,#111827,#1f2937);
    }

    /* =========================
    ANIMACION PANEL
    ========================= */

    @keyframes fadeIn{

        from{
            opacity:0;
            transform:translateY(20px);
        }

        to{
            opacity:1;
            transform:translateY(0px);
        }
    }

    </style>

    <div class="login-panel">

        <div class="login-logo">
            <img src="https://raw.githubusercontent.com/brandyovalles60-sys/SyADominicanaApp/main/assets/sya-logo-premium.png">
        </div>

        <div class="login-title">
            Iniciar sesión
        </div>

        <div class="login-small">
            Sistema profesional de distribución de vinos
        </div>

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