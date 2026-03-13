import streamlit as st
from supabase import create_client
from fpdf import FPDF
from pydantic import BaseModel

class OperaSchema(BaseModel):
    titolo: str
    contenuto: str
    autore_email: str

def show():
    st.markdown("<style>.stApp { background-image: url('https://www.transparenttextures.com/patterns/parchment.png') !important; }</style>", unsafe_allow_html=True)
    
    # Connessione sicura
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    nome = st.session_state.get("utente")
    if not nome:
        st.warning("Torna nella Home per identificarti.")
        return

    st.markdown(f"<h1>✒️ Lo Scrittoio di {nome}</h1>", unsafe_allow_html=True)

    try:
        res = supabase.table("Opere").select("*").eq("autore_email", nome).execute()
        opere = res.data or []
    except Exception as e:
        st.error(f"Errore di connessione al database: {e}")
        opere = []

    scelta = st.sidebar.selectbox("📖 I tuoi scritti:", ["Nuovo Manoscritto"] + [o['titolo'] for o in opere])
    opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
    
    titolo = st.text_input("Titolo dell'Opera", value=opera_corrente['titolo'] if opera_corrente else "")
    testo = st.text_area("Versi", value=opera_corrente['contenuto'] if opera_corrente else "", height=350)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💾 Custodisci"):
            if titolo and testo:
                dati = {"titolo": titolo, "contenuto": testo, "autore_email": nome}
                if opera_corrente:
                    supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                else:
                    supabase.table("Opere").insert(dati).execute()
                st.rerun()
    with c2:
        if st.button("🖨️ Crea PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=f"{titolo}\n\n{testo}")
            st.download_button("Scarica", data=pdf.output(dest='S').encode('latin-1'), file_name=f"{titolo}.pdf")
    with c3:
        if opera_corrente and st.button("🗑️ Brucia"):
            supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
            st.rerun()