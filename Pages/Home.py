import streamlit as st

def show():
    # Stile Pergamena Ruvida specifico per la Home
    st.markdown("""
    <style>
        .stApp { 
            background-color: #f4ecd8 !important;
            background-image: url("https://www.transparenttextures.com/patterns/parchment.png") !important;
            background-attachment: fixed !important;
        }
        h1, h2, h3, label { 
            color: #3e2723 !important; 
            font-family: 'EB Garamond', serif !important; 
            text-align: center; 
        }
        div.stButton > button { 
            background: #5d4037 !important; 
            color: white !important; 
            border-radius: 8px !important; 
            box-shadow: 0 5px 0 #3e2723 !important; 
            width: 100%;
            height: 3em;
            font-weight: bold;
        }
        div.stButton > button:active {
            box-shadow: 0 2px 0 #3e2723 !important;
            transform: translateY(3px) !important;
        }
        input { 
            background-color: #fffaf0 !important; 
            border: 1px solid #c19a6b !important; 
            color: #3e2723 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='font-size: 3.5rem;'>🎨 Poeticamente</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; color: #5d4037;'>L'antico rifugio dei versi dimenticati</p>", unsafe_allow_html=True)
    
    st.write("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.get("utente"):
            st.subheader("🖋️ Chi bussa alla porta?")
            pseudonimo = st.text_input("Inserisci il tuo Pseudonimo:")
            if st.button("Entra nello Scrittoio"):
                if pseudonimo:
                    st.session_state.utente = pseudonimo
                    st.rerun()
                else:
                    st.error("Un poeta deve avere un nome, anche se inventato.")
        else:
            st.success(f"Bentornato, {st.session_state.utente}")
            if st.button("Congeda il Poeta (Logout)"):
                st.session_state.utente = None
                st.rerun()