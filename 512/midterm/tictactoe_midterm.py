# tictactoe_midterm.py
# by Kerstin Voigt, Feb 2018

# MIDTERM: upon completion, this will be a program with
# maximin by progam, with minimax juding of X's moves;
# prints out history of game play

import random
import copy

class T3():
    def __init__(self, init_ttt = None):
        if init_ttt:
            self.ttt = init_ttt
        else:
            self.ttt = {'a': 0, 'b': 0, 'c':0, 'd': 0,'e': 0, 'f':0,\
                        'g': 0, 'h': 0, 'i': 0}
        self.row1 = ['a','b','c']
        self.row2 = ['d','e','f']
        self.row3 = ['g','h','i']
        self.col1 = ['a','d','g']
        self.col2 = ['b','e','h']
        self.col3 = ['c','f','i']
        self.dia1 = ['a','e','i']
        self.dia2 = ['c','e','g']

        self.history = []

    def reset(self):
        self.ttt = {'a': 0, 'b': 0, 'c':0, 'd': 0,'e': 0, 'f':0,
               'g': 0, 'h': 0, 'i': 0}

    # row, col, or diag values
    def rcd_values(self,rcd):
        return [self.ttt[x] for x in rcd]

    def __str__(self):
        return " %s %s %s" % (self.rcd_values(self.row1),
                                   self.rcd_values(self.row2),
                                   self.rcd_values(self.row3))
    # a way to display the board
    def present(self):
        self.present_row(self.row1)
        self.present_row(self.row2)
        self.present_row(self.row3)
        print("\n")


    def present_row(self,row):
        for i in range(3):
            if self.ttt[row[i]] == 0:
                if i < 2:
                    print(row[i]),
                else:
                    print(row[i])
            else:
                if i < 2:
                    print(self.ttt[row[i]]),
                else:
                    print(self.ttt[row[i]])
        

    # prompt for and put X
    def put_X(self):
        self.present()
        #-----------------------------------------
        # NEW
        good = self.judge_X()  # recommended move
        single = self.single_move_left()
        #-----------------------------------------
        while(True):
            pick = raw_input('Choose place for X: ')
            if self.ttt[pick] == 0:
                self.ttt[pick] = 'X'
                #-------------------------------------------
                # NEW
                if pick == single:
                    self.history.append(('X',pick,'HP: +-'))
                elif pick == good: 
                    self.history.append(('X',pick,'HP: ++'))
                else:
                    self.history.append(('X',pick,'HP: --'))
                #-------------------------------------------
                break
            else:
                print "Can't do; choose again:"

    # place a random O (the games current response)
    def random_O(self):
        self.present()
        print "Playing an @ ..."
        rest=[]
        for k in self.ttt.keys():
            if self.ttt[k] == 0:
                rest.append(k)
        pick = random.choice(rest)
        self.ttt[pick] = '@'

    def response_O(self):
        self.present()
        print "Playing an @ ..."
        toplay = self.grab_winO()
        if toplay != None:
            self.ttt[toplay] = '@'
            self.history.append(('@',toplay,'grab Owin'))
            return
        toplay = self.two_XO('X')
        if toplay != None:
            self.ttt[toplay] = '@'
            self.history.append(('@',toplay,'block Xwin'))
            return
        
        pick = self.maxi_min_O()
        self.history.append(('@',pick,'maximin O'))
        
        self.ttt[pick] = '@'
        return

    #-------------------------------------------
    # NEW
    def judge_X(self):
        toplay = self.single_move_left()
        if toplay != None:
            return toplay
        toplay = self.grab_winX()
        if toplay != None:
            return toplay
        toplay = self.two_XO('@')
        if toplay != None:
            return toplay
        
        toplay = self.mini_max_X()
        return toplay
    #-------------------------------------------
    # NEW

    def single_move_left(self):
        if self.ttt.values().count(0) == 1:
            for x in self.row1:
                if self.ttt[x] == 0:
                    return x
            for x in self.row2:
                if self.ttt[x] == 0:
                    return x
            for x in self.row3:
                if self.ttt[x] == 0:
                    return x
        else:
            return None
    #-------------------------------------------

    # possible rows,cols,diags for X -
    # possible rows,cols,diagas for O
    def eval_ttt(self):
        if self.winX():
            return 10000
        if self.winO():
            return -10000
        
        countX = 0
        countO = 0
        for r in [self.row1,self.row2,self.row3]:
            tr = map(lambda x: self.ttt[x],r)
            kX = tr.count('X')
            kO = tr.count('@')
            if kO == 0:
                countX += 1
            if kX == 0:
                countO += 1
        for c  in [self.col1,self.col2,self.col3]:
            tc = map(lambda x: self.ttt[x],c)
            kX = tc.count('X')
            kO = tc.count('@')
            if kO == 0:
                countX += 1
            if kX == 0:
                countO += 1
        for d  in [self.dia1,self.dia2]:
            td = map(lambda x: self.ttt[x],d)
            kX = td.count('X')
            kO = td.count('@')
            if kO == 0:
                countX += 1
            if kX == 0:
                countO += 1
        #print "eval = %d" % (countX - countO)
        return countX - countO 
