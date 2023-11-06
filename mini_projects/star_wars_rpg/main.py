import os
from game import Game

def clear_display():
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    game = Game()
    clear_display()
    game.play()

if __name__ == "__main__":
    main()