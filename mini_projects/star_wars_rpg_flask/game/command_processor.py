
class CommandProcessor:
    def __init__(self, game):
        self.game = game
        self.messages = []  

    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def clear_messages(self):
        self.messages = []

    def process(self, move):
        command, argument = self.parse_command(move)
        if command is None:
            self.add_message('Please enter a command')
            return
        command_method = getattr(self, f'{command}_command', None)
        if callable(command_method):
            command_method(argument)
        else:
            self.add_message('Invalid command!')

    def parse_command(self, move):
        if not move:
            return None, None
        return move[0], move[1] if len(move) > 1 else None

    def go_command(self, direction):
        if self.game.state.trap_active:
            self.add_message("You can't move! The walls are closing in!")
        elif direction:
            move_result = self.game.state.player.move(direction)
            self.add_message(move_result['message'])
        else:
            self.add_message('Go where?')

    def get_command(self, item):
        if item:
            current_room = self.game.state.player.current_room
            if item in current_room.locked_items and current_room.locked_items[item]:
                self.add_message(f"The {item} are locked and you cannot get them without the proper action.")
            else:
                message = self.game.state.player_get_item(item)
                self.add_message(message)
        else:
            self.add_message('Get what?')

    def attack_command(self, enemy_name):
        if enemy_name:
            enemy_name = enemy_name.lower()
            possible_enemies = [enemy for enemy in self.game.state.player.current_room.enemies]
            matching_enemies = [enemy for enemy in possible_enemies if enemy.name.lower() == enemy_name]

            if matching_enemies:
                combat_messages = self.game.combat(matching_enemies[0])  
                for message in combat_messages:
                    self.add_message(message)  
            else:
                if possible_enemies:
                    enemy_list = ', '.join(enemy.name for enemy in possible_enemies)
                    self.add_message(f'No enemy with that name here. Enemies present: {enemy_list}')
                else:
                    self.add_message('There are no enemies here to attack.')
        else:
            self.add_message('Attack who?')

    def map_command(self, _):
        self.add_message(self.game.map_manager.generate_map())

    def look_command(self, _):
        self.add_message(self.game.state.player.current_room.get_details())

    def use_command(self, item):
        if item:
            item = item.lower()
            if item == 'access card' and self.game.state.player.current_room.name == 'Communications Hub':
                if 'access card' in self.game.state.player.inventory:
                    self.add_message('You quickly use the access card and stop the walls from crushing you!')
                    self.game.state.player.current_room.locked_items['access card'] = False
                    self.game.state.trap_active = False
                    self.game.state.stop_trap = True 
                else:
                    self.add_message("You don't have an access card to use.")
            elif item == 'security codes' and self.game.state.player.current_room.name == 'Control Room':
                if 'security codes' in self.game.state.player.inventory:
                    self.add_message('You use the security codes to disable the security systems!')
                else:
                    self.add_message("You don't have the security codes to use.")
            else:
                self.add_message(f"You can't use {item} here.")
        else:
            self.add_message('Use what?')

    def free_command(self, ally_name):
        if ally_name:
            ally_name = ally_name.lower()
            allies_in_room = [ally.lower() for ally in self.game.state.player.current_room.allies]
            if ally_name in allies_in_room:
                original_ally_name = self.game.state.player.current_room.allies[allies_in_room.index(ally_name)]
                if not self.game.state.player.current_room.enemies:
                    if ally_name == 'leia' and 'security codes' in self.game.state.player.inventory:
                        self.game.state.player.allies_rescued.append('Princess Leia')  
                        self.game.state.player.current_room.allies.remove(original_ally_name)
                        self.add_message('You have freed Princess Leia! Now escape the Death Star!')
                    elif ally_name == 'r2-d2' and 'access card' in self.game.state.player.inventory:
                        self.game.state.rooms['Control Room'].locked_items['security codes'] = False
                        self.game.state.player.allies_rescued.append('R2-D2')  # Add to allies_rescued list
                        self.game.state.player.current_room.allies.remove(original_ally_name)
                        self.add_message('You have freed R2-D2 and it has unlocked the security codes in the Control Room!')
                    else:
                        self.add_message(f'You need the proper item to free {original_ally_name}!')
                else:
                    self.add_message(f"You can't free {original_ally_name} while enemies are in the room!")
            else:
                self.add_message(f'There is no {ally_name} here to free.')
        else:
            self.add_message('Free who?')

    def exit_command(self, _):
        self.add_message('Thank you for playing. May the Force be with You!\n')
        self.game.state.set_game_over(True)