################################################################################                
    def maxi_min_O(self):
        # T3 game boards for each @ placement
        # in form of list of tups [(pl,T3),...]
        next_boards_for_O = self.ttts_for_XO('@')
        
        maxes_for_X = []
        for (nxtplO,nxtO) in next_boards_for_O:
            max_X = self.max_for_X_under_O(nxtO)      # eval for max X under nxtO
            maxes_for_X.append((nxtplO,max_X))
        placeO = min(maxes_for_X, key = lambda x: x[1])
        print "... O maximins with at %s" % placeO[0]
        return placeO[0]

    #-----------------------------------------------------
    # MIDTERM: COMPLETE
    def mini_max_X(self):
        next_boards_for_X = self.ttts_for_XO('X')
        
        maxes_for_O = []
        for (nxtplX,nxtX) in next_boards_for_X:
            max_O = self.min_for_O_under_X(nxtX)      # eval for max X under nxtO
            maxes_for_O.append((nxtplX,max_O))
        placeX = min(maxes_for_O, key = lambda o: o[1])
        print "... X maximins with at %s" % placeX[0]
        return placeX[0]
        #return None  
    #-----------------------------------------------------
#################################################################################            
    def ttts_for_XO(self,S):
        places_for_XO = []
        for x in self.ttt.keys():
            if self.ttt[x] == 0:
              places_for_XO.append(x)
        if places_for_XO == []:
            return  None
        ttts_for_XO = []
        for x in places_for_XO:
            nxt = copy.deepcopy(self.ttt)
            nxt[x] = S    # X or @
            nxtT3 = T3(nxt)
            ttts_for_XO.append((x,nxtT3))
        return ttts_for_XO
###############################################################################
    # returns the eval eval of the max X under Oboard
    def max_for_X_under_O(self,Oboard):
        places_for_X = []
        for x in Oboard.ttt.keys():
            if Oboard.ttt[x] == 0:
                places_for_X.append(x)
        maxeval = -100000
        for x in places_for_X:
            nxt = copy.deepcopy(self.ttt)
            nxt[x] = 'X'
            nxtT3 = T3(nxt)
            nxteval = nxtT3.eval_ttt()
            if nxteval > maxeval:
                maxeval = nxteval
        return maxeval

    #-----------------------------------------------------
    # MIDTERM: COMPLETE
    def min_for_O_under_X(self,Xboard):
        places_for_O = []
        for o in Xboard.ttt.keys():
            if Xboard.ttt[o] == 0:
                places_for_O.append(o)
        maxeval = -100000
        for x in places_for_O:
            nxt = copy.deepcopy(self.ttt)
            nxt[x] = 'O'
            nxtT3 = T3(nxt)
            nxteval = nxtT3.eval_ttt()
            if nxteval < maxeval:
                maxeval = nxteval
        return maxeval
        #return None
    #-----------------------------------------------------
#################################################################################    
    def grab_winO(self):
        toplay = self.two_XO('@')
        if toplay != None:
            print "... O grabs a a win at %s" % toplay
            return toplay
        return None

    #-----------------------------------------------------
    # MIDTERM: COMPLETE
    def grab_winX(self):
        toplay = self.two_XO('X')
        if toplay != None:
            print "... X grabs a a win at %s" % toplay
            return toplay
        return None
    #-----------------------------------------------------
