import streamlit as st
import hashlib

def sha_256(data):
    return hashlib.sha256(data).hexdigest()

def md5(data):
    return hashlib.md5(data).hexdigest()

def sha_3(data):
    return hashlib.sha3_256(data).hexdigest()

def ripemd(data):
    h = hashlib.new('ripemd160')
    h.update(data)
    return h.hexdigest()

def hashing(data, mode):
    if mode == "SHA-256":
        return sha_256(data)
    elif mode == "MD5":
        return md5(data)
    elif mode == "SHA-3(256)":
        return sha_3(data)
    elif mode == "RIPEMD(160)":
        return ripemd(data)
    else:
        return "Unsupported mode"

def render():
    st.title("🔐 Hashing Algorithms")
    st.write("Hash text or files using different algorithms")

    with st.expander("ℹ️ What are Hashing Algorithms?"):
        st.write("""
        Hashing algorithms are mathematical functions that convert data into a fixed-size string of characters, 
        known as a hash value or digest. These algorithms are one-way functions, meaning it's computationally 
        difficult to reverse the process and recover the original data. They are commonly used for data integrity checks, 
        password storage, and in various data structures like hash tables. 

        Common hashing algorithms include **MD5**, **SHA-1**, **SHA-2 (SHA-256)**, **SHA-3**, and **RIPEMD**. Each has different levels of security and performance.
        """)

    mode = st.radio("Choose hashing algorithm:", ["SHA-256", "MD5", "SHA-3(256)", "RIPEMD(160)"])

    st.write("### Enter text or upload a file to hash")

    text = st.text_area("Enter text to hash:")
    uploaded_file = st.file_uploader("Or upload a file")

    if st.button("Run Hash Function"):
        if not text.strip() and uploaded_file is None:
            st.error("Please enter some text or upload a file to hash.")
        else:
            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                result = hashing(file_bytes, mode)
                st.success(f"Hash of file '{uploaded_file.name}' using {mode}: {result}")
            else:
                text_bytes = text.encode('utf-8')
                result = hashing(text_bytes, mode)
                st.success(f"Hash of input text using {mode}: {result}")
