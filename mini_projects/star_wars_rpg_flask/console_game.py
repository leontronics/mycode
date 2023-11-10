#!/usr/bin/python3
import os
from game.game import Game

def clear_display():
    '''Clear the console screen.'''
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    '''Initialize and start the game.'''
    game = Game()
    clear_display()
    game.state.game_interface = 'console'  
    game.play_game()

if __name__ == '__main__':
    main()
