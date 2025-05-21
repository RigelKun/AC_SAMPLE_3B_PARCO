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
        st.write("""
        **Diffie-Hellman key exchange** is a secure method that lets two parties generate a **shared secret key** over an insecure channel, without revealing their private keys.
        
        Here’s how it works in simple terms:
        
        - Both users agree on a large prime number `p` and a generator `g`.
        - Each picks a private key (secret number), computes a public key, and exchanges the public keys.
        - Using their own private key and the other’s public key, both compute the **same shared secret key**.
        
        This shared secret is a **number** (e.g., 18) that only they know, even if someone is eavesdropping.
        
        Since the **Vigenère cipher** requires a key made of letters, we convert this number into a string of letters to use as the cipher key:
        
        - Convert each digit of the shared number into a letter by mapping `0 → A`, `1 → B`, `2 → C`, ..., `9 → J`.
        - For example, `18` becomes `B` (for 1) and `I` (for 8), so the key is `"BI"`.
        - This key is repeated or truncated to match the length of the message.
        
        The shared secret number thus seeds the Vigenère key, allowing **secure encryption and decryption** of messages.
        
        This combination leverages Diffie-Hellman’s secure key exchange with Vigenère’s classic substitution cipher.
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
