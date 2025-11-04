import re


def validate_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def validate_password(password: str) -> bool:
    return len(password) >= 8


def validate_username(username: str) -> bool:
    return re.match(r"^[A-Za-z0-9_]+$", username) is not None


def validate_caesar_key(value: str) -> bool:
    if not value.isdigit():
        return False
    num = int(value)
    return 0 <= num <= 25


def validate_vigenere_key(key: str) -> bool:
    return re.fullmatch(r"[A-Za-z\s]+", key) is not None
