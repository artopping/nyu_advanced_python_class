# text based game assignment
# want to make game that explores NYC
# modified from http://inventwithpython.com/blog/2014/12/11/making-a-text-adventure-game-with-the-cmd-and-textwrap-python-modules/
# modified to simplify the experiences and add a time function

import cmd, sys, textwrap

#GLOBALS FOR GAME 

DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
UP = 'up'
DOWN = 'down'
GROUND = 'ground'
SHOP = 'shop'
GROUNDDESC = 'grounddesc'
SHORTDESC = 'shortdesc'
LONGDESC = 'longdesc'
TAKEABLE = 'takeable'
EDIBLE = 'edible'
DESCWORDS = 'descwords'
TIME= 'time'

SCREEN_WIDTH = 80

# put locations and items in data structures that can easily be called by functions

neighborhoods = {
    'Times Square': {
        DESC: 'Times Square is the center of the universe! Or at least this game. Enjoy the lights but try not to spend much time here.',
        NORTH: 'Upper West Side',
        SOUTH: 'Chelsea/West Village',
        GROUND: ['All of the lights', 'Picture with Elmo']},
    'Chelsea/West Village': {
        DESC: 'This is my fav area. Stroll the streets and taste the food.',
        NORTH: 'Times Square',
        EAST: 'East Village',
        GROUND: ['Los Tacos No 1', 'Gifts from Chelsea Market']},
    'Upper West Side': {
        DESC: 'There is lots of hidden amazing food here and Central Park is closeby.',
        EAST: 'Central Park',
        SOUTH: 'Times Square',
        GROUND: ['Levain Cookies', 'Slice from Freddy and Peppers']},
    'Central Park': {
        DESC: 'Truly an amazing experience not far from the hustle and bustle of the city. Get lost on the trails and enjoy a pretzel.',
        WEST: 'Upper West Side',
        GROUND: ['Pretzel', 'MET ticket']},
    'East Village': {
        DESC: 'Funky fun place with lots of cute shops and lovely treats.',
        WEST: 'Chelsea/West Village',
        GROUND: ['PTD cocktails', 'tattoos']}
}

NYCitems= {
    'Welcome Sign': {
        GROUNDDESC: 'A welcome to NYC sign stands here.',
        SHORTDESC: 'a welcome to NYC sign',
        LONGDESC: '"The welcome sign reads, "Welcome to NYC!! Lets explore. You can type "help" for a list of commands to use."',
        TAKEABLE: False,
        DESCWORDS: ['welcome', 'a sign'], 
        TIME: 0},
    'Picture with Elmo': {
        GROUNDDESC: 'Take a pic with  Elmo (type: get a pic)',
        SHORTDESC: 'pic with Elmo ',
        LONGDESC: '"There are a ton of characters around, find Elmo and take a cute pic : ) "',
        TAKEABLE: True,
        DESCWORDS: ['elmo', 'a pic'], 
        TIME: .25},
    'All of the lights': {
        GROUNDDESC: 'In Times Square its daylight all day! (type: get a view)',
        SHORTDESC: 'take in all the lights',
        LONGDESC: 'There is nothing like Times Square. Take in all of the lights around you.',
        TAKEABLE: False,
        DESCWORDS: ['the lights', 'a view'], 
        TIME: 0.25},
    'Los Tacos No 1': {
        GROUNDDESC: 'MMM I feel like tacos (type: get tacos)',
        SHORTDESC: 'tacos',
        LONGDESC: 'These are the best tacos in town!"',
        TAKEABLE: False,
        EDIBLE: True,
        DESCWORDS: ['tacos', 'lunch'], 
        TIME: 1},
    'Gifts from Chelsea Market': {
        GROUNDDESC: 'Lets get some gifts (type: get gifts)',
        SHORTDESC: 'quirky gifts',
        LONGDESC: '"These are the best tacos in town!"',
        TAKEABLE: True,
        EDIBLE: False,
        DESCWORDS: ['gifts'], 
        TIME: 1.5},
    'Levain Cookies': {
        GROUNDDESC: 'The best cookies in NYC (type: get cookies)',
        SHORTDESC: 'cookies',
        LONGDESC: '"These cookies will change your life. They are the best in NYC, maybe the world."',
        TAKEABLE: False,
        EDIBLE: True,
        DESCWORDS: ['cookies', 'a snack'], 
        TIME: 2},
    'Slice from Freddy and Peppers': {
        GROUNDDESC: 'Pizza (type: get pizza)',
        SHORTDESC: 'pizza',
        LONGDESC: '"Easy pizza with that unique NYC crust you keep hearing about."',
        TAKEABLE: False,
        EDIBLE: True,
        DESCWORDS: ['pizza', 'a snack'], 
        TIME: 0.5},
    'Pretzel': {
        GROUNDDESC: 'Pretzel (type: get a pretzel)',
        SHORTDESC: 'Pretzel',
        LONGDESC: '"Classic NYC Pretzel"',
        TAKEABLE: False,
        EDIBLE: True,
        DESCWORDS: ['a pretzel', 'a snack'], 
        TIME: 0.25},
    'MET ticket': {
        GROUNDDESC: 'Ticket to the MET Museum (type: get cultured)',
        SHORTDESC: 'Museum ticket',
        LONGDESC: '"This ticket gets you into one of the most amazing museums in the world!"',
        TAKEABLE: True,
        DESCWORDS: ['cultured', 'a ticket'], 
        TIME: 3},
    'PTD cocktails': {
        GROUNDDESC: 'Lets grab a drink (type: get tipsy)',
        SHORTDESC: 'drinks',
        LONGDESC: '"A unique speakeasy with great cocktails"',
        TAKEABLE: False,
        DESCWORDS: ['tipsy', 'a drink'], 
        TIME: 3},
    'tattoos': {
        GROUNDDESC: 'Do something crazy (type: get a tattoo)',
        SHORTDESC: 'tattoo',
        LONGDESC: '"There are a tone of tattoo shops around, get something to remember NYC by"',
        TAKEABLE: True,
        DESCWORDS: ['a tattoo'], 
        TIME: 3},
}
#game starts here 
location = 'Times Square' # start in town square
experiences = [] # start with blank inventory
menu = []
showFullExits = True
time= 12

