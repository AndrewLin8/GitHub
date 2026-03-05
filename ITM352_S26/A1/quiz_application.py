"""
Interactive Quiz Application
This program presents users with a multiple-choice quiz from various categories.
It tracks scores, maintains a score history file, provides hints, timers, and bonus points.

Features:
- Category selection (Requirement 5)
- Score history tracking (Requirement 1)
- High score notifications (Requirement 2)
- Multiple answer options (Requirement 3)
- Multiple correct answers (Requirement 4)
- Hint system (Requirement 6)
- Answer explanations (Requirement 7)
- Question timer with bonus points (Requirement 9)
- 50/50 feature (Requirement 10)

Author: ITM352 Student
Date: March 2026
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path


def load_questions(filename="quiz_questions.json"):
    """
    Load quiz questions from a JSON file.
    
    Args:
        filename (str): The JSON file containing quiz questions organized by category
        
    Returns:
        dict: Dictionary with categories as keys and question lists as values
    """
    try:
        with open(filename, 'r') as file:
            questions = json.load(file)
        return questions
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: {filename} is not valid JSON.")
        return {}


def get_valid_response(valid_options):
    """
    Prompt user for input and validate it against allowed options.
    This function ensures the user only enters valid responses.
    
    Args:
        valid_options (list): List of acceptable responses (e.g., ['a', 'b', 'c', 'd'])
        
    Returns:
        str: The valid user response in lowercase
    """
    while True:
        user_input = input("Your answer: ").strip().lower()
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid response. Please enter one of: {', '.join([opt.upper() for opt in valid_options])}")


def check_answer(user_answer, correct_answers):
    """
    Check if the user's answer is correct.
    
    Args:
        user_answer (str): The user's answer choice
        correct_answers (list): List of correct answer choices
        
    Returns:
        bool: True if answer is correct, False otherwise
    """
    return user_answer in correct_answers


def load_score_history(filename="quiz_scores.txt"):
    """
    Load the score history from file.
    
    Args:
        filename (str): The file containing score history
        
    Returns:
        list: List of previous scores, or empty list if file doesn't exist
    """
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                scores = [int(line.strip().split(',')[2].split('/')[0]) for line in file if line.strip()]
            return scores
        except (ValueError, IndexError):
            return []
    return []


def save_score_to_history(category, score, total_questions, bonus_points=0, filename="quiz_scores.txt"):
    """
    Save quiz score to the history file with timestamp and category.
    
    Args:
        category (str): The quiz category
        score (int): The user's score
        total_questions (int): Total number of questions in the quiz
        bonus_points (int): Bonus points earned
        filename (str): The file to save history to
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_score = score + bonus_points
    percentage = (total_score / (total_questions + bonus_points)) * 100 if total_questions > 0 else 0
    
    with open(filename, 'a') as file:
        file.write(f"{timestamp},{category},{score}/{total_questions},{bonus_points},Bonus,{percentage:.1f}%\n")


def check_high_score(category, score, total_questions, filename="quiz_scores.txt"):
    """
    Check if the current score is a new high score for the category.
    
    Args:
        category (str): The quiz category
        score (int): The current score
        total_questions (int): Total number of questions
        filename (str): The score history file
        
    Returns:
        bool: True if this is a new high score, False otherwise
    """
    previous_scores = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    if line.strip() and category in line:
                        score_part = line.strip().split(',')[2].split('/')[0]
                        previous_scores.append(int(score_part))
        except (ValueError, IndexError):
            pass
    
    if not previous_scores:
        return True
    
    return score > max(previous_scores)


def display_categories(questions):
    """
    Display available quiz categories to the user.
    
    Args:
        questions (dict): Dictionary of categories and their questions
    """
    print("\n" + "="*50)
    print("Available Quiz Categories:")
    print("="*50)
    categories = list(questions.keys())
    for i, category in enumerate(categories, 1):
        num_questions = len(questions[category])
        print(f"{i}. {category} ({num_questions} questions)")
    print("="*50)


def select_category(questions):
    """
    Prompt user to select a quiz category.
    
    Args:
        questions (dict): Dictionary of categories and their questions
        
    Returns:
        str: The selected category, or None if user wants to quit
    """
    categories = list(questions.keys())
    
    while True:
        display_categories(questions)
        try:
            choice = input("Enter the number of your chosen category (or 'q' to quit): ").strip().lower()
            if choice == 'q':
                return None
            choice_num = int(choice)
            if 1 <= choice_num <= len(categories):
                return categories[choice_num - 1]
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(categories)}.")
        except ValueError:
            print(f"Invalid input. Please enter a number between 1 and {len(categories)}, or 'q' to quit.")


def show_hint(question):
    """
    Display a hint for the current question.
    
    Args:
        question (dict): The question dictionary containing hint information
    """
    if "hint" in question:
        print(f"\n💡 Hint: {question['hint']}")
    else:
        print("\n💡 No hint available for this question.")


