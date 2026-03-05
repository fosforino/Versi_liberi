import streamlit as st
from supabase import create_client
from fpdf import FPDF
import time

# --- CONFIGURAZIONE SUPABASE ---
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

# Parole vietate
parole_vietate = ["violenza", "odio", "anarchia", "terrorismo"]

def contiene_parole_vietate(testo):
    for parola in parole_vietate:
        if parola.lower() in testo.lower():
            return parola
    return None

def pubblica_opera(pseudonimo, titolo, versi):
    forbidden = contiene_parole_vietate(versi)
    if forbidden:
        st.error(f"❌ La parola '{forbidden}' è vietata. Modifica i versi per pubblicare.")
        return False

    # Inseriamo solo i campi utili, ignorando il resto
    data = {
        "titolo": titolo,
        "versi": versi,
        "autore": pseudonimo,
        "likes": 0,
        "tipo_account": "anonimo",
        "creat_ad": "now()"  # Supabase imposta timestamp automatico
    }

    try:
        supabase.table("Poesie").insert(data).execute()
        st.success("Opera salvata nell'Albo Poetico!")
        return True
    except Exception as e:
        st.error(f"Errore durante il salvataggio su Supabase: {e}")
        return False

def download_pdf(pseudonimo):
    res = supabase.table("Poesie").select("titolo, versi").eq("autore", pseudonimo).execute()
    poemi = res.data if res.data else []

    if not poemi:
        st.warning("Non ci sono poesie da scaricare.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for p in poemi:
        pdf.multi_cell(0, 8, f"{p['titolo']}\n{p['versi']}\n\n")

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    st.download_button("Scarica PDF", data=pdf_bytes, file_name="poesie.pdf", mime="application/pdf")

def show():
    st.header("Scrittoio 🖋️")
    pseudonimo = st.text_input("Inserisci il tuo pseudonimo")
    titolo = st.text_input("Titolo della poesia")
    versi = st.text_area("Scrivi i versi della tua poesia")

    if st.button("Pubblica"):
        if pseudonimo.strip() == "":
            st.error("Inserisci un pseudonimo prima di pubblicare.")
        elif titolo.strip() == "" or versi.strip() == "":
            st.error("Titolo e versi non possono essere vuoti.")
        else:
            pubblica_opera(pseudonimo, titolo, versi)

    if st.button("Scarica PDF"):
        download_pdf(pseudonimo)