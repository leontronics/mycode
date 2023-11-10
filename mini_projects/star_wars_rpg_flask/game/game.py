import threading
import time
from .character import Player, Enemy
from .room import Room, RoomManager
from .map_manager import MapManager
from .command_processor import CommandProcessor
from .game_state import GameState

class Game:
    COUNTDOWN_DURATION = 30

    def __init__(self):
        self.state = GameState(game=self)
        self.room_manager = RoomManager()
        self.setup_rooms()
        self.state.update_player(Player(self.room_manager.get_room('Hangar')))
        self.map_manager = MapManager(self.state)
        self.command_processor = CommandProcessor(self)

    def setup_rooms(self):
        self.room_manager.create_room('Hangar', 'You are in the Hangar Bay of the Death Star', items=['blaster'])
        self.room_manager.create_room('Detention Block', 'You are in the Detention Block where prisoners are held', enemies=[Enemy('Stormtrooper', 'A loyal servant of the Empire', 30, ['blaster'])], allies=['Leia'])
        self.room_manager.create_room('Control Room', 'You are in the Control Room, control the security systems here', items=['security codes'], enemies=[Enemy('Stormtrooper', 'A vigilant guardian of the control systems', 30, ['blaster'])], locked_items={'security codes': True})
        self.room_manager.create_room('Communications Hub', 'You are in the Communications Hub, where all communications are monitored and controlled', items=['access card'], enemies=[Enemy('Stormtrooper', 'A loyal servant of the Empire', 30, ['blaster'])], locked_items={'access card': True})
        self.room_manager.create_room('Escape Pods', 'You are by the escape pods, ready to leave the Death Star', enemies=[Enemy('Dark Trooper', 'A menacing Dark Trooper, highly skilled and heavily armored', 120, ['blaster'])])
        self.room_manager.create_room('Imperial Chambers', 'You are in the Imperial Chambers, where the elite forces of the Empire reside', items=['lightsaber'], enemies=[Enemy('Stormtrooper', 'An elite soldier of the Empire, guarding the chambers', 30, ['blaster'])], allies=['R2-D2'])

        self.room_manager.connect_rooms('Hangar', 'Detention Block', 'east')
        self.room_manager.connect_rooms('Detention Block', 'Control Room', 'north')
        self.room_manager.connect_rooms('Control Room', 'Communications Hub', 'east')
        self.room_manager.connect_rooms('Communications Hub', 'Escape Pods', 'south')
        self.room_manager.connect_rooms('Communications Hub', 'Imperial Chambers', 'north')

        self.state.update_rooms(self.room_manager.rooms)

    def add_message(self, message):
        self.command_processor.add_message(message)

    def get_messages(self):
        return self.command_processor.get_messages()

    def clear_messages(self):
        self.command_processor.clear_messages()

    def show_instructions(self):
        instructions = '''
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
        '''
        self.add_message(instructions)

    def show_status(self):
        status = '---------------------------\n'
        status += f'Health: {self.state.player.health}\n'
        status += f'Inventory: {self.state.player.inventory}\n'
        status += f'Rescued Allies: {self.state.player.allies_rescued}\n'
        status += "---------------------------"
        self.add_message(status)

    def combat(self, enemy):
        messages = []
        while enemy.health > 0 and self.state.player.health > 0:
            attack_result = self.state.player.attack(enemy)
            messages.append(attack_result['message'])
            enemy.health -= attack_result['damage']  
            if enemy.health > 0:
                counter_attack_result = enemy.attack(self.state.player)
                messages.append(counter_attack_result['message'])
                self.state.player.health -= counter_attack_result['damage']  
            if enemy.health <= 0:
                defeat_message = f'The {enemy.name} has been defeated!'
                messages.append(defeat_message)
                self.state.remove_enemy_from_room(self.state.player.current_room, enemy)
                self.state.unlock_items_in_room(self.state.player.current_room)
            if self.state.player.health <= 0:
                defeat_message = 'You have been defeated!'
                messages.append(defeat_message)
                self.end_game() 
                break
        return messages

    def get_player_move(self, prompt=''):
        '''Get input from the console or web.'''
        move = ''
        while not move and not self.state.game_over:
            if self.state.game_interface == 'console':
                move = input(prompt).strip()
            elif self.state.game_interface == 'web':
                '''Pending web'''
                move = self.web_input()
            else:
                raise ValueError("Unknown game interface")
        return move.lower().split(' ', 1)

    def play_game(self):
        self.show_instructions()  
        self.process_messages()
        while not self.state.game_over:
            self.show_status() 
            self.process_messages()
            move = self.console_input('>')
            if self.state.game_over:
                break
            self.command_processor.process(move)
            self.process_messages()
            if self.check_game_over():
                break

    def process_messages(self):
        for message in self.get_messages():
            self.console_output(message)
        self.clear_messages()

    def console_input(self, prompt=''):
        '''Get input from the console.'''
        move = ''
        while not move and not self.state.game_over:
            move = input(prompt).strip()
        return move.lower().split(' ', 1)

    def console_output(self, message):
        '''Send output to the console.'''
        print(message)

    def web_output(message):
        '''This function would send output back to the web client'''
        pass

    def trigger_trap(self, message):
        self.start_trap_timer()
        return f"{message} As you pick up the access card, you hear the walls starting to move... they are closing in!"

    def start_trap_timer(self):
        self.state.trap_active = True
        timer_thread = threading.Thread(target=self.crush_walls)
        timer_thread.start()

    def crush_walls(self):
        countdown = self.COUNTDOWN_DURATION
        while countdown > 0 and not self.state.game_over and not self.state.stop_trap:
            if countdown % 10 == 0:
                self.add_message(f'Walls are closing in! {countdown} seconds remaining!')
                self.process_messages()
            time.sleep(1)
            countdown -= 1

        if not self.state.stop_trap and self.state.trap_active and 'access card' in self.state.player.inventory:
            crush_message = "You didn't act fast enough and the walls crushed you!"
            self.add_message(crush_message)
            self.process_messages()
            self.state.player.health = 0
            self.end_game()

    def end_game(self):
        self.state.game_over = True
        self.check_game_over()

    def check_game_over(self):
        if self.check_defeat() or self.check_victory():
            self.state.set_game_over(True)
            return True
        return False

    def check_defeat(self):
        if self.state.player.health <= 0:
            self.add_message('You have been defeated... GAME OVER!\n')
            self.process_messages()
            return True
        return False

    def check_victory(self):
        if 'Princess Leia' in self.state.player.allies_rescued and 'R2-D2' in self.state.player.allies_rescued \
        and self.state.player.current_room.name == 'Escape Pods' \
        and not self.state.player.current_room.enemies:
            self.add_message('You have freed your allies and escaped the Death Star... YOU WIN!\n')
            self.process_messages()
            return True
        return False
