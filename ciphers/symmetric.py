import streamlit as st
from symmetric import caesar, vigenere, vernam, aes, des

def render():
    if "sym_page" not in st.session_state:
        st.session_state.sym_page = "menu"

    if st.session_state.sym_page == "menu":
        st.title("🔒 Symmetric Algorithms")
        st.write("Explore some common symmetric encryption algorithms below:")

        ciphers = [
            {
                "name": "Caesar Cipher",
                "desc": "A simple classical cipher that shifts letters by a fixed key.",
                "key": "caesar",
            },
            {
                "name": "Vigenère Cipher",
                "desc": "Uses a keyword to shift letters for encryption.",
                "key": "vigenere",
            },
            {
                "name": "Vernam Cipher",
                "desc": "Perfectly secure one-time pad cipher.",
                "key": "vernam",
            },
            {
                "name": "AES",
                "desc": "Modern block cipher used worldwide.",
                "key": "aes",
            },
            {
                "name": "DES",
                "desc": "Legacy cipher, replaced by AES but still studied.",
                "key": "des",
            },
        ]

        for cipher in ciphers:
            cols = st.columns([5, 1])
            with cols[0]:
                st.markdown(f"**{cipher['name']}** — {cipher['desc']}")
            with cols[1]:
                if st.button(f"Check out {cipher['name']}", key=cipher['key']):
                    st.session_state.sym_page = cipher['key']
                    st.rerun()
            st.markdown("---")

    else:
        if st.session_state.sym_page == "caesar":
            caesar.render()
        elif st.session_state.sym_page == "vigenere":
            vigenere.render()
        elif st.session_state.sym_page == "vernam":
            vernam.render()
        elif st.session_state.sym_page == "aes":
            aes.render()
        elif st.session_state.sym_page == "des":
            des.render()

    if st.button("⬅️ Back to Main Menu"):
        st.session_state.page = "Main Menu"
        st.session_state.sym_page = "menu"
        st.rerun()
