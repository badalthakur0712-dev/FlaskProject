from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Chatbot API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "").lower()

    if "hello" in user_message or "hi" in user_message:
        reply = "Hello 👋 Welcome to Pavdav College!"
    elif "admission" in user_message:
        reply = "Admissions are open. Visit Pavdav College office for details."
    elif "fees" in user_message:
        reply = "Fees range between ₹30,000 to ₹80,000 per year."
    elif "branch" in user_message:
        reply = "Available branches: Computer, IT, Mechanical, Civil."
    elif "seat" in user_message:
<<<<<<< HEAD
        reply
=======
        reply = "Limited seats available. Apply early."
    else:
        reply = "Please ask about admission, fees, branches, or seats."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    # Bind to 0.0.0.0 for Render + correct port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
>>>>>>> e54b9f8 (Final fix chat route for Render)
