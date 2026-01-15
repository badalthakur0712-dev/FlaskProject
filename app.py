from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

DB_NAME = "college.db"

# Initialize DB
def init_db():
    if os.path.exists(DB_NAME):
        try:
            conn = sqlite3.connect(DB_NAME)
            conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            conn.close()
        except sqlite3.DatabaseError:
            os.remove(DB_NAME)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# FAQ answers
faq_answers = {
    "Fees": "College fees range from ₹40,000 to ₹80,000 per year depending on the course.",
    "Admission Process": """Step 1: Visit Pandav College campus or website.
Step 2: Fill admission form online/offline.
Step 3: Pay fees (₹40,000-₹80,000 depending on course).
Step 4: Submit documents (ID, mark sheets, photos).
Step 5: Admission confirmed after verification.""",
    "Seat Availability": """Seats per branch:
- Computer Science: 120
- Mechanical: 100
- Civil: 80
- Electrical: 90
- Management: 60""",
    "Timetable": "Class timetable is available under 'Timetable' section.",
    "Library": "Library open 9 AM - 6 PM. Student ID required.",
    "Contact Admin": "Email: admin@pandavcollege.com | Phone: 123-456-7890",
    "Events": "Upcoming events updated monthly.",
    "Student Support": "Support via support@college.com or 987-654-3210",
    "Scholarships": "Merit & need-based scholarships available online.",
    "Hostel": "Hostel available for outstation students.",
    "Sports": "Sports and extracurricular activities available.",
    "Technical Clubs": "Coding, robotics, AI clubs active.",
    "Placements": "Placement support for final year students.",
    "Departments": "Departments: Engineering, Management, Science.",
    "Faculty": "Faculty details under 'Faculty Info'."
}

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ROUTES
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    message = ""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        msg = request.form.get("message")
        if not name or not email or not msg:
            message = "Please fill all fields!"
        else:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
                      (name, email, msg))
            conn.commit()
            conn.close()
            message = "Thank you! Your message has been sent."
    return render_template("contact.html", message=message)

@app.route("/chat")
def chat():
    return render_template("chat.html", faq_answers=faq_answers)

@app.route("/get-answer", methods=["POST"])
def get_answer():
    topic = request.form.get("topic")
    answer = faq_answers.get(topic, "Sorry, I don't have info on that.")
    # Save to DB
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (question, answer) VALUES (?, ?)", (topic, answer))
    conn.commit()
    conn.close()
    return jsonify({"answer": answer})

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = username
            return redirect("/admin-panel")
        else:
            error = "Invalid username or password!"
    return render_template("admin_login.html", error=error)

@app.route("/admin-panel")
def admin_panel():
    if "admin" not in session:
        return redirect("/admin-login")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM contacts ORDER BY id DESC")
    contacts = c.fetchall()
    c.execute("SELECT * FROM chat_history ORDER BY id DESC")
    chats = c.fetchall()
    conn.close()
    return render_template("admin_panel.html", contacts=contacts, chats=chats)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/admin-login")

# Render-ready port binding
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
