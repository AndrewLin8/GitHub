# Read the quiz_questions.json file and print its contents.
# Name: Andrew Lin
# Date: March 13, 2026

import json
from pathlib import Path

filename = Path(__file__).with_name("quiz_questions.json")

with open(filename, "r") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions from {filename.name}:\n")

for i, q in enumerate(questions, start=1):
    print(f"Question {i}: {q['question']}")
    print(f"  Options: {', '.join(q['options'])}")
    print(f"  Answer:  {q['answer']}")
    print()
