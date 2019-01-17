# dotbot_learnHW1.py

# to be completed in CSE 515 HW1, Winter 2018

# version of dotbot_learn.py that records sensor settings for positive
# experiences inorder to generalize learned moves ...

# by Kerstin Voigt, Jan 2018; inspired by Nils Nilsson, Introduction to
# Artificial Intelligence: A New Synthesis

# a version of dotbot_forever.py that "learns" to make those move that will
# have dotbot circle a wall forever. 

########################################################################################
# Rodolfo Diaz and Hector Medina
# Other colleagues who helped with this assignment: Frank Victoria and Allen Sokoupatham
#dotbot_learnHW1.py
#CSE 512: Winter 2018
#Dr. Voigt 
########################################################################################

from graphics import *
import random
import time

# global vars
WORLD_MAX_X = 500
WORLD_MAX_Y = 500
GRID = 20
WALL = {}
LMOVES = 1000
ENOUGH = 100

# a piece of wall (one square)

class Wall:
    def __init__(self):
        global WALL
        prompt = Text(Point(8*GRID, WORLD_MAX_Y - 2*GRID),\
                      "Click one square per click, twice for the last")
        prompt.draw(win)
        prompt_on = True

        click = win.getMouse()
        click1x = click.x - click.x % GRID
        click1y = click.y - click.y % GRID

        while True:
            if prompt_on:
                prompt_on = False
                prompt.undraw()

            WALL[(click1x,click1y)] = Rectangle(Point(click1x,click1y),\
                                                Point(click1x + GRID,\
                                                      click1y + GRID))
            WALL[(click1x,click1y)].setFill("black")
            WALL[(click1x,click1y)].draw(win)

            click = win.getMouse()
            click2x = click.x - click.x % GRID
            click2y = click.y - click.y % GRID

            if (click1x,click1y) == (click2x,click2y):
                break
    
            click1x = click2x
            click1y = click2y

    def draw(self):
        for loc in WALL.keys():
            WALL[loc].draw(win)

    def undraw(self):
        for loc in WALL.keys():
            WALL[loc].undraw()
            


