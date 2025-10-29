from auth import hash_password, verify_password


def test_hash_password():
    # --- Arrange ---
    password = "password123"

    # --- Act ---
    hashed_password = hash_password(password)

    # --- Assert ---
    # 1. The hash should ot be None or empty
    assert hashed_password is not None

    # 2. The hash should NOT be the same as the original password
    assert hashed_password != password

    # 3. A bcrypt hash always starts with "$2b$"
    assert hashed_password.startswith("$2b$")


def test_verify_password():
    # --- Arrange ---
    password = "password123"
    hashed_password = hash_password(password)

    # --- Act & Assert ---
    # 1. Assert that the correct password returns True
    assert verify_password(password, hashed_password) == True

    # 2. Assert that an incorrect password returns False
    assert verify_password("wrongpassword", hashed_password) == False