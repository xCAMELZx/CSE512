# puzz8_midterm.py

# STUDENT COMPLETER: Yousef Jarrar


#
# most recently modified Jan 27, 2018
# getting set up for doing graph search for :the 8-puzzle.
# data structures and functions that will enable us to solve 8-puzzles
# with graphsearch

import random
import copy

GOAL = {(1, 1): 1, (1, 2): 2, (1, 3): 3, \
        (2, 1): 8, (2, 2): 'B', (2, 3): 4, \
        (3, 1): 7, (3, 2): 6, (3, 3): 5}

easy1 = {(1, 1): 1, (1, 2): 'B', (1, 3): 3, \
         (2, 1): 8, (2, 2): 2, (2, 3): 4, \
         (3, 1): 7, (3, 2): 6, (3, 3): 5}

easy2 = {(1, 1): 1, (1, 2): 2, (1, 3): 3, \
         (2, 1): 7, (2, 2): 8, (2, 3): 4, \
         (3, 1): 6, (3, 2): 'B', (3, 3): 5}

puzzA = {(1, 1): 1, (1, 2): 'B', (1, 3): 3, \
         (2, 1): 7, (2, 2): 2, (2, 3): 4, \
         (3, 1): 6, (3, 2): 8, (3, 3): 5}

puzzB = {(1, 1): 1, (1, 2): 3, (1, 3): 'B', \
         (2, 1): 7, (2, 2): 2, (2, 3): 4, \
         (3, 1): 6, (3, 2): 8, (3, 3): 5}

puzzC = {(1, 1): 1, (1, 2): 3, (1, 3): 4, \
         (2, 1): 7, (2, 2): 2, (2, 3): 5, \
         (3, 1): 6, (3, 2): 8, (3, 3): 'B'}

puzzD = {(1, 1): 1, (1, 2): 3, (1, 3): 4, \
         (2, 1): 7, (2, 2): 2, (2, 3): 5, \
         (3, 1): 'B', (3, 2): 6, (3, 3): 8}

puzzE = {(1, 1): 'B', (1, 2): 3, (1, 3): 4, \
         (2, 1): 1, (2, 2): 2, (2, 3): 5, \
         (3, 1): 7, (3, 2): 6, (3, 3): 8}

challenge = {(1, 1): 8, (1, 2): 3, (1, 3): 5, \
             (2, 1): 7, (2, 2): 1, (2, 3): 2, \
             (3, 1): 6, (3, 2): 'B', (3, 3): 4}

allpuzz = [easy1, easy2, puzzA, puzzB, puzzC, puzzD, puzzE, challenge]


def puzz8_hash(pz):
    hval = 0
    for (x, y) in pz.keys():
        if pz[(x, y)] == 'B':
            hval += (x + y)
        else:
            hval += (x + y) * pz[(x, y)]
    return hval % 23


# WARNING: generated puzzles may be very difficulty
# or impossible to solve ... for testing, it is
# safer to work with the preset ones above;

def random_puzz8(k):
    while True:
        pz = make_puzz8(k)
        show_puzz8(pz)
        yesno = raw_input("Keeper? [y/n] ")
        if yesno == 'y' or yesno == 'Y':
            return pz


def make_puzz8(k):
    pz = {(1, 1): 1, (1, 2): 2, (1, 3): 3, \
          (2, 1): 8, (2, 2): 'B', (2, 3): 4, \
          (3, 1): 7, (3, 2): 6, (3, 3): 5}
    for i in range(k):
        r = random.randint(1, 4)
        if r == 1:
            nxtpz = move_blank_up(pz)
            if nxtpz != None:
                pz = nxtpz
        elif r == 2:
            nxtpz = move_blank_down(pz)
            if nxtpz != None:
                pz = nxtpz
        elif r == 3:
            nxtpz = move_blank_left(pz)
            if nxtpz != None:
                pz = nxtpz
        else:
            nxtpz = move_blank_right(pz)
            if nxtpz != None:
                pz = nxtpz
    return pz


# print the puzzle
def show_puzz8(pz):
    if pz == None:
        return
    print "\n"
    for i in range(1, 4):
        for j in range(1, 4):
            print "%s " % pz[(i, j)],
        print "\n"
    return


# compare corresponding tiles pz with the goal (global GOAL above)

def puzz8_goal_fct(pz, goal):
    for k in goal.keys():
        if not goal[k] == pz[k]:
            return False
    return True


