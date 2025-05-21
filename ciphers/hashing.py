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
            **Hashing algorithms** are cryptographic functions that take input data of any size and produce a fixed-size output called a **hash value** or **digest**.  
            These algorithms are *one-way functions* — once data is hashed, it is computationally infeasible to retrieve the original input from the hash alone.

            ### Brief History and Popular Algorithms:
            - **MD5** (Message Digest 5): Developed in 1991 by Ronald Rivest, MD5 produces a 128-bit hash. It was widely used for data integrity checks but is now considered insecure due to vulnerabilities to collisions.
            - **SHA-256** (Secure Hash Algorithm 256-bit): Part of the SHA-2 family designed by the NSA, released in 2001. It outputs a 256-bit hash and is currently widely used for security-critical applications.
            - **SHA-3**: The latest member of the SHA family, standardized in 2015, based on the Keccak algorithm. It provides similar output sizes but a different internal design, offering resistance against various attacks.
            - **RIPEMD-160**: Developed in the mid-1990s as an alternative to MD5 and SHA-1, producing a 160-bit hash. It remains used in some blockchain and cryptographic applications.

            ### How Hashing Works (Simplified Overview):
            1. Input data is processed in fixed-size blocks.
            2. Each block is mixed with intermediate hash states using bitwise operations, modular addition, and compression functions.
            3. After all blocks are processed, the final hash digest is produced.

            ### Common Use Cases:
            - Verifying data integrity (e.g., checksums for downloads)
            - Password storage (storing hash instead of plaintext password)
            - Digital signatures and certificates
            - Cryptographic applications in blockchain and security protocols

            Hashing ensures that even a tiny change in input data produces a drastically different hash, making it ideal for detecting tampering and verifying authenticity.
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
            
    if st.button("⬅️ Back to Main Menu"):
        st.session_state.page = "Main Menu"
        st.rerun()