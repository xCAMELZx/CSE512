#graphsearch_lab3.py

#example from Poole et.al.
#Oxford Univ Pres, 1998,

import random

GRAPH = {'o103':['o109','ts','l2d3'],
         'o109':['o111','o119'],
         'ts':['mail'],
         'o111':[],
         'mail':[],
         'o119':['store','o123'],
         'store':[],
         'o123':['o125','r123'],
         'o125':[],
         'r123':[],
         'l2d3':['l2d1','l2d4'],
         'l2d1':['l3d2','l2d2'],
         'l2d4':['o109'],
         'l2d2':['l2d4'],
         'l3d2':['l3d3','l3d1'],
         'l3d3':[],
         'l3d1':['l3d3']}
COST = {('o103','ts'):8, ('o103','o109'):12, ('o103','l2d3'):4,\
        ('ts','mail'):6,\
        ('o109','o111'):4, ('o109','o119'):16,\
        ('o119','store'):7, ('o119','o123'):9,\
        ('o123','r123'):4, ('o123','o125'):4,\
        ('l2d1','l3d2'):3, ('l2d1','l2d2'):6,\
        ('l2d2','l2d4'):3, ('l2d3','l2d1'):4,\
        ('l2d3','l2d4'):7, ('l2d4','o109'):7,\
        ('l3d2','l3d3'):6, ('l3d2','l3d1'):4,\
        ('l3d1','l3d3'):8}

#Traversinc and Printing Nodes in Depth-First Order

def dfs_traverse(start):
    open = [start]
    closed = []
    while open != []:
        nxt = open[0]
        open = open[1:]

        if nxt in closed:   #Used for o109
            continue
        
        closed.append(nxt)
        print "nxt from open: %s" % nxt
        succ = GRAPH[nxt]
        random.shuffle(succ)  #why do we do this?

        for x in succ:
            if not x in closed and not x in open:
                open = [x] + open

    return closed

#Traversing and Printing in Breadth-First Order

def bfs_traverse(start):
    open = [start]
    closed = []
    while open != []:
        nxt = open[0]
        open = open[1:]

        if nxt in closed:
            continue

        closed.append(nxt)
        print "nxt from open: %s" % nxt
        succ = GRAPH[nxt]
        random.shuffle(succ)
        for x in succ:
            if not x in closed and not x in open:
                open.append(x)
    return closed

#Searching connection from start to goal in DFS;
#Returns goal when found, none otherwise;
#does NOT Compute the "path" between start and goal;

def dfs_search(start, goal):
    open = [start]
    closed = []
    steps = 0
    while open != []:
        nxt = open[0]
        open = open[1:]

        #return when GOAL FOUND
        if nxt == goal:
            return goal, steps

        if nxt in closed:
            continue

        print "nxt from open: %s" % nxt
        steps += 1
        closed.append(nxt)
        succ = GRAPH[nxt]
        random.shuffle(succ) #Possible remove? Shuffle the children?
        for x in succ:
            if not x in closed and not x in open:
                open = [x] + open
    return None, steps

#SEARCH from start to goal in bfs;

def bfs_search(start, goal):
    open = [start]
    closed = []
    steps = 0
    while open != []:
        nxt = open[0]
        open = open[1:]

        if nxt == goal:
            return goal, steps

        if nxt in closed:
            continue
        print "nxt from open: %s" % nxt
        steps += 1
        closed.append(nxt)
        succ = GRAPH[nxt]
        random.shuffle(succ)
        for x in succ:
            if not x in closed and not x in open:
                open.append(x)
    return None,steps

#Searching with computing of PATH
#from start to goal; dfs;

def dfs_search_path(start,goal):
    open = [[start,[start]]]
    closed = []
    steps = 0
    while open != []:
        nxt = open[0]
        open = open[1:]
        nxtnode = nxt[0]
        nxtpath = nxt[1]

        if nxtnode == goal:
            return nxtpath,steps,len(closed)

        if nxt in closed:
            continue

        closed.append(nxtnode)
        succ = GRAPH[nxtnode]
        random.shuffle(succ)
        for x in succ:
            if not x in closed:
                open = [[x,addpath(nxtpath,x)]] + open
            steps += 1
        return None,steps
        
#utility function
def addpath(path,x):
    newpath = path[:] #NOTICE A COPY IS MADE
    newpath.append(x)
    return newpath

        #searching and computing PATH in bfs;
######################################################################
def bfs_search_path(start,goal):
    open = [[start,[start]]]
    closed = []
    steps = 0
    while open != []:
        nxt = open[0]
        open = open[1:]
        nxtnode = nxt[0]
        nxtpath = nxt[1]

        if nxtnode == goal:
            return nxtpath,steps,len(closed)  
        if nxt in closed:
            continue
    closed.append(nxtnode)
    succ = GRAPH[nxtnode]
    random.shuffle(succ)
    for x in succ:
        if not x in closed:
            open = [[x,addpath(nxtpath,x)]]
            steps += 1
        return None,steps
    
##### Completed Section, Left Blank for Lab #######
#######################################################################
    
# finding a path by pursing "BEST" first;

def best_first_search_path(start,goal):
    open = [[start,[start],0]]
    closed = []
    steps = 0
    while open != []:
        nxt = open[0]
        open = open[1:]
        nxtnode = nxt[0]
        nxtpath = nxt[1]
        nxtcost = nxt[2]
        
        if nxtnode == goal:
            return nxtpath,steps,len(closed)
        if nxt in closed:
            continue
        
        closed.append(nxtnode)
        succ = GRAPH[nxtnode]
        
        for x in succ:
            if not x in closed:
                xcost = COST[(nxtnode,x)]
                open.append([x,addpath(nxtpath,x),nxtcost+xcost])
                open.sort(lambda x,y: CostCmp(x,y)) # NOTICE SORTING
                steps += 1
                return None
            
# x,y are lists that are compared by magnitude of their third #
# elements; x of type [node,path,cost];
# CostCmp compare costs, to allow sortig of triples by cost

def CostCmp (x,y):
    if x[2] < y[2]:
        return -1
    elif x[2] == y[2]:
        return 0
    else:return 1