def displayLocation(loc):
    """A helper function for displaying an area's description and exits."""
    # Print the room name.
    print(loc)
    print('=' * len(loc))

    # Print the room's description (using textwrap.wrap())
    print('\n'.join(textwrap.wrap(neighborhoods[loc][DESC], SCREEN_WIDTH)))

    # Print all the items on the ground.
    if len(neighborhoods[loc][GROUND]) > 0:
        #print()
        for item in neighborhoods[loc][GROUND]:
            print(NYCitems[item][GROUNDDESC])

    # Print all the exits.
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
        if direction in neighborhoods[loc].keys():
            exits.append(direction.title())
    #print()
    if showFullExits:
        for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
            if direction in neighborhoods[location]:
                print('%s: %s' % (direction.title(), neighborhoods[location][direction]))
    else:
        print('Exits: %s' % ' '.join(exits))

def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global location

    if direction in neighborhoods[location]:
        print('You moved to the %s.' % direction)
        location = neighborhoods[location][direction]
        displayLocation(location)
    else:
        print('You cannot move in that direction')

# item helper functions

def getAllDescWords(itemList):
    """Returns a list of "description words" for each item named in itemList."""
    itemList = list(set(itemList)) # make itemList unique
    descWords = []
    for item in itemList:
        descWords.extend(NYCitems[item][DESCWORDS])
    return list(set(descWords))

def getAllFirstDescWords(itemList):
    """Returns a list of the first "description word" in the list of
    description words for each item named in itemList."""
    itemList = list(set(itemList)) # make itemList unique
    descWords = []
    for item in itemList:
        descWords.append(NYCitems[item][DESCWORDS][0])
    return list(set(descWords))

def getFirstItemMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    for item in itemList:
        if desc in NYCitems[item][DESCWORDS]:
            return item
    return None

def getAllItemsMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    matchingItems = []
    for item in itemList:
        if desc in NYCitems[item][DESCWORDS]:
            matchingItems.append(item)
    return matchingItems


