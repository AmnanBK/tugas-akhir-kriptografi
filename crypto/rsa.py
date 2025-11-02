import random
from math import gcd


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_prime(start=100, end=300) -> int:
    while True:
        p = random.randint(start, end)
        if is_prime(p):
            return p


def modinv(a: int, m: int) -> int:
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def generate_keys() -> tuple:
    p = generate_prime()
    q = generate_prime()
    while q == p:
        q = generate_prime()

    n = p * q
    phi = (p - 1) * (q - 1)

    # pilih e
    e = 3
    while gcd(e, phi) != 1:
        e += 2

    d = modinv(e, phi)
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key


def encrypt(message: str, public_key: tuple) -> list:
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in message]
    return cipher


def decrypt(cipher: list, private_key: tuple) -> str:
    d, n = private_key
    message = "".join([chr(pow(char_code, d, n)) for char_code in cipher])
    return message
