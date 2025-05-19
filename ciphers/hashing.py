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
    st.write("Hash **text** or **files** using cryptographic hash functions.")

    with st.expander("ℹ️ What are Hashing Algorithms?"):
        st.markdown("""
        Hashing algorithms are mathematical functions that convert data into a 
        fixed-size string of characters, known as a hash value or digest. These algorithms are one-way functions, meaning 
        it's computationally difficult to reverse the process and recover the original data. They are commonly used for data integrity checks, 
        password storage, and in various data structures like hash tables. 
        
        Some hashing algorithms are: **MD5**, **SHA-256**, **SHA-3**, **RIPEMD-160**
        """)

    mode = st.radio("🔢 Choose hashing algorithm:", ["SHA-256", "MD5", "SHA-3(256)", "RIPEMD(160)"])
    
    input_type = st.radio("📥 Select input type:", ["Text", "File"])

    data = None
    if input_type == "Text":
        text = st.text_area("📝 Enter text:")
        if text.strip():
            data = text.encode('utf-8')
    else:
        uploaded_file = st.file_uploader("📂 Upload a file to hash")
        if uploaded_file:
            data = uploaded_file.read()

    if st.button("🔄 Run Hash Function"):
        if data is None:
            st.error("⚠️ Please provide input (text or file).")
        else:
            result = hashing(data, mode)
            label = uploaded_file.name if input_type == "File" and uploaded_file else "entered text"
            st.success(f"✅ Hash of {label} using {mode}:\n\n`{result}`")
