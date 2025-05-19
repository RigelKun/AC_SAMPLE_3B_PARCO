import streamlit as st

def render():
    st.title("DES")
    st.write("Project in Applied Cryptography")
    
    st.markdown("---")
    if st.button("⬅️ Back to Symmetric Algorithms"):
        st.session_state.sym_page = "menu"
        st.rerun()