# the dotbot robot ...   
class DotBot:
    def __init__(self,loc = Point(5*GRID,5*GRID), col="red", pwr = 100):
        self.location = loc
        self.previous = Point(-1,-1)
        self.color = col
        self.the_dotbot = Oval(self.location,\
                               Point(self.location.x + GRID, self.location.y + GRID))
        self.the_dotbot.setFill(self.color)
        self.power = pwr
        self.pos_experience = {}
        self.neg_experience = {}
        self.pos_exp_sensors = {} # HW1 notice: sensors for pos experience
        self.what_i_learned = {}  # HW1 notice: will hold the "learned" moves
                               
    def __str__(self):
        return "%s dotbot at (%d,%d) with power %d" % (self.color,\
                                             self.location.x,\
                                             self.location.y,self.power)

    def update_dotbot(self):
        self.the_dotbot.move(self.location.x - self.the_dotbot.p1.x,\
                             self.location.y - self.the_dotbot.p1.y)
        
    def draw(self):
        self.update_dotbot()
        self.the_dotbot.draw(win)

    def undraw(self):
        self.the_dotbot.undraw()

    # HW1 notice: the eight sensors
    def s1(self):
        return WALL.has_key((self.location.x - GRID, self.location.y - GRID))
            
    def s2(self):
        return WALL.has_key((self.location.x, self.location.y - GRID))
            

    def s3(self):
        return WALL.has_key((self.location.x + GRID, self.location.y - GRID))

    def s4(self):
        return WALL.has_key((self.location.x + GRID, self.location.y))

    def s5(self):
        return WALL.has_key((self.location.x + GRID, self.location.y + GRID))

    def s6(self):
        return  WALL.has_key((self.location.x, self.location.y + GRID))

    def s7(self):
        return WALL.has_key((self.location.x - GRID, self.location.y + GRID))

    def s8(self):
        return WALL.has_key((self.location.x - GRID, self.location.y))

    def at_wall(self):
        return self.s1() or self.s2() or self.s3() or\
               self.s4() or self.s5() or self.s6() or\
               self.s7() or self.s8()

    # HW1 notice: given current dotbot, will return a TUPLE with
    # sensor settings s1 to s8
    def sensors_1to8(self):
        s1to8 = [self.s1(), self.s2(), self.s3(),\
                 self.s4(), self.s5(), self.s6(),\
                 self.s7(), self.s8()]
        s1to8 = tuple([1 if x == True else 0 for x in s1to8])
        return s1to8

    def move_learn(self):
        # get all 8 sensor readings
        sensors = self.sensors_1to8()
        (herex,herey) = (self.location.x,self.location.y)
        if (herex,herey) in self.pos_experience.keys() and\
           not Point(self.pos_experience[(herex,herey)][0],\
                     self.pos_experience[(herex,herey)][1]) == self.previous:
            # a good move from here is know from positive experience
            # make this move ... 
            (newx,newy) = self.pos_experience[(herex,herey)]
            self.previous = self.location
            self.location = Point(newx, newy)
            print "make move (%d,%d)->(%d,%d) from pos exp" % (herex,herey,newx,newy)
            self.undraw()
            self.draw()
        else:
            now_at_wall = self.at_wall() # yes or not; need for below
            # make any possible move that is not included in neg_experience
            rand1to4 = range(1,5)
            random.shuffle(rand1to4)
            for select in rand1to4:
                if select == 1:
                    res = self.learn_up()
                    if res != None:
                        print "learning ... moving up"
                        break
                elif select == 2:
                    res = self.learn_down()
                    if res != None:
                        print "learning ... moving down"
                        break
                elif select == 3:
                    res = self.learn_left()
                    if res != None:
                        print "learning ... moving left"
                        break
                else:
                    res = self.learn_right()
                    if res!= None:
                        print "learning ... moving right"
                        break
            
            # test suggested move res; is neg experience if (a) has has crossed
            # wall boundary or (b) bot was at wall and has moved away from it or
            # (c) moves back to the previous location;
            # location is now set to res, but it will be reset to previous
            # if this looks like a bad move

            if res == None:
                print "ALL MOVES TRIED FROM (%d,%d)" %\
                      (self.location.x,self.location.y)
                # neg experience locks progress; reset to unlock
                # quit this move
                self.neg_experience[(herex,herey)] = []
                return
                
            if (res.x,res.y) in WALL.keys() or\
               now_at_wall and not self.at_wall() or\
               (res.x,res.y) == (self.previous.x,self.previous.y):

                # ... color switch below is not working ...
                
                self.undraw()
                #self.color = "yellow"
                self.draw()   # draw in yellow at bad location
                
                time.sleep(0.5)
                self.location = Point(herex,herey) 
                self.undraw()
                #self.color = "red"
                self.draw()   # move back and draw in red at old location
                
                if (herex,herey) in self.neg_experience.keys():
                    self.neg_experience[(herex,herey)].append((res.x,res.y))
                else:
                    self.neg_experience[(herex,herey)]= [(res.x,res.y)]
                    
            elif self.at_wall() and\
                 not (res.x,res.y) == (self.previous.x,self.previous.y):
                # a potentially good move; mark this as a new pos experience
                # unless the reverse move is already listed;
                if (res.x,res.y) in self.pos_experience.keys()and\
                   self.pos_experience[(res.x,res.y)] == (herex,herey):
                    pass
                else:
                    self.pos_experience[(herex,herey)] = (res.x,res.y)
                    self.previous = Point(herex,herey)
                    self.undraw()
                    self.draw()
                    # HW1 notice: records pos experience with sensor readings
                    self.pos_exp_sensors[(herex,herey)] =\
                            [(res.x,res.y),sensors]
                            
            else:
                # nothing speaks against this move ... just make it
                self.previous = Point(herex,herey)
                self.undraw()
                self.draw()

    # HW1 notice: the left/right/up/down moves
    def move_up(self):
        newloc = Point(self.location.x, self.location.y - GRID)
        if self.location.y >= GRID:
            self.location = newloc
      
    def move_down(self):
        newloc = Point(self.location.x, self.location.y + GRID)
        if self.location.y <= WORLD_MAX_Y - GRID:
            self.location = newloc
            
    def move_left(self):
        newloc = Point(self.location.x - GRID, self.location.y)        
        if self.location.x >= GRID:
            self.location = newloc

    def move_right(self):
        newloc = Point(self.location.x + GRID, self.location.y)
        if self.location.x <= WORLD_MAX_X - GRID:
            self.location = newloc

    # used when robot will move into one of four
    # direction (where); meant to be chosen at random
    def go(self,where):
        if where == 1:
            self.move_up()
        elif where == 2:
            self.move_down()
        elif where == 3:
            self.move_left()
        elif where == 4:
            self.move_right()
        else:
            pass
        self.undraw()
        self.draw()

    # ******************************************************
    # COMPLETE THE FOLLOWING THREE MEMBER FUNCTIONS:
    # Partial code below is "commented" because it will not
    # properly in its current form; uncomment as you work ... 
    
    # two xy-tuples, "from" location and "to" location,
    # determine whether this is a 'right', 'left', 'up' or
    # 'down' move; return any of these four strings as applicable;
    # in case no movement was made, return some neutral value;
     #In this function, it uses the coordinate system. So basically, if the data of: x1,y1 to x2,y2\
     #   changes, return a string that states which direction it moved. 

    def direction(self, fromxy,toxy):
        (x1,y1) = fromxy
        (x2,y2) = toxy
        # ... complete ... 
        
        if (x2 > x1):  #It's a right move
            right = 'right'
            return right

        elif (x1 > x2): #It's a left move
            left = 'left'
            return left

        elif (y2 < y1): #It's an up move        
            up = 'up'
            return up

        elif (y2 > y1): #It's a down move
            down = 'down'
            return down

        else :  #No movement; return a neutral value       
           #if no movement was made; Return some neutral value
            no_move = "Some Neutral Value"
            return no_move

