import os

def readfile(self, filename):
        #This makes it easier to read the things from the files.
        f = open(filename)
        #these are the things a room has by default. It also sets the variable r = to studentName which = None.
        r = studentName = None
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
                1) the "if key == 'studentName, items, etc.'" section makes the code determine what the key is.
                2) if there exists a "if ',' in value" the section in the levels/database file means that
                 it is possible for there to be multiple values for that piece of data. However, there do
                  not have to be multiple values.
                3)the "values = value.split makes an array that has the multiple pieces of data, allowing
                 things like multiple lock support, multiple door support, and multiple item support.
            '''
                if key == 'studentName':
                    studentName = value
                if key == 'studentNum':
                    studentNum = value
                if key == '':
                    locks = value
        f.close()