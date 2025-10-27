import bcrypt


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt with a generated salt."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password_bytes, salt).decode("utf-8")
    return hashed_pass


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a stored hash against a password."""
    password_bytes = password.encode("utf-8")
    hash_bytes = stored_hash.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_bytes)

