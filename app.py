from flask import Flask, render_template, request, redirect, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

DB_NAME = "college.db"

# Automatically create database and tables if not exist
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Chatbot table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chatbot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
    """)

    # Insert default admin user if not exists
    cursor.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))

    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect(DB_NAME)

# Homepage
@app.route("/")
def home():
    return render_template("home.html")

# About page
@app.route("/about")
def about():
    return render_template("about.html")

# Contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Admin login
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["admin_logged_in"] = True
            return redirect("/admin")
        else:
            message = "Invalid username or password!"

    return render_template("admin_login.html", message=message)

# Admin panel
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin_logged_in"):
        return redirect("/admin-login")

    message = ""
    if request.method == "POST":
        question = request.form["question"].lower()
        answer = request.form["answer"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chatbot (question, answer) VALUES (?, ?)",
            (question, answer)
        )
        conn.commit()
        conn.close()

        message = "Question & Answer added successfully!"

    return render_template("admin.html", message=message)

# Admin logout
@app.route("/admin-logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect("/admin-login")

# Chat page
@app.route("/chat", methods=["GET", "POST"])
def chat():
    answer = ""
    if request.method == "POST":
        question = request.form["question"].lower()
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT answer FROM chatbot WHERE question=?", (question,))
        result = cursor.fetchone()
        conn.close()

        if result:
            answer = result[0]
        else:
            answer = "Sorry, I don't know the answer yet."

    return render_template("chat.html", answer=answer)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
