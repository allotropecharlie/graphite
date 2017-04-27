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
        #these are the things a room has by default.
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
        if r is not None:
            print("adding last room", r, "at", len(self.roomlist))
            rm = Room(r, exits, desc, items, locks)
            self.roomlist[r] = rm
        f.close()

    def run(self):
        os.system('cls')
        while True:
            print("room:", self.room)
            print("You are in", self.roomlist[self.room].desc)
            print("items here:", self.roomlist[self.room].items)
            print("you are carrying:", self.inventory)
            if self.roomlist[self.room].locks is not None:
                print("the locked doors are:", self.roomlist[self.room].locks)
            print("You can go", self.roomlist[self.room].exits)
            i = input(">").lower()
            cancel = 0
            if (i == 'unlock' or i == 'use key' or i == 'u') and 'key' in self.inventory:
                print('The door unlocks with a resounding clunk.')
                self.inventory.remove('key')
                self.roomlist[self.room].locks = []
            elif (i == 'unlock' or i == 'use key' or i == 'u'):
                print('There is no key in your inventory or there are no exits with locks in this room.')
                cancel = 1
            r = None
            if i == "t" or i == 'take':
                self.inventory.extend(self.roomlist[self.room].items)
                self.roomlist[self.room].items = []
            elif i in ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west']:
                dirname = i[0]
                if dirname in self.roomlist[self.room].exits:
                    if dirname in self.roomlist[self.room].locks:
                        print('That door is locked. Type U to unlock the door if you have a key.')
                    else:
                        r = self.roomlist[self.room].exits[dirname]
                else:
                    print('Invalid exit. Retry your command.')

            elif cancel == 0:
                print("That is invalid. Retype your command.")
                continue

            if r is not None:
                self.room = (r)

#This just makes calling "rt" equal to calling "Runtime()".
rt = Runtime()
#This runs the runtime code.
rt.run()