# number of tiles out of place in pz relative to GOAL;
#
def puzz8_eval_fct_A(pz, goal):  # = None):
    score = 0
    for k in goal.keys():
        if goal[k] != 'B' and not goal[k] == pz[k]:
            score += 1
    return score


# *************************************************************
# MIDTERM -- TAKEHOME PROBLEM
# sum of horizontal and vertical displacements for all tiles

def puzz8_eval_fct_B(pz, goal):

    # set sum to zero
    sum = 0
    # for each record in goal find key and value
    for goal_key, goal_value in goal.items():

        row = goal_key[0]  # row
        col = goal_key[1]  # column

        # for each record in current node
        for key, value in pz.items():
            # find the record with the same value
            if value == goal_value:
                # add horizontal and vertical displacements to the sum
                sum += abs(row - key[0]) + abs(col - key[1])
                break

    return sum

# **************************************************************

# puzz is a dictionary; keys are (r,c), values are tiles;
def find_loc(tile, puzz):
    for (r, c) in puzz.keys():
        if puzz[(r, c)] == tile:
            return (r, c)
    return (-1, -1)  # something wrong if this line reached ...


# try all move functions and collect all non-None results into a list
# of puzzle successor states;
# ... replace 'pass'
def puzz8_successor_fct(pz):
    succs = []
    moves = [move_blank_up(pz), \
             move_blank_down(pz), \
             move_blank_left(pz), \
             move_blank_right(pz)]
    for x in moves:
        if not x == None:
            succs.append(x)
    return succs


# moving a blank up ... B at (i,j) moves to (i-1,j), tile at (i-1,j)
# moves to (i,j); returns a new puzzle data structure or None if the blank
# cannot move up;

def move_blank_up(pz):
    # make a copy and modify that!
    newpz = copy.deepcopy(pz)
    keys = newpz.keys()
    blank = None
    for (i, j) in keys:
        if newpz[(i, j)] == 'B':
            blank = (i, j)
            break
    # need to test whether blank can still move up;
    # if not return None

    if blank[0] == 1:
        # blank cannot move up
        return None

    # tile = newpz[(i-1,j)]
    # newpz[(i-1,j)] = 'B'
    # newpz[(i,j)] = tile
    # ... or ... ONLY IN PYTHON ...

    newpz[(i - 1, j)], newpz[(i, j)] = newpz[(i, j)], newpz[(i - 1, j)]
    return newpz


def move_blank_down(pz):
    newpz = copy.deepcopy(pz)
    keys = newpz.keys()
    blank = None
    for (i, j) in keys:
        if newpz[(i, j)] == 'B':
            blank = (i, j)
            break
    if blank[0] == 3:
        # blank cannot move down
        return None

    # tile = newpz[(i+1,j)]
    # newpz[(i+1,j)] = 'B'
    # newpz[(i,j)] = tile
    # or ... ONLY IN PYTHON ...

    newpz[(i + 1, j)], newpz[(i, j)] = newpz[(i, j)], newpz[(i + 1, j)]
    return newpz


def move_blank_left(pz):
    newpz = copy.deepcopy(pz)
    keys = newpz.keys()
    blank = None
    for (i, j) in keys:
        if newpz[(i, j)] == 'B':
            blank = (i, j)
            break
    if blank[1] == 1:
        # blank cannot move left
        return None

    # tile = newpz[(i,j-1)]
    # newpz[(i,j-1)] = 'B'
    # newpz[(i,j)] = tile

    newpz[(i, j - 1)], newpz[(i, j)] = newpz[(i, j)], newpz[(i, j - 1)]
    return newpz


def move_blank_right(pz):
    newpz = copy.deepcopy(pz)
    keys = newpz.keys()
    blank = None
    for (i, j) in keys:
        if newpz[(i, j)] == 'B':
            blank = (i, j)
            break
    if blank[1] == 3:
        # blank cannot move left
        return None

    # tile = newpz[(i,j+1)]
    # newpz[(i,j+1)] = 'B'
    # newpz[(i,j)] = tile

    newpz[(i, j + 1)], newpz[(i, j)] = newpz[(i, j)], newpz[(i, j + 1)]
    return newpz


# print content of dictionary structure
# more compactly for easy to ready output
def puzz8_compact(puzz):
    print "[",
    for row in [1, 2, 3]:
        print "[",
        for col in [1, 2, 3]:
            print "%s " % puzz[(row, col)],
        print "]",
    print "]"
    return











