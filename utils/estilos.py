import streamlit as st


def cargar_estilos():
    st.markdown("""
    <style>

    .stApp {
        animation: fadeInApp 0.7s ease-in-out;
    }

    @keyframes fadeInApp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    div[data-testid="stMetric"] {
        background: rgba(17, 24, 39, 0.85);
        border: 1px solid rgba(220, 38, 38, 0.25);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 0 20px rgba(220, 38, 38, 0.12);
        transition: all 0.25s ease-in-out;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 0 30px rgba(220, 38, 38, 0.35);
        border-color: rgba(220, 38, 38, 0.65);
    }

    .stButton > button {
        border-radius: 14px;
        transition: all 0.25s ease-in-out;
        font-weight: 700;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 0 22px rgba(220, 38, 38, 0.35);
        border-color: #dc2626;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #020617 100%);
        border-right: 1px solid rgba(220, 38, 38, 0.25);
    }

    section[data-testid="stSidebar"] * {
        transition: all 0.2s ease-in-out;
    }

    div[data-testid="stDataFrame"] {
        animation: fadeInTable 0.6s ease-in-out;
    }

    @keyframes fadeInTable {
        from {
            opacity: 0;
            transform: scale(0.98);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    .premium-card {
        background: rgba(17, 24, 39, 0.90);
        border: 1px solid rgba(220, 38, 38, 0.30);
        border-radius: 22px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(220, 38, 38, 0.12);
        animation: cardFade 0.7s ease-in-out;
        transition: all 0.25s ease-in-out;
    }

    .premium-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 0 35px rgba(220, 38, 38, 0.30);
        border-color: rgba(220, 38, 38, 0.65);
    }

    @keyframes cardFade {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    input, textarea {
        transition: all 0.25s ease-in-out !important;
    }

    input:focus, textarea:focus {
        box-shadow: 0 0 18px rgba(220, 38, 38, 0.30) !important;
        border-color: #dc2626 !important;
    }
                

    /* Fondo general después del login */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(120, 0, 0, 0.35), transparent 35%),
        radial-gradient(circle at bottom right, rgba(80, 0, 0, 0.25), transparent 35%),
        linear-gradient(135deg, #050505 0%, #090909 45%, #160000 100%);
    background-attachment: fixed;
}

/* Menú lateral premium */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #1a0000 0%, #090909 45%, #020202 100%);
    border-right: 1px solid rgba(220, 38, 38, 0.35);
    box-shadow: 6px 0 25px rgba(0,0,0,0.35);
}

/* Tarjeta del select del menú */
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    border-radius: 14px;
    box-shadow: 0 0 18px rgba(220,38,38,0.18);
}

/* Texto del menú */
section[data-testid="stSidebar"] label {
    color: #f3f4f6 !important;
    font-weight: 700;
}

/* Área principal */
.block-container {
    padding-top: 3rem;
    animation: fadeInPage 0.6s ease-in-out;
}

@keyframes fadeInPage {
    from {
        opacity: 0;
        transform: translateY(14px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

    </style>
    """, unsafe_allow_html=True)