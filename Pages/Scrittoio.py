import streamlit as st
from supabase import create_client
from fpdf import FPDF
import pydantic

def show():
    # --- STILE SMERALDO 3D ---
    st.markdown("""
        <style>
        .stApp { background-color: #e0f2f1 !important; }
        
        .stTextArea textarea {
            background-color: #ffffff !important;
            border: 2px solid #b2dfdb !important;
            border-radius: 8px !important;
            color: #004d40 !important;
        }

        /* BOTTONI 3D */
        div.stButton > button {
            border: none !important;
            border-radius: 12px !important;
            font-weight: bold !important;
            color: white !important;
            transition: all 0.1s ease !important;
        }

        /* SALVA */
        div.stButton > button[key="btn_salva"] {
            background-color: #4db6ac !important;
            box-shadow: 0 6px 0 #00796b !important;
        }
        /* STAMPA */
        div.stButton > button[key="btn_stampa"] {
            background-color: #4fc3f7 !important;
            box-shadow: 0 6px 0 #0277bd !important;
        }
        /* BRUCIA */
        div.stButton > button[key="btn_cancella"] {
            background-color: #ef5350 !important;
            box-shadow: 0 6px 0 #c62828 !important;
        }
        
        div.stButton > button:active {
            transform: translateY(4px) !important;
            box-shadow: 0 2px 0 rgba(0,0,0,0.2) !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- LOGICA SUPABASE ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" in st.session_state:
        nome_poeta = st.session_state.utente
        st.markdown(f"<h1 style='text-align: center;'>✒️ Lo Scrittoio di {nome_poeta}</h1>", unsafe_allow_html=True)

        # Logica caricamento opere...
        try:
            res = supabase.table("Opere").select("*").eq("autore_email", nome_poeta).order("creato_il", desc=True).execute()
            opere = res.data
        except:
            opere = []

        scelta = st.sidebar.selectbox("📖 Carica opera:", ["Nuova Opera"] + [o['titolo'] for o in opere])
        opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
        
        titolo = st.text_input("Titolo dell'Opera", value=opera_corrente['titolo'] if opera_corrente else "")
        contenuto = st.text_area("Versi e Pensieri", value=opera_corrente['contenuto'] if opera_corrente else "", height=400)

        st.write("---")
        b1, b2, b3 = st.columns([1, 1, 1])

        with b1:
            if st.button("💾 Salva nel Diario", key="btn_salva"):
                if titolo:
                    dati = {"titolo": titolo, "contenuto": contenuto, "autore_email": nome_poeta}
                    if opera_corrente:
                        supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                    else:
                        supabase.table("Opere").insert(dati).execute()
                    st.success("Versi salvati.")
                    st.rerun()

        with b2:
            if st.button("🖨️ Esporta PDF", key="btn_stampa"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=titolo, ln=1, align='C')
                pdf.multi_cell(0, 10, txt=contenuto)
                st.download_button("Scarica PDF", data=pdf.output(dest='S').encode('latin-1'), file_name=f"{titolo}.pdf")

        with b3:
            if opera_corrente and st.button("🗑️ Brucia Opera", key="btn_cancella"):
                supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                st.rerun()