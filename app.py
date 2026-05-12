from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "quiz_secret_key_2024"
app.jinja_env.filters['enumerate'] = enumerate

# Results store karne ke liye
results_file = "results.json"

def save_result(quiz_id, answers, score):
    results = []
    if os.path.exists(results_file):
        with open(results_file, "r") as f:
            results = json.load(f)
    
    results.append({
        "quiz_id": quiz_id,
        "answers": answers,
        "score": score,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

def get_results():
    if os.path.exists(results_file):
        with open(results_file, "r") as f:
            return json.load(f)
    return []

# Quiz 1 - Fun & Icebreaker
quiz1 = {
    "id": "quiz1",
    "title": "Fun Quiz 💫",
    "subtitle": "Answer these fun questions!",
    "questions": [
        {
            "q": "What's your favorite season?",
            "options": ["Summer ☀️", "Winter ❄️", "Spring 🌸", "Autumn 🍂"],
            "correct": 0
        },
        {
            "q": "What's your ideal weekend?",
            "options": ["Netflix & chill 🎬", "Outdoor adventure 🏕️", "Shopping & friends 🛍️", "Sleeping all day 😴"],
            "correct": 0
        },
        {
            "q": "What kind of movies do you like?",
            "options": ["Romantic 💕", "Comedy 😂", "Horror 😱", "Action 💥"],
            "correct": 0
        },
        {
            "q": "Your dream travel destination?",
            "options": ["Paris 🗼", "Dubai 🌆", "Maldives 🏖️", "Tokyo 🗾"],
            "correct": 0
        },
        {
            "q": "If someone wants to impress you, what would work?",
            "options": ["Sweet words 🥰", "Surprise gifts 🎁", "Quality time ⏰", "Making me laugh 😄"],
            "correct": 0
        }
    ]
}

# Quiz 2 - Romantic & Proposal
quiz2 = {
    "id": "quiz2",
    "title": "Romantic Quiz 💕",
    "subtitle": "Let's see what's in your heart...",
    "questions": [
        {
            "q": "What's your love language?",
            "options": ["Words of affirmation 💬", "Physical touch 🤝", "Acts of service 🛠️", "Gift giving 🎁"],
            "correct": 0
        },
        {
            "q": "Perfect first date?",
            "options": ["Candlelight dinner 🕯️", "Long drive 🚗", "Coffee & talk ☕", "Movie night 🎬"],
            "correct": 0
        },
        {
            "q": "What quality do you value most in a partner?",
            "options": ["Honesty 💯", "Humor 😄", "Loyalty 🤝", "Ambition 🚀"],
            "correct": 0
        },
        {
            "q": "How do you know you like someone?",
            "options": ["Can't stop thinking about them 💭", "Always want to talk to them 📱", "Get nervous around them 😅", "All of the above 😍"],
            "correct": 0
        },
        {
            "q": "Someone has a crush on you secretly, what would you say? 💕",
            "options": ["Aww, tell me who! 🥰", "Let's get to know each other 😊", "That's so sweet! 💖", "I think I know who... 😏"],
            "correct": 0
        }
    ]
}

quizzes = {"quiz1": quiz1, "quiz2": quiz2}

@app.route("/")
def home():
    return "<h2>Quiz Links:</h2><a href='/quiz/quiz1'>Quiz 1 - Fun Quiz</a><br><a href='/quiz/quiz2'>Quiz 2 - Romantic Quiz</a>"

@app.route("/quiz/<quiz_id>")
def quiz(quiz_id):
    if quiz_id not in quizzes:
        return "Quiz not found!", 404
    q = quizzes[quiz_id]
    return render_template("quiz.html", quiz=q)

@app.route("/submit/<quiz_id>", methods=["POST"])
def submit(quiz_id):
    if quiz_id not in quizzes:
        return "Quiz not found!", 404
    
    q = quizzes[quiz_id]
    answers = {}
    for i, question in enumerate(q["questions"]):
        answer = request.form.get(f"q{i}", "Not answered")
        answers[question["q"]] = answer
    
    save_result(quiz_id, answers, len(answers))
    return render_template("result.html", quiz=q, answers=answers)

@app.route("/admin")
def admin():
    results = get_results()
    return render_template("admin.html", results=results, quizzes=quizzes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))