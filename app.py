from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return "<h1>About Pavdav College</h1><p>Quality education and innovation.</p>"

@app.route("/contact")
def contact():
    return "<h1>Contact Us</h1><p>Email: pavdavcollege@gmail.com</p>"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    if "hello" in user_message:
        reply = "Hello 👋 How can I help you?"
    elif "admission" in user_message:
        reply = "Admissions are open. Visit the college office or apply online."
    elif "fees" in user_message:
        reply = "Fees depend on the branch. Average range is ₹30,000–₹80,000 per year."
    elif "branch" in user_message:
        reply = "Available branches: Computer Science, IT, Mechanical, Civil."
    elif "seat" in user_message:
        reply = "Limited seats available. Please apply early."
    else:
        reply = "Sorry, I didn’t understand. Ask about admission, fees, branches, or seats."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
