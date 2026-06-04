import re

def validate_password(password: str) -> str:

    if len(password) < 8:
        raise ValueError(
            "Password must be at least 8 characters"
        )

    if not re.search(r"[A-Z]", password):
        raise ValueError(
            "Password must contain an uppercase letter"
        )

    if not re.search(r"[a-z]", password):
        raise ValueError(
            "Password must contain a lowercase letter"
        )

    if not re.search(r"\d", password):
        raise ValueError(
            "Password must contain a number"
        )

    if not re.search(
        r"[!@#$%^&*(),.?\":{}|<>]",
        password
    ):
        raise ValueError(
            "Password must contain a special character"
        )

    return password