# RiskySite 🔓: A Deliberately Insecure Web Application

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

This project is a simple blog application built with Flask and SQLite. It is **intentionally vulnerable** to some of the most common and critical web security flaws, as defined by the OWASP Top 10.

Its purpose is to serve as a hands-on learning sandbox to demonstrate a practical understanding of identifying, exploiting, and — most importantly — **patching** major security vulnerabilities.

---

## 🎯 Learning Objectives Demonstrated

This project showcases a practical understanding of the following security concepts:

* **Vulnerability Identification & Exploitation:**
    * **SQL Injection (SQLi):** Bypassing authentication by injecting malicious SQL into login forms.
    * **Stored Cross-Site Scripting (XSS):** Injecting malicious JavaScript into a comments section to hijack other users' sessions.
* **Defensive Coding & Patching:**
    * **Password Hashing:** Using `bcrypt` to securely store passwords instead of plaintext.
    * **Parameterised Queries:** The industry-standard method for preventing SQL Injection.
    * **Input Sanitisation & Output Escaping:** The core principle for mitigating XSS attacks.

---

## 🧰 Tech Stack

| Category         | Tools & Libraries                               |
| ---------------- | ----------------------------------------------- |
| **Language** | Python 3                                        |
| **Framework** | Flask                                           |
| **Database** | SQLite                                          |
| **Authentication** | `bcrypt` for secure password hashing            |
| **Frontend** | Basic HTML & CSS with Jinja2 Templating         |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/SOSARS/Risky-Site.git
cd Risky-Site
```

### 2. Environment Setup
Create and activate a Python virtual environment
``` PowerShell
# Create the virtual environment
py -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```Bash
pip install -r requirements.txt   # Bash
```

```PowerShell
py -m pip install -r requirements.txt  # Windows
```

### 4. Initialise the Database
This script creates the users.db file and populates it with a sample admin account.
```Bash
python3 init_db.py  # Bash
```

```PowerShell
py init_db.py  # Windows
```

### 5. Run the Application
```Bash
python3 app.py  # Bash
```

```PowerShell
py app.py  # Windows
```

---
#### The application will now be running at `http://127.0.0.1:5000`
---

# 🔬 Security Analysis: The Two Flaws
This application was built with two critical, intentional vulnerabilities. The Git history for this project tells the story of their discovery, documentation, and remediation.

### 🚩 Vulnerability #1: SQL Injection
* **The Flaw:** The initial login logic used an unsafe f-string to build the SQL query, directly embedding user input. This allowed an attacker to break out of the string and inject their own SQL commands.

#### ❌ Vulnerable Code (`app.py`):

```Python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

* **The Exploit:** By entering `' OR 1=1 --` into the username field, an attacker could create a query that is always true, bypassing the password check entirely.

* **The Fix:** The flaw was patched by replacing the f-string with a parameterised query. The `?` placeholder ensures that user input is always treated as data, never as executable code, making SQL injection impossible.

#### 🩹 Secure Code (`app.py`):
```Python
query = 'SELECT * FROM users WHERE username = ?'
user = conn.execute(query, (username,)).fetchone()
```

### 🚩 Vulnerability #2: Stored Cross-Site Scripting (XSS)
* **The Flaw:** The comments section was designed to display user content using the `| safe` filter in the Jinja2 template. This explicitly disabled Flask's automatic output escaping, allowing any HTML or JavaScript submitted as a comment to be rendered and executed by other users' browsers.

#### ❌ Vulnerable Code (`post.html`):
```HTML
<p>{{ comment['content'] | safe }}</p>
```

* **The Exploit:** An attacker could post a comment containing a `<script>` tag. A common payload to demonstrate this is one that steals a user's session cookie: `<script>alert(document.cookie)</script>`. This script would then execute for every user who viewed the page.

* **The Fix:** The vulnerability was patched by simply removing the `| safe` filter. This re-enables Flask's default security, which automatically escapes dangerous characters (like `<` and `>`), rendering them as harmless text and preventing the browser from executing any injected scripts.

#### 🩹 Secure Code (`post.html`):
```HTML
<p>{{ comment['content'] }}</p>
```

---

## 🏗️ Project Structure
Risky-Site/
├── .gitignore          → Specifies files for Git to ignore.
├── app.py              → Main Flask application, handles web routes.
├── auth.py             → Contains password hashing & verification functions.
├── db.py               → Manages the database connection & setup.
├── init_db.py          → A simple script to initialise the database.
├── requirements.txt    → Lists all Python package dependencies.
├── schema.sql          → The SQL blueprint for creating database tables.
├── users.db            → The SQLite database file (created at runtime).
└── templates/
    ├── login.html      → The HTML template for the login page.
    └── post.html       → The HTML template for the blog post & comments.



