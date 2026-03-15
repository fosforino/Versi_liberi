import streamlit as st
from Pages import Home, Scrittoio, Bacheca
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
    img_html = ""
    if img_base64:
        # Questo crea l'icona SFOCATA e GIGANTE sullo sfondo (Filigrana)
        img_html = f"""
        <img src="data:image/png;base64,{img_base64}" class="bg-watermark">
        """

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

        /* SFONDO PERGAMENA INCRESPATA */
        .stApp {{ 
            background-color: #fdf5e6;
            background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png");
            color: #3e2723 !important; 
            font-family: 'EB Garamond', serif !important; 
        }}

        /* L'ICONA POETICAMENTE COME FILIGRANA */
        .bg-watermark {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 70vw;
            opacity: 0.07; /* Appena visibile */
            filter: blur(8px); /* Effetto sfocato */
            z-index: -1;
            pointer-events: none;
        }}

        /* MENU E BOTTONI */
        div[data-baseweb="select"] > div {{
            background-color: #fdf5e6 !important;
            border: 1px solid #3e2723 !important;
            border-radius: 8px;
        }}
        
        div.stButton > button {{ 
            background-color: #3e2723 !important; 
            color: #fdf5e6 !important; 
            border: 1px solid #c19a6b !important; 
            font-family: 'Playfair Display', serif !important; 
            border-radius: 8px !important;
            transition: 0.3s all ease;
        }}
        
        .poetic-title {{ 
            font-family: 'Playfair Display', serif; 
            font-size: 4rem; 
            text-align: center; 
            color: #3e2723; 
            margin-top: -50px;
        }}
    </style>
    {img_html}
    """, unsafe_allow_html=True)

def esegui_logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- AVVIO STILE ---
path_icona = "Poeticamente.png" 
apply_global_style(path_icona)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- LOGICA DI ACCESSO ---
if not st.session_state.authenticated:
    # Mostriamo l'icona nitida solo nel login, sopra la filigrana
    col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 0.6, 1])
    with col_logo_2:
        if os.path.exists(path_icona):
            st.image(path_icona, use_container_width=True)
    
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

# --- SIDEBAR E NAVIGAZIONE (DOPO LOGIN) ---
with st.sidebar:
    if os.path.exists(path_icona):
        st.image(path_icona, width=150)
    st.markdown(f"<h2 style='text-align: center; color: #3e2723;'>Poeta:<br>{st.session_state.utente}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Scegli la tua meta:", ["Home", "Scrittoio", "Bacheca"])
    st.markdown("---")
    if st.button("Congeda il Profilo"):
        esegui_logout()

# --- NAVIGAZIONE PAGINE ---
if page == "Home": Home.show()
elif page == "Scrittoio": Scrittoio.show()
elif page == "Bacheca": Bacheca.show()streamlit run app.py