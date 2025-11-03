import os
import base64

BLOCK_SIZE = 16  # AES-128

# Padding PKCS#7
def pad(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad_len] * pad_len)

def unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

# AES Block Cipher (XOR) - placeholder
def aes_block_encrypt(block: bytes, key: bytes) -> bytes:
    return bytes([b ^ k for b, k in zip(block, key)])

def aes_block_decrypt(block: bytes, key: bytes) -> bytes:
    return bytes([b ^ k for b, k in zip(block, key)])

# AES-128 CBC Mode
def encrypt_cbc(plaintext: bytes, key: bytes) -> bytes:
    plaintext = pad(plaintext)
    iv = os.urandom(BLOCK_SIZE)
    ciphertext = b""
    prev = iv
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        xored = bytes([b ^ p for b, p in zip(block, prev)])
        enc = aes_block_encrypt(xored, key)
        ciphertext += enc
        prev = enc
    return iv + ciphertext  # prepend IV

def decrypt_cbc(ciphertext: bytes, key: bytes) -> bytes:
    iv = ciphertext[:BLOCK_SIZE]
    ciphertext = ciphertext[BLOCK_SIZE:]
    plaintext = b""
    prev = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        dec = aes_block_decrypt(block, key)
        xored = bytes([d ^ p for d, p in zip(dec, prev)])
        plaintext += xored
        prev = block
    return unpad(plaintext)

def encrypt_text(value_text: str, key: bytes) -> str:
    enc_bytes = encrypt_cbc(value_text.encode("utf-8"), key)
    return base64.b64encode(enc_bytes).decode("utf-8")

def decrypt_text(enc_b64: str, key: bytes) -> str:
    enc_bytes = base64.b64decode(enc_b64.encode("utf-8"))
    return decrypt_cbc(enc_bytes, key).decode("utf-8")