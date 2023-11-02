#!/usr/bin/env python3
import os

def clear_display():
    os.system('clear' if os.name == 'posix' else 'cls')
    print()

def get_max_beers(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print('It has to be a non-negative number. Please try again.')

def sing():
    max_beers = get_max_beers('\nEnter the maximum number of beers on the wall: ')

    for num in range(max_beers, -1, -1):
        if num > 1:
            print(f'{num} bottles of beer on the wall, {num} bottles of beer.')
            print(f'Take one down and pass it around, {num - 1} bottles of beer on the wall.\n')
        elif num == 1:
            print(f'{num} bottle of beer on the wall, {num} bottle of beer.')
            print('Take one down and pass it around, no more bottles of beer on the wall.\n')
        elif num == 0:
            print('No more bottles of beer on the wall, no more bottles of beer.')
            print(f'Go to the store and buy some more, {max_beers} bottles of beer on the wall.\n')

def main():
    clear_display()
    sing()

if __name__ == '__main__':
    main()
