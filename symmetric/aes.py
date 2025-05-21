import streamlit as st
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def render():
    st.title("🔐 AES (ECB Mode)")
    st.write("Encrypt or decrypt data using the AES algorithm in ECB mode.")

    with st.expander("ℹ️ What is AES (ECB Mode)?"):
        st.markdown("""
        **AES (Advanced Encryption Standard)** is a widely used **symmetric block cipher** designed to encrypt data in fixed-size blocks of 128 bits. The **ECB (Electronic Codebook)** mode is the simplest form of AES, where each block is encrypted independently using the same key.

        ### 🔍 Brief History:
        - Standardized by NIST in 2001 to replace the aging DES algorithm.
        - Developed by Belgian cryptographers Joan Daemen and Vincent Rijmen as the Rijndael cipher.
        - AES is now a global standard for secure data encryption.

        ### 🧠 Simplified Process (Pseudocode):
        ```
        Encryption:
            1. Pad the plaintext to a multiple of 16 bytes.
            2. Split plaintext into 16-byte blocks.
            3. For each block:
                Encrypted_Block = AES_Encrypt(Block, Key)

        Decryption:
            1. Split ciphertext into 16-byte blocks.
            2. For each block:
                Decrypted_Block = AES_Decrypt(Block, Key)
            3. Remove padding from the final result.
        ```

        ### 🔐 How ECB Mode Works:
        - Uses a **fixed-size key** (128/192/256 bits) and splits input into **independent blocks**.
        - Each block is encrypted separately with the same key.
        - Simplicity comes at a cost: **identical plaintext blocks produce identical ciphertext blocks**, which can expose patterns.

        ### 🛠️ Common Use Cases:
        - Suitable for **testing, low-risk internal data**, or when encrypting short, unique blocks.
        - **Not recommended** for sensitive or repetitive data due to vulnerability to block-pattern analysis.

        ### ✉️ Example:
        ```
        Plaintext:  helloworld
        Key:        thiskeylongerfrf
        Key Size:   128 bits
        Ciphertext: fbsc9OsCpFSKVtXTSt31OFzvqaxxxTN8HuBGbCqqdXw=
        ```

        ⚠️ **Note:** ECB mode is **not secure** for large or patterned data. Use **CBC, GCM, or other secure modes** for real-world applications.
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
