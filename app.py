from flask import Flask, render_template, request, jsonify
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "").lower()

    # Detailed responses
    if "hello" in user_message or "hi" in user_message:
        reply = "Hello 👋 Welcome to Pavdav College!"
    elif "admission" in user_message:
        reply = ("Admissions are open for all branches. "
                 "You can apply online or visit the college office for details.")
    elif "fees" in user_message:
        reply = ("Fees range between ₹40,000 to ₹80,000 per year depending on the branch.")
    elif "branch" in user_message or "branches" in user_message:
        reply = ("We have the following branches: \n"
                 "- Computer Science\n"
                 "- Information Technology\n"
                 "- Mechanical Engineering\n"
                 "- Civil Engineering\n"
                 "- Electronics & Communication\n"
                 "- Electrical Engineering")
    elif "seat" in user_message:
        reply = ("Seats are limited. Each branch has around 60–120 seats. Apply early!")
    else:
        reply = ("I can answer questions about admissions, fees, branches, and seats. "
                 "Try asking one of these.")

    return jsonify({"reply": reply})
