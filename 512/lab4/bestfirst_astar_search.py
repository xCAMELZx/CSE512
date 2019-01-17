# bestfirst_astar_search.py
# by Kerstin Voigt, Jan 2018, for lectures and lab on GRAPHSEARCH

import random
from puzz8 import *

#directed, acyclic graph of "nodes"
# example from Poole et.al. "Computational Intelligence" Oxford Univ Press,,
# 1998,pp. 117, 121

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

# goal, successor and evaluation functions for best-first search
# in robot domain (above)

def rob_goal(node,target):
  return node == target

def rob_next(node):
  return GRAPH[node]

def rob_cost(node,prevnode,target = None):
  return COST[(prevnode,node)]

# utility function 
def addpath(path,x):
  newpath = path[:]  # NOTICE: a copy is made!
  newpath.append(x)
  return newpath

 # x,y are lists that are compared by
# magnitude of their third elements;
# x of type [node,path,cost]
# CostCmp compare costs, to allow sortig of triples by cost
def CostCmp (x,y):
  if x[2] < y[2]:
    return -1
  elif x[2] == y[2]:
    return 0
  else:
    return 1

# parameterize the goal, successor and evaluation functions;

def BEST_FIRST_SEARCH_FCT(start,target,GOAL_FCT,SUCCESSOR_FCT,EVAL_FCT,\
                    COMPACT_PRINT = None):

  if COMPACT_PRINT == None:
      def myprint (x): print x
      COMPACT_PRINT = myprint

  open = [[start,[start],0]]
  closed = []
  steps = 0  ######### report these as effort!!!
  while open != []:
    nxt = open[0]
    open = open[1:]
    
    nxtnode = nxt[0]
    nxtpath = nxt[1]
    nxteval = nxt[2]
  
    if GOAL_FCT(nxtnode,target): # nxtnode == goal:
      print "GOAL FOUND:"
      #print "Node: %s" % nxtnode
      print "Node:   ",
      COMPACT_PRINT(nxtnode)
      print "PathL:  %d" % len(nxtpath)
      print "Steps:  %d\n" % steps
      return nxt

    if nxt in closed:
      continue
    closed.append(nxt) #nxtnode)

    succ = SUCCESSOR_FCT(nxtnode) #GRAPH[nxtnode]
    random.shuffle(succ)

    for x in succ:
      xcost = EVAL_FCT(x,nxtnode,target)  #COST[(nxtnode,x)]
      newnode = [x,addpath(nxtpath,x),xcost]
      #print newnode

      #check whether newnode[0] (or, x) is already on open or closed with
      #shorter path; if so, do not bother to put open;
      keeper = True
      for c in closed:
        if newnode[0] == c[0] and newnode[2] >= c[2]:
          keeper = False
          break

        if not keeper:
          continue
      
      for op in open:
        if newnode[0] == op[0] and newnode[2] >= op[2]:
          keeper = False
          break

      if keeper:
          open.append(newnode)

      open.sort(lambda x,y: CostCmp(x,y))  # NOTICE SORTING
      steps += 1
  return None

def ASTAR_SEARCH_FCT(start,target,GOAL_FCT,SUCCESSOR_FCT,EVAL_FCT,\
                    COMPACT_PRINT = None):

  if COMPACT_PRINT == None:
      def myprint (x): print x
      COMPACT_PRINT = myprint

  open = [[start,[start],0,0]]
  closed = []
  steps = 0
  while open != []:
    nxt = open[0]
    open = open[1:]
    
    nxtnode = nxt[0]
    nxtpath = nxt[1]
    nxteval = nxt[2]
    nxtdpth = nxt[3]
    
    if GOAL_FCT(nxtnode,target): # nxtnode == goal:
      print "GOAL FOUND:"
      #print "Node: %s" % nxtnode
      print "Node:    ",
      COMPACT_PRINT(nxtnode)
      print "PathL:  %d" % len(nxtpath)
      print "Steps:  %d" % steps
      return nxt

    
    if nxt in closed:
      continue
    closed.append(nxt)  # was: nxtnode
    
    succ = SUCCESSOR_FCT(nxtnode) #GRAPH[nxtnode]
    random.shuffle(succ)
    
    for x in succ:
        xcost = EVAL_FCT(x,nxtnode,target)  #COST[(nxtnode,x)]
        newnode = [x,addpath(nxtpath,x),nxteval+nxtdpth+1,nxtdpth+1]
        #print newnode

        #check whether newnode[0] (or, x) is already on open or closed with
        #shorter path; if so, do not bother to put open;
        keeper = True
        for c in closed:
          if newnode[0] == c[0] and newnode[2] >= c[2]:
            keeper = False
            break
        if not keeper:
          continue
        
        for op in open:
          if newnode[0] == op[0] and newnode[2] >= op[2]:
            keeper = False
            break

        if keeper:
            open.append(newnode) #x,addpath(nxtpath,x),nxtcost+xcost,nxtdpth+1])

    open.sort(lambda x,y: CostCmp(x,y))  # NOTICE SORTING
    steps += 1
  return None




# testing ...

print "\nBest-first search in robot domain:"
for i in range(5):
  BEST_FIRST_SEARCH_FCT('o103', 'r123', rob_goal, rob_next, rob_cost)

print "\nA* search in robot domain:"
for i in range(5):
  ASTAR_SEARCH_FCT('o103', 'r123', rob_goal, rob_next, rob_cost)


print "\nBest-first search in 8-puzzle domains:"
show_puzz8(puzzE)
for i in range(5):
  BEST_FIRST_SEARCH_FCT(puzzE, GOAL, puzz8_goal_fct, puzz8_successor_fct,\
                  puzz8_eval_fct, puzz8_compact)

print "\nA* search in 8-puzzle domains:"
show_puzz8(puzzE)
for i in range(5):
  ASTAR_SEARCH_FCT(puzzE, GOAL, puzz8_goal_fct, puzz8_successor_fct,\
                  puzz8_eval_fct, puzz8_compact)


