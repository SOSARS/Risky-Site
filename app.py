from flask import Flask, request, render_template, flash, redirect, url_for, session
from db import get_db_connection
from auth import verify_password
import os

app = Flask(__name__)

# Essential for signing the session cookie
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key-change-in-production")


@app.route("/", methods=["GET", "POST"])
def index():

    # If the user is already logged in, redirect them away from the login page
    if "username" in session:
        return redirect(url_for("post"))

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db_connection()

        # Parameterised query prevents SQL injection
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        # Verify user exists AND password matches
        if user and verify_password(password, user["password"]):
            # On successful login, store the username in the session
            session["username"] = user["username"]
            return redirect(url_for("post"))  # Redirect to the post page
        else:
            flash("Invalid credentials. Please try again.", "error")
            return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/post", methods=["GET", "POST"])
def post():
    if "username" not in session:
        flash("You must be logged in to view this page.", "error")
        return redirect(url_for("index"))

    conn = get_db_connection()

    # Handle a new comment being posted
    if request.method == "POST":
        comment_text = request.form.get("comment")
        if comment_text:
            # Insert new comment into the database
            conn.execute("INSERT INTO comments (username, content) VALUES (?, ?)",
                         (session["username"], comment_text))
            conn.commit()
            return redirect(url_for("post"))  # Refresh the page

    # Fetch all existing comments to display
    comments = conn.execute("SELECT * FROM comments ORDER BY created DESC").fetchall()
    conn.close()

    return render_template("post.html", comments=comments)


@app.route("/logout")
def logout():
    session.clear()  # Clear the session cookie
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)