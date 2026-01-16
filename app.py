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
    # Contacts table
    c.execute("""
        CREATE TABLE IF NOT EXISTS contacts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)
    # Chat history table
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT
        )
    """)
    # Admission table
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

# ================= CHATBOT =================
faq_answers = {
    "What is the fees structure?": "Thank you for asking! Our fees range between ₹40,000 to ₹80,000 per year depending on the branch and facilities.",
    "How can I apply for admission?": "You can apply by filling the Admission Enquiry form on our website. Our team will guide you step-by-step until your enrollment is confirmed.",
    "Are there seats available in CSE?": "Seats vary per branch. CSE and IT have 60 each, Mechanical 80, Civil 60, Electrical 60. Availability is updated regularly.",
    "What branches do you offer?": "We offer Computer Science (CSE), Information Technology (IT), Mechanical, Civil, and Electrical Engineering.",
    "Where can I check the timetable?": "Timetables are available on the college website and notice boards. Classes start at 9:00 AM and end at 5:00 PM.",
    "What are the library timings?": "Our library is open 9 AM – 6 PM. It has over 10,000 books, journals, and digital resources for students.",
    "Do you provide hostel facilities?": "Separate hostel facilities are available for boys and girls, with all necessary amenities and security.",
    "Do you offer placement assistance?": "We provide placement assistance in the final year, with campus interviews, industry visits, and training programs.",
    "What scholarships are available?": "Merit-based and government scholarships are available. Students can apply through the college office.",
    "How can I contact the admin?": "You can reach our admin at admin@pandavcollege.com or call +91-9876543210.",
    "Do you organize events?": "We organize technical fests, cultural programs, and sports events every year to encourage holistic development.",
    "What sports facilities are available?": "Indoor and outdoor sports facilities include cricket, football, basketball, badminton, and table tennis.",
    "Tell me about your faculty.": "Our faculty members are highly experienced, with PhDs and industry experience in their respective fields.",
    "Where is the college located?": "Pandav College is located in India with easy access by road and public transport.",
    "What are the office hours?": "Office hours are 9 AM to 5 PM, Monday to Friday.",
    "Tell me about the CSE branch.": "CSE branch focuses on Software Development, AI, Machine Learning, and Web & App Development. Fees: ₹80,000/year, Seats: 60.",
    "Tell me about the IT branch.": "IT branch focuses on Networking, Cybersecurity, and Cloud Computing. Fees: ₹75,000/year, Seats: 60.",
    "Tell me about the Mechanical branch.": "Mechanical branch focuses on Machines, Thermodynamics, and Robotics. Fees: ₹70,000/year, Seats: 80.",
    "Tell me about the Civil branch.": "Civil branch focuses on Construction, Design, and Structural Analysis. Fees: ₹65,000/year, Seats: 60.",
    "Tell me about the Electrical branch.": "Electrical branch focuses on Circuits, Power Systems, and Electronics. Fees: ₹68,000/year, Seats: 60."
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
        "CSE": "Computer Science Engineering – Software, AI, Coding",
        "IT": "Information Technology – Networking & Cloud",
        "Mechanical": "Mechanical Engineering – Machines & Robotics",
        "Civil": "Civil Engineering – Construction & Design",
        "Electrical": "Electrical Engineering – Power & Electronics"
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
    answer = faq_answers.get(question, "Thank you for asking! Please contact our admin for detailed information.")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO chat_history(question,answer) VALUES (?,?)", (question, answer))
    conn.commit()
    conn.close()
    return jsonify({"answer": answer})

# ================= ADMIN LOGIN =================
@app.route("/admin-login", methods=["GET","POST"])
def admin_login():
    error = ""
    if request.method == "GET":
        session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
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
    return render_template("admin.html", contacts=contacts, chats=chats, admissions=admissions)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/admin-login")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
