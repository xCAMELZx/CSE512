# path_finder.py
# by Kerstin Voigt, Jan 2016; for CSE 512 lecture/lab
# Modified on 1/30/2016 by Brandon Saunders

import random

counter = 0


# a directed graph
TheMap = {'a':['b', 'c'], 'b':['d','g','a'], 'c':['q','a'], 'd':['h', 'e', 'b'],\
          'e':['f','d'], 'f':['i','e'], 'g':['h','b'], 'h':['m','i','g','d'],\
          'i':['f','h','j','o'], 'j':['k','i','p'], 'k':['j'], 'l':['m'], 'm':['l','n', 'h'],\
          'n':['m'], 'o':['i','p'], 'p':['o','q','j'], 'q':['p','c']}


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
    def __init__(self, current_node, parent_node):
        self.current_node = current_node
        self.parent_node = parent_node

    def __repr__(self):
        node_list = []
        node_i = self
        
        while node_i != None:
            node_list += [node_i.current_node]
            node_i = node_i.parent_node

        node_list.reverse()
        return ','.join(node_list)

    def get_data(self):
        return self.current_node

    def get_parent(self):
        return self.parent_node

    def set_parent(self, parent_node):
        self.parent_node = parent_node

    def does_it_contain(self,current_node):
        if current_node == self.current_node:
            return True
        elif self.parent_node != None:
            return self.parent_node.does_it_contain(current_node)
        return False




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

print(node_all_paths('a','b'))
