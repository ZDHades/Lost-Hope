import random as r


# Lost Hope...


# First map 
map_1 = {'spawn': [('east', 'm1')],
    "m1" : [('north', 'm2'), ('south', 's1a'), ('west', 'spawn')],
    "m2" : [('west', 'npc'), ('south', 'm1')],
    "npc" : [('north', 's2a'), ('east', 'm2'), ('east', 'tr'), ('west', 'm4')],
    "m4" : [('east', 'npc'), ('south', 'm5'), ('north', 's3a')],
    "m5" : [('west', 's4a'), ('south', 'm6'), ('north', 'm5')],
    "m6" : [('west', 'm7'), ('north', 'm5')],
    "m7" : [('east ', 'm6'), ('west', 's5a'), ('south', 'm8')],
    "m8" : [('north', 'm7'), ('south', 'm9')],
    "m9" : [('north', 'm8'), ('east', 'd')],
    "d" : [('west', 'm9')],
    "s1a" : [('south', 'k1'), ('north','m1')],
    'k1' : [('north', 's1a')],
    "s2a" : [('south', 'npc'), ('north', 's2b')],
    "s2b" : [('south', 's2a'), ('east', 'k2')],
    "k2" : [('west', 's2b')],
    "tr" : [('west', 'npc'), ('north', 'treasure')],
    'treasure' : [('south', 'tr')],
    "s3a" : [('north', 's3b'), ('south', 'm4')],
    's3b' :  [('east', 'k3'), ('south', 's3a')],
    'k3' : [('west', 's3b')],
    's4a' : [('east', 'm5'), ('north', 's4b')],
    's4b' : [('south', 's4a'), ('west', 'k4')],
    's5a' : [('east', 'm7'), ('south','s5b')],
    's5b' : [('south', 's5c'), ('north', 's5a')],
    's5c' : [('south', 'k5'), ('north', 's5b')],
    'k5': [('north', 's5c')]
    }

# global variables for inversing directions, and keys for the different room types
inverse_directions = {'east':'west', 'north':'south', 'west':'east', 'south':'north'}
room_types = {'s':'split', 't':'treasure','k':'key','m':'main','d':'defender','n':'market'}


# main board class. Contains the map, most other classes will inherit from it
class Board:
    completed_rooms = []
    def __init__(self, map):
        self.map = map_1
        

# class for everything related to rooms - movement, internal generation, player interactions, and loot 
class Room(Board):
    global inverse_directions
    def __init__(self):
        super().__init__(map)
        self.current_room = 'spawn'
        self.room_type = 'spawn'
        self.previous_direction = ''
        self.paths = self.map[self.current_room]

    # method for moving a player from one room to the next
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
                
    # generating text to tell the user their options, and to validate their choice for room movement (except for markets)
    @classmethod
    def direction_select(self, directions, rooms):
        print("Where would you like to go?")
        if len(directions) == 1 and self.current_room != 'spawn':
            print(f"You have hit a dead end so you can only go {inverse_directions[self.previous_direction]}, which leads to the previous room you were in")
        if inverse_directions[self.previous_direction] in directions:
            print(f"You can go {inverse_directions[self.previous_direction]} which leads to the previous room you were in.")
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

        # method to control movement inside the market, and for leaving it
        @classmethod
        def market_directions(self):
            pass
    
# class entity(Board):
#     pass
