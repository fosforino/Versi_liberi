import streamlit as st
from Pages import Home, Scrittoio, Bacheca

# Configurazione obbligatoria (prima riga)
st.set_page_config(page_title="Poeticamente", page_icon="✒️", layout="wide")

def apply_rough_parchment():
    st.markdown("""
    <style>
        /* SFONDO PERGAMENA RUVIDA GLOBALE */
        .stApp { 
            background-color: #f4ecd8 !important;
            background-image: url("https://www.transparenttextures.com/patterns/parchment.png") !important;
            background-attachment: fixed !important;
        }

        /* STILE SIDEBAR */
        [data-testid="stSidebar"] {
            background-color: rgba(62, 39, 35, 0.05) !important;
            border-right: 1px solid #c19a6b;
        }

        /* TITOLI ANTICATI */
        h1, h2, h3 {
            color: #3e2723 !important;
            font-family: 'EB Garamond', serif !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    apply_rough_parchment()
    
    if "utente" not in st.session_state:
        st.session_state.utente = None

    st.sidebar.title("📜 Navigazione")
    pagina = st.sidebar.radio("Vai a:", ["Home", "Scrittoio", "Bacheca"])

    if pagina == "Home":
        Home.show()
    elif pagina == "Scrittoio":
        Scrittoio.show()
    elif pagina == "Bacheca":
        Bacheca.show()

if __name__ == "__main__":
    main()