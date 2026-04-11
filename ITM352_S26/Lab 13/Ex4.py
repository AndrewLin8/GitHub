from flask import Flask, render_template

app = Flask(__name__)

quiz_questions = [
    {
        "question": "What is the airspeed of an unladen swallow in miles/hr?",
        "choices": ["12", "15", "20", "25"],
    },
    {
        "question": "What is the capital of Texas?",
        "choices": ["Austin", "Dallas", "Houston", "San Antonio"],
    },
    {
        "question": "The Last Supper was painted by which artist?",
        "choices": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"],
    },
]


@app.route("/")
def home():
    return render_template("quiz.html", questions=quiz_questions)


@app.route("/score")
def score():
    return "Quiz scoring will go here."


if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
