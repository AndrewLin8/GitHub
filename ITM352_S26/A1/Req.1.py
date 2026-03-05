def save_score_to_history(category, score, total_questions, filename="quiz_scores.txt"):
    #Save quiz score to the history file including the timestamp and category.
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    
    with open(filename, 'a') as file:
        file.write(f"{timestamp},{category},{score}/{total_questions},{percentage:.1f}%\n")


def display_score_history(filename="quiz_scores.txt"):
    #Display the score history from the file.
    import os
    
    if not os.path.exists(filename):
        print(f"No score history found. {filename} does not exist yet.")
        return
    
    print("Your Score History")
    
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                print("No scores recorded yet.")
            else:
                print(f"{'Date':<12} {'Category':<15} {'Score':<10} {'Percentage':<12}")
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) >= 4:
                        date, category, score, percentage = parts[0], parts[1], parts[2], parts[3]
                        print(f"{date:<12} {category:<15} {score:<10} {percentage:<12}")
    except IOError:
        print(f"Error reading {filename}")