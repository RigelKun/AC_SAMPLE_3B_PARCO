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
        The **Vigenère Cipher** is a **symmetric polyalphabetic substitution cipher** invented in the 16th century by Giovan Battista Bellaso, 
        but later misattributed to Blaise de Vigenère. It improves on the Caesar cipher by using a keyword to determine the shift of each character, 
        making it harder to break with frequency analysis.

        ### 🔍 Brief History:
        - Proposed by Giovan Battista Bellaso in 1553.
        - Blaise de Vigenère later popularized the cipher, leading to its name.
        - Once considered unbreakable, it was eventually broken using statistical methods in the 19th century.

        ### 🧠 How It Works (Simplified Pseudocode):
        ```
        For each letter in the plaintext:
            Use the corresponding letter from the keyword to determine Caesar shift.
            Apply that shift to the plaintext letter.
            Repeat the keyword if shorter than the message.
        ```

        ### 🔐 Process Description:
        - The cipher uses **a repeating keyword** to apply different Caesar shifts to each letter of the plaintext.
        - A = 0, B = 1, ..., Z = 25.
        - For encryption: `(Pi + Ki) mod 26`, where `Pi` is plaintext and `Ki` is keyword letter.
        - For decryption: `(Ci - Ki + 26) mod 26`, where `Ci` is ciphertext.
        - Non-alphabetic characters are not encrypted and remain unchanged.

        ### 🛠️ Use Cases:
        - Used historically for military and diplomatic communication.
        - Useful for teaching cryptography fundamentals.
        - Sometimes used in CTF (Capture the Flag) puzzles or escape rooms.

        ### ✉️ Example:
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

