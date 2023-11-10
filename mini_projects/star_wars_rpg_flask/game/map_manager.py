class MapManager:
    def __init__(self, game_state):
        self.game_state = game_state

    def generate_map(self):
        room_indicators = {room_name: '   ' for room_name in self.game_state.rooms}
        player_room_name = self.game_state.player.current_room.name
        room_indicators[player_room_name] = '[X]'
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