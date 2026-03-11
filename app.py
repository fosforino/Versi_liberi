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

# Funzione per leggere l'immagine e convertirla in base64 (necessaria per lo sfondo CSS)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# --- STILE CSS GLOBALE ---
def apply_global_style():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

        .stApp, [data-testid="stSidebar"] { 
            background-color: #fdf5e6 !important; 
            color: #3e2723 !important; 
            font-family: 'EB Garamond', serif !important; 
        }

        [data-testid="stSidebarContent"] {
            background-color: #f5f1e8 !important;
            border-right: 1px solid #d7ccc8;
        }

        .poetic-title { 
            font-family: 'Playfair Display', serif; 
            font-size: 3.5rem; 
            text-align: center; 
            color: #3e2723; 
            margin-top: -10px;
            margin-bottom: 10px;
        }

        div.stButton > button { 
            background-color: #3e2723 !important; 
            color: #fdf5e6 !important; 
            border: 1px solid #c19a6b !important; 
            font-family: 'Playfair Display', serif !important; 
            transition: 0.3s all ease;
            border-radius: 8px !important;
        }
        
        div.stButton > button:hover {
            background-color: #c19a6b !important; 
            color: #3e2723 !important; 
        }

        .codice-onore {
            background-color: rgba(245, 241, 232, 0.8);
            padding: 15px;
            border-left: 5px solid #3e2723;
            border-radius: 4px;
            font-style: italic;
            margin: 15px 0;
        }

        /* Trucco per fondere il logo centrale con la pergamena */
        .blend-logo img {
            mix-blend-mode: multiply;
            filter: contrast(110%);
        }
    </style>
    """, unsafe_allow_html=True)

def apply_login_background(image_path):
    img_base64 = get_base64_image(image_path)
    if img_base64:
        st.markdown(
            f"""
            <style>
            /* Forza lo sfondo su tutta l'app */
            .stApp {{
                background: 
                    linear-gradient(rgba(253, 245, 230, 0.8), rgba(253, 245, 230, 0.8)), 
                    url("data:image/png;base64,{img_base64}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            
            /* Rende l'area del logo trasparente per far vedere la filigrana sotto */
            [data-testid="stVerticalBlock"] {{
                background-color: transparent !important;
            }}

            /* Miglioriamo la fusione del logo centrale */
            .blend-logo img {{
                mix-blend-mode: darken; /* Meglio di multiply per i bianchi sporchi */
                background-color: transparent !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

def esegui_logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

apply_global_style()

path_icona = "Poeticamente.png" 

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    apply_login_background(path_icona)

    # --- SCHERMATA DI LOGIN ---
    col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 0.8, 1])
    with col_logo_2:
        if os.path.exists(path_icona):
            # Inseriamo il logo dentro un div con la classe 'blend-logo'
            st.markdown('<div class="blend-logo">', unsafe_allow_html=True)
            st.image(path_icona)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1 class='poetic-title'>Poeticamente</h1>", unsafe_allow_html=True)
    
    col_mid_1, col_mid_2, col_mid_3 = st.columns([1, 1.5, 1])
    
    with col_mid_2:
        st.markdown("<h3 style='text-align: center; font-family: Playfair Display;'>Identificazione del Poeta</h3>", unsafe_allow_html=True)
        
        nuovo_pseudo = st.text_input("Scegli il tuo Pseudonimo:")
        password_segreta = st.text_input("Chiave d'Accesso:", type="password")
        
        st.markdown("""
        <div class='codice-onore'>
            <strong>📜 Codice d'Onore:</strong><br>
            Prometto di onorare l'arte della parola, di rispettare gli altri poeti 
            e di non affidare il mio cuore a fredde automazioni.
        </div>
        """, unsafe_allow_html=True)
        
        accetto_codice = st.checkbox("Giuro solennemente di rispettarlo")
        captcha_input = st.text_input("Completa il verso: 'Nel mezzo del cammin di nostra...'")

        if st.button("Entra nello Scrittoio"):
            if (nuovo_pseudo.strip() and 
                password_segreta == "Ermetico_2026" and 
                accetto_codice and 
                captcha_input.strip().lower() == "vita"):
                
                st.session_state.authenticated = True
                st.session_state.utente = nuovo_pseudo.strip()
                st.rerun()
            else:
                st.error("L'accesso è negato. Verifica la Chiave o la sfida.")
    st.stop()

# --- INTERFACCIA PRINCIPALE (Appare solo dopo il login) ---
with st.sidebar:
    if os.path.exists(path_icona):
        st.image(path_icona, width=150)
    st.markdown(f"<h2 style='text-align: center;'>Poeta:<br>{st.session_state.utente}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.sidebar.radio("Scegli la tua meta:", ["Home", "Scrittoio", "Bacheca"])
    
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("Congeda il Profilo"):
        esegui_logout()

# Caricamento Pagine
if page == "Home": 
    Home.show()
elif page == "Scrittoio": 
    Scrittoio.show()
elif page == "Bacheca": 
    Bacheca.show()