class TextAdventureCmd(cmd.Cmd):
    prompt = '\n> '

    # The default() method is called when none of the other do_*() command methods match.
    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    # A very simple "quit" command to terminate the program:
    def do_quit(self, arg):
        """Quit the game."""
        return True # this exits the Cmd application loop in TextAdventureCmd.cmdloop()

    #def help_combat(self):
    #    print('Combat is not implemented in this program.')

    def do_north(self, arg):
        """Go to the area to the north, if possible."""
        moveDirection('north')

    def do_south(self, arg):
        """Go to the area to the south, if possible."""
        moveDirection('south')

    def do_east(self, arg):
        """Go to the area to the east, if possible."""
        moveDirection('east')

    def do_west(self, arg):
        """Go to the area to the west, if possible."""
        moveDirection('west')

    def do_up(self, arg):
        """Go to the area upwards, if possible."""
        moveDirection('up')

    def do_down(self, arg):
        """Go to the area downwards, if possible."""
        moveDirection('down')

    # Since the code is the exact same, we can just copy the
    # methods with shortened names:
    do_n = do_north
    do_s = do_south
    do_e = do_east
    do_w = do_west
    do_u = do_up
    do_d = do_down
    do_q = do_quit

    def do_exits(self, arg):
        """Toggle showing full exit descriptions or brief exit descriptions."""
        global showFullExits
        showFullExits = not showFullExits
        if showFullExits:
            print('Showing full exit descriptions.')
        else:
            print('Showing brief exit descriptions.')

    def do_get(self, arg):
        """"get <item>" - eat an item in your inventory."""
        while time >0:
            itemToEat = arg.lower()
            global time
            if itemToEat == '':
                print('What would you like to do? Your options are: {0}'.format((neighborhoods[location][GROUND])))
                return
            cantEat= False

            for item  in getAllItemsMatchingDesc(itemToEat, neighborhoods[location][GROUND]):
                if NYCitems[item].get(EDIBLE, True)== False:
                    cantEat= True
                    continue
                print('You bought {0}'.format((NYCitems[item][SHORTDESC])))
                menu.append(item)
                print ('You spent {0} hour doing that'.format(NYCitems[item][TIME]))
                time= time - (NYCitems[item][TIME])
                print ('You now have {0} hours left to explore NYC!').format(time)
                return
            else:
                itemToBuy = arg.lower()
                for item in getAllItemsMatchingDesc(itemToBuy, neighborhoods[location][GROUND]):
                    if NYCitems[item].get(TAKEABLE, False)== False:
                        cantBuy= False
                        continue
                    print('You got {0}'.format ((NYCitems[item][SHORTDESC])))
                    experiences.append(item)
                    print ('You spent {0} hour doing that'.format(NYCitems[item][TIME]))
                    time= time - (NYCitems[item][TIME])
                    print ('You now have {0} hours left to explore NYC!').format(time)
                    return 
                return
            print('{0} is not an option'.format(arg))
            return
        print ('You have run out of time! Bye!')
        return quit
    do_get= do_get

    def do_experiences(self, arg):
        """Display a list of the things you've done in NYC"""

        if len(experiences) == 0:
            print('Inventory:\n  (nothing)')
            return

        # first get a count of each distinct item in the inventory
        itemCount = {}
        for item in experiences:
            if item in itemCount.keys():
                itemCount[item] += 1
            else:
                itemCount[item] = 1

        # get a list of inventory items with duplicates removed:
        print('Experiences:')
        for item in set(experiences):
            if itemCount[item] > 1:
                print('  %s (%s)' % (item, itemCount[item]))
            else:
                print('  ' + item)

    do_exp = do_experiences

    def do_menu(self, arg):
        """Display a list of the items in your possession."""

        if len(menu) == 0:
            print('Menu:\n  (nothing)')
            return

        # first get a count of each distinct item in the menu
        MenuCount = {}
        for item in menu:
            if item in MenuCount.keys():
                MenuCount[item] += 1
            else:
                MenuCount[item] = 1

        # get a list of menu items with duplicates removed:
        print('Menu:')
        for item in set(menu):
            if MenuCount[item] > 1:
                print('  %s (%s)' % (item, MenuCount[item]))
            else:
                print('  ' + item)

    do_menu = do_menu

if __name__ == '__main__':
    print('Get ready to explore NYC!!')
    print('====================')
    print()
    print('(Type "help" for commands.)')
    print()
    displayLocation(location)
    TextAdventureCmd().cmdloop()
    print('You have experienced the best of NYC!! Thanks for visiting!')