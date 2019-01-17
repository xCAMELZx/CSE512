
# dotbot_forever.py

# by Kerstin Voigt, Sept 2014; inspired by Nils Nilsson, Introduction to
# Artificial Intelligence: A New Synthesis

# dobot will wander around until it finds the wall,  then circle the wall in
# counter clockwise direction forever; BEHAVIOR IS PROGRAMMED!!

# Implements sensors and features from Nils Nilsson

# with minor updates Jan 2018

# THIS  PROGRAM NEEDS graphics module ... PROVIDE!!

from graphics import *
import random
import time

# global vars
WORLD_MAX_X = 500
WORLD_MAX_Y = 500
GRID = 20
WALL = {}

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
        self.color = col
        self.the_dotbot = Oval(self.location,\
                               Point(self.location.x + GRID, self.location.y + GRID))
        self.the_dotbot.setFill(self.color)
        self.power = pwr
                               
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

    # seven sensors that help to locate bot relative to wall space
#    def s1(self):
#        return WALL.has_key((self.location.x - GRID, self.location.y - GRID))
#
#    def s2(self):
#        return WALL.has_key((self.location.x, self.location.y - GRID))

#    def s3(self):
#        return WALL.has_key((self.location.x + GRID, self.location.y - GRID))

#    def s4(self):
#        return WALL.has_key((self.location.x + GRID, self.location.y))

#    def s5(self):
#        return WALL.has_key((self.location.x + GRID, self.location.y + GRID))

#    def s6(self):
#        return  WALL.has_key((self.location.x, self.location.y + GRID))

#    def s7(self):
#        return WALL.has_key((self.location.x - GRID, self.location.y + GRID))

#    def s8(self):
#        return WALL.has_key((self.location.x - GRID, self.location.y))

    # features that are the relevant composits of sensor readings
#    def x1(self):
#        return self.s2() or self.s3()
#
#    def x2(self):
#        return self.s4() or self.s5()
#
#    def x3(self):
#        return self.s6() or self.s7()
#
#    def x4(self):
#        return  self.s8() or self.s1()

    # True when bot is in next to wall
    def at_wall(self):
        return self.s1() or self.s2() or self.s3() or\
               self.s4() or self.s5() or self.s6() or\
               self.s7() or self.s8()

    # moving counter-clockwise around wall that
    # bot is next to (only works when bot is
    # already at wall;
#    def move_ccw(self):
#        if self.x1() and not self.x2():
#            self.move_right()
#        elif self.x2() and not self.x3():
#            self.move_down()
#        elif self.x3() and not self.x4():
#            self.move_left()
#        elif self.x4 and  not self.x1():
#            self.move_up()
#        else:
#            pass
#        self.undraw()
#        self.draw()
                            
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

    # changing dot location one space up, down, left, right
    # notice: sets location but does not draw bot
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

    
# this could be a main function but doesn't have to be ...
# these lines will be executed as part of loading this file ...

win = GraphWin("Dotbot World", WORLD_MAX_X, WORLD_MAX_Y)

for i in range(GRID,WORLD_MAX_Y,GRID):
    hline = Line(Point(0,i),Point(WORLD_MAX_X,i))
    hline.draw(win)
    vline = Line(Point(i,0),Point(i,WORLD_MAX_Y))
    vline.draw(win)

mybot = DotBot() # at defaulty location
mybot.draw()     # display

# to generate wall space; in interaction with user;
mywall = Wall()

# user clicks once to start bot action
start = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID), "Click to start the action -- twice to stop")
start.draw(win)
click = win.getMouse()
clickx1 = click.x - click.x % GRID
clicky1 = click.y - click.y % GRID

print "click at %d,%d" % (clickx1, clicky1)  # for log

start.undraw() # remove prompt from window

# robot roams around in random movement until if finds
# itself next to some wall space
while True:
#not mybot.at_wall():
    mybot.go(random.randint(1,4))
    time.sleep(0.25)

print "bot is now at wall ... keep circling!"  # for log

# bot executes 1000 moves circling the wall space
# in counter-clockwise direction

#k = 1000
#while k > 0:
#    time.sleep(0.15)
#    #win.getMouse()
#    mybot.move_ccw()
#    print "moved ccw ..."
#    k -= 1

win.getMouse()
win.getMouse()
win.close()
    
    
#############################
    
    

    
            
