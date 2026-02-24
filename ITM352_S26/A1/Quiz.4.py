# Quiz game. Third version
# Name: Andrew Lin
# Date: Feb, 24, 2026
# Make a list with the question and correct answer.
# Make a question a dictionary, to include answer options and the correct choice.
# Allow the user to select the correct answer by a label.

Questions = [
    {"What is the airspeed of an unladen swallow in miles/hr?": ["12", "15", "20", "25"]},
    {"What is the capital of Texas?": ["Austin", "Dallas", "Houston", "San Antonio"]},
    {"The Last Super was painted by which artist?": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"]}
]
for question, options in Questions.items():
        correct_answer = options[0] # The first option is the correct answer.
        sorted_options = sorted(options)
        for label, alternative in enumerate(sorted_options, start=1):
            print(f" {label}: {alternative}")
        
        answer_label = int(input(question + ":"))
        answer = sorted_options(answer_label - 1)
        if answer == correct_answer:
            print("Correct!")
        else:
            print(f"The answer is {correct_answer} not {answer}.")