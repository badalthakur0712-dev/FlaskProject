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
            branch TEXT
        )
    """)
    
    # Add missing columns if not exist
    try:
        c.execute("ALTER TABLE admission ADD COLUMN percentage TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE admission ADD COLUMN address TEXT")
    except sqlite3.OperationalError:
        pass

    # FAQ table
    c.execute("""
        CREATE TABLE IF NOT EXISTS faq(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            answer TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= ADMIN =================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ================= CHATBOT FAQ =================
faq_answers = {
    "What is Pandav College of Polytechnic?":
    "Thank you for asking 😊 Pandav College of Polytechnic is an AICTE-approved institute that offers quality diploma engineering education with a strong focus on discipline, practical learning, and career development.",

    "Which diploma engineering branches are available?":
    "Thank you for your interest 😊 Our college offers diploma programs in Computer Engineering, Mechanical Engineering, Civil Engineering, Electrical Engineering, and Electronics Engineering.",

    "What is the duration of diploma courses?":
    "Thank you for asking 😊 All diploma engineering courses have a duration of 3 years, divided into 6 semesters.",

    "What is the admission process?":
    "Thank you for asking 😊 You can apply for admission by filling out the admission enquiry form available on our website or by visiting the college campus. Our admission team will guide you through each step.",

    "Is admission open for 2026?":
    "Thank you for asking 😊 Yes, admissions for the academic year 2026 are currently open. We recommend applying early as seats are limited.",

    "What is the fee structure?":
    "Thank you for your question 😊 The annual diploma fees range from ₹60,000 to ₹80,000 depending on the chosen engineering branch.",

    "Tell me about Computer Engineering.":
    "Thank you for asking 😊 Computer Engineering focuses on programming, software development, web technologies, databases, and basic artificial intelligence concepts. The course duration is 3 years with 60 seats available.",

    "Tell me about Mechanical Engineering.":
    "Thank you for your interest 😊 Mechanical Engineering covers subjects such as machines, manufacturing processes, CAD design, thermodynamics, and robotics. The course duration is 3 years.",

    "Tell me about Civil Engineering.":
    "Thank you for asking 😊 Civil Engineering focuses on construction technology, surveying, structural design, and infrastructure development. It is a 3-year diploma program.",

    "Tell me about Electrical Engineering.":
    "Thank you for your interest 😊 Electrical Engineering deals with power systems, electrical machines, wiring systems, and industrial automation. The program duration is 3 years.",

    "Tell me about Electronics Engineering.":
    "Thank you for asking 😊 Electronics Engineering focuses on electronic circuits, embedded systems, microcontrollers, and communication systems, preparing students for modern industry needs.",

    "Do you provide placement assistance?":
    "Thank you for asking 😊 Yes, we provide placement assistance to final-year students through training programs, industry interactions, and campus interview support.",

    "Is hostel facility available?":
    "Thank you for your question 😊 For detailed information about hostel facilities, we kindly request you to contact the college administration directly.",

    "Is transport facility available?":
    "Thank you for asking 😊 Transport facility details can be obtained from the college office during working hours.",

    "Where can I check the syllabus?":
    "Thank you for asking 😊 You can check the official syllabus by visiting Student Corner → Syllabus, which redirects to the MSBTE curriculum website.",

    "Where can I check the time table?":
    "Thank you for asking 😊 The latest class time table is available on our website under Student Corner → Time Table.",

    "What are the college office hours?":
    "Thank you for asking 😊 The college office is open from 9:00 AM to 5:00 PM, Monday to Friday.",

    "How can I contact the college?":
    "Thank you for reaching out 😊 You can contact us through the Contact page on our website or visit the college campus during office hours.",

    "Tell me about the faculty": """
Here is detailed information about our experienced faculty:

1️⃣ <b>Kajal Mam</b>  
- <b>Teaching:</b> Computer Science  
- <b>Age:</b> 24  
- <b>Qualification:</b> Diploma in Polytechnic  
- <b>Subjects:</b> Programming, Web Development, Database Management, Basic AI Concepts  
- <b>Experience & Style:</b> Highly interactive teaching, focuses on practical learning, coding exercises, and real-world projects.  
- <b>Image:</b> <br><img src='/static/images/kajal.png' width='150' height='150'>  

2️⃣ <b>Ritika Dorkhande Mam</b>  
- <b>Teaching:</b> Software Technology  
- <b>Age:</b> 21  
- <b>Qualification:</b> Degree in Computer Engineering  
- <b>Subjects:</b> Software Development, Operating Systems, Networking, Project Management  
- <b>Experience & Style:</b> Emphasizes hands-on projects, teamwork, and innovative solutions. Encourages students to explore new technologies and build mini-projects.  
- <b>Image:</b> <br><img src='/static/images/ritika.png' width='150' height='150'>  

3️⃣ <b>Shumbhangi Mam</b>  
- <b>Teaching:</b> NIS (Network & Information Security)  
- <b>Age:</b> 24  
- <b>Qualification:</b> Specialized in Security & Networking  
- <b>Subjects:</b> Cybersecurity, Ethical Hacking, Network Security, Data Protection  
- <b>Experience & Style:</b> Focuses on practical labs and real-time simulations. Guides students in understanding complex security protocols and encourages ethical hacking practice.  
- <b>Image:</b> <br><img src='/static/images/shumbhangi.png' width='150' height='150'>
"""
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
        "Computer Engineering": "Programming, Software Development & AI",
        "Mechanical Engineering": "Machines, Manufacturing & CAD",
        "Civil Engineering": "Construction, Surveying & Structures",
        "Electrical Engineering": "Power Systems & Automation",
        "Electronics Engineering": "Embedded Systems & Communication"
    }
    return render_template("departments.html", branches=branches)

@app.route("/student-corner")
def student_corner():
    return render_template("student_corner.html")

@app.route("/student-corner/syllabus")
def student_syllabus():
    return render_template("syllabus.html")

@app.route("/student-corner/timetable")
def student_timetable():
    return render_template("timetable.html")

@app.route("/student-corner/timetable/<branch>")
def student_timetable_branch(branch):
    return render_template("timetable.html")

@app.route("/admission", methods=["GET", "POST"])
def admission():
    msg = ""
    if request.method == "POST":
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute(
            "INSERT INTO admission(name,email,phone,branch,percentage,address) VALUES (?,?,?,?,?,?)",
            (
                request.form.get("name"),
                request.form.get("email"),
                request.form.get("phone"),
                request.form.get("branch"),
                request.form.get("percentage"),
                request.form.get("address")
            )
        )
        conn.commit()
        conn.close()
        msg = "Thank you 😊 Your admission enquiry has been submitted successfully."
    return render_template("admission.html", msg=msg)

@app.route("/contact", methods=["GET", "POST"])
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
        msg = "Thank you 😊 Your message has been sent successfully."
    return render_template("contact.html", msg=msg)

@app.route("/chat")
def chat():
    return render_template("chat.html", faq=faq_answers)

@app.route("/get-answer", methods=["POST"])
def get_answer():
    question = request.form.get("question")
    answer = faq_answers.get(
        question,
        "Thank you for asking 😊 For more detailed information, please contact the college administration."
    )
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO chat_history(question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()
    return jsonify({"answer": answer})

@app.route("/admin-login", methods=["GET", "POST"])
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
    c.execute("SELECT * FROM faq ORDER BY id DESC")
    faqs = c.fetchall()
    conn.close()
    return render_template("admin.html", contacts=contacts, chats=chats, admissions=admissions, faqs=faqs)

@app.route("/admin-add-faq", methods=["POST"])
def admin_add_faq():
    if not session.get("admin_logged_in"):
        return redirect("/admin-login")
    question = request.form.get("question")
    answer = request.form.get("answer")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO faq(question, answer) VALUES (?, ?)", (question, answer))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # question already exists
    conn.close()
    return redirect("/admin-panel")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/admin-login")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
