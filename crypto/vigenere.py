def generate_key(plaintext: str, key: str) -> str:
    key = key.upper()
    key_extended = ""
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            key_extended += key[key_index % len(key)]
            key_index += 1
        else:
            key_extended += char
    return key_extended


def encrypt_vigenere(plaintext: str, key: str) -> str:
    ciphertext = ""
    key_extended = generate_key(plaintext, key)

    for p_char, k_char in zip(plaintext, key_extended):
        if p_char.isupper():
            shift = ord(k_char) - 65
            ciphertext += chr((ord(p_char) - 65 + shift) % 26 + 65)
        elif p_char.islower():
            shift = ord(k_char) - 65
            ciphertext += chr((ord(p_char) - 97 + shift) % 26 + 97)
        else:
            ciphertext += p_char
    return ciphertext


def decrypt_vigenere(ciphertext: str, key: str) -> str:
    plaintext = ""
    key_extended = generate_key(ciphertext, key)

    for c_char, k_char in zip(ciphertext, key_extended):
        if c_char.isupper():
            shift = ord(k_char) - 65
            plaintext += chr((ord(c_char) - 65 - shift) % 26 + 65)
        elif c_char.islower():
            shift = ord(k_char) - 65
            plaintext += chr((ord(c_char) - 97 - shift) % 26 + 97)
        else:
            plaintext += c_char
    return plaintext
