
class CommandProcessor:
    def __init__(self, game):
        self.game = game

    def process(self, move):
        command, argument = self.parse_command(move)
        command_method = getattr(self, f'{command}_command', None)
        if callable(command_method):
            command_method(argument)
        else:
            print('Invalid command!')

    def parse_command(self, move):
        return move[0], move[1] if len(move) > 1 else None

    def go_command(self, direction):
        if self.game.trap_active:
            print("You can't move! The walls are closing in!")
        elif direction:
            self.game.player.move(direction)
        else:
            print('Go where?')

    def get_command(self, item):
        if item:
            self.game.player.get_item(item, self.game)
        else:
            print('Get what?')

    def attack_command(self, enemy_name):
        if enemy_name:
            enemy_name = enemy_name.lower()
            possible_enemies = [enemy for enemy in self.game.player.current_room.enemies]
            matching_enemies = [enemy for enemy in possible_enemies if enemy.name.lower() == enemy_name]

            if matching_enemies:
                self.game.combat(matching_enemies[0])
            else:
                if possible_enemies:
                    enemy_list = ', '.join(enemy.name for enemy in possible_enemies)
                    print(f'No enemy with that name here. Enemies present: {enemy_list}')
                else:
                    print('There are no enemies here to attack.')
        else:
            print('Attack who?')

    def map_command(self, _):
        print(self.game.generate_map())

    def look_command(self, _):
        print(self.game.player.current_room.get_details())

    def use_command(self, item):
        if item:
            item = item.lower()
            if item == 'access card' and self.game.player.current_room.name == 'Communications Hub':
                if 'access card' in self.game.player.inventory:
                    print('You quickly use the access card and stop the walls from crushing you!')
                    self.game.player.current_room.locked_items['access card'] = False
                    self.game.trap_active = False
                    self.game.stop_trap = True 
                else:
                    print("You don't have an access card to use.")
            elif item == 'security codes' and self.game.player.current_room.name == 'Control Room':
                if 'security codes' in self.game.player.inventory:
                    print('You use the security codes to disable the security systems!')
                else:
                    print("You don't have the security codes to use.")
            else:
                print(f"You can't use {item} here.")
        else:
            print('Use what?')

    def free_command(self, ally_name):
        if ally_name:
            ally_name = ally_name.lower()
            allies_in_room = [ally.lower() for ally in self.game.player.current_room.allies]
            if ally_name in allies_in_room:
                original_ally_name = self.game.player.current_room.allies[allies_in_room.index(ally_name)]
                if not self.game.player.current_room.enemies:
                    if ally_name == 'leia' and 'security codes' in self.game.player.inventory:
                        self.game.player.inventory.append('Princess Leia')
                        self.game.player.current_room.allies.remove(original_ally_name)
                        print('You have freed Princess Leia! Now escape the Death Star!')
                    elif ally_name == 'r2-d2' and 'access card' in self.game.player.inventory:
                        self.game.rooms['Control Room'].locked_items['security codes'] = False
                        self.game.player.inventory.append('R2-D2')
                        self.game.player.current_room.allies.remove(original_ally_name)
                        print('You have freed R2-D2 and it has unlocked the security codes in the Control Room!')
                    else:
                        print(f'You need the proper item to free {original_ally_name}!')
                else:
                    print(f"You can't free {original_ally_name} while enemies are in the room!")
            else:
                print(f'There is no {ally_name} here to free.')
        else:
            print('Free who?')

    def exit_command(self, _):
        print('Thank you for playing. May the Force be with You!\n')
        exit(0)
