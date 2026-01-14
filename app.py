from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# About page
@app.route("/about")
def about():
    return render_template("about.html")

# Contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Chatbot API
@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message").lower()

    if any(word in user_msg for word in ["hello", "hi", "hey"]):
        reply = "Hello! Welcome to Pavdav College. How can I assist you today?"

    elif "admission" in user_msg:
        reply = (
            "Admission Procedure:\n"
            "1. Fill the admission form\n"
            "2. Submit required documents\n"
            "3. Merit list verification\n"
            "4. Fee payment\n"
            "Admissions are open from June to August."
        )

    elif "branches" in user_msg or "courses" in user_msg:
        reply = (
            "We offer the following branches:\n"
            "• Computer Science\n"
            "• Mechanical Engineering\n"
            "• Civil Engineering\n"
            "• Electrical Engineering\n"
            "• Arts & Commerce"
        )

    elif "seat" in user_msg or "seats" in user_msg:
        reply = (
            "Seat Availability:\n"
            "• Computer Science – 60 seats\n"
            "• Mechanical – 60 seats\n"
            "• Civil – 60 seats\n"
            "• Electrical – 60 seats\n"
            "• Arts & Commerce – 120 seats"
        )

    elif "fees" in user_msg or "fee" in user_msg:
        reply = (
            "Approximate Annual Fees:\n"
            "• Engineering – ₹45,000 per year\n"
            "• Arts & Commerce – ₹20,000 per year"
        )

    elif "eligibility" in user_msg:
        reply = (
            "Eligibility Criteria:\n"
            "• Engineering: 10+2 with Science\n"
            "• Arts & Commerce: 10+2 pass"
        )

    elif "contact" in user_msg:
        reply = "Please visit the Contact page for phone number and email."

    elif "bye" in user_msg or "exit" in user_msg:
        reply = "Thank you for visiting Pavdav College. Have a great day 😊"

    else:
        reply = (
            "I can help with:\n"
            "• Admission procedure\n"
            "• Branches / courses\n"
            "• Seat availability\n"
            "• Fees\n"
            "• Eligibility\n"
            "Please ask any of these."
        )

    return jsonify({"reply": reply})


    # Simple AI logic
    if "hello" in user_msg or "hi" in user_msg:
        reply = "Hello! Welcome to Pavdav College. How can I help you?"
    elif "college" in user_msg:
        reply = "Pavdav College offers quality education with modern facilities."
    elif "courses" in user_msg:
        reply = "We offer Science, Arts, and Commerce courses."
    elif "contact" in user_msg:
        reply = "You can contact us via the Contact page of this website."
    elif "bye" in user_msg:
        reply = "Goodbye! Have a great day 😊"
    else:
        reply = "Sorry, I didn’t understand that. Please ask something else."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
