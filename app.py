from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3, os

app = Flask(__name__)
app.secret_key = "pandav_secret_key"

DB = "college.db"

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS chat_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= ADMIN =================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ================= CHATBOT DATA =================
faq_answers = {
    "Fees": "Fees range between ₹40,000 to ₹80,000 depending on branch.",
    "Admission Process": "Visit college → Fill admission form → Pay fees → Admission confirmed.",
    "Seat Availability": "Seats vary by branch (60–120 seats).",
    "Branches": "CSE, IT, Mechanical, Civil, Electrical.",
    "Timetable": "Timetable available at college notice board & website.",
    "Library": "Library open 9 AM – 6 PM.",
    "Hostel": "Hostel available for boys and girls.",
    "Placements": "Placement assistance provided in final year.",
    "Scholarships": "Government & merit scholarships available.",
    "Contact Admin": "Email: admin@pandavcollege.com",
    "Events": "Technical & cultural events conducted yearly.",
    "Sports": "Indoor & outdoor sports facilities.",
    "Faculty": "Experienced and qualified faculty members.",
    "Location": "Pandav College, India",
    "Office Time": "9 AM to 5 PM (Mon–Fri)"
}

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    msg = ""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO contacts(name,email,message) VALUES (?,?,?)",
                  (name, email, message))
        conn.commit()
        conn.close()

        msg = "Message sent successfully!"

    return render_template("contact.html", msg=msg)

@app.route("/chat")
def chat():
    return render_template("chat.html", faq=faq_answers)

@app.route("/get-answer", methods=["POST"])
def get_answer():
    q = request.form["question"]
    a = faq_answers.get(q, "Please contact admin for this information.")

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO chat_history(question,answer) VALUES (?,?)", (q, a))
    conn.commit()
    conn.close()

    return jsonify({"answer": a})

# ================= ADMIN LOGIN =================
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error = ""
    if request.method == "POST":
        if request.form["username"] == ADMIN_USERNAME and request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin-panel")
        else:
            error = "Invalid username or password"
    return render_template("admin_login.html", error=error)

@app.route("/admin-panel")
def admin_panel():
    if "admin" not in session:
        return redirect("/admin-login")

    conn = sqlite3.connect(DB)
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

# ================= RENDER PORT FIX =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
