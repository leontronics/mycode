import threading
import time
from character import Player, Enemy
from room import Room

class Game:

    COUNTDOWN_DURATION = 20

    def __init__(self):
        self.setup_rooms()
        self.player = Player(self.rooms['Hangar'])
        self.game_over_lock = threading.Lock()
        self.game_over = False
        self.trap_active = False

    def setup_rooms(self):
        self.rooms = {
            'Hangar': Room('Hangar', 'You are in the Hangar Bay of the Death Star', items=['blaster']),
            'Detention Block': Room('Detention Block', 'You are in the Detention Block where Princess Leia is held', enemies=[Enemy('Stormtrooper', 'A loyal servant of the Empire', 30, ['blaster'])], allies=['leia']),
            'Control Room': Room('Control Room', 'You are in the Control Room, control the security systems here', items=['security codes'], enemies=[Enemy('Stormtrooper', 'A vigilant guardian of the control systems', 30, ['blaster'])], locked_items={'security codes': True}),
            'Communications Hub': Room('Communications Hub', 'You are in the Communications Hub, where all communications are monitored and controlled', items=['access card'], enemies=[Enemy('Stormtrooper', 'A loyal servant of the Empire', 30, ['blaster'])], locked_items={'access card': True}),
            'Escape Pods': Room('Escape Pods', 'You are by the escape pods, ready to leave the Death Star', enemies=[Enemy('Dark Trooper', 'A menacing Dark Trooper, highly skilled and heavily armored', 120, ['blaster'])]),
            'Imperial Chambers': Room('Imperial Chambers', 'You are in the Imperial Chambers, where the elite forces of the Empire reside', items=['lightsaber'], enemies=[Enemy('Stormtrooper', 'An elite soldier of the Empire, guarding the chambers', 30, ['blaster'])], allies=['r2-d2'])
        }

        self.rooms['Hangar'].connect_room(self.rooms['Detention Block'], 'east')
        self.rooms['Detention Block'].connect_room(self.rooms['Control Room'], 'north')
        self.rooms['Control Room'].connect_room(self.rooms['Communications Hub'], 'east')
        self.rooms['Communications Hub'].connect_room(self.rooms['Escape Pods'], 'south')
        self.rooms['Communications Hub'].connect_room(self.rooms['Imperial Chambers'], 'north')

    def show_instructions(self):
        print('''
Star Wars RPG Game
==================
Objective: Free your allies, defeat the Dark Trooper guarding the escape pods, and escape the Death Star.

Commands:
    go [direction]  - Move in the specified direction (north, south, east, west)
    get [item]      - Pick up an item
    attack [enemy]  - Attack an enemy in the room
    map             - Show a map of the Death Star
    look            - Look around the room to see items and enemies
    free [ally]     - Free your ally if they are in the room with you
    use [item]      - Use an item from your inventory
    exit            - Exit the game

Beware of the Dark Trooper in the Escape Pods room. You will need powerful weapons and strategy to defeat it.

Use your skills wisely to defeat enemies, collect items, and save your allies!
        ''')

    def show_status(self):
        print('---------------------------')
        print(f'Health: {self.player.health}')
        print(f'Inventory: {self.player.inventory}')
        print("---------------------------")

    def get_player_move(self):
        move = ''
        while not move and not self.game_over:
            move = input('>').strip()
        return move.lower().split(" ", 1)

    def combat(self, enemy):
        while enemy.health > 0 and self.player.health > 0:
            self.player.attack(enemy)
            if enemy.health > 0:
                enemy.attack(self.player)
            if enemy.health <= 0:
                print(f"The {enemy.name} has been defeated!")
                self.player.current_room.enemies.remove(enemy)
                for item, locked in self.player.current_room.locked_items.items():
                    if locked:
                        self.player.current_room.locked_items[item] = False
                        print(f"The {item} is now available to pick up.")

    def play(self):
        self.show_instructions()
        command_methods = {
            'go': self.go_command,
            'get': self.get_command,
            'attack': self.attack_command,
            'map': self.map_command,
            'look': self.look_command,
            'free': self.free_command,
            'use': self.use_command,
            'exit': self.exit_command
        }

        while not self.game_over:
            self.show_status()
            move = self.get_player_move()
            if self.game_over:
                break
            command = move[0]
            argument = move[1] if len(move) > 1 else None

            if command in command_methods:
                command_methods[command](argument)
            else:
                print("Invalid command!")

            if self.check_game_over():
                break

    def go_command(self, direction):
        if self.trap_active:
            print("You can't move! The walls are closing in!")
        elif direction:
            self.player.move(direction)
        else:
            print("Go where?")

    def get_command(self, item):
        if item:
            self.player.get_item(item, self)
        else:
            print("Get what?")

    def attack_command(self, enemy_name):
        if enemy_name:
            enemy_name = enemy_name.lower()
            possible_enemies = [enemy for enemy in self.player.current_room.enemies]
            matching_enemies = [enemy for enemy in possible_enemies if enemy.name.lower() == enemy_name]

            if matching_enemies:
                self.combat(matching_enemies[0])
            else:
                if possible_enemies:
                    enemy_list = ', '.join(enemy.name for enemy in possible_enemies)
                    print(f"No enemy with that name here. Enemies present: {enemy_list}")
                else:
                    print("There are no enemies here to attack.")
        else:
            print("Attack who?")

    def map_command(self, _):
        print(self.generate_map())

    def look_command(self, _):
        print(self.player.current_room.get_details())

    def use_command(self, item):
        if item:
            item = item.lower()
            if item == 'access card' and self.player.current_room.name == 'Communications Hub':
                if 'access card' in self.player.inventory:
                    print("You quickly use the access card and stop the walls from crushing you!")
                    self.player.inventory.remove('access card')
                    self.player.current_room.locked_items['access card'] = False
                    self.trap_active = False  
                else:
                    print("You don't have an access card to use.")
            else:
                print(f"You can't use {item} here.")
        else:
            print("Use what?")

    def start_trap_timer(self, room):
        self.trap_active = True  
        timer_thread = threading.Thread(target=self.crush_walls, args=(self.player, self.end_game))
        timer_thread.start()

    def crush_walls(self, player, end_game_callback):
        countdown = self.COUNTDOWN_DURATION
        while countdown > 0 and not self.game_over:
            if countdown % 5 == 0:
                print(f"Walls are closing in! {countdown} seconds remaining!")
            time.sleep(1)
            countdown -= 1

        with self.game_over_lock:
            if 'access card' in player.inventory and not self.game_over:
                print("You didn't act fast enough and the walls crushed you!")
                player.health = 0
                end_game_callback()

    def end_game(self):
        self.game_over = True
        self.check_game_over()

    def free_command(self, ally_name):
        if ally_name:
            ally_name = ally_name.lower()
            if ally_name in self.player.current_room.allies:
                if not self.player.current_room.enemies:
                    if ally_name == 'leia' and 'security codes' in self.player.inventory:
                        self.player.inventory.append('Princess Leia')
                        self.player.current_room.allies.remove(ally_name)
                        print("You have freed Princess Leia! Now escape the Death Star!")
                    elif ally_name == 'r2-d2':
                        self.rooms['Control Room'].locked_items['security codes'] = False
                        self.player.inventory.append('R2-D2')
                        self.player.current_room.allies.remove(ally_name)
                        print("R2-D2 has unlocked the security codes in the Control Room!")
                    else:
                        print(f"You have freed {ally_name}!")
                else:
                    print(f"You cannot free {ally_name} while enemies are in the room!")
            else:
                print(f"There is no {ally_name} here to free.")
        else:
            print("Free who?")

    def exit_command(self, _):
        print("Thank you for playing. May the Force be with You!")
        exit(0)

    def check_game_over(self):
        if self.player.health <= 0:
            self.print_game_over_message()
            return True
        if 'Princess Leia' in self.player.inventory and 'R2-D2' in self.player.inventory \
        and self.player.current_room.name == 'Escape Pods' \
        and not self.player.current_room.enemies:
            print('You have freed your allies and escaped the Death Star... YOU WIN!')
            return True
        return False

    def print_game_over_message(self):
        print("You have been defeated... GAME OVER!")

    def generate_map(self):
        return '''
						    +--------------------+
						    |                    |	
						    |                    |
						    |                    |
						    | Imperial Chambers  |
						    |                    |
						    |                    |
						    |                    |
						    +--------------------+
	  			  			      |		
			  +--------------------+    +--------------------+
			  |                    |    |                    |	
			  |                    |    |                    |
			  |                    |    |                    |
			  |    Control Room    |----| Communications Hub |
			  |                    |    |                    |
			  |                    |    |                    |
			  |                    |    |                    |
			  +--------------------+    +--------------------+
	  			    |			      |
+--------------------+	  +--------------------+    +--------------------+
|                    |	  |                    |    |                    |	
|                    |	  |                    |    |                    |
|                    |	  |                    |    |                    |
|     Hangar Bay     |----|  Detention Block   |    |    Escape Pods     |
|                    |	  |                    |    |                    |
|                    |	  |                    |    |                    |
|                    |	  |                    |    |                    |
+--------------------+	  +--------------------+    +--------------------+'''