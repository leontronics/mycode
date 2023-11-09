class Room:
    
    OPPOSITE_DIRECTIONS = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}

    def __init__(self, name, description, items=None, enemies=None, locked_items=None, allies=None):
        '''Initialize the room with a name, description, and optional items, enemies, locked items, and allies.'''
        self.name = name
        self.description = description
        self.connected_rooms = {}
        self.items = items if items is not None else []
        self.enemies = enemies if enemies is not None else []
        self.locked_items = locked_items if locked_items is not None else {}
        self.allies = allies if allies is not None else []

    def connect_room(self, other_room, direction):
        '''Connect this room to another room in the given direction.'''
        opposite_direction = self.OPPOSITE_DIRECTIONS[direction]
        self.connected_rooms[direction] = other_room
        other_room.connected_rooms[opposite_direction] = self

    def get_details(self):
        '''Return a string with the details of the room.'''
        paths = ', '.join(self.connected_rooms.keys())
        items = ', '.join(self.items)
        alive_enemies = ', '.join(str(enemy) for enemy in self.enemies if enemy.health > 0)
        allies = ', '.join(self.allies)

        details = f'{self.description}\nPaths: {paths}'
        if items:
            details += f'\nItems in the room: {items}'
        if alive_enemies:
            details += f'\nEnemies in the room: {alive_enemies}'
        if allies:
            details += f'\nAllies in the room: {allies}'
        return details
    
    def trigger_trap(self, game):
        '''Trigger a trap in the room.'''
        print('As you pick up the access card, you hear the walls starting to move... they are closing in!')
        game.start_trap_timer()
