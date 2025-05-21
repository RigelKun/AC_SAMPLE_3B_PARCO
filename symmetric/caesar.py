import streamlit as st

def caesar_cipher(text, key, mode="encrypt"):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = key if mode == "encrypt" else -key
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def render():
    st.title("🔐 Caesar Cipher")
    st.write("Encrypt or decrypt a message using the Caesar Cipher.")

    with st.expander("ℹ️ What is the Caesar Cipher?"):
        st.markdown("""
        The **Caesar Cipher** is a **symmetric substitution cipher** and one of the oldest known encryption techniques. 
        It was used by Julius Caesar to send confidential military messages by shifting each letter in the plaintext 
        by a fixed number of positions down the alphabet.

        ### 🔍 Brief History:
        - Named after Julius Caesar, who used it in 58 BC.
        - One of the simplest and most well-known encryption techniques.
        - Easily broken with brute force or frequency analysis, but foundational in cryptography education.

        ### 🧠 How It Works (Simplified Pseudocode):
        ```
        For each letter in the plaintext:
            Convert the letter to its alphabet index (A=0, B=1, ..., Z=25).
            Add the shift key for encryption or subtract it for decryption.
            Apply modulo 26 to wrap around the alphabet.
            Convert the result back to a letter.
        ```

        ### 🔐 Process Description:
        - Each letter in the plaintext is shifted by a fixed number (the key).
        - Encryption: `Ci = (Pi + key) mod 26`
        - Decryption: `Pi = (Ci - key + 26) mod 26`
        - Only alphabetic characters are encrypted; all others are left unchanged.
        - The same key is used for both encryption and decryption.

        ### 🛠️ Use Cases:
        - Originally used for secure military communication.
        - Often used for puzzles, games, and teaching encryption fundamentals.
        - Simple enough for manual implementation, making it a great learning tool.

        ### ✉️ Example:
        ```
        Plaintext:  HELLO
        Key:        3
        Encrypted:  KHOOR
        ```
        """)


    mode = st.radio("Choose mode:", ["Encrypt", "Decrypt"])
    input_type = st.radio("Input type:", ["Text", "File"])

    text = ""
    filename = None

    if input_type == "Text":
        text = st.text_input("Enter the text:")
    else:
        uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded_file:
            text = uploaded_file.read().decode("utf-8")
            filename = uploaded_file.name

    key = st.number_input("Enter the key (1–25):", min_value=1, max_value=25, value=3)

    if st.button("Run Caesar Cipher"):
        if not text.strip():
            st.error("Please enter some text or upload a file.")
        elif input_type == "Text" and text.isnumeric():
            st.warning("Input must be a string, not a number.")
        else:
            result = caesar_cipher(text, key, mode.lower())
            st.success("✅ Operation successful!")
            st.text_area("Result:", value=result, height=200)

            if input_type == "File":
                st.download_button(
                    label="📥 Download Result",
                    data=result.encode(),
                    file_name=f"{mode.lower()}ed_{filename or 'output.txt'}",
                    mime="text/plain"
                )

            if any(not c.isalpha() and not c.isspace() for c in text):
                st.info("Note: Non-letter characters (e.g., punctuation, numbers) were left unchanged.")

    st.markdown("---")
    if st.button("⬅️ Back to Symmetric Algorithms"):
        st.session_state.sym_page = "menu"
        st.rerun()
