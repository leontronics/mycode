#!/usr/bin/env python3
import os
import time
import re

data_dictionary = {
    "one": {
        "two": {
            "three": {
                "four": "five",
            },
        },
    },
}


def clear_display():
    os.system('clear')

def post_action_prompt():
    choice = input("\nReturn to Main Menu (y/n): ").strip().lower()
    if choice == 'n':
        exit()
    elif choice == 'y':
        return
    else:
        print("Invalid choice, please try again")
        post_action_prompt()

def display_data():

    def display_keys(data, prefix=""):
        for key, value in data.items():
            print(f'{prefix}• {key}')
            if isinstance(value, dict):
                display_keys(value, prefix + "  ")

    while True:  
        display_keys(data_dictionary)
        chosen_input = input("\nEnter a key to display its value (for nested keys use 'key > subkey > ...'): ")

        keys = [key.strip() for key in re.split(r'\s*>\s*', chosen_input)]
        temp_data = data_dictionary

        try:
            for key in keys:
                if isinstance(temp_data, dict):
                    temp_data = temp_data[key]
                else:
                    raise KeyError
            print(f"{' > '.join(keys)}: {temp_data}")
            break
        except KeyError:
            print(f"Invalid key: '{key}'!")
            retry = input("\nDo you want to try again? (y/n): ").strip().lower()
            if retry == 'n':
                break
            clear_display()

    post_action_prompt()



def add_data():
    key = input('\nEnter the key: ')
    value = input('Enter the value: ')
    data_dictionary[key] = value
    print(f"Data added successfully: {key} = {value}")
    post_action_prompt()


def delete_data():
    while True: 
        key_to_delete = input('\nEnter the key to delete: ')
        
        if key_to_delete in data_dictionary:
            data_dictionary.pop(key_to_delete)
            print(f"Key '{key_to_delete}' deleted successfully!")
            break 
        else:
            print(f"Key '{key_to_delete}' not found!")
            retry = input("Do you want to try again? (y/n): ").strip().lower()
            if retry == 'n':
                break

    post_action_prompt()


def menu():
    while True:
        clear_display()
        print('\nMain Menu:')
        print('1. Display Data')
        print('2. Add Data')
        print('3. Delete Data')
        print('4. Exit')
        choice = input('\nEnter your choice (1/2/3/4): ')
        clear_display()
        if choice == '4':
            break
        elif choice == '1':
            display_data()
        elif choice == '2':
            add_data()
        elif choice == '3':
            delete_data()
        else:
            print('Invalid choice, please try again')
            time.sleep(1)

menu()
