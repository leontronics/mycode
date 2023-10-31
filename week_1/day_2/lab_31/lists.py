#!/usr/bin/env python3
import random

def getStudentIndex(max_index):
    while True:
        user_input = input(f"Please enter a number between 0 and {max_index} or type 'random': ").strip().lower()
        
        if user_input == "random":
            return random.randint(0, max_index)
        
        try:
            index = int(user_input)
            if 0 <= index <= max_index:
                return index
            else:
                raise ValueError
        except ValueError:
            retry = input("Invalid input. Would you like to retry? (yes/no): ").strip().lower()
            if retry != 'yes':
                print("Choosing a random number instead then")
                return random.randint(0, max_index)

def main():
    wordbank = ["indentation", "spaces"]
    tlgstudents = ['Albert', 'Anthony', 'Brenden', 'Craig', 'Deja', 'Elihu', 'Eric', 'Giovanni', 'James', 'Joshua', 'Maria', 'Mohamed', 'PJ', 'Philip', 'Sagan', 'Suchit', 'Meka', 'Trey', 'Winton', 'Xiuxiang', 'Yaping']

    wordbank.append(4)

    max_index = len(tlgstudents) - 1
    student_index = getStudentIndex(max_index)

    student_name = tlgstudents[student_index]
    print(f"{student_name} always uses {str(wordbank[-1])} {wordbank[1]} to indent")

if __name__ == "__main__":
    main()