##################################################################################################
    #For this function, we are filling in the what_i_learned data with sensor info and def direction
    #info. We need to fill this up to get a general sense of how the robot should be moving. 

    # to fill up directory data member self.what_i_learned with
    # associations of sensor info with move directions;
    def generalize_learned(self):
        for xy in self.pos_exp_sensors.keys():
            
            self.what_i_learned[self.pos_exp_sensors[xy][1]] =\
                self.direction(xy, self.pos_experience[xy])
            



##################################################################################################
    # apply knowledge of associations of sensor settings with directions
    # f moving to make a "good move";

    def move_by_know(self):
        s1to8 = self.sensors_1to8()
        if s1to8 in self.what_i_learned.keys():
            if (self.what_i_learned[s1to8] == 'up'):
                print (self.what_i_learned[s1to8])
                self.move_up()
                self.undraw()
                self.draw()
            elif(self.what_i_learned[s1to8] == 'down'):
                print (self.what_i_learned[s1to8])
                self.move_down()
                self.undraw()
                self.draw()
            elif(self.what_i_learned[s1to8] == 'left'):
                print (self.what_i_learned[s1to8])
                self.move_left()
                self.undraw()
                self.draw()
            elif(self.what_i_learned[s1to8] == 'right'):
                print (self.what_i_learned[s1to8])
                self.move_right()
                self.undraw()
                self.draw()
            # ... complete ...
        else:
            # in case there is no good move for the
            # sensed environment, a random move is made
            rnum = random.randint(1,4)
            self.go(rnum)
        return        

    
    # END COMPLETE
    #*****************************************************************
    
    # True if the transition from the current location to a
    # suggested new location is already known as a bad
    # prior experience
    
    def had_bad_experience(self,newloc):
        (oldx,oldy) = (self.location.x,self.location.y)
        (newx,newy) = (newloc.x, newloc.y)
        if (oldx,oldy) in self.neg_experience.keys():
            return (newx,newy) in self.neg_experience[(oldx,oldy)]

    # moving and learning ... 

    def learn_up(self):
        newloc = Point(self.location.x, self.location.y - GRID)
        if self.location.y >= GRID and\
           not self.had_bad_experience(newloc):
            self.location = newloc
            return newloc
        else:
            return None

    def learn_down(self):
        newloc = Point(self.location.x, self.location.y + GRID)
        if self.location.y <= WORLD_MAX_Y - GRID and\
           not self.had_bad_experience(newloc):
            self.location = newloc
            return newloc
        else:
            return None
            
    def learn_left(self):
        newloc = Point(self.location.x - GRID, self.location.y)        
        if self.location.x >= GRID and\
           not self.had_bad_experience(newloc):
            self.location = newloc
            return newloc
        else:
            return None

    def learn_right(self):
        newloc = Point(self.location.x + GRID, self.location.y)
        if self.location.x <= WORLD_MAX_X - GRID and\
           not self.had_bad_experience(newloc):
            self.location = newloc
            return newloc
        else:
            return None


# used to detect whether the robot has learned (= the robot's path keeps
# repeating the same sequence of moves;

