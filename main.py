from os import system as sys
from time import sleep as s
import random as r

# Creating our map in a global variable
map_1 = {'entrance': [('east', 'm1')],
    "m1" : [('north', 'm2'), ('south', 's1a'), ('west', 'entrance')],
    "m2" : [('west', 'npc'), ('south', 'm1')],
    "npc" : [('northeast','tr'), ('southeast', 'm2'), ('north', 's2a'), ('west', 'm4')],
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

# Creating the intro sequence, also in a global variable
intro = """
You thought it was just a tale told to young children to scare them. Never did you think you’d actually stumble upon the entrance to the 
Forgotten Labyrinth.  As you survey the entrance, you remember the story your mother told you... In the world before, there was a 
terrible battle between the light and dark, it was called the Era of Antimony. The heroes of the realm fought against the swaths of 
minions controlled by an unknown dark force, whose name has been lost to time. Some of his minions, called the Cultists of Malus, sought 
to seek this dark power for themselves. They bound this dark force to a pocket dimension, slowly leeching his life force, and created an 
automaton of solid marble to guard the secret. When the heroes found out that the darkness had been locked away and stripped of its 
power, they sought to kill it while it was weak. The foolish heroes gathered their armies and launched a crusade into the labyrinth; 
however, they were all lost within the maze, and they lost all hope as the magic of the Cultists slowly drove them mad. Legend says that 
the Cultists and the darkness are still fighting for dominance within the walls of the Forgotten Labyrinth, and if either win, they will 
come to throw the world back into the dark ages. However, if a hero, should he be worthy, could navigate the treacherous labyrinth and 
kill the two legendary foes, he would be rewarded with great riches and save the world from a terrible inevitable fate...The entrance 
seems to be locked, so you walk around the area to explore and look for clues, and possibly a key. After a while of searching, you find a 
pillar of marble, crumbling on the top, with moss and vines growing along its sides. You go to scrape the vines off, hoping to see some 
preserved text, but as soon as you touch it, the rest of the pillar crumbles and topples over. You slowly back up, not wanting to damage 
it more, and you hear a soft rumbling coming from the entrance. When you run back to check where they noise is coming from, you notice the 
door slowly opening on its own. Shocked, you silently stare into the foreboding dark corridors for several minutes, when suddenly the 
doors start to close again...this is your chance...this is your chance at glory, to save the world, and you don’t have much time to make 
the choice. At the last second, you jump into the Forgotten Labyrinth and barely make it in as the doors fully close. As if the Labyrinth 
somehow knew it had a visitor, flames grow from torches, illuminating the hall, and whatever shred and you feel the last shreds of hope you 
held slowly dissipate as you see the horrors of the Forgotten Labyrinth. You hear some faint banging on the doors from the outside, but you
are too amazed to hear or recognize what the sounds could be...
"""

# Creating a simple class that will hold our color tags, for formatting some text messages from Bosses
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# Board class, will hold all of the pieces together, help with movement and generation of rooms 
class Board():
    # some local variables for holding a key dictionary for our map
    room_types = {'s':'split', 't':'treasure','k':'key','m':'main','d':'defender','n':'market', 'e': 'entrance'}
    # This list will hold the list of rooms the player has already visited
    completed_rooms = []
    
    # creating the constructor for the class, using the required attributes to make stuff happen
    def __init__(self, map):
        self.map = map
        self.current_room = 'entrance'
        self.room_type = 'entrance'
        self.previous_direction = ''
    
    # a quick __repr__ method for the main game display, also lets us safely view our attributes
    def __repr__(self):
        display = '*{left:^19}|{right:^18}*'
        print("="*40)
        print(display.format(left = 'Nisarg', right = 'Wizard'))
        print(display.format(left = 'Current Room', right = self.room_type))
        # there are no player hero classes to choose from yet, so these are placeholders
        print(display.format(left = 'Weapon', right = 'Staff'))
        print(display.format(left = 'Armor', right = 'Robe'))
        print(display.format(left = 'Accessory', right = 'Amulet'))
        print(display.format(left = 'Ability', right = 'Spell'))
        # sending the last line on a return statement to make sure the function works properly
        return '='*40
    
    # This is the movement method, from here we update the current room based on player input
    def movement(self, player):
        # these two empty lists will hold split information from the map
        directions = []
        rooms = []
        paths = self.map[self.current_room]
        for _ in paths:
            directions.append(_[0])
            rooms.append(_[1])
        # sending information about our current room to the direction_select method
        direction = self.direction_select(directions)
        # using this attribute to filter for 'quit' incase the player is bored or busy
        self.previous_direction = direction
        if self.previous_direction == 'quit':
            print(f"Thank you for playing, your skill was {player.get_skill(self)}!")
            # return true to indicate the player is quitting
            return True
        # matching up the direction/room lists with the information from our dictionary
        # to make sure we accurately move in the correct new direction
        x = directions.index(direction)
        if self.current_room not in self.completed_rooms:
            # if the player is moving to a new room, we add that to the completed rooms list
            self.completed_rooms.append(self.current_room)
        else:
            # otherwise we add a fatigue counter to the player (debuff)
            player.fatigue += 1
        # assigning new attributes dependent on the status of the new room
        self.current_room = rooms[x]
        self.room_type = self.room_types[self.current_room[0]]
        # clearing out any leftover equipment on the floor (despawns once you leave the room)
        Equipment.on_floor.clear()
        # quick return false to indicate that the user is still playing the game
        return False
                
    # our direction select method
    def direction_select(self, directions):
        # adding quit to the list of possible directions we got passed
        directions.append('quit')
        print("Where would you like to go?")
        print("Your options are", end=' ')
        # printing our list in 1 line
        for _ in directions:
            print(f"{_}", end=' ')
        print("!")
        # creating a while not flag
        direction_chosen = False
        while not direction_chosen: 
            # taking user input for direction
            direction = input("Please choose a direction to go!\n{for example - go east}\n").lower().split()
            if len(direction) > 1:
                direction = direction[1]
            else:
                print("Please type the direction like this - {go east}")
                continue
            # validating that the user's input is a valid direction
            if direction in directions:
                # if so, we send it back, and update the flag for saftey
                direction_chosen = True
                return direction
            # if the user didnt select a valid direction, we continue to the start of the loop and ask them to try again
            else:
                print("You did not select a valid direction, please try again!\n")
                continue
    
    # Old method that is no longer used - previously used to generate items when visiting a room for the first time
    def no_item_rooms(self):
        no_item_rooms = ['entrance', 'Treasure', 'k1', 'k2', 'k3', 'k4', 'k5', 'd'] + self.completed_rooms
        return no_item_rooms
    
    # method that shows the final game over sequence if the player wins!
    def complete(self, player):
        print("There is a small rumble, and from within the arena purple smoke flows out to form a portal in front of you")
        print("With confidence, you step through, and find yourself at the entrance of the Forgotten Labrynth...")
        print("In front of you, you see...yourself...jumping into the Labrynth, as the doors shut behind yourself")
        s(2)
        print("You run up and bang on the doors to try to get them to open, but they dont budge.")
        print("You look around for hours, to try to find another key, to try and save yourself but you find none...")
        s(2)
        print("The sun fades into the far west as night approaches, so you give up and decide to rest.")
        print("In the morning, you awake with renewed energy, ready to begin your travel to the Captial.")
        s(1)
        print("You knew that when you arrived, you would be the hero that the world had been waiting a millena for...")
        print(f'You have beaten the Forgotten Labrynth at level {player.get_skill(self)}! Congratulations!')
        
    # This method is the meat of our code. It will check to see which room type the user is in
    # and if this is their first visit or not. Based on that, it will generate the nescessary enemies and do battle with them
    # it will also generate most of the items for the player to use.
    def generate_room(self, player):
        # if this is a room the player has already visited, we warn them about fatigue (we take care of applying fatigue elsewhere)
        if self.current_room in self.completed_rooms:
            print("You have already defeated all of the enemies in this room.")
            print("Try to conserve your stamina by not visiting rooms multiple times when possible.")
            # return false to indicate that we are still not dead and havnt quit (works the same for the rest of the conditionals below)
            return False
        # Key rooms! We give the user a key, and a message from the cultists of malus until they get 3 keys
        elif self.room_type == 'key' and self.current_room not in self.completed_rooms:
            print()
            print("You arrive in a room, adorned on the walls are severals vases with ornate drawings on them.")
            print(f"In the center of the room there is a glass display and inside lies a {color.YELLOW}golden key{color.END}.")
            print("With each step, as you walk closer to the display, the glass cracks a little more.")
            print("By the time you arrive to the display, the display shatters and the key floats into your hands")
            print("The room darkens and you hear a rumble from afar and a cold breeze passes over you.")
            player.keys += 1
            Equipment.create_item(player.get_skill(self) + 1, player)
            if player.keys == 1:
                print("There is silence for a moment, then you hear a shriek...")
                Intro.slow_print(f'{color.RED}{color.BOLD}WHO DARES{color.END}', .1)
            elif player.keys == 2:
                print(f"{color.RED}Deities of the underworld, grant us a champion to fight for us!")
            elif player.keys ==3:
                # the treasure room is open! The cultists of Malus are scared
                print(f"{color.RED}Rise my friends...{color.BOLD}AND STRIKE THEM DOWN!")
            return False
        
        # Split rooms are those that lead to a key room or the treasure room
        # main rooms are the ones that lead to the marble defender and the void entity
        # in each of these rooms we spawn a random enemy and have them fight the player.
        elif self.room_type == 'split' or self.room_type == 'main' and self.current_room not in self.completed_rooms:
            minions = ['Lost Crusade', 'Grotto Slime', 'Henchmen of Malu', 'Tormented Golem', 'Spectral Sentry']
            minion = r.choice(minions)
            enemy = Minions(minion)
            enemy.get_skill(player, self)
            if player.get_combat_skill() >= enemy.get_skill(player, self):
                enemy.fight_me(player, self)
                # Equipment.create_item(player.get_skill(self), player)
                return False
            else:
                enemy.not_ready()
                return True
        # The market for now is just a free room, if the player has not had an excessive amount of fatigue, they will recieve
        # a free bonus item
        elif self.room_type == 'market' and self.current_room not in self.completed_rooms:
            if player.fatigue <= 10:
                Equipment.create_item(player.get_skill(self), player)
                # will add lore in the future
                print("Not sure what to do with this yet...")
        # the marble defender is the 2nd boss that the user *should* fight, though it can be the first
        elif self.room_type == 'defender' and self.current_room not in self.completed_rooms:
            # using the class method fight_me from the marble defender to initate battle
            dead = Marble_Defender.fight_me(player, self)

            if 'Cultist of Malus' in Enemies.defeated_enemies and dead == False:
                print("From the crumbled remains of the Marble Defender, a small portal appears, and from within you")
                print("the strange gas from the Cultist flows out and gets absorbed into the portal, causing it to")
                print("grow...strangely just large enough for you to comfortably step inside...and stupidly...you do")
                win = Void.fight_me(player, self)
                if win == True:
                    self.completed(player)
                # returning true since the game is over and we want to close out of the main loop
                return True
            # as per the lore, the cultist had trapped the void but since you killed it and released it...you loose
            elif dead == False:
                print("From the crumbled remains of the Marble Defender, a small portal appears...")
                print("Out from within comes a purple ooze...when it stops the puddle on the floor coalesces into an entity")
                print("It takes a quick look at you and lurches forward, consuming you within an instant")
                print("You have just freed the Entity from the Void it was trapped within...Thus dooming the world")
                print(f"You have died at level {player.get_skill(self)} to the Void Entity")
                return True
        # if we get to the treasure room
        elif self.room_type == 'treasure' and self.current_room not in self.completed_rooms:
            # we need to check that it can be unlocked with 3 keys
            if player.keys >= 3:
                # calling the Cultist classmethod to initate the fight
                player_defeated = Cultist_of_Malus.fight_me(player, self)
                # if you win;
                if player_defeated == False:
                    print("From the robes of the Cultist, a strange purple vial falls out and cracks on the floor")
                    print("The vial shatters and a purple gas slowly rises up and as if with sentience,")
                    print("the gas flows towards you. Stupified, you stand there unable to move as it embraces you.")
                    print("It seems to get absorbed into your skin, and assuming there is nothing you can do about it")
                    print("You continue onwards...")
                    return False
                # if you loose the fight;
                else:
                    return True
            # if you cannot unlock the treasure room;
            else:
                Cultist_of_Malus.not_ready()
                return False

# A pretty empty Enemies class, using it for creating a centralized __repr__ so we dont have to make one for each enemy
class Enemies():
    # a list of defeated enemies, used now for checking if the cultists are dead
    # in the future it will be checked for a skill buff
    defeated_enemies = []
    # repr method for a enemy banner - to show what you are fighting against
    def __repr__(self):
        enemy_string = '|{left:^10}|{right:^30}|'
        print('_'*43)
        print(enemy_string.format(left = self.type, right = f'{self.name}'))
        print(enemy_string.format(left = 'Skill', right = f'{self.skill}'))
        print(enemy_string.format(left = 'Health', right = f'{self.health}'))
        print(enemy_string.format(left = 'Defense', right = f'{self.defense}'))
        return('-'*43)
    
# class for the cultists, inheriting from Enemies so we can utilize the __repr__ method
class Cultist_of_Malus(Enemies):
    def __init__(self):
        self.type = 'Boss'
        self.name = 'Cultists of Malus'
        self.skill = 35
        self.health = self.skill *7
        self.defense = self.skill *3
    
    # class method printing the dialogue if the player cant unlock the gates
    @classmethod
    def not_ready(self):
        print("On the floor lays a trap door, with large locks glowing with a faint purple energy.")
        print("With rightful caution, you choose to not touch them.")
    
    # class method for fighting the cultists
    @classmethod
    def fight_me(self, player, board):
        print(repr(self()))
        print(f"{color.RED}Azamoth, we require the assistance of another warrior so that we may bring glory to you!{color.END}")
        s(1)
        print(f"{color.RED}We shall not let these gifts be in vain!{color.END}")
        s(1)
        print(f"{color.RED}This power…it is overwhelming! IT PULSES THROUGH ME!{color.END}")
        s(1)
        if player.get_combat_skill() > self.skill:
            print(f"""{color.RED}{color.BOLD}Even if you are victorious...
            that…that THING still crawls in the halls! You make an irredeemable mistake by defeating the only people keeping it suppressed!{color.END}""")
            # a slightly OP item for beating one of the main bosses
            Equipment.create_item(player.get_skill(board) + 5, player)
            Enemies.defeated_enemies.append(self.name)
            return False
        else:
            print(f"{color.RED}Ha...hahah...You never stood a chance...{color.END}")
            print(f"You have died at level {player.get_skill(board)} to the Cultist of Malus")
            return True

# same stuff as the cultist class
class Marble_Defender(Enemies):
    def __init__(self):
        self.type = 'Boss'
        self.name = 'Marble Defender'
        self.skill = 55
        self.health = self.skill * 7
        self.defense = self.skill * 3
    
    # same sort of fighting class method
    @classmethod
    def fight_me(self, player, board):
        print(repr(self()))
        print(f"{color.BOLD}You know not what awaits behind this wall. Please, turn back before you regret your actions.{color.END}")
        s(1)
        print(f"{color.BOLD}I wish to only protect you. Forgive me, but I have no other choice.{color.END}")
        s(1)
        print(f"{color.BOLD}Hero...Your confidence is gravely misplaced...{color.END}")
        s(1)
        print(f"{color.BOLD}Do not allow this evil to escape...{color.END}")
        s(1)        
        if player.get_combat_skill() >= self.skill:
            print(f"{color.BOLD}I can protect your world no longer...the fate of the world is now in your hands...{color.END}")
            Equipment.create_item(player.get_skill(board)+1, player)
            Enemies.defeated_enemies.append(self.name)
            return False
        else:
            print(f"My condolences, young hero...but for the sake of the world, you could not be allowed to proceed")
            s(1)
            print(f"You have died at level {player.get_skill(board)} to the marble defender...")
            return True

# same sort of class for the Void entity
class Void(Enemies):
    def __init__(self):
        self.type = 'Boss'
        self.name = 'Void Entity'
        self.skill = 75
        self.health = self.skill * 7
        self.defense = self.skill * 3
    
    # classmethod for fighting the void
    @classmethod
    def fight_me(self, player, board):
        print(repr(self()))
        print("You enter into a large room, resembling sort of a battle arena.")
        print("You hear a deep voice from all around you, as if the air itself was speaking")
        print(f"{color.UNDERLINE}{color.BOLD}{color.PURPLE}Those who enter my realm hold little value for their lives.{color.END}")
        s(3)
        print("From the far end opposite to you, a being made purely of some purple liquid rises from the floor")
        print(f"{color.UNDERLINE}{color.BOLD}{color.PURPLE}Ah, heroes, blessed souls…I shall destroy you with the power of shadow!{color.END}")
        s(3)
        print("There is a slight rumble from the edges of the arena.")
        print(f"{color.UNDERLINE}{color.BOLD}{color.PURPLE}My army will put an end to your meaningless lives.{color.END}")
        print("From all around you, versions of the same purple monster, in varying sizes, climb out of the floor")
        print("You ready your staff, and mutter a small prayer to your village gods")
        print("You leap into action, slowly but surely obliterating the minions of the Void.")
        s(4)
        print(f"{color.UNDERLINE}{color.BOLD}{color.PURPLE}The anguish you feel is the wrath of your own creation!{color.END}")
        print("From the center of the room, a small pool of purple ooze boils into existence, and it spreads to the walls, cutting the room in two.")
        print(f"{color.UNDERLINE}{color.BOLD}{color.PURPLE}Yes, become one with the void!{color.END}")
        print("With a wave of its arms, another army steps out of the pool in the center...")
        s(5)
        print(f"{color.UNDERLINE}{color.BOLD}{color.PURPLE}I have fed off the sorrow and hatred of the lost souls… AND I WILL FEED AGAIN!{color.END}")
        if player.get_combat_skill() >= self.skill:
            print(f"{color.UNDERLINE}{color.BOLD}{color.PURPLE}A fallen King, an imprisoned Queen, an Effigy of Gold.{color.END}")
            s(1)
            print(f"{color.UNDERLINE}{color.BOLD}{color.PURPLE}A glacial elder who knows more than you think, and a necromancer of old.{color.END}")
            s(1)
            print("You grow tired of the Void's boasting, and prep yourself to cast the strongest attack you have ever done")
            s(1)
            print(f"{color.UNDERLINE}{color.BOLD}{color.PURPLE}An experiment that surpassed its master, a ventroliquist’s final show.{color.END}")
            s(1)
            print(f"{color.UNDERLINE}{color.BOLD}{color.PURPLE}And a white titan to conquer the Mad God…{color.END}")
            s(1)
            print("When you notice the entity's gaze leave you for a moment, you fire it...")
            s(1)
            print(f"{color.UNDERLINE}{color.BOLD}{color.PURPLE}ALL UNDER MY CONTROL!{color.END}")
            s(1)
            print("A large bolt of energy fires off from your staff, with such force that you feel it break...")
            print("Faster than even the entity can react, your attack hits it percisely")
            s(1)
            print("Smoke, dust, and magicial residue pollute the air not allowing you to see the outcome of your assault")
            s(3)
            print("Broken...tattered...and bleeding, the entity emerges from the shadow...")
            print("You are shocked, nothing could have survived that hit...")
            print(f"{color.PURPLE}No…NO! THIS IS NOT THE END!{color.END}")
            print("The entity limps forward slightly, it goes to raise one of its arms however the arm simply falls off")
            s(1)
            print("You sigh, feeling more assured as you gaze at the broken remnants of the entity")
            print(f"{color.PURPLE}You fools..you can never truly defeat me! I am in all of you! I AM all of you!{color.END}")
            print(f"{color.PURPLE}I am the embodiment of your own sin! To destroy me would be to destroy yourselves!{color.END}")
            print("You ready another attack, calling forth much less energy this time, and fire it at the entity")
            s(2)
            print("The energy flies straight through leaving a massive hole in its body...")
            print("The entity slowly melts into a purple goo, leaving behind just a puddle where before stood a being of pure evil")
            print("As the puddle boils away, there is a small item in its place")
            print("You cautiously walk towards it and when you finally identify the item, you gasp...")
            s(2)
            print("It is the Lost Crown, the symbol of peace from an ancient time.")
            print("A symbol of a unified kingdom, under reign of the Forgotten King")
            print("Having been lost for so long, its glory had been forgotten and replaced with a false trinket")
            print("You take the crown and wipe the remaining ooze off on your robes, and store it in your inventory")
            print("There could have been not a more perfect artifact to recover to prove your successful adventure into the \n Forgotten Labrynth...")
            return True
        else:
            print("""
A fallen king, an imprisoned queen, an effigy of gold.
A glacial elder who knows more than you think, and a necromancer of old.
An experiment that surpassed its master, a ventroliquist’s final show.
And a white titan to conquer the Mad God…

ALL UNDER MY CONTROL!
""")
            print("The Void Entity erupts from the center of the room and summons a massive bow to his hands")
            print(f"{color.UNDERLINE}{color.BOLD}{color.PURPLE}ALL NOW ENDS!{color.END}")
            print("It readies a massive arrow, and you feel only dread. You regret all of your choices to this point")
            print("The arrow fires, and tears you right in two...")
            print("The entity snorts, annoyed at having wasted time to present itself to you")
            print(f"You have died at level {player.get_skill(board)} to the void entity...")
            return False

# a general minions class, we pass in the name in the main/split room checks
class Minions(Enemies):
    def __init__(self, name):
        self.type = 'Minions'
        self.name = name
        self.skill = 0
        self.health = self.skill * 7
        self.defense = self.skill * 3
    
    # we vary the difficulty based on the players progress
    # if their fatigue is too high, and their item rolls were unlucky, they will die
    # otherwise theyre supposed to be easy
    # needs a balance patch because theyre too hard currently
    def get_skill(self, player, board):
        skill_diff = r.randint(-2, 2)
        self.skill = player.get_skill(board) + skill_diff
        return self.skill
    
    # if the player has a lower skill than the enemies, they die, this is the print sequence for it
    def not_ready(self):
#         print(repr(self()))
        print(f"As you step into the room, the heads of a dozen {self.name} turns to face you.")
        print("With a look of fierce malice, their eyes lock onto yours, you sense no mercy in them.")
        print("As if answering to a war cry, they all rush at you.")
        print("Your legs get caught in the dusty bones of a creature and you trip...")
        print("As you die, your last words were 'AHHHHHHHHHHHH', so valiant...A hero to remember.")
    
    # if they can win, this will be the print sequence
    def fight_me(self, player, board):
#         print(repr(self()))
        print(f"You walk into a room full {self.name}s")
        print("With a determined look, you ready your staff, bellow with bravery and charge at the opposition")
        print("In no time, you have decimated the lot of them, and from the center of the room decends an object\nwrapped in a silk cloth")
        Equipment.create_item(player.get_skill(board), player)
        if self.name not in Enemies.defeated_enemies:
            Enemies.defeated_enemies.append(self.name)
        

# Class for our player 
class Player():
    def __init__(self):
        self.inventory = []
        self.skill = 0
        self.fatigue = 0
        self.keys = 0
        self.combat_skill = 0
        self.name = ''
    
    # picking items up from the floor into their inventory
    # since we have a max cap for inventory, we also drop items here
    # recursion to see if the player wants to repick up any of the dropped items
    # player input will break out of the recursion
    def pick_item_up(self, item):
        if len(self.inventory) >= 8:
            print("Your inventory is full, this item cannot be picked up.")
            choice_drop = False
            while not choice_drop:
                choice = input("Would you like to drop an item? (y/n)\n").lower()
                if choice == 'y' or choice == 'n':
                    choice_drop = True
                else:
                    print("Please select Y or N to drop an item.")
            if choice == 'y':
                d = self.drop_item()
                if d:
                    for _ in Equipment.on_floor:
                        self.pick_item_up(_)
        else:
            item.in_inventory = True
            self.inventory.append(item)
            Equipment.on_floor.remove(item)
            print(f"{item.type} of {item.name} has been added to your inventory!")
            self.show_inventory()
    
    # a DIY __repr__ method, 
    def show_inventory(self):
        if self.inventory:
            inventory_string = '|{left:^ 5}-{right:^30}-{last:^5}|'
            print('|', "-"*40, '|')
            for _ in range(len(self.inventory)):
                print(inventory_string.format(left = _+1, right = f"{self.inventory[_].type} of {self.inventory[_].name}", last = f'T{self.inventory[_].tier}'))
            print('|', "-"*40, '|')
        else:
            print("There are no items in your inventory")
    
    # method for dropping items, we only call it internally from the pick_up_item method
    def drop_item(self):
        print(f"Please select an item number from your inventory to drop:")
        self.show_inventory()
        if len(self.inventory) <=0:
            print("You have no items to drop")
            return False
        item_selected = False
        while not item_selected:
            n = input("What item would you like to drop?")
            if n.isnumeric():
                if int(n) <= len(self.inventory) and int(n) > 0:
                    item_selected = True
                else:
                    print("You have selected an item that you do not have")
            else:
                print("Please enter the number for the item slow you would like to drop!")
        n = int(n) - 1
        self.inventory[n].in_inventory = False
        Equipment.on_floor.append(self.inventory[n])
        print(f"{self.inventory[n].type} of {self.inventory[n].name} has been dropped!")
        self.inventory.pop(n)
        return True
    
    # method for skill checking
    def get_skill(self, board):
        self.skill = len(board.completed_rooms) *4 - self.fatigue + 2
#         if every enemy is defeated, skill + 3
#         if completed rooms too high, skill - 5
        return self.skill
    
    # method for combat skill checking
    def get_combat_skill(self):
        x = 0
        for item in self.inventory:
            x += item.tier
        self.combat_skill = x
        return self.combat_skill
    
    # method to get initial items when creating a player object
    def set_up_player(self):
        # the difficulty mechanics are not yet balanced, so for testing purposes (moving around, interacting with enemies) one of the items is set to tier 300
        # this makes it to so you dont die, and essentially is godmode cheat. Will be fixed for future play, but for the scope of the project it is OK.
        self.inventory = [Staff(1), Spell(300), Robe(1), Ring(3)]
        name = input("What is your name?\n").lower()
        self.name = name

# base class for Equipment, similar to Enemy for enemies, just contains a repr and a singular method for creating items
class Equipment():
    # items drop to this list, and are picked up from here
    on_floor = []

    # ez repr
    def __repr__(self):
        item_string = '*{left:^17}|{right:^20}*'
        name_string = '*{name:^38}*'
        print("#"*40)
        print(name_string.format(name = f'{self.type} of {self.name}'))
        print(item_string.format(left = self.effect, right = f'+ {self.tier}'))
        return "#"*40
    
    # method for creating items. uses the players skill, we also pick up an item from here using the method in the Player class
    @classmethod
    def create_item(self, skill, player):
        potential_drops = [Ring(skill), Staff(skill), Spell(skill), Robe(skill)]
        drop = r.choice(potential_drops)
        self.on_floor.append(drop)
        print("An item has dropped on the floor!")
        print(repr(drop))
        pickup_choice = False
        while not pickup_choice:
            choice = input("Would you like to pick this item up? (y/n)\n").lower()
            if choice == 'y' or choice == 'n':
                pickup_choice = True
        if choice == 'y':
            player.pick_item_up(drop)
        
# creating a random staff type equipment. Select a random name, and scale the tier of the item based on the players progression
class Staff(Equipment):
    staffs = ['Cosmic Whole', 'Vital Unity', 'Extreme Prejudice', 'Unholy Sacrafice', 'the Blasphemous Prayer']
    def __init__(self, skill):
        self.name = r.choice(self.staffs)
        self.tier = r.randint(0, skill) if skill <=5 else r.randint(skill - 3, skill+1)
        self.type = "Staff"
        self.effect = 'Damage'
        self.equipped = False
        self.in_inventory = False

# creating a random robe type equipment. Select a random name, and scale the tier of the item based on the players progression
class Robe(Equipment):
    Robes = ['The Holy Light', 'The Mad Scientist', 'The Ancient Intellect', 'The Grand Sorcerer', 'The Star Mother', 'The Neophyte']
    def __init__(self, skill):
        self.name = r.choice(self.Robes)
        self.tier = r.randint(0, skill) if skill <=5 else r.randint(skill - 3, skill+1)
        self.type = "Robe"
        self.effect = 'Defense'
        self.equipped = False
        self.in_inventory = False

# creating a random spell type equipment. Select a random name, and scale the tier of the item based on the players progression
class Spell(Equipment):
    Spells = ['Recurring Terror', 'Genesis', 'A Thousand Suns', 'Burning Retribution', 'Ancient Destruction', 'The Cursed Spire']
    def __init__(self, skill):
        self.name = r.choice(self.Spells)
        self.tier = r.randint(0, skill) if skill <=5 else r.randint(skill - 3, skill+1)
        self.type = "Spell"
        self.effect = 'Mana'
        self.equipped = False
        self.in_inventory = False

# creating a random ring type equipment. Select a random name, and scale the tier of the item based on the players progression        
class Ring(Equipment):
    Rings = ['Divine Faith', 'Omnipotence', 'The Covetous Heart', 'Pure Wishes', 'The Inferno', 'The Divine Coronation']
    def __init__(self, skill):
        self.name = r.choice(self.Rings)
        self.tier = r.randint(0, skill) if skill <=5 else r.randint(skill - 3, skill+1)
        self.type = "Ring"
        self.effect = 'Strength'
        self.equipped = False
        self.in_inventory = False

# creating an intro class
class Intro():
    # fetching the global intro variable 
    global intro
    
    # just a method using the sleep library to slowly print text
    @classmethod
    def slow_print(self, string, time):
        for _ in range(len(string)):
            print(string[_], end = '')
            s(time)
        print("")
    
    # method that validates wether the player wants to start playing the game or not
    @classmethod
    def show_intro(self):
        self.slow_print("Welcome to Lost Hope...", .05)
        s(1)
        self.slow_print("A text based adventure game!", .05)
        s(1)
        starting = False
        while not starting:
            start = input("Are you ready to start? (yes/no)\n").lower()
            if start == 'no' or start == 'n':
                print("Thank you for coming! Hope you get a chance to play sometime soon.")
                return False
            else:
                print(intro)
                s(2)
                input('Press ENTER to continue')
                return True

# this is our main class, here we run everything above and create instances of nescessary classes to ensure everything runs smothly
# we put it on a loop to let the user keep playing until they win/quit/ or loose
class Play:
    def game():
        rmap = map_1 #When there are multiple maps, we will randomly choose a map here
        board = Board(map_1)
        player = Player()
        player.set_up_player()
        Equipment.on_floor.clear()
        intro_done = Intro.show_intro()
        if intro_done == False:
            return "Bye"
        quit_or_dead = False
        while not quit_or_dead:
            # I cannot find a good place to place this clear output yet...i end up either flooding the chat or removing important bits :(
            # sys('clear')
            print(repr(board))
            quit_or_dead = board.movement(player)
            if quit_or_dead == True:
                continue
            quit_or_dead = board.generate_room(player)
        print(f"Thank you for playing {color.UNDERLINE}Lost Hope{color.END} a text based adventure game,")
        print("By Nisarg Patel")

# calling the game method to bring it all together!
Play.game()