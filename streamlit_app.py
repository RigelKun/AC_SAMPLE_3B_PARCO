import streamlit as st
import main     
from ciphers import hashing, asymmetric, symmetric


def render():
    if "page" not in st.session_state:
        st.session_state.page = "Main Menu"

    st.sidebar.title("🔍 Navigation")
    if st.sidebar.button("🏠 Main Menu"):
        st.session_state.page = "Main Menu"
    if st.sidebar.button("🔐 Hashing Algorithms"):
        st.session_state.page = "Hashing Algorithms"
    if st.sidebar.button("🔒 Symmetric Algorithms"):
        st.session_state.page = "Symmetric Algorithms"
    if st.sidebar.button("🔓 Asymmetric Algorithms"):
        st.session_state.page = "Asymmetric Algorithms"

    if st.session_state.page == "Main Menu":
        main.render()
    elif st.session_state.page == "Hashing Algorithms":
        hashing.render()
    elif st.session_state.page == "Symmetric Algorithms":
        symmetric.render()
    elif st.session_state.page == "Asymmetric Algorithms":
        asymmetric.render()

if __name__ == "__main__":
    render()

