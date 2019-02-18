# astar_midterm.py

# STUDENT COMPLETER: ______________________

#
# Nodes with parent; compute solution path rather than
# containing it within node

import random
import time
import operator
from puzz8_midterm import *


class Node:
    def __init__(self, state=None, par=None, depth=0, evalue=None):
        self.thestate = state
        # self.thepath = path
        self.theparent = par
        self.thedepth = depth
        self.theeval = evalue

    def __eq__(self, other):
        return self.thestate == other.thestate  # equality by state only!


# parameterize the goal, successor and evaluation functions;


def ASTAR_SEARCH_FCT(start, target, GOAL_FCT, SUCCESSOR_FCT, EVAL_FCT, \
                     COMPACT_PRINT=None):
    if COMPACT_PRINT == None:
        def myprint(x): print x

        COMPACT_PRINT = myprint

    open = [Node(start, None, 0, EVAL_FCT(start, target))]
    closed = []
    steps = 0
    while open != []:
        nxt = open[0]
        open = open[1:]

        nxtstate = nxt.thestate
        nxtpar = nxt.theparent
        nxteval = nxt.theeval
        nxtdpth = nxt.thedepth

        if GOAL_FCT(nxtstate, target):
            # MIDTERM TAKEHOME PROBLEM
            # define extract_path ... see below
            nxtpath = extract_path(nxt, closed)

            print "GOAL FOUND:"
            print "State:    ",
            print nxtstate
            print "PathL:  %d" % len(nxtpath)
            print "Steps:  %d\n" % steps
            # return 3 items of info: the last state, solution path,
            # and number of search steps (iterations);
            return [nxtstate, nxtpath, steps]

        if nxt in closed:
            # MIDTERM provided
            adjust_parents(nxt, closed)
            continue

        closed.append(nxt)

        succ = SUCCESSOR_FCT(nxtstate)
        random.shuffle(succ)

        for x in succ:
            xcost = EVAL_FCT(x, target)
            # Node nxt is parent of node with state x
            newnode = Node(x, nxt, nxtdpth + 1, xcost + nxtdpth + 1)

            # check whether newstate[0] (or, x) is already on open or closed with
            # shorter path; if so, do not bother to put open;
            keeper = True
            for c in closed:
                if newnode.thestate == c.thestate and \
                        newnode.thedepth >= c.thedepth:
                    keeper = False
                    break
            if not keeper:
                continue

            for op in open:
                if newnode.thestate == op.thestate and \
                        newnode.thedepth >= op.thedepth:
                    keeper = False
                    break

            if keeper:
                open.append(newnode)

        # open.sort(lambda x,y: CostCmp(x,y))  # NOTICE SORTING
        # below works for Python 2 and 3 ...
        open_plus = [(x, x.theeval) for x in open]
        open_plus.sort(key=operator.itemgetter(1))
        open = [x for (x, _) in open_plus]

        steps += 1
    return None


# MIDTERM provided
def adjust_parents(nd, nodes):
    for x in nodes:
        if nd == x:
            # see whether x needs adjusting
            if nd.thedepth < x.thedepth:
                # adjust ...
                # print "adjusting parents backwards ... "
                x.theparent = nd.parent
                x.thedepth = nd.thedepth
                x.theeval = nd.theeval
                return
            else:
                # print "no need to adjust parents"
                return
    return


# ************************************************************
# MIDTERM -- TAKEHOME PROBLEM
# returns a list of states from start to goal;

def extract_path(nd, closed):
    path = []
    # set current node to goal node
    current = nd
    # continue until parent node is None (parent of start node)
    while current:
        # add state of current node to the path
        path.append(current.thestate)
        # go to the parent node
        current = current.theparent
    # reverse path from start to goal
    path.reverse()

    return path  # return the path


# ************************************************************

if __name__ == '__main__':

    random.seed()

    print "\nA* search in 8-puzzle domain:"

    stats = []
    for puzz in allpuzz:
        show_puzz8(puzz)

        # run for #tiles-out-of-place as eval fct;
        (_, pathA, stepsA) = ASTAR_SEARCH_FCT(puzz, GOAL, puzz8_goal_fct, \
                                              puzz8_successor_fct, \
                                              puzz8_eval_fct_A)

        # run for sum-of-horiz-and-vert-displacements as eval fct;
        (_, pathB, stepsB) = ASTAR_SEARCH_FCT(puzz, GOAL, puzz8_goal_fct, \
                                              puzz8_successor_fct, \
                                              puzz8_eval_fct_B)

        stats.append(((len(pathA), stepsA), (len(pathB), stepsB)))

    print "\n"
    print "#tiles-out-of-place(A) vs Sum-vert-horiz-displace(B):\n"
    for ((pA, sA), (pB, sB)) in stats:
        print "A: pathlen %d at %d steps     B: pathlen %d at %d steps" % \
              (pA, sA, pB, sB)
