import streamlit as st
from supabase import create_client
from fpdf import FPDF

def show():
    # CSS per l'area di scrittura
    st.markdown("""
        <style>
        .stTextArea textarea {
            background-color: #fffaf0 !important;
            border: 1px solid #c19a6b !important;
            color: #3e2723 !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.3rem !important;
            line-height: 1.6;
        }
        
        /* BOTTONI STILE RETRÒ */
        div.stButton > button {
            border-radius: 5px !important;
            color: white !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 0 4px 0 #2a1b19 !important;
        }
        
        div.stButton > button[key="btn_salva"] { background-color: #5d4037 !important; }
        div.stButton > button[key="btn_stampa"] { background-color: #2c3e50 !important; }
        div.stButton > button[key="btn_cancella"] { background-color: #7b1f1f !important; }
        
        div.stButton > button:active {
            transform: translateY(3px) !important;
            box-shadow: 0 1px 0 #2a1b19 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # Logica Database
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    nome = st.session_state.get("utente")

    if not nome:
        st.warning("⚠️ Identificati in Home per iniziare a scrivere.")
        return

    st.markdown(f"<h1>✒️ Lo Scrittoio di {nome}</h1>", unsafe_allow_html=True)

    # Caricamento Opere
    res = supabase.table("Opere").select("*").eq("autore_email", nome).execute()
    opere = res.data or []
    
    scelta = st.sidebar.selectbox("📖 I tuoi manoscritti:", ["Nuova Opera"] + [o['titolo'] for o in opere])
    opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
    
    titolo = st.text_input("Titolo dell'opera", value=opera_corrente['titolo'] if opera_corrente else "")
    testo = st.text_area("Versi e pensieri...", value=opera_corrente['contenuto'] if opera_corrente else "", height=350)

    st.write("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Salva", key="btn_salva"):
            dati = {"titolo": titolo, "contenuto": testo, "autore_email": nome}
            if opera_corrente:
                supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
            else:
                supabase.table("Opere").insert(dati).execute()
            st.success("Versi custoditi.")
            st.rerun()

    with col2:
        if st.button("🖨️ Scarica PDF", key="btn_stampa"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=f"{titolo}\n\n{testo}")
            st.download_button("Clicca qui per il PDF", data=pdf.output(dest='S').encode('latin-1'), file_name=f"{titolo}.pdf")

    with col3:
        if opera_corrente and st.button("🗑️ Brucia", key="btn_cancella"):
            supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
            st.rerun()