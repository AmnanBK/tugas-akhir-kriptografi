from typing import ByteString, Generator


def KSA(key: ByteString) -> list[int]:
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S


def PRGA(S: list[int]) -> Generator[int, None, None]:
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K


def rc4_encrypt_decrypt(data: bytes, key: bytes) -> bytes:
    S = KSA(key)
    keystream = PRGA(S)
    output = bytearray()
    for byte in data:
        k = next(keystream)
        output.append(byte ^ k)
    return bytes(output)
