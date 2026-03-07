# Create the categories the user can select from for the quiz.
def display_categories():
    print("Quiz Categories:")
    print("1. Science")
    print("2. Math")
    print("3. English")
    print("4. History")
    print("5. Art")
   

# Allow the user to choose which category they want.
def select_category():
    categories = ["Science", "Math", "English", "History", "Art"]
    
    while True:
        display_categories()
        choice = input("\nSelect a category (1-5): ").strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= 5:
                selected = categories[choice_num - 1]
                print(f"\nYou selected: {selected}")
                return selected
            else:
                print("Invalid. Enter 1-5.")
        except ValueError:
            print("Invalid. Enter a number 1-5.")