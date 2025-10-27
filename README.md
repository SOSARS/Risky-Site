---

## 🔬 Security Analysis: SQL Injection (AUTH BYPASS variant)

This initial version of the application is **intentionally vulnerable** to a classic SQL Injection attack.

### The Flaw
The vulnerability exists in the `app.py` file, where user input is directly formatted into an SQL query using an f-string. This allows an attacker to inject their own SQL commands.

**Vulnerable Code (`app.py`):**
```
python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

### The Exploit
An attacker can bypass the login form without a password by injecting a tautology (a statement that is always true) into the query.
1. **Run the application:** `py app.py`
2. **Open the login form** in a browser.
3. **Enter the following payload** in the `username` field:
```SQL
' OR 1=1 --
```
4. Leave the `password` field blank and submit.


### Why It Works
The injected payload modifies the SQL query to:
```SQL
SELECT * FROM users WHERE username = '' OR 1=1 -- ' AND password = ''
```
The database sees `OR 1=1`, which is always true, and the `--` comment marker tells the database to ignore the rest of the query (the password check). The query therefore returns the first user in the database, resulting in a successful login bypass.

### The Fix: Parameterised Queries & Password Hashing

The application has been patched to prevent SQL Injection and to securely store user passwords.

1.  **SQL Injection:** The vulnerable f-string query was replaced with a **parameterised query**. The `?` placeholder ensures that user input is treated as data, not as executable code, making injection attacks impossible.

    **Secure Code (`app.py`):**
    ```python
    query = 'SELECT * FROM users WHERE username = ?'
    user = conn.execute(query, (username,)).fetchone()
    ```

2.  **Password Storage:** Plaintext passwords have been replaced with secure hashes using the `bcrypt` library.
    * **Hashing:** New passwords are put through a one-way hashing algorithm with a random salt before being stored.
    * **Verification:** At login, the submitted password is put through the same process and the resulting hash is compared to the one in the database. This means the actual password is never stored or compared directly.

---