def cyclic_list (lst):
    if len(lst) <= 1:
        return False
    elif len(lst) == 2 and lst[0] == lst[1]:
        return True
    else:
        target = lst[-1]
        #print "target is %s at index %d" % (target, len(lst)-1)
        i = -2
        repeat_at = None
        while True:
            if i < -len(lst):
                break
            if lst[i] == target:
                repeat_at = i
                #print "repeat of target %s at index %d" % (lst[i], i)
                break
            i -= 1
        if repeat_at == None:
            return False

        if 2*repeat_at + 1 < -len(lst):
            return False
        
        if lst[2*repeat_at + 1] == target:
            #print "2nd repeat of target %s at index %d" %\
            #(lst[2*repeat_at + 1], 2*repeat_at + 1)
            i1 = 2*repeat_at + 2
            i2 = repeat_at + 1
            while i2 < -1:
                if lst[i1] != lst[i2]:
                    return False
                i2 += 1
                i1 += 1
            return True


# CODE TO EXECUTE AS AS PART OF LOADING THIS MODULE
# (this could be a main function but doesn't have to be with Python


win = GraphWin("Dotbot World", WORLD_MAX_X, WORLD_MAX_Y)

for i in range(GRID,WORLD_MAX_Y,GRID):
    hline = Line(Point(0,i),Point(WORLD_MAX_X,i))
    hline.draw(win)
    vline = Line(Point(i,0),Point(i,WORLD_MAX_Y))
    vline.draw(win)

mywall = Wall()


plunkbot = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID), "Click square to place your DotBot")
plunkbot.draw(win)
click = win.getMouse()
plunkx1 = click.x - click.x % GRID
plunky1 = click.y - click.y % GRID
print "click to place at %d,%d" % (plunkx1, plunky1)
plunkbot.undraw()
mybot = DotBot(Point(plunkx1,plunky1))
mybot.draw()

start = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID), "Click to start the action -- twice to stop")
start.draw(win)

click = win.getMouse()
clickx1 = click.x - click.x % GRID
clicky1 = click.y - click.y % GRID
print "click at %d,%d" % (clickx1, clicky1)
start.undraw()


# LEARNING: dotbot learns to circle a given wall area; following successful
# learning, user is asked to provide four more (and different) wall areas
# on the same canvas, replace the robot, and test to what degree the robot's
# learning enables it to circle these other walls; 

count = 0
HAS_LEARNED = False
history = [(mybot.location.x,mybot.location.y)]

for m in range(LMOVES):
    time.sleep(0.25)
    print "%d. move_learn ..." % (m+1)
    mybot.move_learn()
    history.append((mybot.location.x,mybot.location.y))
    count += 1
    if count % ENOUGH == 0:
        if cyclic_list(history):
            '''
            learned = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID),\
                          "Dotbot has learned!!")
            learned.draw(win)
            '''
            time.sleep(1.0)
            #text.undraw()
            mybot.generalize_learned()
            
            HAS_LEARNED = True
            break
        
            
    else:
        pass

if HAS_LEARNED:
    for rounds in range(4):
        # demonstrate learning by applying new knowledge to circle
        # a different wall;
        #learned.undraw()
        #another = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID),\
        #            "Build another wall, place dotbot and start")
        #another.draw(win)
        mywall2 = Wall()
        #another.undraw()

        plunkbot = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID),\
                        "Click square to place your DotBot")
        plunkbot.draw(win)

        click = win.getMouse()
        plunkbot.undraw()
        plunkx1 = click.x - click.x % GRID
        plunky1 = click.y - click.y % GRID

        mybot.location = Point(plunkx1,plunky1)
        mybot.undraw()
        mybot.draw()

        start = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID), "Click to start the action -- twice to stop")
        start.draw(win)
        click = win.getMouse()
        clickx1 = click.x - click.x % GRID
        clicky1 = click.y - click.y % GRID
        start.undraw()

        i = 0
        while i < 100:
            mybot.move_by_know()
            time.sleep(0.2)
            i +=1

    text = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID),\
                "Click twice to quit")
    text.draw(win)
    win.getMouse()
    win.getMouse()
    win.close()
else:
    # after LMOVES many moves and not enough learning
    text = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID),\
                "Click twice to quit")
    text.draw(win)
    win.getMouse()
    win.getMouse()
    win.close()
 



        
                
            
        
    

    
            
