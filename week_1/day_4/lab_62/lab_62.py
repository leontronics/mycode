#!/usr/bin/env python3
import os

def clear_display():
    os.system('clear' if os.name == 'posix' else 'cls')
    print()

farms = [{"name": "Southwest Farm", "agriculture": ["chickens", "carrots", "celery"]},
         {"name": "Northeast Farm", "agriculture": ["sheep", "cows", "pigs", "chickens", "llamas", "cats"]},
         {"name": "East Farm", "agriculture": ["bananas", "apples", "oranges"]},
         {"name": "West Farm", "agriculture": ["pigs", "chickens", "llamas"]}]


from_the_ground = ['carrots', 'celery', 'bananas', 'apples', 'oranges'] 

def old_macdonald():
    print('Please choose between one of the following farms:')
    for farm in farms:
        print(f'  {farm["name"]}')

    while True:
        farm_name = input('\nEnter the farm name: ').strip()
        selected_farm = next((farm for farm in farms if farm["name"].lower() == farm_name.lower()), None)
        
        if selected_farm:
            animals = [item for item in selected_farm["agriculture"] if item not in from_the_ground]
            if animals:
                print(f'\nThese are the animals in the {selected_farm["name"]}:')
                for animal in animals:
                    print(f'  {animal}')
            else:
                print(f'\nThere are no animals in the {selected_farm["name"]}\n')
            break
        else:
            print('Farm not found. Please try again.')


def main():
    clear_display()
    old_macdonald()

if __name__ == '__main__':
    main()