def apply_fifty_fifty(question, used_fifty_fifty):
    """
    Apply the 50/50 feature by removing 2 incorrect answers.
    
    Args:
        question (dict): The question dictionary
        used_fifty_fifty (bool): Whether 50/50 has already been used
        
    Returns:
        tuple: (modified_question, updated_used_status)
    """
    if used_fifty_fifty:
        print("50/50 feature already used!")
        return question, used_fifty_fifty
    
    options = question["options"].copy()
    correct_answers = question["correct_answers"]
    
    # Find indices of incorrect answers
    incorrect_indices = []
    for i in range(len(options)):
        option_letter = chr(97 + i)  # Convert index to letter (a, b, c, d)
        if option_letter not in correct_answers:
            incorrect_indices.append(i)
    
    # Remove 2 incorrect answers if possible
    if len(incorrect_indices) >= 2:
        indices_to_remove = incorrect_indices[:2]
        indices_to_remove.sort(reverse=True)
        
        for idx in indices_to_remove:
            del options[idx]
        
        print("\n🎯 50/50 Feature Used!")
        print("Remaining options:")
        for i, option in enumerate(options):
            print(f"  {option}")
        
        question["options"] = options
        return question, True
    else:
        print("Cannot use 50/50 - not enough incorrect answers to remove.")
        return question, used_fifty_fifty


def run_quiz(category, questions):
    """
    Run the quiz for the selected category.
    
    Args:
        category (str): The selected quiz category
        questions (dict): Dictionary of all quiz questions
        
    Returns:
        tuple: (user_score, bonus_points)
    """
    quiz_questions = questions[category]
    score = 0
    total_questions = len(quiz_questions)
    bonus_points = 0
    used_fifty_fifty = False
    
    print("\n" + "="*50)
    print(f"Welcome to the {category} Quiz!")
    print(f"Total Questions: {total_questions}")
    print("Commands: (h)int, (5)0/50, (c)ontinue to answer")
    print("="*50 + "\n")
    
    for i, q in enumerate(quiz_questions, 1):
        question = q.copy()  # Create a copy to avoid modifying original
        print(f"Question {i} of {total_questions}:")
        print(question["question"])
        print()
        for option in question["options"]:
            print(f"  {option}")
        print()
        
        # Start timer
        start_time = time.time()
        
        # Determine valid options based on number of answer options
        valid_options = [chr(97 + j) for j in range(len(question["options"]))]
        valid_options.extend(['h', '5', 'c'])  # Add special commands
        
        # Question loop with special commands
        answered = False
        while not answered:
            user_input = input("Your answer (or h for hint, 5 for 50/50): ").strip().lower()
            
            if user_input == 'h':
                show_hint(question)
                continue
            elif user_input == '5':
                question, used_fifty_fifty = apply_fifty_fifty(question, used_fifty_fifty)
                # Update valid options after removing answers
                valid_options = [chr(97 + j) for j in range(len(question["options"]))]
                valid_options.extend(['h', '5', 'c'])
                continue
            elif user_input in [chr(97 + j) for j in range(len(question["options"]))]:
                answered = True
                user_answer = user_input
            else:
                print(f"Invalid response. Enter a-{chr(97 + len(question['options']) - 1)}, 'h' for hint, or '5' for 50/50")
                continue
        
        # Stop timer
        elapsed_time = time.time() - start_time
        
        # Check if answer is correct
        if check_answer(user_answer, question["correct_answers"]):
            print("✓ Correct!")
            score += 1
            
            # Award bonus points for speed (< 10 seconds = 1 bonus point)
            if elapsed_time < 10:
                bonus_points += 1
                print(f"⚡ Speed bonus! ({elapsed_time:.1f}s)")
        else:
            correct_str = ", ".join(question["correct_answers"]).upper()
            print(f"✗ Incorrect. The correct answer(s): {correct_str}")
        
        if "explanation" in question:
            print(f"  {question['explanation']}")
        print()
    
    return score, bonus_points


def main():
    """
    Main function to run the quiz application.
    """
    print("\n" + "="*50)
    print("Welcome to the Interactive Quiz Application!")
    print("="*50)
    
    # Load questions from file
    questions = load_questions()
    if not questions:
        print("Cannot start quiz without questions. Exiting.")
        return
    
    # Main quiz loop
    while True:
        # Select category
        category = select_category(questions)
        if category is None:
            print("\nThank you for using the Interactive Quiz Application!")
            break
        
        # Run the quiz
        score, bonus_points = run_quiz(category, questions)
        total_questions = len(questions[category])
        total_score = score + bonus_points
        percentage = (total_score / (total_questions + bonus_points)) * 100 if total_questions > 0 else 0
        
        # Display results
        print("="*50)
        print("Quiz Complete!")
        print("="*50)
        print(f"Category: {category}")
        print(f"Your Score: {score}/{total_questions}")
        if bonus_points > 0:
            print(f"Bonus Points: {bonus_points}")
            print(f"Total Score: {total_score} ({percentage:.1f}%)")
        else:
            percentage = (score / total_questions) * 100
            print(f"Percentage: {percentage:.1f}%")
        
        # Check for high score
        if check_high_score(category, score, total_questions):
            print("🎉 NEW HIGH SCORE for this category! 🎉")
        
        # Save score to history
        save_score_to_history(category, score, total_questions, bonus_points)
        print("Score saved to history.\n")
        
        # Ask if user wants to take another quiz
        while True:
            again = input("Take another quiz? (yes/no): ").strip().lower()
            if again in ['yes', 'y']:
                break
            elif again in ['no', 'n']:
                print("\nThank you for using the Interactive Quiz Application!")
                return
            else:
                print("Please enter 'yes' or 'no'.")


if __name__ == "__main__":
    main()
