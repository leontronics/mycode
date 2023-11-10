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
        details = f"You are in the {self.description}\n"
        paths = ', '.join(self.connected_rooms.keys())
        details += f"Paths: {paths}\n" if paths else ""
        items = ', '.join(self.items)
        details += f"Items in the room: {items}\n" if items else ""
        alive_enemies = ', '.join(enemy.name for enemy in self.enemies if enemy.health > 0)
        details += f"Enemies here: {alive_enemies}\n" if alive_enemies else ""
        allies = ', '.join(self.allies)
        details += f"Allies here: {allies}\n" if allies else ""
        return details.strip() 

class RoomManager:
    def __init__(self):
        self.rooms = {}

    def create_room(self, name, description, items=None, enemies=None, locked_items=None, allies=None):
        room = Room(name, description, items, enemies, locked_items, allies)
        self.rooms[name] = room
        return room

    def connect_rooms(self, room1_name, room2_name, direction):
        room1 = self.rooms.get(room1_name)
        room2 = self.rooms.get(room2_name)
        if room1 and room2:
            room1.connect_room(room2, direction)

    def get_room(self, room_name):
        return self.rooms.get(room_name)