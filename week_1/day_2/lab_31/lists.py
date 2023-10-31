#!/usr/bin/env python3
import random
def main():

    wordbank= ["indentation", "spaces"] 
    tlgstudents= ['Albert', 'Anthony', 'Brenden', 'Craig', 'Deja', 'Elihu', 'Eric', 'Giovanni', 'James', 'Joshua', 'Maria', 'Mohamed', 'PJ', 'Philip', 'Sagan', 'Suchit', 'Meka', 'Trey', 'Winton', 'Xiuxiang', 'Yaping']

    wordbank.append(4)
    num = int(input(f"Please enter a number between 0 and {len(tlgstudents)-1}: "))

    student_name = tlgstudents[num]

    print(f"{student_name} always uses {wordbank[-1]} {wordbank[1]} to indent")

    currentStudents = ["Bert", "Angel", "Chandan", "Chris", "Gen", "Jojo", "Joseph", "Robert", "Sar", "Zack"]
    randomNum = random.randint(0, (len(currentStudents)-1))
    otherStudentName = currentStudents[randomNum]
    print("\nRandom student")
    print(f"{otherStudentName} always uses {wordbank[-1]} {wordbank[1]} to indent")


if __name__ == "__main__":
    main()