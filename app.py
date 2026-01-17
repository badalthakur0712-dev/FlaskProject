from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3, os

app = Flask(__name__)
app.secret_key = "pandav_secret_key_2026_force_logout"

# ================= DATABASE =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "college.db")

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

    c.execute("""
        CREATE TABLE IF NOT EXISTS admission(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            branch TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= ADMIN =================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ================= CHATBOT (UPDATED) =================
faq_answers = {

    "What is Pandav College of Polytechnic?":
    "Pandav College of Polytechnic is an AICTE-approved institute offering quality diploma engineering education with a strong focus on discipline, practical knowledge, and career readiness.",

    "What diploma engineering branches are available in your college?":
    "We offer diploma programs in Computer Science Engineering, Mechanical Engineering, Civil Engineering, Electrical Engineering, and Electronics Engineering.",

    "What is the admission process for diploma courses?":
    "Students can apply by filling the admission enquiry form on our website or by visiting the college campus. Our admission team will guide you step by step.",

    "Is admission currently open for 2026?":
    "Yes, admissions for the academic year 2026 are currently open. Seats are limited, so early application is recommended.",

    "What is the fee structure for diploma engineering courses?":
    "The annual diploma fees range from ₹60,000 to ₹80,000 depending on the selected engineering branch.",

    "Tell me about the Computer Science Engineering branch.":
    "Computer Science Engineering focuses on programming, software development, web technologies, and basic AI concepts. Duration: 3 years | Fees: ₹80,000 per year | Seats: 60.",

    "Tell me about the Mechanical Engineering branch.":
    "Mechanical Engineering covers machines, manufacturing processes, CAD design, thermodynamics, and robotics. Duration: 3 years | Fees: ₹65,000 per year | Seats: 80.",

    "Tell me about the Civil Engineering branch.":
    "Civil Engineering focuses on construction technology, surveying, structural design, and infrastructure development. Duration: 3 years | Fees: ₹60,000 per year | Seats: 60.",

    "Tell me about the Electrical Engineering branch.":
    "Electrical Engineering deals with power systems, electrical machines, wiring systems, and industrial automation. Duration: 3 years | Fees: ₹60,000 per year | Seats: 60.",

    "Tell me about the Electronics Engineering branch.":
    "Electronics Engineering focuses on electronic circuits, communication systems, embedded systems, microcontrollers, and industrial electronics. Duration: 3 years | Fees: ₹65,000 per year | Seats: 60.",

    "What career opportunities are available after Electronics Engineering?":
    "Electronics Engineering graduates can work in electronics manufacturing, automation industries, embedded systems, telecom companies, and industrial electronics sectors.",

    "Do you provide placement assistance?":
    "Yes, we provide placement assistance in the final year through training programs, industry interaction, and campus interview support.",

    "Is hostel or transport facility available?":
    "Information regarding hostel and transport facilities can be obtained directly from the college administration office.",

    "Where can I check the college timetable?":
    "Timetables are prepared semester-wise and are available on department notice boards and through the college office.",

    "How can I contact the college administration?":
    "You can contact the college through the Contact page on the website or visit the campus during office hours.",

    "What are the college office hours?":
    "The college office works from 9:00 AM to 5:00 PM, Monday to Friday."
}

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("home.html", faq=faq_answers)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/departments")
def departments():
    branches = {
        "Computer Science Engineering": "Software Development, Programming, AI & Web Technologies",
        "Mechanical Engineering": "Machines, Manufacturing, CAD & Robotics",
        "Civil Engineering": "Construction, Surveying & Structural Design",
        "Electrical Engineering": "Power Systems, Wiring & Industrial Automation",
        "Electronics Engineering": "Embedded Systems, Communication & Industrial Electronics"
    }
    return render_template("departments.html", branches=branches)

@app.route("/admission", methods=["GET","POST"])
def admission():
    msg = ""
    if request.method == "POST":
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute(
            "INSERT INTO admission(name,email,phone,branch,message) VALUES (?,?,?,?,?)",
            (
                request.form.get("name"),
                request.form.get("email"),
                request.form.get("phone"),
                request.form.get("branch"),
                request.form.get("message")
            )
        )
        conn.commit()
        conn.close()
        msg = "Thank you! Your admission enquiry has been submitted successfully."
    return render_template("admission.html", msg=msg)

@app.route("/contact", methods=["GET","POST"])
def contact():
    msg = ""
    if request.method == "POST":
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute(
            "INSERT INTO contacts(name,email,message) VALUES (?,?,?)",
            (
                request.form.get("name"),
                request.form.get("email"),
                request.form.get("message")
            )
        )
        conn.commit()
        conn.close()
        msg = "Message sent successfully! Our team will get back to you shortly."
    return render_template("contact.html", msg=msg)

@app.route("/chat")
def chat():
    return render_template("chat.html", faq=faq_answers)

@app.route("/get-answer", methods=["POST"])
def get_answer():
    question = request.form.get("question")
    answer = faq_answers.get(
        question,
        "Thank you for asking! For detailed information, please contact the college administration."
    )

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO chat_history(question,answer) VALUES (?,?)", (question, answer))
    conn.commit()
    conn.close()

    return jsonify({"answer": answer})

# ================= ADMIN =================
@app.route("/admin-login", methods=["GET","POST"])
def admin_login():
    error = ""
    if request.method == "GET":
        session.clear()
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USERNAME and request.form.get("password") == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect("/admin-panel")
        else:
            error = "Invalid username or password"
    return render_template("admin_login.html", error=error)

@app.route("/admin-panel")
def admin_panel():
    if not session.get("admin_logged_in"):
        return redirect("/admin-login")

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM contacts ORDER BY id DESC")
    contacts = c.fetchall()

    c.execute("SELECT * FROM chat_history ORDER BY id DESC")
    chats = c.fetchall()

    c.execute("SELECT * FROM admission ORDER BY id DESC")
    admissions = c.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        contacts=contacts,
        chats=chats,
        admissions=admissions
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/admin-login")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
