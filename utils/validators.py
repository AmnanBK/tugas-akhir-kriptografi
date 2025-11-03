import re


def validate_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def validate_password(password: str) -> bool:
    return len(password) >= 8


def validate_username(username: str) -> bool:
    return re.match(r"^[A-Za-z0-9_]+$", username) is not None
