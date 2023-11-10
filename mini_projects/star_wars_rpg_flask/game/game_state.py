import json

class GameState:
    def __init__(self, game=None, game_interface='console'):
        self.game = game
        self.rooms = {}
        self.player = None
        self.game_over = False
        self.trap_active = False
        self.stop_trap = False
        self.game_interface = game_interface

    def serialize(self):
        return json.dumps(self.__dict__)

    def deserialize(self, data):
        self.__dict__ = json.loads(data)

    def update_player(self, player):
        self.player = player

    def update_rooms(self, rooms):
        self.rooms = rooms

    def set_game_over(self, game_over):
        self.game_over = game_over

    def set_trap_active(self, trap_active):
        self.trap_active = trap_active

    def set_stop_trap(self, stop_trap):
        self.stop_trap = stop_trap

    def remove_enemy_from_room(self, room, enemy):
        if enemy in room.enemies:
            room.enemies.remove(enemy)

    def unlock_items_in_room(self, room):
        for item, locked in room.locked_items.items():
            if locked:
                room.locked_items[item] = False

    def player_move(self, direction):
        move_result = self.player.move(direction)
        if move_result['new_room']:
            self.player.current_room = move_result['new_room']
        return move_result['message']

    def player_get_item(self, item):
        get_item_result = self.player.get_item(item)
        if get_item_result['success']:
            self.player.inventory.append(get_item_result['item'])
            self.player.current_room.items.remove(get_item_result['item'])
            if get_item_result['item'] == 'access card':
                return self.game.trigger_trap(get_item_result['message'])
        return get_item_result['message']

    def player_attack(self, target_name):
        target = next((enemy for enemy in self.player.current_room.enemies if enemy.name == target_name), None)
        if not target:
            return f"There is no {target_name} here to attack."
        attack_result = self.player.attack(target)
        if target and target in self.player.current_room.enemies:
            target.health -= attack_result['damage']
            if target.health <= 0:
                attack_result['message'] += f' {target.name} has been defeated!'
                self.player.current_room.enemies.remove(target)
        return attack_result['message']

