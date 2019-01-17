# Original: dotbot0.py -> Modified: cse512-lab-1.py
# by Kerstin Voigt, Sept 2014; inspired by Nils Nilsson, Introduction to
# Artificial Intelligence: A New Synthesis
# with modifications Jan 2016

# Modified on 1/21/16 by Brandon Saunders.
# Requirements: 
# 1. "mybot" wanders random until it finds itself next to a wall.
# 2. Once the "mybot" reaches a wall it circles it forever in the counter-clockwise motion. 

from graphics import *
import random
import time

# global vars
WORLD_MAX_X = 250
WORLD_MAX_Y = 250
GRID = 20
WALL = {}  # introduce GLOBAL VARIABLES and DIRECTORIES
WALL_ADDRESSES_X = []
WALL_ADDRESSES_Y = []


# Wall is a section of contiguous 20x20 black squares on the canvas;
# Wall object builds itself according to user input;

class Wall:
    def __init__(self):
        global WALL, CoordinatesX, CoordinatesY   # <<<< global

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

            # <<<<< why is GRID not declared above like WALL??
            WALL[(click1x,click1y)] = Rectangle(Point(click1x,click1y),\
                                                Point(click1x + GRID,\
                                                      click1y + GRID))
            WALL[(click1x,click1y)].setFill("black")
            WALL[(click1x,click1y)].draw(win)

            click = win.getMouse()
            click2x = click.x - click.x % GRID
            click2y = click.y - click.y % GRID

            # <<< the double-click to stop wall building;
            if (click1x,click1y) == (click2x,click2y):
                break
    
            click1x = click2x
            click1y = click2y

            WALL_ADDRESSES_X.append(click1x)
            WALL_ADDRESSES_Y.append(click1y)



    def draw(self):
        for loc in WALL.keys():
            WALL[loc].draw(win)

    # undrawing is needed for "animation"
    def undraw(self):
        for loc in WALL.keys():
            WALL[loc].undraw()


            


# the dotbot robot ... displayed as a circle; it has location, color, and power;   
class DotBot:
    
    # explain "constructor"
    def __init__(self,loc = Point(5*GRID,5*GRID), col="red", pwr = 100):
        self.location = loc
        self.color = col
        self.the_dotbot = Oval(self.location,\
                               Point(self.location.x + GRID, self.location.y + GRID))
        self.the_dotbot.setFill(self.color)
        self.power = pwr
                               
    # used when object is argument to "print" function; 
    def __str__(self):
        return "%s dotbot at (%d,%d) with power %d" % (self.color,\
                                             self.location.x,\
                                             self.location.y,self.power)
    
    # make sure that .location and  canvas coordinates where dotbot is
    # drawn  match up correctly; 
    def update_dotbot(self):
        self.the_dotbot.move(self.location.x - self.the_dotbot.p1.x,\
                             self.location.y - self.the_dotbot.p1.y)
        
    def draw(self):
        self.update_dotbot()
        self.the_dotbot.draw(win)

    def undraw(self):
        self.the_dotbot.undraw()

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
            pass # a no-op (non-opeation; place holder for instruction
        self.undraw()
        self.draw()
            
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

    def atWall(self, x, y):
        locx = self.location.x 
        locy = self.location.y 
        if (x,y) in WALL.keys():
            print("located in WALL")
            return True
        return False

    def atAnyWall(self):
        locx = self.location.x 
        locy = self.location.y 
        around = [(locx-GRID, locy-GRID),(locx,locy-GRID),(locx+GRID,locy-GRID),(locx+GRID,locy),(locx+GRID,locy+GRID),(locx,locy+GRID),(locx-GRID,locy+GRID),(locx-GRID,locy)]
        for loc in around:
            if self.atWall(loc[0],loc[1]):
                print("Near a wall")
                print(loc[0],loc[1])
                return True;
            
        return False

    def followWall(self, decision_made):
        # Temp variable to store the next move.
        decision = decision_made

        # Store the x,y coordinates of the current location. 
        locx = self.location.x
        locy = self.location.y

        # Re-label the locations for readability.
        topLeft_x = locx-GRID
        topLeft_y = locy-GRID
        topMiddle_x = locx
        topMiddle_y = locy-GRID
        topRight_x = locx+GRID
        topRight_y = locy-GRID
        rightSide_x = locx+GRID
        rightSide_y = locy
        leftSide_x = locx-GRID
        leftSide_y = locy
        bottomLeft_x = locx-GRID
        bottomLeft_y = locy+GRID
        bottomRight_x = locx+GRID
        bottomRight_y = locy+GRID
        bottomSide_x = locx
        bottomSide_y = locy+GRID

        # Labelling the states.
        x1 = 0
        x2 = 0
        x3 = 0
        x4 = 0

        # The top middle only.
        if (topMiddle_x,topMiddle_y) in WALL.keys():
            x1 = 1
        # The top right only.
        elif (topRight_x,topRight_y) in WALL.keys():
            x1 = 1
        else:
            x1 = 0

        # The right middle only.
        if (rightSide_x,rightSide_y) in WALL.keys():
            x2 = 1
        # The bottom right only.
        elif (bottomRight_x,bottomRight_y) in WALL.keys():
            x2 = 1
        else:
            x2 = 0

        # The bottom middle only.       
        if (bottomSide_x,bottomSide_y) in WALL.keys():
            x3 = 1
        # The bottom left only.
        elif (bottomLeft_x, bottomLeft_y) in WALL.keys():
            x3 = 1
        else:
            x3 = 0

        # The left middle only.
        if (leftSide_x, leftSide_y) in WALL.keys():
            x4 = 1
        # The top left only.
        elif (topLeft_x, topLeft_y) in WALL.keys():
            x4 = 1
        else:
            x4 = 0

        # Testing each combination of states.
        if x1 == 1 and x2 == 0:
            # Move east/right.
            decision = 4
            print("bottom side")
        if x2 == 1 and x3 == 0:
            # Move south/down.
            decision = 2
            print("left side")
        if x3 == 1 and x4 == 0:
            # Move west/left
            decision = 3
            print("top side")
        if x4 == 1 and x1 == 0:
            # Move north/up.
            decision = 1
            print("right side")
        else:
            print("No adjacent walls")
        
        # Move in the intended direction.
        self.go(decision)


# this could be a main function but doesn't have to be ...
# these lines will be executed as part of loading this file ...

win = GraphWin("Dotbot World", WORLD_MAX_X, WORLD_MAX_Y)

# define and display a grid
for i in range(GRID,WORLD_MAX_Y,GRID):
    hline = Line(Point(0,i),Point(WORLD_MAX_X,i))
    hline.draw(win)
    vline = Line(Point(i,0),Point(i,WORLD_MAX_Y))
    vline.draw(win)

# declare and display the dotbot
mybot = DotBot()
mybot.draw()

# declare/build wall space
mywall = Wall()

# interact with user
start = Text(Point(8*GRID, WORLD_MAX_Y-2*GRID), "Click to start the action -- twice to stop")
start.draw(win)

click = win.getMouse()
clickx1 = click.x - click.x % GRID
clicky1 = click.y - click.y % GRID
print "click at %d,%d" % (clickx1, clicky1)

# remove the prompt
start.undraw()

print(WALL.keys())

# repeat until double-click ... 
while True:
    direct = random.randint(1,4)

    mybot.followWall(direct)

    time.sleep(1)
   
    print "bot moved ..."


# two clicks to close ...
win.getMouse()
win.getMouse()
win.close()



    
    

    
            
