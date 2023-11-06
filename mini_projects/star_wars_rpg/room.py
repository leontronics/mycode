class Room:
    def __init__(self, name, description, items=None, enemies=None, locked_items=None, allies=None):
        self.name = name
        self.description = description
        self.connected_rooms = {}
        self.items = items or []
        self.enemies = enemies or []
        self.locked_items = locked_items or {}
        self.allies = allies or []

    def connect_room(self, other_room, direction):
        opposite_directions = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
        self.connected_rooms[direction] = other_room
        other_room.connected_rooms[opposite_directions[direction]] = self

    def get_details(self):
        details = f"{self.description}\nPaths: {', '.join(self.connected_rooms.keys())}"
        if self.items:
            details += f"\nItems in the room: {', '.join(self.items)}"
        if self.enemies:
            alive_enemies = [enemy for enemy in self.enemies if enemy.health > 0]
            if alive_enemies:
                details += f"\nEnemies in the room: {', '.join(str(enemy) for enemy in alive_enemies)}"
        return details
    
    def trigger_trap(self, game):
        print("As you pick up the access card, you hear the walls starting to move... they're closing in!")
        game.start_trap_timer(self)