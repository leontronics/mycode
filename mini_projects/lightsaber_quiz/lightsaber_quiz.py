#!/usr/bin/env python3

from lightsaber_db import lightsaber_questions, lightsaber_colors
from colorama import init, Fore, Style
import os
import random

# Initialize the colorama library for colored terminal text
init(autoreset=True)

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

# Mapping of lightsaber colors to their corresponding terminal text colors
COLOR_MAPPING = {
    'Blue': Fore.BLUE,
    'Green': Fore.GREEN,
    'Red': Fore.RED,
    'Purple': Fore.MAGENTA,
    'White': Fore.WHITE,
    'Black': Fore.BLACK,
    'Yellow': Fore.YELLOW,
    'Orange': Fore.LIGHTYELLOW_EX
}

# Function to retrieve the color based on the lightsaber color
def get_color_for_result(max_color):
    return COLOR_MAPPING.get(max_color)

# Function to display the user's lightsaber color and its meaning
def display_result(max_color):
    clear_display()
    lightsaber_color = get_color_for_result(max_color)
    print(Style.BRIGHT + lightsaber_color + f'Your lightsaber color is: {max_color}\n')
    print(lightsaber_colors[max_color])
    input('\nPlease press the Enter key to return to the main menu.')

# Function to start the quiz
def start_quiz(lightsaber_questions):
    # Dictionary to store the count of each lightsaber color based on user's answers
    results = {}

    # Convert the dictionary to a list and shuffle the order
    lightsaber_questions_shuffled = list(lightsaber_questions.items())
    random.shuffle(lightsaber_questions_shuffled)
    total_questions = len(lightsaber_questions_shuffled)
    
    # Loop through each shuffled question and its associated answers
    for index, (question, answers) in enumerate(lightsaber_questions_shuffled, 1):
        clear_display()
        print(f'Question {index} of {total_questions}: {question}\n')
        
        # Shuffle the answers for the current question
        answers_shuffled = list(answers.keys())
        random.shuffle(answers_shuffled)
        
        # Display each shuffled answer option for the current question
        for option_index, answer in enumerate(answers_shuffled, 1):
            print(f'{option_index}. {answer}')
        
        # Get the user's choice for the current question
        choice = get_user_input('\nEnter your choice (1 - 4): ', range(1, 5))
        selected_answer = answers_shuffled[choice - 1]
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
