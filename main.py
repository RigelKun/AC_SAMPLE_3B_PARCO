import streamlit as st

def render():
    if "page" not in st.session_state:
        st.session_state.page = "Main Menu"

    st.title("🔐 Project in Applied Cryptography")
    st.subheader("An Interactive Cryptography Tool")

    st.markdown("""
    Welcome to our Applied Cryptography project! This app helps you explore and understand the core techniques
    used to protect data through interactive tools and demonstrations.

    ### 📌 What You Can Do:
    - Hash text and files using secure hashing algorithms
    - Encrypt and decrypt messages using classical symmetric methods
    - Understand how public-key cryptography works
    """)

    st.markdown("---")
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔐 Hashing Algorithms", key="btn_hashing"):
            st.session_state.page = "Hashing Algorithms"
            st.rerun()
    with col2:
        if st.button("🔒 Symmetric Algorithms", key="btn_symmetric"):
            st.session_state.page = "Symmetric Algorithms"
            st.rerun()
    with col1:
        if st.button("🔓 Asymmetric Algorithms", key="btn_asymmetric"):
            st.session_state.page = "Asymmetric Algorithms"
            st.rerun()

    st.markdown("---")


    st.markdown("""
    **👨‍💻 Project By:**  
    - Rigel Parco 
    - Caren Joy Epress
    - Kenth Lorenz Collao 

    **📘 Course:** Applied Cryptography – BSCS 3B  
    **👩‍🏫 Instructor:** Mr. Allan Ibo Jr.
    **📅 Date:** May 2025
    """)

