import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP
import random
from random import randint, sample
import time
import optparse

def generate_row_obstacles(W, seed=[0], n=5): 
    """ 
    @param W: screen width
    @param seed: list of random seed
    @return: a new row of 5 random generated obstacles
    """
    random.seed(seed[0])
    seed[0] += 1
    ylist = random.sample(range(1, W - 1), n)
    row_obstacles = []
    
    for y in ylist: 
        
        row_obstacles.append(y)
    return row_obstacles

def next_frame(obstacles, W, seed=[0], n=5): 
    """
    @param obstacles: list of obstacles
    @param W: screen width 
    @param seed: list of random seed
    @return: obstacles with a new row of random generated obstacles
    """
    row = generate_row_obstacles(W, seed, n)

    obstacles = [row] + obstacles[:-1]

    return obstacles

def clear_screen(obstacles):
    """ clear screen obstacles
    @param obstacles: list of obstacles
    @return
    """
    for i in range(len(obstacles)): 

        for j in range(len(obstacles[i])): 

            window.addch(i + 1, obstacles[i][j], ' ')

def redraw_screen(obstacles): 
    """ redraw screen obstacles
    @param obstacles: list of obstacles
    @return
    """
    for i in range(len(obstacles)): 

        for j in range(len(obstacles[i])): 

            window.addch(i + 1, obstacles[i][j], '_')

parser = optparse.OptionParser()
parser.add_option('-l', action="store", type="float", default="2")
parser.add_option('-s', action="store", type="choice", choices=["small", "medium", "large"], default="small")
options, args = parser.parse_args()

Height, Width = 10, 40
# game level: the higher, the more difficult
level = options.l
if level < 1e-6: 

    print('please be nice: input larger value, game over')
    exit()

if options.s == 'medium':

    Height = int(Height * 1.5)
    Width = int(Width * 1.5)
elif options.s == 'large': 

    Height *= 2
    Width *= 2

obstacles = [[] for _ in range(Height - 2)]
curses.initscr() #initialize
window = curses.newwin(Height, Width, 0, 0) #create new window (Height, Width)
window.keypad(True) #enable keypad
curses.noecho() #turn off automatic echoing of keys to the screen
curses.curs_set(0)
window.nodelay(True) #makes it possible to not wait for the user input

#initiate values
key = KEY_UP
score = 0
seeds = [0]
#initialize space ship coordinates
space_ship = [Height - 2, Width // 2]
#display space ship coordinates
window.addch(space_ship[0], space_ship[1], '*')
GAME_OVER = False

while key != 27: # While they Esc key is not pressed

    window.border(0)
    #display the score and title
    window.addstr(0, 2, 'Score: ' + str(score) + ' ')
    title = ' Space Ship! '
    window.addstr(0, Width // 2 - len(title) // 2, title)

    window.timeout(0)
    event = window.getch() #event listening
    key = key if event == -1 else event 
    if GAME_OVER: 

        time.sleep(.1)
        continue
    #clear and redraw obstacles on the screen
    clear_screen(obstacles)
    obstacles = next_frame(obstacles, Width, seeds)
    redraw_screen(obstacles)
     
    if event in [KEY_LEFT, KEY_RIGHT]: 

        last = space_ship[1]
        last += (event == KEY_LEFT and -1) + (event == KEY_RIGHT and 1)
        #check if the space ship has crossed the border
        if last != 0 and last != Width - 1: 

            window.addch(space_ship[0], space_ship[1], ' ')
            space_ship[1] = last
            window.addch(space_ship[0], space_ship[1], '*')
    #check if the space ship hits the obstacle, otherwise, score ++ 
    if space_ship[1] in obstacles[-1]: 

        window.addch(space_ship[0] - 1, space_ship[1], 'x')
        window.addch(space_ship[0], space_ship[1], '*')
        GAME_OVER = True
    elif len(obstacles[-1]) != 0:

        score += 1
    time.sleep(1 / level)    
curses.endwin() #close the window and end the game
print("\nScore: " + str(score))