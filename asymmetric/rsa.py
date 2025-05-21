import streamlit as st
from math import gcd

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def mod_exp(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result

def mod_inverse(e, t):
    for d in range(2, t):
        if (e * d) % t == 1:
            return d
    return None

def render():
    st.title("🔐 RSA Encryption / Decryption")

    with st.expander("ℹ️ How RSA Works"):
        st.markdown("""
        The **RSA (Rivest-Shamir-Adleman)** algorithm is a widely used **asymmetric public-key cryptosystem**. 
        It uses a pair of mathematically linked keys — a public key for encryption and a private key for decryption — 
        making it essential for secure communication and digital signatures, especially on the internet.

        ### 🔍 Brief History:
        - Developed in 1977 by Ron Rivest, Adi Shamir, and Leonard Adleman.
        - One of the first practical public-key cryptosystems.
        - Forms the backbone of many secure communication protocols today.

        ### 🧠 How It Works (Simplified Pseudocode):
        ```
        Choose two large primes p and q
        Compute n = p * q
        Calculate totient t = (p-1)*(q-1)
        Choose public key exponent e such that 1 < e < t and gcd(e, t) = 1
        Calculate private key exponent d such that (d * e) mod t = 1

        Encryption: For each plaintext number m,
            ciphertext c = (m^e) mod n

        Decryption: For each ciphertext number c,
            plaintext m = (c^d) mod n
        ```

        ### 🔐 Process Description:
        - Two large primes (p and q) generate modulus n.
        - Public key (e, n) encrypts messages by modular exponentiation.
        - Private key (d, n) decrypts messages by modular exponentiation.
        - Messages are converted into numeric form (e.g., ASCII codes) before encryption.
        - Only the holder of the private key can decrypt and recover the original message.

        ### 🛠️ Use Cases:
        - Secure transmission of messages and data.
        - Digital signatures and certificate authorities.
        - Basis for many internet security protocols such as TLS/SSL.

        ### ✉️ Example with the word “bob”:
        - Convert letters to ASCII numbers:  
        'b' → 98, 'o' → 111, 'b' → 98

        - Encrypt with public key → Ciphertext:  
        516 1270 516

        - Only the private key can decrypt these back to 'b', 'o', 'b'.

        This demonstrates how RSA transforms readable text into encrypted numbers, ensuring message secrecy.
        """)





    st.subheader("🔧 Key Generation")
    p = st.number_input("Value of prime number p:", min_value=2, value=53)
    q = st.number_input("Value of prime number q:", min_value=2, value=61)

    if not is_prime(p) or not is_prime(q):
        st.error("❌ Both p and q must be prime numbers.")
        return

    n = p * q
    t = (p - 1) * (q - 1)

    e = st.number_input("Enter public key exponent e (coprime with t):", min_value=2, max_value=t-1, value=1409)

    if gcd(e, t) != 1:
        st.error(f"❌ The entered e = {e} is not coprime with t = {t}.")
        return

    d = mod_inverse(e, t)
    if not d:
        st.error("❌ Couldn't find modular inverse of e. Try a different value.")
        return

    st.success(f"""
    ✅ Key Pair Generated:
    - n = {n}
    - t = {t}
    - Public Key (e, n): ({e}, {n})
    - Private Key (d, n): ({d}, {n})
    """)

    st.divider()
    st.subheader("🔒 Encryption")

    plain_text = st.text_input("Enter message to encrypt (letters, spaces, symbols allowed):")
    if st.button("Encrypt"):
        if not plain_text.strip():
            st.warning("Please enter a message.")
        else:
            cipher_nums = [
                mod_exp(ord(c), e, n)
                for c in plain_text
            ]
            st.success("🔐 Encrypted Message (as numbers):")
            st.code(' '.join(map(str, cipher_nums)), language="text")

    st.divider()
    st.subheader("🔓 Decryption")

    cipher_input = st.text_area("Enter ciphertext numbers (space-separated):", placeholder="Example: 855 1311 2187 ...")
    priv_d = st.number_input("Enter private key d:", min_value=1, value=d)
    priv_n = st.number_input("Enter modulus n:", min_value=1, value=n)

    if st.button("Decrypt"):
        try:
            cipher_list = [int(c) for c in cipher_input.strip().split()]
            decrypted_chars = [
                chr(mod_exp(c, priv_d, priv_n))
                for c in cipher_list
            ]
            decrypted_message = ''.join(decrypted_chars)
            st.success("🟢 Decrypted Message:")
            st.text_area("Result:", value=decrypted_message, height=150)
        except Exception as e:
            st.error(f"Decryption failed: {e}")

    st.markdown("---")
    if st.button("⬅️ Back to Asymmetric Algorithms"):
        st.session_state.asym_page = "menu"
        st.rerun()
