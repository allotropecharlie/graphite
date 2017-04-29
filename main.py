# (c) 2017 Charlie Welsh, Fourange, Clackamas Academy of Industrial Sciences.
# This program comes with absolutely NO WARRANTY.


#This imports OS calls and what kind of OS it is.
import os


#This class is the Room class
class Room(object):
    #this initialises what a room is, and what parameters it has. It defines what a room can be.
    def __init__(self, r, exits=[],
                 desc="a perfect cube of a room. It is 2 meters cubed. There seems to be no way out.",
                 items=[], locks=[]):
        self.r = r
        self.exits = exits
        self.desc = desc
        self.items = items
        self.locks = locks
    #Later in the code, the exits possible are printed. This tells that block to print "Nowhere" if you can't go
    # anywhere.
    def exits(self):
        if len(self.exits) == 0:
            return "nowhere."
        return self.exits

#This defines the runtime class, which is used at runtime.
class Runtime(object):
    #this is the section where all the parameters the game has for the player at the start of the game.
    def __init__(self):
        self.roomlist = {}
        self.room = '0'
        self.readfile('level.txt')
        self.health = 100
        self.inventory = []
    #This is the readfile mechanism. The filename argument is, well, the filename.
    def readfile(self, filename):
        #This makes it easier to read the things from the files.
        f = open(filename)
        #these are the things a room has by default. It also sets the variable r = to desc which = None.
        r = desc = None
        items = []
        locks = []
        exits = {}
        #this makes the file be read line by line.
        for line in f:
            #this defines what a line is. A line is all the characters before and after an EOL character.
            # An "Enter" if you will.
            line = line.rstrip('\n')
            #this tells the code "If you see a colon, treat that as the split between the data and the name of that
            # data."
            if ':' in line:
                key, value = line.split(':')
                #the value is what the data is, the key is the name, i,e. "StudentNum"

                '''this entire section behaves by the following rules:
                1) the "if key == 'desc, items, etc.'" section makes the code determine what the key is.
                2) if there exists a "if ',' in value" the section in the levels/database file means that
                 it is possible for there to be multiple values for that piece of data. However, there do
                  not have to be multiple values.
                3)the "values = value.split makes an array that has the multiple pieces of data, allowing
                 things like multiple lock support, multiple door support, and multiple item support.
            '''
                if key == 'desc':
                    desc = value
                if key == 'items':
                    if ',' in value:
                        values = value.split(',')
                    else:
                        values = [value]
                    items = values
                if key == 'locks':
                    if ',' in value:
                        values = value.split(',')
                    else:
                        values = [value]
                    locks = values
                if key == 'exits':
                    if ',' in value:
                        values = value.split(',')
                    else:
                        values = [value]
                    for val in values:
                        e_dir = val[0]
                        e_rm = val[2:]
                        print("room", r, "dir", e_dir, "exit is", e_rm)
                        exits[e_dir] = e_rm
                #this makes the room structure accessible by the code. It makes the room number the value at readtime.
                # It also sets the room value equal to r. This is useful later.
                if key == 'room':
                    print("adding room")
                    if r is not None:
                        print("adding previous room", r, "at", len(self.roomlist))
                        rm = Room(r, exits, desc, items, locks)
                        self.roomlist[r] = rm
                        r = desc = None
                        items = []
                        locks = []
                        exits = {}
                    r = value
        #This sets what the Runtime sees from the file as a room.
        if r is not None:
            #This prints "adding last room [room number] at [roomlist]"
            print("adding last room", r, "at", len(self.roomlist))
            #This has the variable "rm" which had been previously defined, equal to a room with the parameters from the
            # file.
            rm = Room(r, exits, desc, items, locks)
            #this sets the room in the roomlist equal to the room previously defined in "rm". It just reuses it and
            # replaces whatever was previously there.
            self.roomlist[r] = rm
        #this closes the file.
        f.close()

    #This is the run function. This is the actual game portion.
    def run(self):
        #this runs the clear screen command in a system prompt, clearing the screen for the game to look nice.
        os.system('cls')
        #while True is just a way to do an infinite loop.
        while True:
            #prints the room you are in.
            print("room:", self.room)
            #prints the description of the room description.
            print("You are in", self.roomlist[self.room].desc)
            #prints the items in the room
            print("items here:", self.roomlist[self.room].items)
            #prints the items in the player's inventory
            print("you are carrying:", self.inventory)
            #if there are no locks for that room, it displays the locked doors, and what exits you can exit into.
            if self.roomlist[self.room].locks is not None:
                print("the locked doors are:", self.roomlist[self.room].locks)
            print("You can go", self.roomlist[self.room].exits)
            #this is what the input is. Anything after the ">" is considered input, and is equal to "i".
            i = input(">").lower()
            #this is a variable that keeps track of whether or not a command is valid..
            cancel = 0
            #if the input is "unlock", "use key" or "u", while there is a key in the player's inventory, consume the key
            #  and unlock the door.
            if (i == 'unlock' or i == 'use key' or i == 'u') and 'key' in self.inventory:
                print('The door unlocks with a resounding clunk.')
                self.inventory.remove('key')
                self.roomlist[self.room].locks = []
            #this just prints what's in that print statement down there.
            elif (i == 'unlock' or i == 'use key' or i == 'u'):
                print('There is no key in your inventory or there are no exits with locks in this room.')
                cancel = 1
            r = None
            #if t, take, or take all are inputted,it removes the items from the room and adds them to the player's
            # inventory.
            if i == "t" or i == 'take' or i == 'take all':
                self.inventory.extend(self.roomlist[self.room].items)
                self.roomlist[self.room].items = []
            #if a direction is typed in the prompt, move to the room in that direction.
            elif i in ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west']:
                dirname = i[0]
                #if the door is locked, don't let the player move to that room, and report that the door is locked.
                if dirname in self.roomlist[self.room].exits:
                    if dirname in self.roomlist[self.room].locks:
                        print('That door is locked. Type U to unlock the door if you have a key.')
                    else:
                        r = self.roomlist[self.room].exits[dirname]
                #if a user types in a direction that is incorrect, it notifies the user as such.
                else:
                    print('Invalid exit. Retry your command.')
            #if an invalid command is typed, it notifies the user as such.
            elif cancel == 0:
                print("That is invalid. Retype your command.")
                continue

            if r is not None:
                self.room = (r)

#This just makes calling "rt" equal to calling "Runtime()".
rt = Runtime()
#This runs the runtime code.
rt.run()
