def display_categories(questions):
    # Display available quiz categories with numbered options.
    print("\n" + "="*50)
    print("Available Quiz Categories:")
    print("="*50)
    categories = list(questions.keys())
    for i, category in enumerate(categories, 1):
        num_questions = len(questions[category])
        print(f"{i}. {category} ({num_questions} questions)")
    print("="*50)


def select_category(questions):
    # Ask user to select a quiz category from the list.
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