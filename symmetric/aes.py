import streamlit as st
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def render():
    st.title("🔐 AES (ECB Mode)")
    st.write("Encrypt or decrypt data using the AES algorithm in ECB mode.")

    with st.expander("ℹ️ What is AES in ECB Mode?"):
        st.write("""
        The Advanced Encryption Standard (AES) is a symmetric encryption algorithm 
        widely used for securing data. It operates on fixed-size blocks (typically 128 bits) and supports key sizes of 128, 192, or 256 bits.

        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ECB (Electronic Codebook) is one of the simplest modes of AES. In ECB mode, 
        each block of plaintext is encrypted independently using the same key. This makes it fast and easy to implement, 
        but it is less secure for large or patterned data since identical plaintext blocks result in identical ciphertext blocks.

        Use AES-ECB only for small, random, or non-repetitive data where pattern leakage is not a concern.
        """)

    mode = st.radio("Mode:", ["Encrypt", "Decrypt"])
    input_type = st.radio("Input Type:", ["Text", "File"])

    data = None
    filename = None

    if input_type == "Text":
        text = st.text_area("Enter text:")
        if text:
            data = text.encode()
    else:
        uploaded_file = st.file_uploader("Upload file:")
        if uploaded_file:
            data = uploaded_file.read()
            filename = uploaded_file.name

    key_size = st.selectbox("Select key size (bits):", [128, 192, 256])
    key_length = key_size // 8 

    key_input = st.text_input(f"🔐 Enter {key_length}-character secret key:")
    key_valid = len(key_input) == key_length
    if not key_valid and key_input:
        st.warning(f"Key must be exactly {key_length} characters ({key_size}-bit).")

    key = key_input.encode() if key_valid else None

    if st.button("🚀 Run"):
        if not key_valid:
            st.error("Invalid key length.")
        elif not data:
            st.error("Please provide input data (text or file).")
        else:
            cipher = AES.new(key, AES.MODE_ECB)

            if mode == "Encrypt":
                padded = pad(data, AES.block_size)
                ciphertext = cipher.encrypt(padded)
                b64_cipher = base64.b64encode(ciphertext).decode()
                st.success("✅ Encrypted!")
                st.text_area("Ciphertext (Base64):", value=b64_cipher, height=150)
            else:
                try:
                    decoded = base64.b64decode(data)
                    decrypted = unpad(cipher.decrypt(decoded), AES.block_size)
                    if input_type == "Text":
                        st.success("✅ Decrypted!")
                        st.text_area("Plaintext:", value=decrypted.decode(), height=150)
                    else:
                        st.download_button("📥 Download Decrypted File", data=decrypted, file_name=f"decrypted_{filename}")
                except Exception as e:
                    st.error(f"❌ Decryption failed: {e}")

    st.markdown("---")            
    if st.button("⬅️ Back to Symmetric Algorithms"):
        st.session_state.sym_page = "menu"
        st.rerun()
