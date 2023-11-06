import random

class Character:
    
    BASE_DAMAGE = 0
    WEAPONS_DAMAGE = {
        'blaster': (20, 30),
        'lightsaber': (50, 60)
    }

    def __init__(self, name, health=100, inventory=None):
        self.name = name
        self.health = health
        self.inventory = inventory if inventory is not None else []

    def attack(self, target):
        weapon_damage = self.get_weapon_damage()
        damage = random.randint(*weapon_damage)
        target.health -= damage
        print(f"{self.name} attacks {target.name} and deals {damage} damage.")
        if target.health <= 0:
            print(f"{target.name} has been defeated!")

    def get_weapon_damage(self):
        if 'lightsaber' in self.inventory:
            return self.WEAPONS_DAMAGE['lightsaber']
        elif 'blaster' in self.inventory:
            return self.WEAPONS_DAMAGE['blaster']
        else:
            return (self.BASE_DAMAGE, self.BASE_DAMAGE + 10)

class Player(Character):
    def __init__(self, start_room, health=100):
        super().__init__("Player", health)
        self.current_room = start_room

    def move(self, direction):
        if direction in self.current_room.connected_rooms:
            self.current_room = self.current_room.connected_rooms[direction]
            print(f"You move to the {self.current_room.name}.")
        else:
            print("You can't go that way!")

    def get_item(self, item, game):
        if self.current_room.enemies:
            print("You can't pick up items while enemies are in the room!")
            return
        if item in self.current_room.items:
            if item == 'security codes' and 'R2-D2' not in self.inventory:
                print("You can't get the security codes without R2-D2's help!")
                return
            if item in self.current_room.locked_items and self.current_room.locked_items[item]:
                print(f"The {item} is locked and cannot be picked up yet.")
                return
            self.inventory.append(item)
            self.current_room.items.remove(item)
            print(f'{item} got!')
            if item == 'access card':
                self.current_room.trigger_trap(game)
        else:
            print(f"Can't get {item}!")


class Enemy(Character):
    def __init__(self, name, description, health, inventory=None):
        super().__init__(name, health, inventory)
        self.description = description

    def __str__(self):
        return f"{self.name} - {self.description}"