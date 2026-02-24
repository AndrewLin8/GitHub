# Quiz game. Third version
# Name: Andrew Lin
# Date: Feb, 24, 2026
# Make a list with the question and correct answer.
# Make a question a dictionary, to include answer options and the correct choice.

Questions = [
    {"What is the airspeed of an unladen swallow in miles/hr?": ["12", "15", "20", "25"]},
    {"What is the capital of Texas?": ["Austin", "Dallas", "Houston", "San Antonio"]},
    {"The Last Super was painted by which artist?": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"]}
]
for question_dict in Questions:
    for question, options in question_dict.items():
        print(question)
        correct_answer = options[0] # The first option is the correct answer.
        for alternative in sorted(options):
            print(f" - {alternative}")
        
        answer = input("Your answer: ")
        if answer == correct_answer:
            print("Correct!")
        else:
            print(f"The answer is {correct_answer} not {answer}.")