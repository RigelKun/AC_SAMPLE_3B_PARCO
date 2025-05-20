import streamlit as st

def render():
    st.title("Elliptic Curve")
    st.write("Project in Applied Cryptography")
    
    if st.button("⬅️ Back to Asymmetric Menu"):
        st.session_state.asym_page = "menu"
        st.rerun()