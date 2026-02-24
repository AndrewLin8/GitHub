# Quiz game. Third version
# Name: Andrew Lin
# Date: Feb, 24, 2026
# Make a list with the question and correct answer.
# Make a question a dictionary, to include answer options and the correct choice.
# Allow the user to select the correct answer by a label.
# Improve look and usability. Keep track of correct answers.

from string import ascii_lowercase

Questions = [
    {"What is the airspeed of an unladen swallow in miles/hr?": ["12", "15", "20", "25"]},
    {"What is the capital of Texas?": ["Austin", "Dallas", "Houston", "San Antonio"]},
    {"The Last Super was painted by which artist?": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"]}
]

num_correct = 0
for num, question_dict in enumerate(Questions, start=1):
    for question, options in question_dict.items():
        print(f"Question {num}:")
        print(question)
        correct_answer = options[0] # The first option is the correct answer.
        labeled_alternatives = dict(zip(ascii_lowercase, sorted(options)))
        for label, alternative in labeled_alternatives.items():
            print(f" {label}: {alternative}")
        
        answer_label = input("Choice: ")
        answer = labeled_alternatives.get(answer_label)
        if answer == correct_answer:
            print("Correct!")
            num_correct += 1
        else:
            print(f"The answer is {correct_answer} not {answer}.")

      