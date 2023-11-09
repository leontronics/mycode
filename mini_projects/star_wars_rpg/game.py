import threading
import time
from character import Player, Enemy
from room import Room
from command_processor import CommandProcessor

class Game:

    COUNTDOWN_DURATION = 30

    def __init__(self):
        self.rooms = {}
        self.setup_rooms()
        self.player = Player(self.rooms['Hangar'])
        self.game_over_lock = threading.Lock()
        self.game_over = False
        self.trap_active = False
        self.stop_trap = False
        self.command_processor = CommandProcessor(self)

    def setup_rooms(self):
        self.initialize_rooms()
        self.connect_rooms()

    def initialize_rooms(self):
        '''Initialize each room with its description, items, enemies, etc.'''
        self.rooms = {
            'Hangar': Room('Hangar', 'You are in the Hangar Bay of the Death Star', items=['blaster']),
            'Detention Block': Room('Detention Block', 'You are in the Detention Block where prisoners are held', enemies=[Enemy('Stormtrooper', 'A loyal servant of the Empire', 30, ['blaster'])], allies=['Leia']),
            'Control Room': Room('Control Room', 'You are in the Control Room, control the security systems here', items=['security codes'], enemies=[Enemy('Stormtrooper', 'A vigilant guardian of the control systems', 30, ['blaster'])], locked_items={'security codes': True}),
            'Communications Hub': Room('Communications Hub', 'You are in the Communications Hub, where all communications are monitored and controlled', items=['access card'], enemies=[Enemy('Stormtrooper', 'A loyal servant of the Empire', 30, ['blaster'])], locked_items={'access card': True}),
            'Escape Pods': Room('Escape Pods', 'You are by the escape pods, ready to leave the Death Star', enemies=[Enemy('Dark Trooper', 'A menacing Dark Trooper, highly skilled and heavily armored', 120, ['blaster'])]),
            'Imperial Chambers': Room('Imperial Chambers', 'You are in the Imperial Chambers, where the elite forces of the Empire reside', items=['lightsaber'], enemies=[Enemy('Stormtrooper', 'An elite soldier of the Empire, guarding the chambers', 30, ['blaster'])], allies=['R2-D2'])
        }

    def connect_rooms(self):
        '''Connect the rooms to each other'''
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
        return move.lower().split(' ', 1)

    def combat(self, enemy):
        while enemy.health > 0 and self.player.health > 0:
            self.player.attack(enemy)
            if enemy.health > 0:
                enemy.attack(self.player)
            if enemy.health <= 0:
                print(f'The {enemy.name} has been defeated!')
                self.player.current_room.enemies.remove(enemy)
                for item, locked in self.player.current_room.locked_items.items():
                    if locked:
                        self.player.current_room.locked_items[item] = False
                        print(f'The {item} is now available to pick up.')

    def play(self):
        self.show_instructions()
        while not self.game_over:
            self.show_status()
            move = self.get_player_move()
            if self.game_over:
                break
            self.command_processor.process(move)
            if self.check_game_over():
                break

    def start_trap_timer(self, room):
        self.trap_active = True  
        timer_thread = threading.Thread(target=self.crush_walls, args=(self.player, self.end_game))
        timer_thread.start()

    def crush_walls(self, player, end_game_callback):
        countdown = self.COUNTDOWN_DURATION
        while countdown > 0 and not self.game_over and not self.stop_trap:
            if countdown % 10 == 0:
                print(f'Walls are closing in! {countdown} seconds remaining!')
            time.sleep(1)
            countdown -= 1

        with self.game_over_lock:
            if not self.stop_trap and self.trap_active and 'access card' in player.inventory and not self.game_over:
                print("You didn't act fast enough and the walls crushed you!")
                player.health = 0
                end_game_callback()

    def end_game(self):
        self.game_over = True
        self.check_game_over()

    def check_game_over(self):
        return self.check_defeat() or self.check_victory()

    def check_defeat(self):
        if self.player.health <= 0:
            self.print_game_over_message()
            return True
        return False

    def check_victory(self):
        if 'Princess Leia' in self.player.inventory and 'R2-D2' in self.player.inventory \
        and self.player.current_room.name == 'Escape Pods' \
        and not self.player.current_room.enemies:
            print('You have freed your allies and escaped the Death Star... YOU WIN!\n')
            return True
        return False

    def print_game_over_message(self):
        print('You have been defeated... GAME OVER!\n')

    def generate_map(self):       
        room_indicators = {room_name: '   ' for room_name in self.rooms}
        room_indicators[self.player.current_room.name] = '[X]'
        game_map = f'''    
						    +--------------------+
						    |                    |	
						    |                    |
						    |                    |
						    | Imperial Chambers  |
						    |                    |
						    |        {room_indicators['Imperial Chambers']}         |
						    |                    |
						    +--------------------+
	  			  			      |		
			  +--------------------+    +--------------------+
			  |                    |    |                    |	
			  |                    |    |                    |
			  |                    |    |                    |
			  |    Control Room    |----| Communications Hub |
			  |                    |    |                    |
			  |        {room_indicators['Control Room']}         |    |        {room_indicators['Communications Hub']}         |
			  |                    |    |                    |
			  +--------------------+    +--------------------+
	  			    |			      |
+--------------------+	  +--------------------+    +--------------------+
|                    |	  |                    |    |                    |	
|                    |	  |                    |    |                    |
|                    |	  |                    |    |                    |
|     Hangar Bay     |----|  Detention Block   |    |    Escape Pods     |
|                    |	  |                    |    |                    |
|        {room_indicators['Hangar']}         |	  |        {room_indicators['Detention Block']}         |    |        {room_indicators['Escape Pods']}         |
|                    |	  |                    |    |                    |
+--------------------+	  +--------------------+    +--------------------+'''

        return game_map