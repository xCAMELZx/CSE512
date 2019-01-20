# graph_search.py
# Kerstin Voigt, Feb 2016, after Nils Nilsson's Graph Search Algorithm
# an expanded version of search.py
# Expanded on 02/11/2016 by Brandon Saunders
import random
from puzz8 import *
from operator import *
import time 

# a directed graph made of Nodes.
class Node:
    def __init__(self, num = None, parnum=None, thestate=None, dep=0, val=None):
        self.no = num # a unique state number
        self.parno = parnum # state number of parent node
        self.state = thestate # the actual state
        self.depth = dep # depth of node in search
        self.eval = val # eval fct value 

    def __eq__(self,other):
        if (other == None):
            return False
        return self.state == other.state

    def __lt__(self,value):
        if (value == None):
            return False
        return self.state < self.state

# x a "state", nodes a list of elements of type Node

def on_list_of_Nodes(x,lst):
    for y in lst:
        if x == y.state:
            return True
    return False

def on_open(x,op):
    return on_list_of_Nodes(x,op)

def on_closed(x,cl):
    return on_list_of_Nodes(x,cl) 

def sort_open(open):
    open = open.sort()
    


NUM = 1

# search to GOAL from state start
def search(start):
    global NUM
    all = []
    start_node = Node(NUM,None,start,0,None) # casting start "node"
    NUM += 1
    # open: a list of all (partial) paths seen until now
    # initial to path to starting point, [x] 
    open = [start_node] # Stores possible moves

    closed = [] # Holds all the moves already done
    k = 1
    while open != []:
        if k > 50000:
            break

        time.sleep(.2)

        curr = open[0]
        open = open[1:] # Slice from 
        closed.append(curr)  # store copy on closed;

        show_puzz8(curr.state)
        #print "%d. From open... (%d) %s" % (k,curr.no,curr.state)
        
        if goal_fct(curr.state):
            #return True  
            print("Found a path!")
            return compute_path(start_node,curr,closed)
        else:
            neighs = successor_fct(curr.state) # successor "states"
            for n in neighs:
                if not on_open(n,open) and not on_closed(n,closed):
                    ev = evaluate(n)
                    new_node = Node(NUM,curr.no,n,curr.depth + 1, ev)
                    open.append(new_node)
                    NUM += 1

        # Then sort the list and compare to make smart moves.
        if open:
            sorted(open, key = attrgetter('eval'))

        k += 1
    print("Did not find a path.")
    return False

# start and stop are of type Node, nodes is a listof Nodes
# returns a list of Nodes on the solution path;
def compute_path(start, stop, nodes):
    if start.state == stop.state:
        return [start]
    parent = None
    # stop node has a parent with number (.no) equal to stop.parnum
    # find this parent node ... 
    for n in nodes:
        if n.no == stop.parno:
            parent = n
            break
    if parent == None:
        return []
    return compute_path(start,parent,nodes) + [stop]


# Need to create a single numerical value evaluation of how many pieces are in the wrong position.
# The lower the number, the better.
def evaluate(puzzle):
    if (goal_fct(puzzle)):
        return True
    numberOutOfPlace = 0

    for k in GOAL.keys():
        if not GOAL[k] == puzzle[k]:
            numberOutOfPlace += 1
    return numberOutOfPlace
           


puzzle = make_puzz8()
show_puzz8(puzzle)
search(easy)


search(easy)





    
          
                                                    
