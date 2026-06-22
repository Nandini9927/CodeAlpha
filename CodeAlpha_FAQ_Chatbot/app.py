from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load FAQ data
with open("faq_data.json", "r", encoding="utf-8") as file:
    faq_data = json.load(file)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    user_question = request.json["message"].lower().strip()

    best_answer = "Sorry, I couldn't find a matching answer."
    best_score = 0

    user_words = set(user_question.split())

    for faq in faq_data:

        faq_question = faq["question"].lower()
        faq_words = set(faq_question.split())

        score = len(user_words.intersection(faq_words))

        if score > best_score:
            best_score = score
            best_answer = faq["answer"]

    return jsonify({
        "response": best_answer
    })

if __name__ == "__main__":
    app.run(debug=True)