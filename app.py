from flask import Flask, render_template, request, jsonify
import os

# 1️⃣ Create the Flask app first
app = Flask(__name__)

# Branch-specific info
branches_info = {
    "computer science": {"fees": 80000, "seats": 120},
    "information technology": {"fees": 70000, "seats": 100},
    "mechanical engineering": {"fees": 60000, "seats": 80},
    "civil engineering": {"fees": 50000, "seats": 80},
    "electronics & communication": {"fees": 65000, "seats": 90},
    "electrical engineering": {"fees": 60000, "seats": 90}
}

# 2️⃣ Routes
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
    data = request.get_json(force=True)
    user_message = data.get("message", "").lower()

    # Chatbot logic
    if "hello" in user_message or "hi" in user_message:
        reply = "Hello 👋 Welcome to Pavdav College!"
    elif "admission" in user_message:
        reply = ("Admissions are open for all branches. "
                 "You can apply online or visit the college office for details.")
    elif "fees" in user_message:
        for branch, info in branches_info.items():
            if branch in user_message:
                reply = f"Fees for {branch.title()} is ₹{info['fees']} per year."
                break
        else:
            reply = "Fees range between ₹40,000 to ₹80,000 per year depending on the branch."
    elif "branch" in user_message or "branches" in user_message:
        reply = "We have the following branches:\n" + "\n".join(
            [f"- {b.title()}" for b in branches_info.keys()]
        )
    elif "seat" in user_message or "seats" in user_message:
        for branch, info in branches_info.items():
            if branch in user_message:
                reply = f"Seats available for {branch.title()}: {info['seats']}."
                break
        else:
            reply = "Each branch has around 60–120 seats. Apply early!"
    else:
        reply = ("I can answer questions about admissions, fees, branches, and seats. "
                 "Try asking one of these or include the branch name for specific info.")

    return jsonify({"reply": reply})

# 3️⃣ Run the app (for Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
