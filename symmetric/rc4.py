import streamlit as st

def rc4(key, text):
    S = list(range(256))
    j = 0
    key_bytes = [ord(c) for c in key]
    key_length = len(key_bytes)

    for i in range(256):
        j = (j + S[i] + key_bytes[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    result = []
    for char in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        result.append(chr(ord(char) ^ K))
    return ''.join(result)

def render():
    st.title("🔐 RC4 Stream Cipher")
    st.write("Encrypt or decrypt a message using the RC4 stream cipher.")

    with st.expander("ℹ️ What is RC4?"):
        st.write("""
        RC4 is a stream cipher that uses a secret key to generate a pseudo-random keystream. This keystream is XORed with the plaintext to produce ciphertext, and the same process is used to decrypt.
        
        **Example:**
        - Plaintext: `Hello im bob`
        - Key: `love`
        - Encrypted Output: `¨�Í*Ñ)�©Ë#~E`  
          *(Output limited to printable characters — some characters replaced by �)*

        ⚠️ RC4 may produce non-printable characters in the result. You can still decrypt correctly using the same key.
        """)

    mode = st.radio("Choose mode:", ["Encrypt", "Decrypt"])
    input_type = st.radio("Input type:", ["Text", "File"])

    text = ""
    filename = None

    if input_type == "Text":
        if mode == "Encrypt":
            text = st.text_area("Enter plaintext:")
        else:
            text = st.text_area("Enter ciphertext:")
    else:
        uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded_file:
            text = uploaded_file.read().decode("utf-8")
            filename = uploaded_file.name

    key = st.text_input("Enter the secret key (any length):", max_chars=256)

    if st.button(f"Run RC4 {mode}"):
        if not text.strip():
            st.error("Please enter some text or upload a file.")
        elif not key:
            st.error("Please enter a secret key.")
        else:
            result = rc4(key, text)
            st.success("✅ Operation successful!")
            st.text_area("Result:", value=result, height=200)

    st.markdown("---")
    if st.button("⬅️ Back to Symmetric Algorithms"):
        st.session_state.sym_page = "menu"
        st.rerun()
