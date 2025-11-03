import re


def validate_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def validate_password(password: str) -> bool:
    return len(password) >= 8
