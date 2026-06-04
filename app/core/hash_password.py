from pwdlib import PasswordHash

# Initialize with OWASP recommended secure settings
password_hash = PasswordHash.recommended()

# Generates a secure hash from a plain text password.
def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

 # Verifies a plain text password against an existing database hash.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)