#!/usr/bin/env python3

import requests
import html
import random
import os

API_BASE_URL = 'https://opentdb.com'
API_CATEGORY_ENDPOINT = f'{API_BASE_URL}/api_category.php'
API_QUESTION_ENDPOINT = f'{API_BASE_URL}/api.php'

def get_response(endpoint, params=None):
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'An error occurred: {err}')
    return {}

def prompt_for_input(prompt, valid_options=None, is_digit=True):
    while True:
        user_input = input(prompt).strip()
        if is_digit and user_input.isdigit():
            if not valid_options or int(user_input) in valid_options:
                return int(user_input)
        elif not is_digit and user_input in valid_options:
            return user_input
        print('Invalid input. Please try again.\n')

def display_questions(data):
    for question_data in data.get('results', []):
        question = html.unescape(question_data['question'])
        correct_answer = html.unescape(question_data['correct_answer'])
        incorrect_answers = [html.unescape(answer) for answer in question_data['incorrect_answers']]
        
        answers = incorrect_answers + [correct_answer]
        random.shuffle(answers)
        
        print(f'Question: {question}')
        for idx, answer in enumerate(answers, 1):
            print(f'{idx}. {answer}')
        
        prompt = 'Your answer (1/2): ' if question_data['type'] == 'boolean' else 'Your answer (1/2/3/4): '
        user_answer = prompt_for_input(prompt, range(1, len(answers) + 1))
        
        if answers[user_answer - 1] == correct_answer:
            print('Correct!\n')
        else:
            print(f'Wrong! The correct answer was: {correct_answer}\n')

def fetch_categories():
    return get_response(API_CATEGORY_ENDPOINT).get('trivia_categories', [])

def clear_display():
    os.system('clear' if os.name == 'posix' else 'cls')

def setup_trivia_params():
    number_of_questions = prompt_for_input('Enter the number of questions you want (1-50): ', range(1, 51))
    print('')
    difficulty = prompt_for_input('Select difficulty (easy, medium, hard): ', ['easy', 'medium', 'hard'], is_digit=False)
    print('')
    categories = fetch_categories()
    print('Available Categories:')
    print('0: Any Category')
    for category in categories:
        print(f'{category["id"]}: {category["name"]}')
    category_id = prompt_for_input('Select the category by ID (or 0 for any): ', [0] + [cat['id'] for cat in categories])
    print('')
    
    params = {
        'amount': number_of_questions,
        'difficulty': difficulty,
        'type': 'multiple'
    }
    if category_id != 0:
        params['category'] = category_id
    return params

def main():
    clear_display()
    trivia_params = setup_trivia_params()
    trivia_data = get_response(API_QUESTION_ENDPOINT, params=trivia_params)
    display_questions(trivia_data)

if __name__ == '__main__':
    main()
