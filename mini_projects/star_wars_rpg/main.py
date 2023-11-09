import os
from game import Game

def clear_display():
    '''Clear the console screen.'''
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    '''Initialize and start the game.'''
    game = Game()
    clear_display()
    game.play()

if __name__ == '__main__':
    main()
