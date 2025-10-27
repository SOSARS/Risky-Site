---

## 🔬 Security Analysis: SQL Injection (CVE-2021-44228)

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
