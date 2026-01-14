from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Homepage
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

# Chatbot response
@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message")
    if "hello" in user_message.lower():
        bot_message = "Hello! How can I help you?"
    elif "how are you" in user_message.lower():
        bot_message = "I'm good, thanks! What about you?"
    else:
        bot_message = f"You said: {user_message}"
    return jsonify({"response": bot_message})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

