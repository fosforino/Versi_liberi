import streamlit as st
import os
from supabase import create_client, Client

# 1. SETUP DELLA PAGINA
st.set_page_config(page_title="Poeticamente", page_icon="📝", layout="centered")

# 2. STILE ESTETICO (CSS)
st.markdown("""
<style>
.main { background-color: #fcfaf7; }
.stButton>button { width: 100%; border-radius: 20px; border: 1px solid #d4af37; background-color: white; color: #d4af37; height: 3em; }
.stButton>button:hover { background-color: #d4af37; color: white; }
.poesia-card { padding: 25px; border-left: 4px solid #d4af37; background-color: white; margin-bottom: 25px; border-radius: 0 10px 10px 0; box-shadow: 3px 3px 10px rgba(0,0,0,0.05); }
h1, h2, h3 { color: #4a4a4a; font-family: 'Georgia', serif; }
</style>
""", unsafe_allow_html=True)

# 3. TITOLO
st.title("Poeticamente")

# 4. CONNESSIONE AL DATABASE
@st.cache_resource
def init_connection():
    try:
        if "SUPABASE_URL" in st.secrets:
            return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        return None
    except Exception:
        return None

supabase = init_connection()

# 5. LOGICA DI LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🚧 Area in Manutenzione: accesso riservato.")
    with st.form("login_form"):
        email = st.text_input("Email")
        access_code = st.text_input("Codice di Accesso", type="password")
        if st.form_submit_button("Entra nello Scrittoio"):
            if access_code == "123456":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Codice errato.")
else:
    # 6. APP DOPO IL LOGIN
    st.sidebar.title("Menu")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    tab1, tab2 = st.tabs(["✍️ Scrittoio", "📖 La Bacheca"])
    
    with tab1:
        st.subheader("Crea un nuovo componimento")
        titolo = st.text_input("Titolo dell'opera")
        contenuto = st.text_area("I tuoi versi", height=300)
        
        if st.button("Pubblica nel Mondo"):
            if supabase and titolo and contenuto:
                try:
                    # Corretto: Tabella "Poesie" e colonna "versi" come da database
                    supabase.table("Poesie").insert({
                        "titolo": titolo, 
                        "versi": contenuto 
                    }).execute()
                    st.success("L'opera è stata pubblicata!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Errore: {e}")
            else:
                st.warning("Compila tutti i campi.")

    with tab2:
        st.subheader("Opere Recenti")
        if supabase:
            try:
                # Recupero dati ordinati per data
                response = supabase.table("Poesie").select("*").order("created_at", desc=True).execute()
                for p in response.data:
                    st.markdown(f"""
                    <div class="poesia-card">
                        <h3>{p['titolo']}</h3>
                        <p style="white-space: pre-wrap;">{p['versi']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception:
                st.info("Nessuna poesia ancora pubblicata.")