import os

from flask import Flask, request, render_template, flash, redirect, url_for
from db import get_db_connection
from auth import verify_password
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)


@app.route('/', methods=["GET", "POST"])
def index():
    error_message = None

    if request.method == "POST":
        username = request.form.get("username")  # Prevents crashing if the key is missing
        password = request.form.get("password")

        conn = get_db_connection()

        # --- Vulnerability Fix ----
        # 1. Securely query for the user's username ONLY.
        # The '?' is a palceholder that prevents the SQL Injection.
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        # 2. Verify if the user is found AND if their password matches the hash.
        if user and verify_password(password, user["password"]):
            flash("Login successful!", "success")  # Optional success message
            return f"<h2>Welcome {username}!</h2><p>Login successful ☑️"
        else:
            flash("Invalid credentials. Please try again.", "error")
            error_message = "❌ Invalid credentials. Please try again."
            return redirect(url_for("index"))

    return render_template("login.html", error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)











