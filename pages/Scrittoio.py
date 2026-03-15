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
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", 'B', 24)
    pdf.cell(0, 20, titolo.encode('latin-1', 'replace').decode('latin-1'), ln=True, align='C')
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, f"Categoria: {categoria}".encode('latin-1', 'replace').decode('latin-1'), ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Times", size=14)
    pdf.multi_cell(0, 10, contenuto.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(20)
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, f"Scritto da: {autore}".encode('latin-1', 'replace').decode('latin-1'), ln=True, align='R')
    return pdf.output(dest='S').encode('latin-1')

def show():
    path_icona = "Poeticamente.png"
    img_base64 = get_base64_image(path_icona)
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="bg-watermark-scrittoio">' if img_base64 else ""

    st.markdown(f"""
        <style>
        .stApp {{ background-color: #fdf5e6 !important; background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png") !important; }}
        .bg-watermark-scrittoio {{ position: fixed; top: 50%; left: 55%; transform: translate(-50%, -50%); width: 50vw; opacity: 0.05; filter: blur(12px); z-index: -1; pointer-events: none; }}
        .stTextArea textarea {{ background-color: rgba(255, 250, 240, 0.7) !important; border: 1px solid #c19a6b !important; border-radius: 5px !important; font-family: 'EB Garamond', serif !important; font-size: 1.3rem !important; color: #3e2723 !important; }}
        
        div.stButton > button {{ border: none !important; color: white !important; font-weight: bold !important; padding: 0.6em 1.2em !important; border-radius: 8px !important; text-transform: uppercase; transition: 0.3s; }}
        div.stButton > button:hover {{ opacity: 0.9; transform: translateY(-2px); }}
        
        div.stButton > button[key="btn_salva"] {{ background: #2e7d32 !important; box-shadow: 0 4px 0 #1b5e20; }}
        div.stButton > button[key="btn_stampa"] {{ background: #455a64 !important; box-shadow: 0 4px 0 #263238; }}
        div.stButton > button[key="btn_cancella"] {{ background: #8e0000 !important; box-shadow: 0 4px 0 #4a0000; }}
        </style>
        {img_html}
        """, unsafe_allow_html=True)

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" in st.session_state:
        nome_poeta = st.session_state.utente
        st.markdown(f"<h1 style='text-align: center; color: #3e2723;'>✒️ Lo Scrittoio di {nome_poeta}</h1>", unsafe_allow_html=True)

        try:
            res = supabase.table("Opere").select("*").eq("autore", nome_poeta).order("created_at", desc=True).execute()
            opere = res.data if res.data else []
        except Exception as e:
            st.error(f"Errore recupero: {e}")
            opere = []

        scelta = st.sidebar.selectbox("📖 Carica un'opera:", ["Nuova Opera"] + [o['titolo'] for o in opere])
        opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
        
        v_titolo = opera_corrente['titolo'] if opera_corrente else ""
        v_testo = opera_corrente['versi'] if opera_corrente else ""
        v_cat = opera_corrente.get('categoria', "Poesia") if opera_corrente else "Poesia"
        v_pubblica = opera_corrente.get('pubblica', False) if opera_corrente else False
        v_img = opera_corrente.get('immagine_url', "") if opera_corrente else ""

        col_t, col_c = st.columns([2, 1])
        with col_t:
            titolo = st.text_input("Titolo dell'Opera", value=v_titolo)
        with col_c:
            cats = ["Poesia", "Romanzo", "Filastrocca", "Narrazione", "Opera Teatrale", "Canzone"]
            idx = cats.index(v_cat) if v_cat in cats else 0
            categoria = st.selectbox("Categoria", cats, index=idx)

        # --- CAMPO IMMAGINE ---
        img_url = st.text_input("🔗 Link Immagine dal Web (opzionale):", value=v_img)
        if img_url:
            try:
                st.image(img_url, caption="Anteprima Copertina", width=300)
            except:
                st.warning("Immagine non visualizzabile. Verifica il link.")

        contenuto = st.text_area("Versi e Pensieri", value=v_testo, height=400)
        
        # --- PUBBLICAZIONE ---
        pubblica = st.toggle("📢 Affiggi in Bacheca (Rendi l'opera pubblica)", value=v_pubblica)
        
        st.markdown("---")
        b1, b2, b3 = st.columns([1, 1, 1])

        with b1:
            if st.button("💾 Custodisci", key="btn_salva"):
                if titolo and contenuto:
                    try:
                        dati = {
                            "titolo": titolo, 
                            "versi": contenuto, 
                            "categoria": categoria, 
                            "autore": nome_poeta,
                            "pubblica": pubblica,
                            "immagine_url": img_url
                        }
                        if opera_corrente:
                            supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                        else:
                            supabase.table("Opere").insert(dati).execute()
                        
                        st.success("Versi custoditi nel tempo.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Errore salvataggio: {e}")
                else:
                    st.warning("Inserisci titolo e testo.")

        with b2:
            if titolo and contenuto:
                pdf_data = genera_pdf(titolo, categoria, contenuto, nome_poeta)
                st.download_button("🖨️ Scarica PDF", data=pdf_data, file_name=f"{titolo}.pdf", mime="application/pdf", key="btn_stampa")

        with b3:
            if opera_corrente:
                if st.button("🗑️ Brucia", key="btn_cancella"):
                    supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                    st.rerun()
    else:
        st.warning("Identificati nella Home.")

if __name__ == "__main__":
    show()