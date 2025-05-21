import streamlit as st
from math import gcd

# Primality check
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

# Fast exponentiation
def mod_exp(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result

# Modular inverse
def mod_inverse(e, t):
    for d in range(2, t):
        if (e * d) % t == 1:
            return d
    return None

def render():
    st.title("🔐 RSA Encryption / Decryption")

    with st.expander("ℹ️ How RSA Works"):
        st.write("""
        RSA is a way to securely send messages using two special keys:

        - **Public key** — you share this with everyone. People use it to lock (encrypt) messages they want to send to you.
        - **Private key** — you keep this secret. Only you can use it to unlock (decrypt) the messages sent with your public key.

        Here’s the basic process:
        
        1. You pick two large prime numbers and multiply them together to create a number called **n**.
        2. From these primes, you generate two keys: one public and one private.
        3. When someone wants to send you a message, they use your public key to encrypt it — turning the message into something unreadable.
        4. When you get the message, you use your private key to decrypt it back to the original text.

        This way, even if someone intercepts the encrypted message, they can’t read it without your private key.

        The app lets you enter your primes and keys, encrypt messages using the public key, and decrypt messages using the private key — all while keeping spaces and letter casing intact.
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
