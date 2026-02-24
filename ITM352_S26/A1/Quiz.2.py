# Quiz game. Second version.
# Name: Andrew Lin
# Date: Feb, 24, 2026
# Make a list with the question and correct answer.

Questions = [
    ["What is the airspeed of an unladen swallow in miles/hr?", "12"],
    ["What is the capital of Texas?", "Austin"]
    ["The Last Super was painted by which artist?", "Leonardo da Vinci"]
]

for question, correct_answer in Questions:
    answer = input(question)
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is {correct_answer} not {answer}.")