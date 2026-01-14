from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").lower()

    if any(w in user_msg for w in ["hi", "hello", "hey"]):
        reply = "Hello! Welcome to Pavdav College. How can I help you?"

    elif "admission" in user_msg:
        reply = (
            "Admission Procedure:\n"
            "1. Fill admission form\n"
            "2. Submit documents\n"
            "3. Merit verification\n"
            "4. Fee payment"
        )

    elif "branch" in user_msg or "course" in user_msg:
        reply = (
            "Available Branches:\n"
            "• Computer Science\n"
            "• Mechanical\n"
            "• Civil\n"
            "• Electrical\n"
            "• Arts & Commerce"
        )

    elif "seat" in user_msg:
        reply = (
            "Seat Availability:\n"
            "• CS – 60\n"
            "• Mechanical – 60\n"
            "• Civil – 60\n"
            "• Electrical – 60\n"
            "• Arts & Commerce – 120"
        )

    elif "fee" in user_msg:
        reply = (
            "Fees Structure:\n"
            "Engineering: ₹45,000/year\n"
            "Arts & Commerce: ₹20,000/year"
        )

    elif "eligibility" in user_msg:
        reply = (
            "Eligibility:\n"
            "Engineering: 10+2 Science\n"
            "Arts & Commerce: 10+2 Pass"
        )

    elif "bye" in user_msg:
        reply = "Thank you for visiting Pavdav College 😊"

    else:
        reply = (
            "I can help with:\n"
            "Admission, Branches, Seats, Fees, Eligibility"
        )

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
