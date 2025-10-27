from flask import Flask, request, render_template
from db import get_db_connection

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")  # Prevents crashing if the key is missing
        password = request.form.get("password")

        conn = get_db_connection()

        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = conn.execute(query).fetchone()
        conn.close()

        if user:
            return f"<h2>Welcome {username}!</h2><p>Login successful ☑️"
        else:
            return f"<h2>Login failed! ❌<h2><p>Invalid credentials.</p>"

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)










