import random

class Character:

    BASE_DAMAGE = 0
    DAMAGE_RANGE_UPGRADE = 10
    WEAPONS_DAMAGE = {
        'blaster': (20, 30),
        'lightsaber': (50, 60)
    }

    def __init__(self, name, health=100, inventory=None):
        '''Initialize a character with a name, health, and inventory.'''
        self.name = name
        self.health = health
        self.inventory = [] if inventory is None else inventory

    def attack(self, target):
        '''Attack another character and deal damage.'''
        weapon_damage = self.get_highest_weapon_damage()
        damage = random.randint(*weapon_damage)
        target.health -= damage
        print(f'{self.name} attacks {target.name} and deals {damage} damage.')
        if target.health <= 0:
            print(f'{target.name} has been defeated!')

    def get_highest_weapon_damage(self):
        '''Get the highest damage range based on the character's inventory.'''
        highest_damage = (self.BASE_DAMAGE, self.BASE_DAMAGE + self.DAMAGE_RANGE_UPGRADE)
        for weapon in sorted(self.WEAPONS_DAMAGE, key=lambda w: self.WEAPONS_DAMAGE[w][1], reverse=True):
            if weapon in self.inventory:
                highest_damage = self.WEAPONS_DAMAGE[weapon]
                break
        return highest_damage

class Player(Character):
    '''Class representing the player character.'''

    def __init__(self, start_room, health=100):
        '''Initialize the player with a starting room and health.'''
        super().__init__('Player', health)
        self.current_room = start_room

    def move(self, direction):
        '''Move the player to a different room.'''
        if direction in self.current_room.connected_rooms:
            self.current_room = self.current_room.connected_rooms[direction]
            print(f'You move to the {self.current_room.name}.')
        else:
            print("You can't go that way!")

    def get_item(self, item, game):
        '''Attempt to pick up an item.'''
        if self.current_room.enemies:
            print("You can't pick up items while enemies are in the room!")
            return
        if item in self.current_room.items:
            self.attempt_item_pickup(item, game)
        else:
            print(f"Can't get {item}!")

    def attempt_item_pickup(self, item, game):
        '''Private method to handle item pickup logic.'''
        if item == 'security codes' and 'R2-D2' not in self.inventory:
            print("You can't get the security codes without R2-D2's help!")
            return
        if item in self.current_room.locked_items and self.current_room.locked_items[item]:
            print(f'The {item} is locked and cannot be picked up yet.')
            return
        self.inventory.append(item)
        self.current_room.items.remove(item)
        print(f'{item} got!')
        if item == 'access card':
            self.current_room.trigger_trap(game)

class Enemy(Character):
    '''Class representing an enemy character.'''

    def __init__(self, name, description, health, inventory=None):
        '''Initialize an enemy with a name, description, health, and inventory.'''
        super().__init__(name, health, inventory)
        self.description = description

    def __str__(self):
        '''Return a string representation of the enemy.'''
        return f'{self.name} - {self.description}'
