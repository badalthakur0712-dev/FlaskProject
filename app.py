from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"reply": "No message received"}), 400

    user_message = data["message"].lower()

    if "hello" in user_message or "hi" in user_message:
        reply = "Hello 👋 How can I help you?"
    elif "admission" in user_message:
        reply = "Admissions are open. Please visit the college office."
    elif "fees" in user_message:
        reply = "Fees range from ₹30,000 to ₹80,000 per year."
    elif "branch" in user_message:
        reply = "Available branches: Computer, IT, Mechanical, Civil."
    elif "seat" in user_message:
        reply = "Limited seats available. Apply early."
    else:
        reply = "Please ask about admission, fees, branches, or seats."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
