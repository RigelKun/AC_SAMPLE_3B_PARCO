import streamlit as st
import main
from ciphers import caesar, vigenere, block, rsa, diffie, primitive, hashing

if "page" not in st.session_state:
    st.session_state.page = "main"
    
with st.sidebar:
    if st.button("Main Menu", type="tertiary"):
        st.session_state.page = "main"
    if st.button("Caesar Cipher"):
        st.session_state.page = "caesar"
    if st.button("Vigenere Cipher"):
        st.session_state.page = "vigenere"
    if st.button("Diffie-Hellman Key Exchange"):
        st.session_state.page = "diffie"
    if st.button("RSA Encryption"):
        st.session_state.page = "rsa"
    if st.button("Block Cipher"):
        st.session_state.page = "block"
    if st.button("Primitive Root"):
        st.session_state.page = "primitive"
    if st.button("SHA-256 hashing"):
        st.session_state.page = "hashing"

if st.session_state.page == "main":
    main.render()
if st.session_state.page == "caesar":
    caesar.render()
elif st.session_state.page == "vigenere":
    vigenere.render()
elif st.session_state.page == "diffie":
    diffie.render()
elif st.session_state.page == "rsa":
    rsa.render()
elif st.session_state.page == "block":
    block.render()
elif st.session_state.page == "primitive":
    primitive.render()
elif st.session_state.page == "hashing":
    hashing.render()