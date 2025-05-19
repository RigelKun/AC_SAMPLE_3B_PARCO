import streamlit as st
import hashlib 

def sha_256(text):
    encoded_string = text.encode('utf-8')
    hash_object = hashlib.sha256(encoded_string)
    hex_digest = hash_object.hexdigest()
    return hex_digest

def render():
    st.title("🔐 SHA-256 Hashing Algorithm")
    st.write("Hash a message using SHA-256")
    with st.expander("ℹ️ What is SHA-256??"):
        st.write("""
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; SHA-256 is a cryptographic hash 
                 function that produces a 256-bit hash value, 
                 also known as a "fingerprint" or "signature,"
                  for any given input. It's part of the Secure 
                 Hash Algorithm 2 (SHA-2) family, which is 
                 widely used for security and data integrity 
                 verification.
        """)
    text = st.text_input("Enter text:")
    mode = st.radio("Choose mode:", ["SHA-256", "MD5", "SHA-3", "RIPEMD"])
    if st.button("Run Hash Function"):
        if not text.strip():
            st.error("Please enter some text.")
        else:
            result = hashing(text)
            st.success(f"Result: {result}")
            