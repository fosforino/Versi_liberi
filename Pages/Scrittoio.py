import streamlit as st
from supabase import create_client
from fpdf import FPDF
import os
import base64

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def genera_pdf(titolo, categoria, contenuto, autore):
    """Crea un PDF elegante pronto per il download."""
    pdf = FPDF()
    pdf.add_page()
    
    # Titolo
    pdf.set_font("Times", 'B', 24)
    pdf.cell(0, 20, titolo.encode('latin-1', 'replace').decode('latin-1'), ln=True, align='C')
    
    # Categoria
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, f"Categoria: {categoria}".encode('latin-1', 'replace').decode('latin-1'), ln=True, align='C')
    
    pdf.ln(10)
    
    # Contenuto
    pdf.set_font("Times", size=14)
    # Multi_cell gestisce i ritorni a capo dei versi
    pdf.multi_cell(0, 10, contenuto.encode('latin-1', 'replace').decode('latin-1'))
    
    pdf.ln(20)
    
    # Firma
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, f"Scritto da: {autore}".encode('latin-1', 'replace').decode('latin-1'), ln=True, align='R')
    
    return pdf.output(dest='S').encode('latin-1')

def show():
    # --- STILE E FILIGRANA ---
    path_icona = "Poeticamente.png"
    img_base64 = get_base64_image(path_icona)
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="bg-watermark-scrittoio">' if img_base64 else ""

    st.markdown(f"""
        <style>
        .stApp {{
            background-color: #fdf5e6 !important;
            background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png") !important;
        }}
        .bg-watermark-scrittoio {{
            position: fixed;
            top: 50%;
            left: 55%;
            transform: translate(-50%, -50%);
            width: 50vw;
            opacity: 0.05;
            filter: blur(12px);
            z-index: -1;
            pointer-events: none;
        }}
        .stTextArea textarea {{
            background-color: rgba(255, 250, 240, 0.7) !important;
            border: 1px solid #c19a6b !important;
            border-radius: 5px !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.3rem !important;
            color: #3e2723 !important;
        }}
        /* BOTTONI 3D */
        div.stButton > button {{
            border: none !important;
            color: white !important;
            font-weight: bold !important;
            padding: 0.6em 1.2em !important;
            border-radius: 8px !important;
            text-transform: uppercase;
        }}
        div.stButton > button[key="btn_salva"] {{
            background: #2e7d32 !important;
            box-shadow: 0 5px 0 #1b5e20, 0 8px 15px rgba(0,0,0,0.2) !important;
        }}
        div.stButton > button[key="btn_stampa"] {{
            background: #455a64 !important;
            box-shadow: 0 5px 0 #263238, 0 8px 15px rgba(0,0,0,0.2) !important;
        }}
        div.stButton > button[key="btn_cancella"] {{
            background: #8e0000 !important;
            box-shadow: 0 5px 0 #4a0000, 0 8px 15px rgba(0,0,0,0.2) !important;
        }}
        div.stButton > button:active {{
            transform: translateY(3px) !important;
            box-shadow: 0 2px 0 inherit !important;
        }}
        </style>
        {img_html}
        """, unsafe_allow_html=True)

    # --- LOGICA SUPABASE ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" in st.session_state:
        nome_poeta = st.session_state.utente
        st.markdown(f"<h1 style='text-align: center; color: #3e2723;'>✒️ Lo Scrittoio di {nome_poeta}</h1>", unsafe_allow_html=True)

        try:
            res = supabase.table("Opere").select("*").eq("autore_email", nome_poeta).order("creato_il", desc=True).execute()
            opere = res.data
        except:
            opere = []

        scelta = st.sidebar.selectbox("📖 Carica un'opera:", ["Nuova Opera"] + [o['titolo'] for o in opere])
        opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
        
        v_titolo = opera_corrente['titolo'] if opera_corrente else ""
        v_testo = opera_corrente['contenuto'] if opera_corrente else ""
        v_cat = opera_corrente.get('categoria', "Poesia") if opera_corrente else "Poesia"

        col_t, col_c = st.columns([2, 1])
        with col_t:
            titolo = st.text_input("Titolo dell'Opera", value=v_titolo)
        with col_c:
            cats = ["Poesia", "Romanzo", "Filastrocca", "Narrazione", "Opera Teatrale", "Canzone"]
            idx = cats.index(v_cat) if v_cat in cats else 0
            categoria = st.selectbox("Categoria", cats, index=idx)

        contenuto = st.text_area("Versi e Pensieri", value=v_testo, height=450)
        st.markdown("<br>", unsafe_allow_html=True)
        
        b1, b2, b3 = st.columns([1, 1, 1])

        with b1:
            if st.button("💾 Custodisci", key="btn_salva"):
                if titolo:
                    dati = {"titolo": titolo, "contenuto": contenuto, "categoria": categoria, "autore_email": nome_poeta}
                    if opera_corrente:
                        supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                    else:
                        supabase.table("Opere").insert(dati).execute()
                    st.success("Versi salvati.")
                    st.rerun()
                else:
                    st.warning("Manca il titolo.")

        with b2:
            # Qui usiamo FPDF per il download diretto
            if titolo and contenuto:
                pdf_data = genera_pdf(titolo, categoria, contenuto, nome_poeta)
                st.download_button(
                    label="🖨️ Scarica PDF",
                    data=pdf_data,
                    file_name=f"{titolo}.pdf",
                    mime="application/pdf",
                    key="btn_stampa"
                )
            else:
                st.button("🖨️ Scarica PDF", key="btn_stampa", disabled=True)

        with b3:
            if opera_corrente:
                if st.button("🗑️ Brucia", key="btn_cancella"):
                    supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                    st.rerun()
    else:
        st.warning("Identificati nella Home.")