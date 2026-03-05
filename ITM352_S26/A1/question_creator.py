"""
Quiz Question Creator Application
This interactive application allows users to create and add new quiz questions
to the JSON question database. Questions are stored in the proper JSON format.

Author: ITM352 Student
Date: March 2026
"""

import json
import os


def load_questions(filename="quiz_questions.json"):
    """
    Load existing quiz questions from JSON file.
    
    Args:
        filename (str): The JSON file containing quiz questions
        
    Returns:
        dict: Dictionary with categories as keys and question lists as values
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found. Creating new question database.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: {filename} is not valid JSON.")
        return {}


def save_questions(questions, filename="quiz_questions.json"):
    """
    Save questions to JSON file with proper formatting.
    
    Args:
        questions (dict): Dictionary of categories and questions
        filename (str): The JSON file to save to
    """
    try:
        with open(filename, 'w') as file:
            json.dump(questions, file, indent=2)
        print(f"\n✓ Questions saved to {filename}")
    except IOError as e:
        print(f"Error saving to {filename}: {e}")


def get_valid_int(prompt, min_val=1, max_val=None):
    """
    Get a valid integer input from user.
    
    Args:
        prompt (str): The prompt to display
        min_val (int): Minimum acceptable value
        max_val (int): Maximum acceptable value (optional)
        
    Returns:
        int: The valid integer entered
    """
    while True:
        try:
            value = int(input(prompt).strip())
            if value < min_val:
                print(f"Please enter a number >= {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Please enter a number <= {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")


def create_question():
    """
    Interactively create a new question.
    
    Returns:
        dict: A question dictionary
    """
    print("\n" + "="*50)
    print("Create New Question")
    print("="*50)
    
    question_text = input("Enter the question: ").strip()
    if not question_text:
        print("Question cannot be empty.")
        return None
    
    # Get number of answer options
    num_options = get_valid_int("How many answer options? (2-10): ", min_val=2, max_val=10)
    
    options = []
    for i in range(num_options):
        option = input(f"Enter option {chr(97 + i).upper()}: ").strip()
        if not option:
            print("Option cannot be empty.")
            return None
        options.append(f"{chr(97 + i)}) {option}")
    
    # Get correct answers
    print(f"\nEnter the letter(s) of the correct answer(s) (e.g., 'a' or 'a,c'):")
    while True:
        correct_input = input("Correct answer(s): ").strip().lower().replace(" ", "")
        if not correct_input:
            print("Please enter at least one correct answer.")
            continue
        
        correct_answers = correct_input.split(',')
        valid = all(ans in [chr(97 + i) for i in range(num_options)] for ans in correct_answers)
        
        if valid:
            break
        else:
            print(f"Please enter valid letters from a-{chr(97 + num_options - 1)}")
    
    # Get explanation
    explanation = input("Enter explanation for the correct answer: ").strip()
    
    # Get hint (optional)
    hint = input("Enter a hint (optional, press Enter to skip): ").strip()
    
    # Create question dictionary
    question = {
        "question": question_text,
        "options": options,
        "correct_answers": correct_answers,
        "explanation": explanation
    }
    
    if hint:
        question["hint"] = hint
    
    return question


def display_categories(questions):
    """
    Display all available categories.
    
    Args:
        questions (dict): Dictionary of categories and questions
    """
    if not questions:
        print("\nNo categories exist yet.")
        return
    
    print("\nExisting Categories:")
    print("="*50)
    for i, (category, q_list) in enumerate(questions.items(), 1):
        print(f"{i}. {category} ({len(q_list)} questions)")
    print("="*50)


def view_questions(questions, category):
    """
    Display all questions in a category.
    
    Args:
        questions (dict): Dictionary of categories and questions
        category (str): The category to view
    """
    if category not in questions:
        print(f"Category '{category}' not found.")
        return
    
    print(f"\n{category} Questions:")
    print("="*50)
    for i, q in enumerate(questions[category], 1):
        print(f"\nQuestion {i}: {q['question']}")
        for option in q['options']:
            print(f"  {option}")
        print(f"  Correct Answer(s): {', '.join(q['correct_answers']).upper()}")
        if 'hint' in q:
            print(f"  Hint: {q['hint']}")


def add_to_category(questions):
    """
    Add a new question to a category.
    
    Args:
        questions (dict): Dictionary of categories and questions
    """
    # Display existing categories
    display_categories(questions)
    
    # Get category
    category = input("\nEnter category name (new or existing): ").strip()
    if not category:
        print("Category name cannot be empty.")
        return
    
    # Create question
    question = create_question()
    if question is None:
        print("Question creation cancelled.")
        return
    
    # Add to questions dictionary
    if category not in questions:
        questions[category] = []
    
    questions[category].append(question)
    print(f"\n✓ Question added to '{category}' category!")
    
    # Save immediately
    save_questions(questions)


def edit_question(questions):
    """
    Edit an existing question.
    
    Args:
        questions (dict): Dictionary of categories and questions
    """
    display_categories(questions)
    
    category = input("\nEnter category name: ").strip()
    if category not in questions:
        print(f"Category '{category}' not found.")
        return
    
    view_questions(questions, category)
    
    q_num = get_valid_int(f"Enter question number to edit (1-{len(questions[category])}): ", 
                          max_val=len(questions[category])) - 1
    
    print(f"\nEditing: {questions[category][q_num]['question']}")
    new_question = create_question()
    if new_question:
        questions[category][q_num] = new_question
        save_questions(questions)
        print("✓ Question updated!")


def delete_question(questions):
    """
    Delete a question from a category.
    
    Args:
        questions (dict): Dictionary of categories and questions
    """
    display_categories(questions)
    
    category = input("\nEnter category name: ").strip()
    if category not in questions:
        print(f"Category '{category}' not found.")
        return
    
    view_questions(questions, category)
    
    q_num = get_valid_int(f"Enter question number to delete (1-{len(questions[category])}): ", 
                          max_val=len(questions[category])) - 1
    
    deleted_q = questions[category].pop(q_num)
    print(f"✓ Deleted: {deleted_q['question']}")
    
    # Remove category if empty
    if not questions[category]:
        del questions[category]
    
    save_questions(questions)


def main():
    """
    Main function to run the question creator application.
    """
    print("\n" + "="*50)
    print("Quiz Question Creator Application")
    print("="*50)
    
    questions = load_questions()
    
    while True:
        print("\n" + "="*50)
        print("Options:")
        print("1. Add new question to a category")
        print("2. View questions in a category")
        print("3. Edit a question")
        print("4. Delete a question")
        print("5. View all categories")
        print("6. Exit")
        print("="*50)
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == '1':
            add_to_category(questions)
        elif choice == '2':
            category = input("Enter category name: ").strip()
            view_questions(questions, category)
        elif choice == '3':
            edit_question(questions)
        elif choice == '4':
            delete_question(questions)
        elif choice == '5':
            display_categories(questions)
        elif choice == '6':
            print("\nThank you for using the Question Creator!")
            break
        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
