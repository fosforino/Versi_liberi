import streamlit as st
from supabase import create_client

# --- CONNESSIONE SUPABASE ---
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

def apply_aesthetic_style():
    """Applica l'estetica vintage e poetica alla Bacheca."""
    st.markdown(
        """
        <style>
        /* Sfondo generale color crema */
        .stApp {
            background-color: #fdf5e6;
            color: #2c2c2c;
        }

        /* Titoli in font Serif e colore inchiostro antico */
        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            color: #4b3621;
            text-align: center;
        }

        /* Contenitore per ogni singola poesia (effetto foglio appoggiato) */
        .poesia-card {
            background-color: #fffaf0;
            padding: 30px;
            border-radius: 2px;
            border-left: 5px solid #d2b48c;
            box-shadow: 3px 3px 10px rgba(0,0,0,0.05);
            margin-bottom: 40px;
            transition: transform 0.3s ease;
        }
        
        .poesia-card:hover {
            transform: translateY(-5px);
            box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        }

        /* Stile per i versi (preserva spazi e font poetico) */
        .versi-testo {
            font-family: 'Georgia', serif;
            font-size: 1.1rem;
            line-height: 1.6;
            white-space: pre-wrap;
            color: #333;
            margin: 20px 0;
        }

        /* Firma dell'autore */
        .firma-autore {
            font-style: italic;
            text-align: right;
            color: #6b4a3a;
            font-size: 0.9rem;
            border-top: 1px solid #eee;
            padding-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show():
    apply_aesthetic_style()
    
    st.markdown("<h1>Bacheca Poetica 🖋️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; margin-bottom: 50px;'>Le voci dei poeti si rincorrono tra i fogli del tempo.</p>", unsafe_allow_html=True)
    
    try:
        # Recuperiamo le ultime 20 poesie dalla tabella "opere" (o "Poesie" come nel tuo snippet)
        # Nota: assicurati che il nome della tabella sia coerente con quello dello Scrittoio
        res = supabase.table("opere").select("*").order("created_at", desc=True).limit(20).execute()
        poemi = res.data if res.data else []

        if not poemi:
            st.info("La bacheca è ancora bianca. Sii il primo a lasciare un'impronta!")
        
        for p in poemi:
            # Creiamo una "card" per ogni poesia usando l'HTML per il massimo controllo estetico
            st.markdown(
                f"""
                <div class="poesia-card">
                    <h3 style='margin-top: 0;'>{p['titolo']}</h3>
                    <div class="versi-testo">{p['testo']}</div>
                    <div class="firma-autore">Versi di {p['autore']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Se è presente un'immagine, la mostriamo sotto la card
            if p.get('immagine_url'):
                st.image(p['immagine_url'], use_container_width=True)
                st.markdown("<br>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Il calamaio sembra vuoto: {e}")