#!/usr/bin/python3

from random import randint

class Player:
    def __init__(self):
        self.dice = []

    def roll(self):
        self.dice = [] 
        for _ in range(3):  
            self.dice.append(randint(1,6))  

    def get_dice(self): 
        return self.dice


class Cheat_Swapper(Player):  
    def cheat(self):
        self.dice[-1] = 6


class Cheat_Loaded_Dice(Player):
    def cheat(self):
        i = 0
        while i < len(self.dice):
            if self.dice[i] < 6:
                self.dice[i] += 1
            i += 1

class Cheat_Mulligan(Player):
    def cheat(self):
        if sum(self.dice) < 9:
            self.roll()

class Cheat_Extra_Die(Player):
    def cheat(self):
        self.dice.append(randint(1, 6))

class Cheat_Weighted_Dice(Player):
    def cheat(self):
        self.dice = [randint(3, 6)] + [randint(1, 6) for _ in range(2)]

class Cheat_Sabotage(Player):
    def cheat(self, other_player):
        other_player.dice = [randint(1, 3) for _ in range(3)]