##################################################################################        

    def two_XO(self,S):
        r2 = self.two_XO_row(S)
        c2 = self.two_XO_col(S)
        d2 = self.two_XO_diag(S)
        picks = r2
        picks.extend(c2)
        picks.extend(d2)
        while None in picks:
            picks.remove(None)
        if picks != []:
            block = random.choice(picks)
            if S == 'X':
                print "...two X to be blocked at %s" % block
            return block
        return None

    def two_XO_row(self,S):
        picks = []
        places = self.row1[:]
        for x in self.row1:
            if self.ttt[x] == S:
                places.remove(x)
        if len(places) == 1 and self.ttt[places[0]] == 0:
            picks.append(places[0])
        places = self.row2[:]
        for x in self.row2:
            if self.ttt[x] == S:
                places.remove(x)
        if len(places) == 1 and self.ttt[places[0]] == 0:
            picks.append(places[0])
        places = self.row3[:]
        for x in self.row3:
            if self.ttt[x] == S:
                places.remove(x)
        if len(places) == 1 and self.ttt[places[0]] == 0:
            picks.append(places[0])
        return picks

    def two_XO_col(self,S):
        picks = []
        places = self.col1[:]
        for x in self.col1:
            if self.ttt[x] == S:
                places.remove(x)
        if len(places) == 1 and self.ttt[places[0]] == 0:
            picks.append(places[0])
        places = self.col2[:]
        for x in self.col2:
            if self.ttt[x] == S:
                places.remove(x)
        if len(places) == 1 and self.ttt[places[0]] == 0:
            picks.append(places[0])
        places = self.col3[:]
        for x in self.col3:
            if self.ttt[x] == S:
                places.remove(x)
        if len(places) == 1 and self.ttt[places[0]] == 0:
            picks.append(places[0])
        return picks

    def two_XO_diag(self,S):
        picks = []
        places = self.dia1[:]
        for x in self.dia1:
            if self.ttt[x] == S:
                places.remove(x)
        if len(places) == 1 and self.ttt[places[0]] == 0:
            picks.append(places[0])     
        places = self.dia2[:]
        for x in self.dia2:
            if self.ttt[x] == S:
                places.remove(x)
        if len(places) == 1 and self.ttt[places[0]] == 0:
            picks.append(places[0])
        return picks
        
            
    # True if there is a full row of symbol 'symb'    
    def full_row(self,symb):
        rs = list(3*symb)
        return rs==self.rcd_values(self.row1) or\
               rs==self.rcd_values(self.row2) or\
               rs==self.rcd_values(self.row3)

    # True if there is a full col of symbol 'symb'
    def full_col(self,symb):
        rs = list(3*symb)
        return rs==self.rcd_values(self.col1) or\
               rs==self.rcd_values(self.col2) or\
               rs==self.rcd_values(self.col3)

    # True if there is a full diag of symbol 'symb'
    def full_diag(self,symb):
        rs = list(3*symb)
        return rs==self.rcd_values(self.dia1) or\
               rs==self.rcd_values(self.dia2)

    # True if X wins
    def winX(self):
        return self.full_row('X') or\
               self.full_col('X') or\
               self.full_diag('X')

    # True if O wins
    def winO(self):
        return self.full_row('@') or\
               self.full_col('@') or\
               self.full_diag('@')

    def full_board(self):
        return self.ttt.values().count(0) == 0

    # the game loop
    def play(self):
        self.reset()
        print "\n\n"
        print "Starting a new game of tictactoe. X begins ...\n"
        while not self.winX() and not self.winO():
            if self.full_board():
                print "\nX and O, you tie  :-|\n\n"
                break
        
            self.put_X()
            if self.winX():
                self.present()
                print "X, you win  :-))\n\n"
                break
            
            #self.random_O()
            if not self.full_board():
                self.response_O()
                if self.winO():
                    self.present()
                    print "O wins, you loose  :-((\n\n"
                    
        #----------------------------------------------------
        # NEW
        print "\nHow the game played out:\n"
        for (player,move,comment) in self.history:
            print "player %s picks %s (%s)" % (player,move,comment)
        print "\n"
        #----------------------------------------------------
        return
        

myttt = T3()
myttt.play()

            

    
               
   
                                   
