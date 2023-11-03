#!/usr/bin/python3

from cheatdice import (
    Cheat_Swapper,
    Cheat_Loaded_Dice,
    Cheat_Mulligan,
    Cheat_Extra_Die,
    Cheat_Weighted_Dice,
    Cheat_Sabotage,
)

def play_game(player1, player2):
    player1.roll()
    player2.roll()


    if isinstance(player1, Cheat_Sabotage):
        player1.cheat(player2)
    else:
        player1.cheat()

    if isinstance(player2, Cheat_Sabotage):
        player2.cheat(player1)
    else:
        player2.cheat()

    score1 = sum(player1.get_dice())
    score2 = sum(player2.get_dice())

    print(f"{player1.__class__.__name__} rolled {player1.get_dice()}")
    print(f"{player2.__class__.__name__} rolled {player2.get_dice()}")

    if score1 == score2:
        print("It's a draw!\n")
    elif score1 > score2:
        print(f"{player1.__class__.__name__} wins!\n")
    else:
        print(f"{player2.__class__.__name__} wins!\n")

def main():
    cheaters = [
        Cheat_Swapper(),
        Cheat_Loaded_Dice(),
        Cheat_Mulligan(),
        Cheat_Extra_Die(),
        Cheat_Weighted_Dice(),
        Cheat_Sabotage()
    ]

    for i in range(len(cheaters)):
        for j in range(i + 1, len(cheaters)):
            print(f"Playing {cheaters[i].__class__.__name__} against {cheaters[j].__class__.__name__}")
            play_game(cheaters[i], cheaters[j])

if __name__ == "__main__":
    main()
