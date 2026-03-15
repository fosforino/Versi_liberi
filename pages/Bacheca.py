import streamlit as st
from supabase import create_client
import os
import base64
import urllib.parse

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def apply_aesthetic_style():
    path_icona = "Poeticamente.png"
    img_base64 = get_base64_image(path_icona)
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="bg-watermark-bacheca">' if img_base64 else ""

    st.markdown(f"""
        <style>
        .stApp {{
            background-color: #fdf5e6;
            background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png");
            color: #3e2723;
        }}

        .bg-watermark-bacheca {{
            position: fixed;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            width: 60vw; opacity: 0.05; filter: blur(10px);
            z-index: -1; pointer-events: none;
        }}

        .poesia-card {{
            background-color: rgba(255, 250, 240, 0.8);
            padding: 35px;
            border-radius: 2px;
            border-left: 4px solid #c19a6b;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }}
        
        .poesia-card:hover {{
            transform: scale(1.01);
            background-color: rgba(255, 255, 255, 0.9);
        }}

        .titolo-poesia {{
            font-family: 'Playfair Display', serif;
            color: #3e2723;
            font-size: 2rem;
            margin-bottom: 10px;
        }}

        .versi-testo {{
            font-family: 'EB Garamond', serif;
            font-size: 1.3rem;
            line-height: 1.6;
            white-space: pre-wrap;
            color: #2c2c2c;
            margin: 25px 0;
        }}

        .firma-autore {{
            font-family: 'Playfair Display', serif;
            font-style: italic;
            text-align: right;
            color: #795548;
            font-size: 1rem;
            border-top: 1px solid rgba(193, 154, 107, 0.3);
            padding-top: 15px;
        }}

        .social-box {{
            display: flex; gap: 15px;
            justify-content: flex-start;
            margin-top: 10px;
            padding-bottom: 20px;
        }}

        .social-link {{
            text-decoration: none;
            font-size: 0.9rem;
            font-family: 'Playfair Display', serif;
            color: #795548;
            border: 1px solid #c19a6b;
            padding: 5px 12px;
            border-radius: 15px;
            transition: 0.3s;
        }}
        .social-link:hover {{
            background-color: #3e2723;
            color: #fdf5e6 !important;
        }}
        </style>
        {img_html}
        """, unsafe_allow_html=True)

def show():
    apply_aesthetic_style()
    
    st.markdown("<h1 style='font-size: 3.5rem; text-align: center;'>Bacheca Poetica</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; font-size: 1.2rem; color: #795548; margin-bottom: 60px;'>Le voci dei poeti si rincorrono tra i fogli del tempo.</p>", unsafe_allow_html=True)
    
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    try:
        # --- FILTRO PUBBLICAZIONE AGGIUNTO QUI ---
        res = supabase.table("Opere").select("*").eq("pubblica", True).order("created_at", desc=True).limit(20).execute()
        poemi = res.data if res.data else []

        if not poemi:
            st.info("La bacheca è ancora bianca. Sii il primo ad affiggere un'opera dallo Scrittoio!")
        
        col_m_1, col_m_2, col_m_3 = st.columns([0.1, 1, 0.1])
        
        with col_m_2:
            for p in poemi:
                titolo = p.get('titolo', 'Senza Titolo')
                testo = p.get('versi', 'Testo mancante')
                autore = p.get('autore', 'Poeta Anonimo')
                categoria = p.get('categoria', 'Poesia')
                
                st.markdown(
                    f"""
                    <div class="poesia-card">
                        <div class="titolo-poesia">{titolo}</div>
                        <div style='color: #c19a6b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;'>{categoria}</div>
                        <div class="versi-testo">{testo}</div>
                        <div class="firma-autore">Affisso dal Poeta: {autore}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                testo_share = f"✨ *{titolo}*\n\n{testo}\n\n— Poeta: {autore}\n\n_Condiviso da Poeticamente_"
                testo_url = urllib.parse.quote(testo_share)
                
                wa_link = f"https://wa.me/?text={testo_url}"
                mail_link = f"mailto:?subject=Poesia: {titolo}&body={testo_url}"

                st.markdown(f"""
                    <div class="social-box">
                        <a href="{wa_link}" target="_blank" class="social-link">📱 WhatsApp</a>
                        <a href="{mail_link}" class="social-link">✉️ Email</a>
                    </div>
                    <hr style="border: 0; border-top: 1px solid rgba(62, 39, 35, 0.1); margin-bottom: 40px;">
                """, unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"Il calamaio della bacheca ha un intoppo: {e}")

if __name__ == "__main__":
    show()