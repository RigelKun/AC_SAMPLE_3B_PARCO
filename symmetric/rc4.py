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
        st.markdown("""
        **RC4 (Rivest Cipher 4)** is a **symmetric stream cipher** known for its simplicity and speed. 
        It generates a pseudo-random keystream from a secret key and XORs it with the plaintext to 
        produce the ciphertext. The same operation is used for decryption.

        ### 🔍 Brief History:
        - Designed by Ron Rivest in 1987.
        - Originally a trade secret of RSA Security, later leaked and became widely used.
        - Common in early protocols like SSL/TLS and WEP, but now deprecated due to discovered vulnerabilities.

        ### 🧠 How It Works (Simplified Pseudocode):
        ```
        Key Scheduling Algorithm (KSA):
            Initialize an array S with values from 0 to 255.
            Use the key to shuffle the array S.

        Pseudo-Random Generation Algorithm (PRGA):
            For each byte of input:
                Continuously update indices i and j and swap values in S.
                Generate a keystream byte from S.
                XOR the keystream byte with the plaintext byte to get the ciphertext.
        ```

        ### 🔐 Process Description:
        - RC4 turns a key (usually a byte array) into a pseudo-random keystream.
        - Each byte of the plaintext is XORed with a byte from the keystream.
        - Decryption works the same way as encryption: `Cipher XOR Keystream = Plaintext`.

        ### 🛠️ Use Cases:
        - Previously used in WEP (Wi-Fi), SSL/TLS (HTTPS), and Microsoft PPTP VPN.
        - Currently **not recommended** for secure applications due to bias and vulnerability issues.
        - Still useful in educational demos and legacy systems.

        ### ✉️ Example:
        ```
        Plaintext:  Hello im bob
        Key:        love
        Encrypted:  ¨�Í*Ñ)�©Ë#~E
                    (Output limited to printable characters — others shown as �)
        ```

        ⚠️ **Note:** RC4 may produce non-printable or special characters in its output. 
        The encrypted result may not display correctly, but decryption using the same key will still work.
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
