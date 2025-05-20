import streamlit as st

def format_key(text, key):
    key = key.upper()
    return (key * (len(text) // len(key) + 1))[:len(text)]

def encrypt_vigenere(plain_text, key):
    plain_text = plain_text.upper()
    key = format_key(plain_text, key)
    encrypted = ""

    for p, k in zip(plain_text, key):
        if p.isalpha():
            encrypted += chr((ord(p) - ord('A') + ord(k) - ord('A')) % 26 + ord('A'))
        else:
            encrypted += p
    return encrypted

def decrypt_vigenere(cipher_text, key):
    cipher_text = cipher_text.upper()
    key = format_key(cipher_text, key)
    decrypted = ""

    for c, k in zip(cipher_text, key):
        if c.isalpha():
            decrypted += chr((ord(c) - ord(k) + 26) % 26 + ord('A'))
        else:
            decrypted += c
    return decrypted

def render():
    st.title("🔐 Vigenère Cipher")

    with st.expander("ℹ️ What is the Vigenère Cipher?"):
        st.markdown("""
        The Vigenère cipher is a method of encrypting alphabetic 
        text using a polyalphabetic substitution technique, where each letter is encrypted 
        using a different Caesar cipher determined by a keyword.

        **Encryption formula:**
        - `Ci = (Pi + Ki) mod 26`

        **Decryption formula:**
        - `Pi = (Ci - Ki + 26) mod 26`

        Only alphabetic characters are encrypted. Non-alphabetic characters are preserved.

        **Example:**
        ```
        Plaintext:  ATTACKATDAWN
        Keyword:    LEMON
        Encrypted:  LXFOPVEFRNHR
        ```
        """)

    mode = st.radio("Mode", ["Encrypt", "Decrypt"])
    input_method = st.radio("Input Method", ["Type Text", "Upload File"])

    text = ""
    if input_method == "Type Text":
        text = st.text_area("Enter your text:")
    else:
        uploaded_file = st.file_uploader("Upload a .txt file", type="txt")
        if uploaded_file:
            text = uploaded_file.read().decode("utf-8")

    key = st.text_input("Enter a keyword (letters only):")

    if st.button("🔐 Run"):
        if not text.strip() or not key.strip():
            st.error("Please enter both text and a keyword.")
            return
        if not key.isalpha():
            st.error("Keyword must contain letters only.")
            return

        if mode == "Encrypt":
            result = encrypt_vigenere(text, key)
            st.success("Encryption complete!")
            st.text_area("Encrypted Text", result, height=150)
        else:
            result = decrypt_vigenere(text, key)
            st.success("Decryption complete!")
            st.text_area("Decrypted Text", result, height=150)

    st.markdown("---")
    if st.button("⬅️ Back to Symmetric Menu"):
        st.session_state.sym_page = "menu"
        st.rerun()

