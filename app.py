import streamlit as st
from Pages import Home, Scrittoio, Bacheca

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(
    page_title="Poeticamente", 
    page_icon="🖋️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STILE CSS GLOBALE (L'ANIMA DI POETICAMENTE) ---
def apply_global_style():
    st.markdown("""
    <style>
        /* Importazione Font Eleganti */
        @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

        /* Sfondo Pergamena Totale (App e Sidebar) */
        .stApp, [data-testid="stSidebar"] { 
            background-color: #fdf5e6 !important; 
            color: #2b1d0e !important; 
            font-family: 'EB Garamond', serif !important; 
        }

        /* Testi della Sidebar */
        [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p {
            color: #4b3621 !important;
            font-family: 'Playfair Display', serif !important;
        }

        /* Titolo Poetico Login */
        .poetic-title { 
            font-family: 'Playfair Display', serif; 
            font-size: 4rem; 
            text-align: center; 
            color: #2b1d0e; 
            margin-top: -20px;
            margin-bottom: 20px;
        }

        /* Bottoni Stile Antico (Inchiostro su Carta) */
        div.stButton > button { 
            background-color: #4b3621 !important; 
            color: #fdf5e6 !important; 
            border: 1px solid #d4af37 !important; 
            font-family: 'Playfair Display', serif !important; 
            border-radius: 4px !important;
            padding: 0.5rem 2rem !important;
            transition: 0.3s all ease;
        }
        
        div.stButton > button:hover {
            background-color: #2b1d0e !important;
            border-color: #fdf5e6 !important;
            transform: scale(1.02);
        }

        /* Nascondi Elementi Standard Streamlit */
        #MainMenu, footer, header {visibility: hidden;}

        /* Box Codice d'Onore */
        .codice-onore { 
            background-color: #f4ece0; 
            padding: 20px; 
            border-left: 5px solid #d4af37; 
            border-radius: 4px;
            font-style: italic; 
            margin: 20px 0; 
            color: #5d4037;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        }

        /* Input Fields personalizzati */
        .stTextInput input, .stTextArea textarea {
            background-color: #fffaf0 !important;
            border: 1px solid #d2b48c !important;
            color: #2b1d0e !important;
        }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE LOGOUT ---
def esegui_logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- ESECUZIONE STILE ---
apply_global_style()

# --- GESTIONE ACCESSO ---
if "utente" not in st.session_state:
    st.session_state.utente = None

if st.session_state.utente is None:
    # --- PAGINA DI LOGIN / IDENTIFICAZIONE ---
    st.markdown("<h1 class='poetic-title'>Poeticamente 🖋️</h1>", unsafe_allow_html=True)
    
    col_mid_1, col_mid_2, col_mid_3 = st.columns([1, 2, 1])
    
    with col_mid_2:
        st.markdown("<h3 style='text-align: center;'>Identificazione del Poeta</h3>", unsafe_allow_html=True)
        nuovo_pseudo = st.text_input("Scegli il tuo Pseudonimo:")
        email_utente = st.text_input("La tua Email (per l'invio dei versi):")
        
        st.markdown("""
        <div class='codice-onore'>
            <strong>📜 Codice d'Onore:</strong><br>
            Prometto di onorare l'arte della parola, di rispettare gli altri poeti 
            e di non affidare il mio cuore a fredde automazioni.
        </div>
        """, unsafe_allow_html=True)
        
        accetto_codice = st.checkbox("Giuro solennemente di rispettarlo")
        
        st.markdown("---")
        st.write("#### Sfida di Verità")
        captcha_input = st.text_input("Completa il verso: 'Nel mezzo del cammin di nostra...'")

        if st.button("Entra nello Scrittoio", use_container_width=True):
            # Controllo validazione (Dante approverebbe)
            if nuovo_pseudo.strip() and email_utente.strip() and accetto_codice and captcha_input.strip().lower() == "vita":
                st.session_state.utente = nuovo_pseudo.strip()
                st.rerun()
            else:
                st.error("Il calamaio è ancora vuoto o la sfida non è stata risolta. Verifica i dati.")
else:
    # --- INTERFACCIA PRINCIPALE (DOPO IL LOGIN) ---
    st.sidebar.markdown(f"<h2 style='text-align: center;'>Poeta:<br>{st.session_state.utente}</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio("Scegli la tua meta:", ["Home", "Scrittoio", "Bacheca"])

    # --- PULSANTE LOGOUT IN FONDO ALLA SIDEBAR ---
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("Congeda il Profilo", use_container_width=True):
        esegui_logout()

    # --- CARICAMENTO PAGINE DINAMICO ---
    if page == "Home": 
        Home.show()
    elif page == "Scrittoio": 
        Scrittoio.show()
    elif page == "Bacheca": 
        Bacheca.show()