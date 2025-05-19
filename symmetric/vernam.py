import streamlit as st
import re
import random

def text_to_ascii(text):
    return ''.join(f"{ord(c):03}" for c in text)

def ascii_to_text(ascii_str):
    return ''.join(chr(int(ascii_str[i:i+3])) for i in range(0, len(ascii_str), 3))

def encrypt_vernam(ascii_text, key):
    return ''.join(str((int(a) - int(k)) % 10) for a, k in zip(ascii_text, key))

def decrypt_vernam(cipher_text, key):
    return ''.join(str((int(c) + int(k)) % 10) for c, k in zip(cipher_text, key))

def generate_random_key(length):
    return ''.join(str(random.randint(0,9)) for _ in range(length))

def render():
    st.title("🔐 Vernam Cipher (One-Time Pad)")

    with st.expander("ℹ️ What is Vernam Cipher?"):
        st.markdown(""" 
        The Vernam Cipher is a symmetric encryption method that uses a numeric key as long as the message's ASCII representation.

        **Encryption process overview:**

        1. Convert text to decimal ASCII (3-digit codes per char).
        2. Provide a numeric key of the same length (or generate one).
        3. Encrypt by digit-wise subtraction modulo 10.
        4. Decrypt by digit-wise addition modulo 10.

        **Example:**

        ```
        Plaintext: HELLO
        ASCII: 072069076076079
        Key:    727272727272727
        Cipher: 355897359804352
        ```
        """)

    mode = st.radio("Mode", ["Encrypt", "Decrypt"])

    if mode == "Encrypt":
        input_method = st.radio("Input Method", ["Type Text", "Upload File"])

        text = ""
        if input_method == "Type Text":
            text = st.text_area("Enter your text:")
        else:
            uploaded_file = st.file_uploader("Upload a .txt file", type="txt")
            if uploaded_file:
                text = uploaded_file.read().decode("utf-8")

        if text:
            ascii_str = text_to_ascii(text)
            key_length = len(ascii_str)

            generate_key = st.checkbox("Generate random key", value=True)
            if generate_key:
                key_input = generate_random_key(key_length)
                st.text_area("Generated Key (remember this!)", key_input, height=80)
            else:
                key_input = st.text_input(f"Enter a numeric key exactly {key_length} digits long:")

            if st.button("🔒 Encrypt"):
                if not text.strip():
                    st.error("Please enter or upload some text.")
                    return
                if not key_input or len(key_input) != key_length:
                    st.error(f"Key must be exactly {key_length} digits long.")
                    return
                if not re.fullmatch(r'\d+', key_input):
                    st.error("Key must be numeric.")
                    return
                cipher = encrypt_vernam(ascii_str, key_input)
                st.success("Encryption successful!")
                st.text_area("Cipher Text", cipher, height=150)
        else:
            st.info("Enter or upload text to enable key input.")

    else: 
        key_input = st.text_input("Enter the numeric key:")
        cipher_input = st.text_area("Enter the cipher text:")

        if st.button("🔓 Decrypt"):
            if not re.fullmatch(r'\d+', key_input) or not re.fullmatch(r'\d+', cipher_input):
                st.error("Key and ciphertext must be numeric.")
                return
            if len(key_input) != len(cipher_input):
                st.error("Key length must match ciphertext length.")
                return

            ascii_recovered = decrypt_vernam(cipher_input, key_input)
            try:
                plain = ascii_to_text(ascii_recovered)
                st.success("Decryption successful!")
                st.text_area("Decrypted Text", plain, height=150)
            except Exception:
                st.error("Failed to convert ASCII to text. The key or ciphertext may be incorrect.")

    if st.button("⬅️ Back to Symmetric Menu"):
        st.session_state.sym_page = "menu"
        st.rerun()
