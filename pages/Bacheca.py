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
            padding: 0; /* Tolto padding per far aderire l'immagine ai bordi sopra */
            border-radius: 4px;
            border: 1px solid rgba(193, 154, 107, 0.3);
            box-shadow: 2px 4px 15px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            overflow: hidden;
        }}
        .card-content {{
            padding: 30px;
        }}
        .titolo-poesia {{
            font-family: 'Playfair Display', serif;
            color: #3e2723;
            font-size: 2.2rem;
            margin-bottom: 5px;
        }}
        .versi-testo {{
            font-family: 'EB Garamond', serif;
            font-size: 1.35rem;
            line-height: 1.6;
            white-space: pre-wrap;
            color: #2c2c2c;
            margin: 20px 0;
        }}
        .firma-autore {{
            font-family: 'Playfair Display', serif;
            font-style: italic;
            text-align: right;
            color: #795548;
            border-top: 1px solid rgba(193, 154, 107, 0.2);
            padding-top: 15px;
        }}
        .social-link {{
            text-decoration: none;
            font-size: 0.85rem;
            color: #795548;
            border: 1px solid #c19a6b;
            padding: 4px 10px;
            border-radius: 12px;
            margin-right: 10px;
        }}
        </style>
        {img_html}
        """, unsafe_allow_html=True)

def show():
    apply_aesthetic_style()
    
    st.markdown("<h1 style='text-align: center;'>Bacheca Poetica</h1>", unsafe_allow_html=True)
    
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    try:
        # Filtro: solo opere pubbliche
        res = supabase.table("Opere").select("*").eq("pubblica", True).order("created_at", desc=True).execute()
        poemi = res.data if res.data else []

        if not poemi:
            st.info("Nessuna opera è stata ancora affissa. Sii il primo!")
        
        col_m_1, col_m_2, col_m_3 = st.columns([0.1, 1, 0.1])
        
        with col_m_2:
            for p in poemi:
                titolo = p.get('titolo', 'Senza Titolo')
                testo = p.get('versi', '')
                autore = p.get('autore', 'Anonimo')
                categoria = p.get('categoria', 'Poesia')
                img_url = p.get('immagine_url', "")

                # Inizio Card
                st.markdown('<div class="poesia-card">', unsafe_allow_html=True)
                
                # Se c'è l'immagine, la mostriamo in cima
                if img_url:
                    st.image(img_url, use_container_width=True)
                
                # Testo della poesia
                st.markdown(f"""
                    <div class="card-content">
                        <div class="titolo-poesia">{titolo}</div>
                        <div style='color: #c19a6b; font-size: 0.8rem; text-transform: uppercase;'>{categoria}</div>
                        <div class="versi-testo">{testo}</div>
                        <div class="firma-autore">Il Poeta: {autore}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Social links
                testo_share = f"*{titolo}*\n\n{testo}\n\n— {autore}"
                testo_url = urllib.parse.quote(testo_share)
                st.markdown(f"""
                    <div style="padding: 0 30px 30px 30px;">
                        <a href="https://wa.me/?text={testo_url}" target="_blank" class="social-link">WhatsApp</a>
                        <a href="mailto:?body={testo_url}" class="social-link">Email</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"Errore bacheca: {e}")

if __name__ == "__main__":
    show()