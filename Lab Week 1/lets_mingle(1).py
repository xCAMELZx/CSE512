# lets_mingle.py

# by Kerstin Voigt, Jan 2019; a starter (demo) program for CSE 512

from graphics import *  
import random
import time

WORLD_MAX_X = 500
WORLD_MAX_Y = 500
GRID = 20

# the "dotbot" robot;

class dotbot:
    def __init__(self,loc = Point(100,100), col="red", pwr = 100):
        self.location = loc
        self.color = col
        self.the_dotbot = Oval(self.location,\
                               Point(self.location.x + 20, self.location.y + 20))
        #self.the_dotbot.setFill(self.color)
        self.power = pwr
                               
    def __str__(self):
        return "%s dotbot at (%d,%d) with power %d" % (self.color,\
                                             self.location.x,\
                                             self.location.y,self.power)

    def update_dotbot(self):
        self.the_dotbot.move(self.location.x - self.the_dotbot.p1.x,\
                             self.location.y - self.the_dotbot.p1.y)
        self.update_power()
        
    def update_color(self):
        if self.power <= 0:
            self.color = "black"
        else:
            if self.power > 100:
                self.color = "green"
            elif self.power >= 80:
                self.color = "red"
            elif self.power >= 60:
                self.color = "orange"
            elif self.power >= 30:
                self.color = "yellow"
            elif self.power > 0:
                self.color = "purple"
            else:
                pass

    def update_power(self):
        if self.power < 0:
            self.power = 0
        
    def draw(self):
        self.update_dotbot()
        self.update_color()
        self.the_dotbot.setFill(self.color)
        self.the_dotbot.draw(win)

    def undraw(self):
        self.the_dotbot.undraw()

    # for now ...
    def is_blocked(self,loc):
        return False

    def go(self,where):
        if self.power <= 0:
            return
        if where == 1:
            for i in range(random.randint(1,5)):
                self.move_up()
        elif where == 2:
            for i in range(random.randint(1,5)):
                self.move_down()
        elif where == 3:
            for i in range(random.randint(1,5)):
                self.move_left()
        elif where == 4:
            for i in range(random.randint(1,5)):
                self.move_right()
        else:
            pass
            
    def move_up(self):
        newloc = Point(self.location.x, self.location.y - GRID)
        if self.location.y >= GRID and not self.is_blocked(newloc):
            #self.the_dotbot.undraw()
            self.location = newloc
            #self.the_dotbot.draw(win)
            self.power -= 5
        
    def move_down(self):
        newloc = Point(self.location.x, self.location.y + GRID)
        if self.location.y <= WORLD_MAX_Y - GRID and not self.is_blocked(newloc):
            #self.the_dotbot.undraw()
            self.location = newloc
            #self.the_dotbot.draw(win)
            self.power -= 5
            
    def move_left(self):
        newloc = Point(self.location.x - GRID, self.location.y)        
        if self.location.x >= GRID and not self.is_blocked(newloc):
            #self.the_dotbot.undraw()
            self.location = newloc
            #self.the_dotbot.draw(win)
            self.power -= 5

    def move_right(self):
        newloc = Point(self.location.x + GRID, self.location.y)
        if self.location.x <= WORLD_MAX_X - GRID and not self.is_blocked(newloc):
            #self.the_dotbot.undraw()
            self.location = newloc
            #self.the_dotbot.draw(win)
            self.power -= 5

    def recharge(self,pwr):
        self.power += pwr

    def is_awake(self):
        return self.power > 0

    def is_asleep(self):
        return self.power <= 0

    def colliding(self, other):
        return (self.location.x,self.location.y) == (other.location.x, other.location.y)

    def meeting(self,other):
        return (self.location.x,self.location.y) == (other.location.x - GRID, other.location.y) or\
               (self.location.x,self.location.y) == (other.location.x + GRID, other.location.y) or\
               (self.location.x,self.location.y) == (other.location.x, other.location.y - GRID) or\
               (self.location.x,self.location.y) == (other.location.x, other.location.y + GRID)


    def handle_collide(self,other):
        if self.power >= 10:
            self.power -= 10
        else:
            self.power = 0
        if other.power >= 10:
            other.power -= 10
        else:
            other.power = 0

    def handle_meeting(self,other):
        self.power += 5
        other.power += 5

class Society:
    def __init__(self,k = 10):
        self.members = k
        self.queue = []
        for i in range(self.members):
            wx = random.randint(GRID,480)
            wy = random.randint(GRID,480)
            wx = wx - wx % GRID
            wy = wy - wy % GRID
            self.queue.append(dotbot(Point(wx,wy)))

        for i in range(self.members):
            for j in range(i+1,self.members):
                #print "checking %d. and %d." % (i,j)
                if self.queue[i].colliding(self.queue[j]):
                    self.queue[i].handle_collide(self.queue[j])
                    #print "collision"
                elif self.queue[i].meeting(self.queue[j]):
                    self.queue[i].handle_meeting(self.queue[j])
                    #print "meeting"
                else:
                    pass

        print "Society of %d members is built ..." % self.members
            
    def draw(self):
        for w in self.queue:
            print "draw %s" % w
            w.draw()

    def redraw(self):
        for w in self.queue:
            w.undraw()
        self.draw()

    def pulse(self):
        #random.seed()
        random.shuffle(self.queue)

        for w in self.queue[:5]:
            w.go(random.randint(1,4))

        for i in range(5):
            for j in range(i+1,5):
                if self.queue[i].colliding(self.queue[j]):
                    self.queue[i].handle_collide(self.queue[j])
                elif self.queue[i].meeting(self.queue[j]):
                    self.queue[i].handle_meeting(self.queue[j])
                else:
                    pass

        self.redraw() 

    def lets_mingle(self, rounds = 100):
        if self.members <= 0:
            return
        k = rounds
        while k > 0:
            #click = win.getMouse()
            time.sleep(0.15)
            self.pulse()
            k-=1

    
        

win = GraphWin("Dotbot World", 500, 500)

for i in range(20,1000,20):
    hline = Line(Point(0,i),Point(500,i))
    hline.draw(win)
    vline = Line(Point(i,0),Point(i,500))
    vline.draw(win)

wsoc = Society(50)
wsoc.draw()
wsoc.lets_mingle(200)
click = win.getMouse()
win.close()



    
            
