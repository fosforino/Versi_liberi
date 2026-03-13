import streamlit as st

def show():
    st.markdown("""
    <style>
        .stApp { 
            background-color: #f4ecd8 !important;
            background-image: url("https://www.transparenttextures.com/patterns/parchment.png") !important;
            background-attachment: fixed !important;
        }
        h1, h2, h3, label, p { 
            color: #3e2723 !important; 
            font-family: 'EB Garamond', serif !important; 
            text-align: center; 
        }
        div.stButton > button { 
            background: #5d4037 !important; color: white !important; border-radius: 8px !important; 
            box-shadow: 0 5px 0 #3e2723 !important; width: 100%; height: 3em; font-weight: bold;
            border: none !important;
        }
        div.stButton > button:active { box-shadow: 0 2px 0 #3e2723 !important; transform: translateY(3px) !important; }
        input { background-color: #fffaf0 !important; border: 1px solid #c19a6b !important; color: #3e2723 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='font-size: 3.5rem;'>🎨 Poeticamente</h1>", unsafe_allow_html=True)
    st.markdown("<p>Benvenuto nell'antico rifugio dei versi.</p>", unsafe_allow_html=True)
    
    if not st.session_state.get("utente"):
        pseudonimo = st.text_input("Come desideri essere chiamato?")
        if st.button("Entra nello Scrittoio"):
            if pseudonimo:
                st.session_state.utente = pseudonimo
                st.rerun()
    else:
        st.success(f"Sei identificato come: {st.session_state.utente}")
        if st.button("Esci (Cambia Poeta)"):
            st.session_state.utente = None
            st.rerun()