def encrypt_caesar(plaintext: str, shift: int) -> str:
    ciphertext = ""
    for char in plaintext:
        if char.isupper():
            ciphertext += chr((ord(char) - 65 + shift) % 26 + 65)
        elif char.islower():
            ciphertext += chr((ord(char) - 97 + shift) % 26 + 97)
        else:
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int) -> str:
    return encrypt_caesar(ciphertext, -shift)
