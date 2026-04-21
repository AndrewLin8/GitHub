from flask import Flask, redirect, render_template, request, session, url_for
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "quiz-demo-secret-key"

USER_DATA_FILE = "user_data.json"


def load_questions():
    """Load quiz questions and prepare them for use."""
    return [
        {
            "question": "What is the capital of France?",
            "options": ["London", "Berlin", "Madrid", "Paris"],
            "answer": "Paris",
            "hint": "It's known as the City of Light and has the Eiffel Tower.",
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Venus", "Mars", "Jupiter", "Saturn"],
            "answer": "Mars",
            "hint": "It's named after the Roman god of war and is the 4th planet from the Sun.",
        },
        {
            "question": "How many days are in a leap year?",
            "options": ["364", "365", "366", "367"],
            "answer": "366",
            "hint": "A leap year occurs every 4 years and has one extra day.",
        },
    ]


def load_user_data():
    """Load user data from JSON file."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_user_data(data):
    """Save user data to JSON file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def setup_quiz():
    """Initialize quiz state in session."""
    session["question_index"] = 0
    session["score"] = 0
    session["hints_used"] = []  # Track which questions used hints


@app.route("/")
def home() -> str:
    user_id = session.get("user_id")
    user_data = load_user_data()
    
    if user_id and user_id in user_data:
        user = user_data[user_id]
        return render_template("index.html", user_name=user["name"], score_history=user["scores"])
    return render_template("index.html", user_name=None, score_history=None)


@app.route('/name_entry', methods=['GET', 'POST'])
def name_entry():
    """Handle first-time user name entry."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            user_data = load_user_data()
            user_id = str(len(user_data) + 1)
            user_data[user_id] = {"name": name, "scores": []}
            save_user_data(user_data)
            
            session["user_id"] = user_id
            return redirect(url_for('restart'))
        return render_template("name_entry.html", error="Please enter a valid name.")
    
    return render_template("name_entry.html")


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = load_questions()

    if "question_index" not in session or "score" not in session:
        setup_quiz()

    question_index = session.get("question_index", 0)

    if question_index >= len(questions):
        return redirect(url_for("result"))

    if request.method == 'POST':
        selected_answer = request.form.get("answer")
        current_question = questions[question_index]

        is_correct = selected_answer == current_question["answer"]
        if is_correct:
            session["score"] = session.get("score", 0) + 1

        session["question_index"] = question_index + 1
        is_last_question = session["question_index"] >= len(questions)

        return render_template(
            "question_result.html",
            is_correct=is_correct,
            selected_answer=selected_answer,
            correct_answer=current_question["answer"],
            is_last_question=is_last_question,
        )

    current_question = questions[question_index]
    hint_used = question_index in session.get("hints_used", [])
    
    return render_template(
        "quiz.html",
        question_number=question_index + 1,
        total_questions=len(questions),
        question=current_question["question"],
        options=current_question["options"],
        hint=current_question.get("hint", ""),
        hint_used=hint_used,
    )

@app.route('/result')
def result():
    questions = load_questions()
    score = session.get("score", 0)
    total_questions = len(questions)
    
    user_id = session.get("user_id")
    user_data = load_user_data()
    
    # Save score to user history if logged in
    if user_id and user_id in user_data:
        user_data[user_id]["scores"].append({
            "score": score,
            "total": total_questions,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_user_data(user_data)
    
    return render_template('result.html', score=score, total_questions=total_questions)


@app.route('/use_hint', methods=['POST'])
def use_hint():
    """Handle hint usage."""
    question_index = session.get("question_index", 0)
    hints_used = session.get("hints_used", [])
    
    if question_index not in hints_used:
        hints_used.append(question_index)
        session["hints_used"] = hints_used
    
    return {"status": "hint_used"}


@app.route('/restart')
def restart():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for('name_entry'))
    
    setup_quiz()
    return redirect(url_for('quiz'))


@app.route('/logout')
def logout():
    """Clear user session."""
    session.clear()
    return redirect(url_for('home'))

def main():
   app.run(debug=True)

if __name__ == "__main__":
   main()