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

    with st.expander("ℹ️ What is the Vernam Cipher?"):
        st.markdown("""
        The **Vernam Cipher** is a **symmetric encryption** technique and a special case of the one-time pad cipher. 
        It operates by combining a plaintext message with a numeric key of the same length using modular arithmetic.

        ### 🔍 Brief History:
        - Invented by Gilbert Vernam in 1917.
        - Originally used in telegraphy and early digital communications.
        - When used with a truly random, one-time-use key (of equal length to the message), it becomes theoretically **unbreakable**.

        ### 🧠 How It Works (Simplified Pseudocode):
        ```
        For Encryption:
            1. Convert each character in the plaintext to its 3-digit ASCII code.
            2. Generate a numeric key of the same length.
            3. Perform digit-wise subtraction modulo 10:
            C_i = (P_i - K_i + 10) mod 10

        For Decryption:
            1. Use the same numeric key.
            2. Perform digit-wise addition modulo 10:
            P_i = (C_i + K_i) mod 10
        ```

        ### 🔐 Process Description:
        - The cipher treats the ASCII code of the message as a numeric string.
        - Encryption and decryption work digit by digit.
        - The key must be purely numeric and exactly the same length as the ASCII-expanded plaintext.

        ### 🛠️ Use Cases:
        - Educational purposes to demonstrate the concept of **perfect secrecy**.
        - Forms the basis for the **one-time pad**, used in highly secure communication systems.
        - **Note**: Secure only if the key is random, the same length as the message, and never reused.

        ### ✉️ Example:
        ```
        Plaintext:  HELLO
        ASCII:      072069076076079
        Key:        727272727272727
        Encrypted:  355897359804352
        ```

        ⚠️ **Important**: The key must be a numeric string with the same number of digits as the ASCII version of the message. Otherwise, encryption/decryption will fail or produce incorrect results.
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
                
    st.markdown("---")
    if st.button("⬅️ Back to Symmetric Menu"):
        st.session_state.sym_page = "menu"
        st.rerun()
