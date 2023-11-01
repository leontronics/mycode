#!/usr/bin/env python3

from lightsaber_db import lightsaber_questions, lightsaber_colors
import os

# Function to clear the terminal or command prompt display
def clear_display():
    os.system('clear' if os.name == 'posix' else 'cls')

# Function to get and validate user input based on a set of valid choices
def get_user_input(prompt, valid_choices):
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_choices:
                return choice
            else:
                raise ValueError
        except ValueError:
            print(f"\nInvalid input, please choose one of the following numbers: {', '.join(map(str, valid_choices))}.")

# Function to display the user's lightsaber color and its meaning
def display_result(max_color):
    clear_display()
    print(f'Your lightsaber color is: {max_color}\n')
    print(lightsaber_colors[max_color])
    input('\nPlease press the Enter key to return to the main menu.')

# Function to start the quiz
def start_quiz(lightsaber_questions):
    # Dictionary to store the count of each lightsaber color based on user's answers
    results = {}
    total_questions = len(lightsaber_questions)
    
    # Loop through each question and its associated answers
    for index, (question, answers) in enumerate(lightsaber_questions.items(), 1):
        clear_display()
        print(f'Question {index} of {total_questions}: {question}\n')
        # Display each answer option for the current question
        for option_index, answer in enumerate(answers.keys(), 1):
            print(f'{option_index}. {answer}')
        
        # Get the user's choice for the current question
        choice = get_user_input('\nEnter your choice (1 - 4): ', range(1, 5))
        selected_answer = list(answers.keys())[choice - 1]
        selected_color = answers[selected_answer]
        # Update the results dictionary with the selected color
        results[selected_color] = results.get(selected_color, 0) + 1

    # Determine the most frequently selected color
    max_color = max(results, key=results.get)
    # Display the result to the user
    display_result(max_color)

# Main function to display the menu and handle user choices
def main():
    while True:
        clear_display()
        print('Star Wars Lightsaber Color Quiz\n')
        print('1. Start the Quiz')
        print('2. Exit')
        choice = get_user_input('\nEnter your choice (1 or 2): ', [1, 2])

        # Start the quiz or exit based on user's choice
        if choice == 1:
            start_quiz(lightsaber_questions)
        elif choice == 2:
            print('\nThank you for playing! May the Force be with You.\n')
            break

# Start the app
if __name__ == "__main__":
    main()
