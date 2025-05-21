import streamlit as st

def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

def generate_vigenere_key(shared_key, length):
    shifts = [chr((int(digit) % 26) + ord('a')) for digit in str(shared_key)]
    key = ''.join(shifts)
    return (key * (length // len(key) + 1))[:length]

def vigenere_encrypt(text, key):
    result = []
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i]) - ord('a')
            enc = (ord(char.lower()) - ord('a') + shift) % 26
            result.append(chr(enc + ord('a')))
        else:
            result.append(char)
    return ''.join(result)

def vigenere_decrypt(text, key):
    result = []
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i]) - ord('a')
            dec = (ord(char.lower()) - ord('a') - shift) % 26
            result.append(chr(dec + ord('a')))
        else:
            result.append(char)
    return ''.join(result)


def is_prime(n: int) -> bool:
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

def is_primitive_root(g: int, p: int) -> bool:
    if not is_prime(p):
        return False
    required_set = set(range(1, p))
    actual_set = set(pow(g, powers, p) for powers in range(1, p))
    return required_set == actual_set

def render():
    st.title("🔐 Diffie-Hellman Key Exchange")
    with st.expander("ℹ️ What is Diffie-Hellman Key Exchange?"):
        st.markdown("""
        The **Diffie-Hellman Key Exchange** is an **asymmetric key exchange protocol** that allows two parties to securely generate a shared secret key over an insecure communication channel.

        ### 🔍 Brief History:
        - Proposed in 1976 by Whitfield Diffie and Martin Hellman.
        - The first practical method enabling secure key exchange without prior shared secrets.
        - Fundamental in modern cryptography and widely used in protocols like TLS.

        ### 🧠 How It Works (Simplified Pseudocode):
        ```
        Agree on a large prime number p and generator g
        Each user picks a private key (a, b)
        Compute public keys: A = g^a mod p, B = g^b mod p
        Exchange public keys A and B
        Compute shared secret: s = B^a mod p = A^b mod p
        ```

        ### 🔐 Process Description:
        - Both parties agree on public parameters p (prime) and g (generator).
        - Each chooses a private key and computes their public key.
        - By exchanging public keys and performing modular exponentiation with their private keys, both compute the same shared secret number.
        - This shared secret can then be converted into a symmetric key for encryption algorithms.

        ### 🛠️ Use Cases:
        - Securely establishing symmetric keys over insecure channels.
        - Foundation for secure communications in internet protocols.
        - Often combined with classical ciphers to provide encryption keys.

        ### ✉️ Example:
        ```
        Shared secret number: 18
        Converted key for Vigenère cipher: "BI"
        ```
        Here, digit '1' maps to 'B' and '8' maps to 'I', which is then used as the Vigenère cipher key.
        """)

        
        
        
    st.header("1. Diffie-Hellman Key Exchange")

    p = st.number_input("Enter prime number (p):", min_value=2, value=23)
    if not is_prime(p):
        st.warning("⚠️ The number entered for p is NOT prime. Please enter a prime number.")

    g = st.number_input("Enter generator (g):", min_value=2, value=5)
    if is_prime(p) and not is_primitive_root(g, p):
        st.warning(f"⚠️ {g} is NOT a primitive root modulo {p}. Please enter a valid generator.")

    private_key = st.number_input("Enter your private key:", min_value=1, value=8)

    if is_prime(p) and is_primitive_root(g, p):
        public_key = mod_exp(g, private_key, p)
        st.write(f"🔑 Your Public Key: `{public_key}`")

        other_public = st.number_input("Enter received public key from other party:", min_value=1, value=3)

        if st.button("Compute Shared Key"):
            st.session_state.shared_key = mod_exp(other_public, private_key, p)

        if "shared_key" in st.session_state:
            shared_key = st.session_state.shared_key
            st.success(f"Shared Secret Key: `{shared_key}`")

            st.header("2. Vigenère Cipher Encryption & Decryption")

            encrypt_text = st.text_input("🔏 Enter plaintext to encrypt:", key="enc")
            if st.button("Encrypt"):
                if encrypt_text:
                    v_key_enc = generate_vigenere_key(shared_key, len(encrypt_text))
                    encrypted = vigenere_encrypt(encrypt_text, v_key_enc)
                    st.write(f"🔐 Vigenère Key Used: `{v_key_enc}`")
                    st.success(f"Encrypted Result: `{encrypted}`")
                else:
                    st.warning("Please enter text to encrypt.")

            decrypt_text = st.text_input("🔓 Enter ciphertext to decrypt:", key="dec")
            if st.button("Decrypt"):
                if decrypt_text:
                    v_key_dec = generate_vigenere_key(shared_key, len(decrypt_text))
                    decrypted = vigenere_decrypt(decrypt_text, v_key_dec)
                    st.write(f"🔐 Vigenère Key Used: `{v_key_dec}`")
                    st.success(f"Decrypted Result: `{decrypted}`")
                else:
                    st.warning("Please enter text to decrypt.")
    else:
        st.info("Please enter valid prime and generator to continue.")



    st.markdown("---")
    if st.button("⬅️ Back to Asymmetric Menu"):
        st.session_state.asym_page = "menu"
        st.rerun()
