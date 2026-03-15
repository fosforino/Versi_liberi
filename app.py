import streamlit as st
from pages import Home, Scrittoio, Bacheca, Archivio
import os
import base64

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(
    page_title="Poeticamente", 
    page_icon="🖋️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def apply_global_style(image_path):
    img_base64 = get_base64_image(image_path)
    
    if img_base64:
        st.markdown(f"""
            <img src="data:image/png;base64,{img_base64}" class="bg-watermark">
        """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

        .stApp { 
            background-color: #fdf5e6 !important;
            background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png") !important;
            color: #3e2723 !important; 
            font-family: 'EB Garamond', serif !important; 
        }

        .bg-watermark {
            position: fixed;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 70vw; opacity: 0.07; filter: blur(8px);
            z-index: -1; pointer-events: none;
        }

        [data-testid="stSidebarNav"] { display: none; }

        @media (min-width: 992px) {
            section[data-testid="stSidebar"] {
                width: 260px !important;
                min-width: 260px !important;
            }
        }

        .main .block-container {
            max-width: 1000px;
            padding-top: 2rem;
            margin: auto;
        }

        div.stButton > button { 
            background-color: #3e2723 !important; 
            color: #fdf5e6 !important; 
            border: 1px solid #c19a6b !important; 
            border-radius: 8px !important;
        }
        
        .poetic-title { 
            font-family: 'Playfair Display', serif; 
            font-size: 4rem; text-align: center; 
            color: #3e2723; margin-top: -20px;
        }
    </style>
    """, unsafe_allow_html=True)

def esegui_logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

path_icona = "Poeticamente.png" 
apply_global_style(path_icona)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- LOGICA DI ACCESSO ---
if not st.session_state.authenticated:
    st.markdown("<style>[data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)
    
    col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 0.6, 1])
    with col_logo_2:
        if os.path.exists(path_icona):
            # FIX: rimosso use_container_width per conformità 2026
            st.image(path_icona, width=250)
    
    st.markdown("<h1 class='poetic-title'>Poeticamente</h1>", unsafe_allow_html=True)
    
    col_mid_1, col_mid_2, col_mid_3 = st.columns([1, 1.2, 1])
    with col_mid_2:
        st.markdown("<h3 style='text-align: center; color: #3e2723;'>Identificazione del Poeta</h3>", unsafe_allow_html=True)
        nuovo_pseudo = st.text_input("Scegli il tuo Pseudonimo:")
        password_segreta = st.text_input("Chiave d'Accesso:", type="password")
        accetto_codice = st.checkbox("Giuro solennemente di rispettare il Codice d'Onore")
        captcha_input = st.text_input("Completa: 'Nel mezzo del cammin di nostra...'")

        if st.button("Entra nello Scrittoio"):
            if (nuovo_pseudo.strip() and password_segreta == "Ermetico_2026" and 
                accetto_codice and captcha_input.strip().lower() == "vita"):
                st.session_state.authenticated = True
                st.session_state.utente = nuovo_pseudo.strip()
                st.rerun()
            else:
                st.error("La chiave o il giuramento non sono validi.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists(path_icona):
        st.image(path_icona, width=150)
    st.markdown(f"<h2 style='text-align: center; color: #3e2723;'>Poeta:<br>{st.session_state.utente}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.sidebar.radio("Scegli la tua meta:", ["Home", "Scrittoio", "Bacheca", "Archivio"])
    st.markdown("---")
    if st.button("Congeda il Profilo"):
        esegui_logout()

# --- NAVIGAZIONE ---
if page == "Home": Home.show()
elif page == "Scrittoio": Scrittoio.show()
elif page == "Bacheca": Bacheca.show()
elif page == "Archivio": Archivio.show()