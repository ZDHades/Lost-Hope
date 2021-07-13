import random as r


# Lost Hope...

map_1 = {'spawn': [('right', 'm1')],
    "m1" : [('up', 'm2'), ('down', 's1a'), ('left', 'spawn')],
    "m2" : [('left', 'npc'), ('down', 'm1')],
    "npc" : [('up', 's2a'), ('right', 'm2'), ('right', 'tr'), ('left', 'm4')],
    "m4" : [('right', 'npc'), ('down', 'm5'), ('up', 's3a')],
    "m5" : [('left', 's4a'), ('down', 'm6'), ('up', 'm5')],
    "m6" : [('left', 'm7'), ('up', 'm5')],
    "m7" : [('right ', 'm6'), ('left', 's5a'), ('down', 'm8')],
    "m8" : [('up', 'm7'), ('down', 'm9')],
    "m9" : [('up', 'm8'), ('right', 'mbd')],
    "mbd" : [('left', 'm9')],
    "s1a" : [('down', 'k1'), ('up','m1')],
    'k1' : [('up', 's1a')],
    "s2a" : [('down', 'npc'), ('up', 's2b')],
    "s2b" : [('down', 's2a'), ('right', 'k2')],
    "k2" : [('left', 's2b')],
    "tr" : [('left', 'npc'), ('up', 'treasure')],
    'treasure' : [('down', 'tr')],
    "s3a" : [('up', 's3b'), ('down', 'm4')],
    's3b' :  [('right', 'k3'), ('down', 's3a')],
    'k3' : [('left', 's3b')],
    's4a' : [('right', 'm5'), ('up', 's4b')],
    's4b' : [('down', 's4a'), ('left', 'k4')],
    's5a' : [('right', 'm7'), ('down','s5b')],
    's5b' : [('down', 's5c'), ('up', 's5a')],
    's5c' : [('down', 'k5'), ('up', 's5b')],
    'k5': [('up', 's5c')]
    }
    
inverse_directions = {'east':'west', 'north':'south', 'west':'east', 'south':'north'}
room_types = {'s':'split', 't':'treasure','k':'key','m':'main','d':'defender','n':'market'}


class Board:
    completed_rooms = []
    def __init__(self, map):
        self.map = map_1
        
        
class Room(Board):
    global inverse_directions
    def __init__(self):
        super().__init__(map)
        self.current_room = 'spawn'
        self.room_type = 'spawn'
        self.previous_direction = ''
        self.paths = self.map[self.current_room]
        
    @classmethod
    def movement(self):
        directions = []
        rooms = []
        for _ in self.paths:
            directions.append(_[0])
            rooms.append(_[1])
        direction = self.direction_select(directions, rooms) if self.room_type != 'market' else self.market_directions(directions, rooms)
        self.previous_direction = direction
        x = directions.index([direction])
        self.current_room = rooms[x]
        self.room_type = room_types[self.current_room[0]]
                
    
    @classmethod
    def direction_select(self, directions, rooms):
        print("Where would you like to go?")
        if len(directions) == 1 and self.current_room != 'spawn':
            print(f"You have hit a dead end so you can only go {inverse_directions[self.previous_direction]}, which is the previous room you were in")
        
        if inverse_directions[self.previous_direction] in directions:
            print(f"You can go {inverse_directions[self.previous_direction]} which is the previous room you were in.")
            print("Your other options are ", end=' ')
        else:
            print("Your options are", end=' ')
        for _ in directions:
            if _ != inverse_directions[self.previous_direction]:
                print(f"{_}", end=' ')
        print("!")
        direction_chosen = False
        while not direction_chosen: 
            direction = input("Please choose a direction to go!\n").lower()
            if direction in directions:
                direction_chosen = True
                return direction
            else:
                print("You did not select a valid direction, please try again!\n")
                continue
                
        @classmethod
        def market_directions(self):
            pass