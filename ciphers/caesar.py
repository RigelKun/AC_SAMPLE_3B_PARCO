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
    with st.expander("ℹ️ What is Caesar Cipher?"):
        st.write("""
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Caesar cipher, also known as Caesar's cipher, the shift cipher, Caesar's code, 
        or Caesar shift, is one of the simplest and most widely known encryption techniques. 
        It is a type of substitution cipher in which each letter in the plaintext is replaced by a 
        letter some fixed number of positions down the alphabet. 
    
        Non-letter characters like spaces and punctuation are not changed.
        """)

    mode = st.radio("Choose mode:", ["Encrypt", "Decrypt"])
    text = st.text_input("Enter the text:")
    key = st.number_input("Enter the key (1–25):", min_value=1, max_value=25, value=3)

    if st.button("Run Caesar Cipher"):
        if not text.strip():
            st.error("Please enter some text.")
        elif text.isnumeric():
            st.warning("Input must be a string, not a number.")
        else:
            result = caesar_cipher(text, key, mode.lower())
            st.success(f"Result: {result}")
            if any(not c.isalpha() and not c.isspace() for c in text):
                st.info("Note: Non-letter characters (e.g., punctuation, numbers) were left unchanged.")
