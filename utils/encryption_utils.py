from crypto.caesar import encrypt_caesar, decrypt_caesar
from crypto.vigenere import encrypt_vigenere, decrypt_vigenere
from crypto.rsa import generate_keys, encrypt as rsa_encrypt, decrypt as rsa_decrypt

# Konfigurasi default
DEFAULT_CAESAR_KEY = 3
DEFAULT_VIGENERE_KEY = "SECRET"


# Fungsi Super Encryption
def super_encrypt(
    message: str,
    caesar_key: int = DEFAULT_CAESAR_KEY,
    vigenere_key: str = DEFAULT_VIGENERE_KEY,
    rsa_public: tuple | None = None,
) -> tuple[str, list]:
    # Caesar
    caesar_encrypted = encrypt_caesar(message, caesar_key)

    # Vigenere
    vigenere_encrypted = encrypt_vigenere(caesar_encrypted, vigenere_key)

    # RSA
    if rsa_public is None:
        rsa_public, rsa_private = generate_keys()
    rsa_cipher = rsa_encrypt(vigenere_encrypted, rsa_public)

    return rsa_cipher


# Fungsi Super Decryption
def super_decrypt(
    rsa_cipher: list,
    rsa_private: tuple,
    vigenere_key: str = DEFAULT_VIGENERE_KEY,
    caesar_key: int = DEFAULT_CAESAR_KEY,
) -> str:
    decrypted_rsa = rsa_decrypt(rsa_cipher, rsa_private)
    decrypted_vigenere = decrypt_vigenere(decrypted_rsa, vigenere_key)
    decrypted_caesar = decrypt_caesar(decrypted_vigenere, caesar_key)

    return decrypted_caesar
