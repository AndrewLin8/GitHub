# Write the quiz questions dictionary from Assignment 1 to a JSON file.
# Name: Andrew Lin
# Date: March 13, 2026

import json
from pathlib import Path

Questions = [
    {
        "question": "What is the airspeed of an unladen swallow in miles/hr?",
        "options": ["12", "15", "20", "25"],
        "answer": "12"
    },
    {
        "question": "What is the capital of Texas?",
        "options": ["Austin", "Dallas", "Houston", "San Antonio"],
        "answer": "Austin"
    },
    {
        "question": "The Last Supper was painted by which artist?",
        "options": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"],
        "answer": "Leonardo da Vinci"
    }
]

filename = Path(__file__).with_name("quiz_questions.json")

with open(filename, "w") as f:
    json.dump(Questions, f, indent=4)

print(f"Quiz questions saved to: {filename.name}")
print(f"Number of questions saved: {len(Questions)}")
print("\nContents written to JSON:")
print(json.dumps(Questions, indent=4))
