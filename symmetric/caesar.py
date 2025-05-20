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
        The Caesar cipher is a basic encryption technique that shifts each letter 
        in a message by a fixed number of positions down the alphabet. It's a substitution cipher, 
        meaning each letter is replaced with another letter according to a predefined rule. 
    
        Non-letter characters like spaces and punctuation are not changed.
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
