import streamlit as st
import requests
import json
from fpdf import FPDF
#from supabase import create_client, Client

# --- 1. CONFIGURAZIONE DATABASE (SUPABASE) ---
# Usiamo i dati che abbiamo configurato insieme
URL_SUPABASE = st.secrets["SUPABASE_URL"]
KEY_SUPABASE = st.secrets["SUPABASE_KEY"]

#if "supabase" not in st.session_state:
#    st.session_state.supabase = create_client(URL_SUPABASE, KEY_SUPABASE)

# --- 2. LOGICA BACKEND ---

def esporta_pdf(titolo, testo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, titolo.upper(), ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    testo_pulito = testo.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, testo_pulito, align='L')
    return pdf.output(dest="S")

def pubblica_opera(titolo, versi, link_yt, tag):
    utente = st.session_state.user
    payload = {
        "titolo": titolo,
        "versi": versi,
        "autore": utente.email,
        "youtube_link": link_yt,
        "tag": tag,
        "id_utente": utente.id,
        "likes": 0
    }
    try:
        st.session_state.supabase.table("poesie").insert(payload).execute()
        return True
    except Exception as e:
        st.error(f"Errore tecnico {e}")
        return False

# --- 3. INTERFACCIA E CSS ---
st.set_page_config(page_title="Versi Liberi", page_icon="✒️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display&family=EB+Garamond&display=swap');
    .stApp { background-color: #f5eedc; background-image: url("https://www.transparenttextures.com/patterns/natural-paper.png"); }
    [data-testid="stSidebar"] { background-color: #1a0f08 !important; }
    [data-testid="stSidebar"] * { color: #d4af37 !important; }
    .poesia-card { 
        background: white; padding: 30px; border-radius: 15px; border-left: 8px solid #d4af37; 
        margin-bottom: 30px; box-shadow: 5px 5px 15px rgba(0,0,0,0.05); font-family: 'EB Garamond', serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNZIONE LOGIN (CODICE MAGICO) ---
def schermata_login():
    st.markdown("<h1 style='text-align:center; font-family:Playfair Display;'>Versi Liberi</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Inserisci la tua email per ricevere il codice di accesso</p>", unsafe_allow_html=True)
    
    email = st.text_input("La tua Email", placeholder="poeta@esempio.it")
    if st.button("Invia Codice Magico"):
        if email:
            try:
                st.session_state.supabase.auth.sign_in_with_otp({"email": email})
                st.info("Controlla la tua posta! Ti abbiamo inviato il link per entrare")
            except Exception as e:
                st.error(f"Errore {e}")
        else:
            st.warning("Inserisci un email valida")

# --- 5. APP PRINCIPALE ---
def main_app():
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>Stanze</h2>", unsafe_allow_html=True)
        scelta = st.radio("", ["Scrittoio", "Bacheca", "Profilo"])
        if st.button("Esci"):
            st.session_state.supabase.auth.sign_out()
            del st.session_state.user
            st.rerun()

    if scelta == "Scrittoio":
        st.markdown("<h1 style='font-family:Playfair Display;'>✒️ Lo Scrittoio</h1>", unsafe_allow_html=True)
        titolo = st.text_input("Titolo dell opera", placeholder="L anima del vento...")
        tag = st.selectbox("Tema", ["Amore", "Natura", "Esistenza", "Libero"])
        testo = st.text_area("Inizia a scrivere i tuoi versi...", height=300)
        link_yt = st.text_input("Link YouTube (opzionale)")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 PUBBLICA IN BACHECA", use_container_width=True):
                if titolo and testo:
                    if pubblica_opera(titolo, testo, link_yt, tag):
                        st.success("L opera è ora immortale!")
                        st.balloons()
                else:
                    st.warning("Compila titolo e versi")
        with c2:
            if titolo and testo:
                raw_pdf = esporta_pdf(titolo, testo)
                st.download_button("📄 SCARICA PDF", data=bytes(raw_pdf), file_name=f"{titolo}.pdf", mime="application/pdf", use_container_width=True)

    elif scelta == "Bacheca":
        st.markdown("<h1 style='font-family:Playfair Display;'>📜 La Bacheca</h1>", unsafe_allow_html=True)
        try:
            res = st.session_state.supabase.table("poesie").select("*").order("created_at", desc=True).execute()
            for p in res.data:
                st.markdown(f"""
                <div class="poesia-card">
                    <h2>{p['titolo']}</h2>
                    <p style="color:#7d1d1d;">Tema: {p['tag']} | Scritta da {p['autore']}</p>
                    <div style="white-space: pre-wrap; font-size:1.2em;">{p['versi']}</div>
                </div>
                """, unsafe_allow_html=True)
                if p.get('youtube_link'):
                    st.video(p['youtube_link'])
        except:
            st.info("La bacheca è in attesa dei tuoi versi")

    elif scelta == "Profilo":
        st.header("👤 Il tuo Profilo")
        st.write(f"Poeta collegato: {st.session_state.user.email}")

# --- 6. CONTROLLO SESSIONE ---
try:
    session = st.session_state.supabase.auth.get_session()
    if session and session.user:
        st.session_state.user = session.user
        main_app()
    else:
        schermata_login()
except:
    schermata_login()