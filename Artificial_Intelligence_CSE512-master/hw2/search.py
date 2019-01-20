# search.py
# by Kerstin Voigt, Feb 2016; for CSE 512 lecture/lab
# Modified on 2/2/2016 by Brandon Saunders

import random

counter = 0


# a directed graph
TheMap = {'a':['b', 'c'], 'b':['a','d','g'], 'c':['a','q'], 'd':['h', 'e', 'b'],\
          'e':['f','d'], 'f':['i','e'], 'g':['b','h'], 'h':['d','g','m','i'],\
          'i':['h','o','f','j'], 'j':['i','k','p'], 'k':['j'], 'l':['m'], 'm':['l','h', 'n'],\
          'n':['m'], 'o':['i','p'], 'p':['j','q','o'], 'q':['c','p']}


def next(x):
    return TheMap[x]

def path(x,y):
    print "seeking path %s - %s" % (x,y)
    if x == y:
        return  [x]
    neighs = next(x)
    if next == []:
        return None
    #random.shuffle(neighs)
    for n in neighs:
        p = path(n,y)
        if p != None:
            return [x] + p
    print "No Path"
    return None

def all_paths(x,y, mode):
    global counter
    all = []
    open = [[x]]
    while open != []:
        counter+=1
        if (counter < 500):
            pth = open[0]
            print("pth",pth)
            open = open[1:]
            last = pth[-1]
            if last == y:
               all.append(pth)
               if (mode == "first"):
                    break
            else:
                neighs = next(last)
                for n in neighs:
                    extpth = pth[:]
                    extpth.append(n)
                    open.append(extpth)
        else:
            print("Exceeded 500 cycles. Breaking loop")
            break

    if (mode == "all"):
        return all
    elif (mode == "first"):
        return pth




def short_long(x,y):
    shortest = None
    longest = None
    open = [[x]]
    while open != []:
        pth = open[0]
        open = open[1:]
        last = pth[-1]
        if last == y:
            if shortest == None:
                shortest = pth
                longest = pth
            else:
                if len(pth) < len(shortest):
                    shortest = pth
                elif len(pth) > len(longest):
                    longest = pth
                else:
                    pass
        else:
            neighs = next(last)
            for n in neighs:
                extpth = pth[:]
                extpth.append(n)
                open.append(extpth)
    return shortest,longest





class Node(object):
    def __init__(self, par=None, lab=None):
        self.parent = par
        self.label = lab

def next(x):
    return TheMap[x]

def on_list_of_Nodes(x,lst):
    for y in lst:
        if x == y.label:
            return True
        return False
def on_open(x,op):
    return on_list_of_Nodes(x,op)

def on_closed(x,cl):
    return on_list_of_Nodes(x,cl)

def search(x,y):
    open = [Node(None,x)]
    closed = []
    k=1 
    while open != []:
        if k > 10000:
            break
        curr = open[0]
        open = open[1:]
        closed.append(curr)
        print ("[%d] Next node from open: %s" % (k,curr.label))

        if curr.label == y:
            return True
        else:
            neighs = next(curr.label)
            for n in neighs:
                if not on_open(n,open) and not on_closed(n,closed):
                    open.append(Node(curr,n))

def computer_path(start, stop, nodes):
    print "seeking path %s - %s" % (x,y)
    if x == y:
        return  [x]
    neighs = next(x)
    if next == []:
        return None
    #random.shuffle(neighs)
    for n in neighs:
        p = path(n,y)
        if p != None:
            return [x] + p
    print "No Path"
    return None

def node_all_paths(x, y, first=False):
    global counter
    graph = TheMap
    all = []
    open = [Node(x, None)]

    while open != []:
        path = open[0]
        open = open[1:]
        counter+=1
        if (counter < 500):
            if path.current_node == y:      
                if first:
                    return path
                else:
                    all.append(path)
            else:
                neighs = next(path.current_node)
                for n in neighs:

                    if path.does_it_contain(n):
                        continue
                    open.append(Node(n, path))               
                
        else:
            print("Exceeded 500 cycles. Breaking loop")
            break

    return [all]

computer_path('a','b')