# IT 140 6-4 Milestone: Moving Between Rooms
# Nisarg Patel
# Lost Hope - A Text Based Adventure Game


# Creating our map dictionary
map_1 = {'entrance': [('east', 'm1')],
    "m1" : [('north', 'm2'), ('south', 's1a'), ('west', 'entrance')],
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

# Skeleton class for the introduction to the game
class Intro():
    def intro():
        print('hi')

# Skeleton class for getting player variables such as name, class and others
class Player():
    def select_class():
        print('pick a class')

# Board class, this is where all of the action will happen!
class Board():
    # Declaring local variables for the Board class. These will help to classify the room types, and for movement within the Market (large room)
    room_types = {'s':'split', 't':'treasure','k':'key','m':'main','d':'defender','n':'market', 'e': 'entrance'}
    map_1_market_keys = [('northeast','tr'), ('southeast', 'm2'), ('north', 's2a'), ('west', 'm4')]

    # creating the constructor for the class. Getting our required attributes for the class to make it run!
    def __init__(self, map):
        # Creating an attribute for the map because eventually we will have multiples, however for now it is static
        self.map = map
        # This will be used to keep track of the players location
        self.current_room = 'entrance'
        # this will be used to display to the user, the type of room they are currently in
        self.room_type = 'entrance'
        # this is used to help the user quit 
        self.previous_direction = ''
    
    # Using the __repr__ method for our display. Using this method lets us easily access attributes without risk of accidentally minuplating them
    def __repr__(self):
        # using a string formatting to create a displayboard for the game. Will show the user all of the relevant information such as their
        # current equipment and location within the Labrynth
        display = '{left:^20}|{right:^20}'
        print("="*40)
        print(display.format(left = 'Nisarg', right = 'Wizard'))
        print(display.format(left = 'Current Room', right = self.room_type))
        # for now there is no equipment so random placeholders are used to help structure the format
        print(display.format(left = 'Weapon', right = 'someting'))
        print(display.format(left = 'Armor', right = 'sometin'))
        print(display.format(left = 'Accessory', right = 'somet'))
        print(display.format(left = 'Ability', right = 'some'))
        # important to have a return statement so the function is complete :D
        return '='*40
        
    # This is the method that we will use to move our player around the board. It takes no arguments, since all of the information we need
    # will either be inputted by the player or can already be locally found within our object.
    def movement(self):
        # creating empty lists that we will use to hold information the possible routes the player can take
        directions = []
        rooms = []
        # using a turnary assignment to find the values associcated to the current room's key within the map dictionary. If they are in the 
        # market, we want to use an alternate dictionary. This will be changed to be accomidated within the main dictionary on the next build.
        paths = self.map[self.current_room] if self.room_type != 'market' else self.map_1_market_keys
        # looping through the list taken from accessing the map dictionary's values. It is important later, that we store each combination in the
        # same index of both lists
        for _ in paths:
            # every 0th element in the tuples within the list are the direction the player can go, so we append that to the directions list
            directions.append(_[0])
            # every 1st element in the tuples within the list are the rooms the player can go, so we append that to the rooms list
            rooms.append(_[1])
        # Here we call our direction_select method, we want to use this to validate the direction that the user submits. It is moved to a
        # seperate method so the overall purpose of this method is easily understandable and it helps to remove some of the clutter
        direction = self.direction_select(directions, rooms)
        # by updating the object to have a new attribute, we can easily check it from a global perspective this to exit out of external loops/functions
        self.previous_direction = direction
        # if the user submitted 'quit' we show the user some rating to show how far they got and then quit out of the game. 
        if self.previous_direction == 'quit':
            print("Thank you for playing, your skill was {some_skill_level_here}!")
            # returning True to update the outside flag to exit the loop where this method will be used. 
            return True
        # if they submitted just a normal acceptable direction, we find the index of that direction within its list.
        x = directions.index(direction)
        # then we use that same index location to peek into the rooms list and get our room type
        self.current_room = rooms[x]
        # updating the attributes of the object so we can easily observe it on the global perspective
        self.room_type = self.room_types[self.current_room[0]]
        return False
                
    # Our method for validating the user's input for moving around the map
    # we are passed two arguments, the direction and rooms list (rooms isnt used, and will be removed in the next build) which lets us pick up 
    # from the same place we left off on in the previous method
    def direction_select(self, directions, rooms):
        # we want to add the option to quit into the directions. This may be changed to be an invisible option in future builds since
        # it is not very visually pleasing :(
        directions.append('quit')
        # Some print statements to talk to our player
        print("Where would you like to go?")
        # Using the end = argument for the print statement so we can add all of the directions they can go into 1 line.
        print("Your options are", end=' ')
        for _ in directions:
            print(f"{_}", end=' ')
        # finishing it off with an ! so we can get the \n character naturally added in. **need to figure out how to get rid of the extra space 
        # after the last direction **
        print("!")
        # a while not loop with a flag variable to continue looping until we have an input we like :D
        direction_chosen = False
        while not direction_chosen: 
            # getting our input for direction from the player
            direction = input("Please choose a direction to go!\n").lower() #Fancy .lower() so we dont have to worry about people using random caps
            # testing membership of the input within our possible directions {might update the directions list to be a Set for 
            # more efficient membership tests}
            if direction in directions:
                # if they entered a valid direction, we reset our flag, and return the direction the previous method!
                direction_chosen = True
                return direction
            # other wise we send them back to the start to try again :D
            else:
                print("You did not select a valid direction, please try again!\n")
                continue

# Skeleton Play class, This just exists temporarily for the purpose of this milestone. It will be very different in the next build
# Currently it is being used to tie our classes and methods together into a 'playable' script
class Play:
    def game():
        rmap = map_1 #When there are multiple maps, we will randomly choose a map here
        # creating an instance of our Board class, using rmap
        board = Board(rmap)
        # calling the class method from Intro to play our introduction
        Intro.intro()
        # calling the class method from Player as a place holder
        Player.select_class()
        # fun while not loop with a flag so we can keep exploring our labrynth until the player gets bored and decides to quit!
        done = False
        while not done:
            print(repr(board))
            done = board.movement()

# Calling our Play class method to run the script! Hope you enjoy =)
Play.game()