import streamlit as st
from asymmetric import rsa, diffie, ecc

def render():
    if "asym_page" not in st.session_state:
        st.session_state.asym_page = "menu"

    if st.session_state.asym_page == "menu":
        st.title("🔑 Asymmetric Algorithms")
        st.write("Explore common asymmetric encryption algorithms:")

        ciphers = [
            {
                "name": "RSA",
                "desc": "Widely-used public key encryption system based on large prime factorization.",
                "key": "rsa",
            },
            {
                "name": "Diffie-Hellman",
                "desc": "Secure key exchange protocol using modular exponentiation.",
                "key": "diffie",
            },
            {
                "name": "Elliptic Curve Cryptography (ECC)",
                "desc": "Efficient encryption using elliptic curve mathematics.",
                "key": "ecc",
            },
        ]

        for cipher in ciphers:
            cols = st.columns([5, 1])
            with cols[0]:
                st.markdown(f"**{cipher['name']}** — {cipher['desc']}")
            with cols[1]:
                if st.button(f"Check out {cipher['name']}", key=cipher['key']):
                    st.session_state.asym_page = cipher['key']
                    st.rerun()
            st.markdown("---")

    else:
        if st.session_state.asym_page == "rsa":
            rsa.render()
        elif st.session_state.asym_page == "diffie":
            diffie.render()
        elif st.session_state.asym_page == "ecc":
            ecc.render()
            
    if st.button("⬅️ Back to Main Menu"):
        st.session_state.page = "Main Menu"
        st.session_state.asym_page = "menu"
        st.rerun()
