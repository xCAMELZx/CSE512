# Tiles1to8.py
# KV Jan 2019, to support 8-puzzle graphics

from graphics import *
import random
import pickle
import bestfirst_astar_search

TBASE = 30
WIN_MAX_X = 7*TBASE*3
WIN_MAX_Y = 7*TBASE*3
SOLVED = False
RECENT_SETUP = None

class Tiles1to8_Frame:
  def __init__(self, soln = None, stateinit = None):
    
    self.A1 = Point(0,0)
    self.A2 = Point(7*TBASE,0)
    self.A3 = Point(14*TBASE,0)
    self.A4 = Point(0,7*TBASE)
    self.A5 = Point(7*TBASE,7*TBASE)
    self.A6 = Point(14*TBASE,7*TBASE)
    self.A7 = Point(0, 14*TBASE)
    self.A8 = Point(7*TBASE,14*TBASE)
    self.A9 = Point(14*TBASE,14*TBASE)

    # Ai are the anchor points for the tiles (upperleft corner)
    if stateinit != None:
      self.state = {}
      a_index = 1
      #print "setting up with stateinit %s" % stateinit
      for tval in stateinit:
        #print "self.state[%d] <- %s" % (tval,eval('self.A%d' % a_index))
        self.state[tval] = eval('self.A%d' % a_index)

        if tval == 0:
          self.blank = self.state[tval]
          
        a_index += 1
    else:
      self.state = {1:self.A1, 2:self.A2, 3:self.A3,\
                    4:self.A6, 5:self.A9, 6:self.A8,\
                    7:self.A7, 8:self.A4, 0:self.A5}
      self.blank = self.A5

    # the list of tile objects
    self.thetiles = {}
    for tval in range(9):     
      tile = Tile1to8(self.state[tval],tval)
      self.thetiles[tval] = tile
      #self.thetiles.append(tile)

    self.solution = {}
    if soln != None:
      a_index = 1
      for tsol in soln:
        self.solution[tsol] = eval('self.A%d' % a_index)
        a_index += 1
    else:
      self.solution = None

      
  def is_solved(self):
      global SOLVED
      for tval in range(9):
        if self.state[tval].x != self.solution[tval].x or\
           self.state[tval].y != self.solution[tval].y:
          return False
      # self.state matches up with self.solution
      SOLVED = True
      msg = Text(Point(self.blank.x + 3*TBASE,\
                       self.blank.y + 3*TBASE), "SOLVED :-)")
      msg.draw(win)
      return True
        
          
  def draw(self):
    for tval in range(9):      
      self.thetiles[tval].draw()

  def undraw(self):
    for tval in range(9):
      self.thetiles[tval].undraw()

  # identify tile by clickpoint,
  # return tile object
  def tile_by_click(self,clickpt):
    cx = clickpt.x
    cy = clickpt.y

    print "cx: %d, cy: %d\n" % (cx,cy)
    # integer div
    ax = int(cx / (7*TBASE))
    ay = int(cy / (7*TBASE))

    print "ax: %d, ay: %d\n" % (ax,ay)

    for tval in range(9):
      print "checking state[%d].x of %d" % (tval,self.state[tval].x)
      print "checking state[%d].y of %d" % (tval,self.state[tval].y)
      print "against %d,%d\n" % (ax*7*TBASE,ay*7*TBASE)
      
      if self.state[tval].x == ax*210 and\
         self.state[tval].y == ay*210:
        return self.thetiles[tval]
    return None

  # tile objects above,below,left of, right of blank
  # returns list of neighboring tile with orientation
  # to set up swap
  def tiles_about_blank(self):
    blk = self.thetiles[0]
    anchor_blk = self.state[0]
    bx = anchor_blk.x
    by = anchor_blk.y

    about = []
    for tval in range(1,9):
      tile = self.thetiles[tval]
      if  tile.lowerleft.y == by:
        if tile.lowerright.x == bx:
          about.append((tile,'toleft'))
        elif tile.lowerleft.x == bx + 7*TBASE:
          about.append((tile,'toright'))
        else:
          pass
      elif tile.lowerleft.x == bx:
        if tile.upperleft.y == by:
          about.append((tile,'above'))
        elif tile.lowerleft.y == by + 7*TBASE:
          about.append((tile,'below'))
        else:
          pass
    return about
  
    # given a click point, the tile is identified;
    # it should be other than blank tile, and it should
    # be among the ones that are "about" the blank
    # if so, swap blank tile wit clicked tile: (1) undraw
    # both tiles, recompute tile specs relative to new
    # achor point, redraw both tiles

  def random_start(self,k):
    global RECENT_SETUP
    RECENT_SETUP = None
    random.seed()
    ind = range(1,8)
    random.shuffle(ind)
    for i in ind[:k]:
      self.make_move(True) # in setup move ... 
      
  def make_move(self, setup = False):
    global RECENT_SETUP
    blank = self.thetiles[0]
    tiles_about = self.tiles_about_blank()
    if not setup:
      click = win.getMouse()
      target = self.tile_by_click(click)
      #blank = self.thetiles[0]
      while target.lowerleft.x == blank.lowerleft.x and\
            target.lowerleft.y == blank.lowerleft.y:
        click = win.getMouse()
        target = self.tile_by_click(click)
      print "... moving tile %d" % target.value
    
      # target tile is not blank; is target "about" blank?
      # tiles_about = self.tiles_about_blank()
      for (tile,orient) in tiles_about:
        if target.lowerleft.x == tile.lowerleft.x and\
           target.lowerleft.y == tile.lowerleft.y:
          # clicked target tile is a tile about blank

          print " ... swapping tile with blank"
          self.swap_tile_with_blank(target)
          return
      print "bad news ... no swapping happened"
    else:
      # in setup mode used by random_start
      # get tiles around blank and randomly selecgt
      # one to execute ...
      (target, orient) = random.choice(tiles_about)
      while target.value == RECENT_SETUP:
        (target, orient) = random.choice(tiles_about)    
      print "setup move ... tile %d, %s" % (target.value, orient)
      self.swap_tile_with_blank(target)
      RECENT_SETUP = target.value
    return

  def swap_tile_with_blank(self,tile):
    blank = self.thetiles[0]
    # undraw the the two affected tiles
    tile.undraw()
    blank.undraw()
    # tile becomes blank and blank becomes tile
    # swap anchor point assignments, values and  lowerleft corners;
    # then recompute dots etc. 
    A_tilex = self.state[tile.value].x
    A_tiley = self.state[tile.value].y
    A_blankx = self.state[0].x
    A_blanky = self.state[0].y
    
    self.state[tile.value] = Point(A_blankx,A_blanky)
    self.state[0] = Point(A_tilex,A_tiley)
    self.blank = self.state[0]

    newtile = Tile1to8(Point(A_blankx,A_blanky),tile.value)
    newblank = Tile1to8(Point(A_tilex,A_tiley),0)

    self.thetiles[tile.value] = newtile
    self.thetiles[0] = newblank

    # redraw ...
    newtile.draw()
    newblank.draw()
    return

  def make_start(self,k):
    for i in range(k):
      self.make_move(True) # make move in "setting up mode"
    return
      


class Tile1to8:
  def __init__ (self, llf = Point(0,0), val = 1):
    self.lowerleft = llf
    self.upperleft = Point(self.lowerleft.x,self.lowerleft.y+7*TBASE)
    self.lowerright = Point(self.lowerleft.x+7*TBASE,self.lowerleft.y)
    self.upperright = Point(self.lowerright.x,self.upperleft.y)

    self.value = val

    self.a = Point(self.lowerleft.x + 1.5*TBASE,\
                   self.lowerleft.y + 1.5*TBASE)
    self.b = Point(self.lowerleft.x + 5.5*TBASE,\
                   self.lowerleft.y + 1.5*TBASE)
    self.c = Point(self.lowerleft.x + 3.5*TBASE,\
                   self.lowerleft.y + 2.5*TBASE)
    self.d = Point(self.lowerleft.x + 1.5*TBASE,\
                   self.lowerleft.y + 3.5*TBASE)
    self.e = Point(self.lowerleft.x + 3.5*TBASE,\
                   self.lowerleft.y + 3.5*TBASE)
    self.f = Point(self.lowerleft.x + 5.5*TBASE,
                   self.lowerleft.y + 3.5*TBASE)
    self.g = Point(self.lowerleft.x + 3.5*TBASE,\
                   self.lowerleft.y + 4.5*TBASE)
    self.h = Point(self.lowerleft.x + 1.5*TBASE,
                   self.lowerleft.y + 5.5*TBASE)
    self.i = Point(self.lowerleft.x + 5.5*TBASE,
                   self.lowerleft.y + 5.5*TBASE)

    self.theborder = [Line(self.lowerleft, self.lowerright),\
                      Line(self.upperleft, self.upperright),\
                      Line(self.lowerleft, self.upperleft),\
                      Line(self.lowerright, self.upperright)]

    self.blk_cover = None
    if self.value == 0:
      # the blank tile "cover"object
      self.blk_cover = Rectangle(self.lowerleft,\
                                 Point(self.lowerleft.x+7*TBASE,\
                                       self.lowerleft.y+7*TBASE))

    self.thedots = []
    self.create_dots()
    return

  # rainbow mode on when puzzle solved
  def draw(self): 
    if self.value == 0:
      self.blk_cover.setFill("grey")
      self.blk_cover.draw(win)   
    else:
      for dot in self.thedots:
        dot.setFill("black")
        dot.draw(win)
      
    for line in self.theborder:
      line.setWidth(4)
      line.draw(win)
                                
  # leave the border; no need to undraw
  def undraw(self):
      if self.value == 0:
        self.blk_cover.undraw()
      else:
        for dot in self.thedots:
          dot.undraw()
  
  # creates list of dot objects
  def create_dots(self):
    if self.value == 0:
      return
    if self.value == 1:
      self.thedots.extend(self.one_dot())
    elif self.value == 2:
      self.thedots.extend(self.two_dots())
    elif self.value == 3:
      self.thedots.extend(self.three_dots())
    elif self.value == 4:
      self.thedots.extend(self.four_dots())
    elif self.value == 5:
      self.thedots.extend(self.five_dots())
    elif self.value == 6:
      self.thedots.extend(self.six_dots())
    elif self.value == 7:
      self.thedots.extend(self.seven_dots())
    elif self.value == 8:
      self.thedots.extend(self.eight_dots())
    else:
      pass
    
  def one_dot(self):
    # create center dot e
    dot = Circle(self.e, TBASE/2)
    return [dot]

  def two_dots(self):
    # create dots c and g
    dotc = Circle(self.c, TBASE/2)
    dotg = Circle(self.g, TBASE/2)
    return [dotc,dotg]
  
  def three_dots(self):
    # dots h,e,b
    doth = Circle(self.h, TBASE/2)
    dote = Circle(self.e, TBASE/2)
    dotb = Circle(self.b, TBASE/2)
    return [dotb,dote,doth]
    
  def four_dots(self):
    # dots a,b,h,i,
    doth = Circle(self.h, TBASE/2)
    dota = Circle(self.a, TBASE/2)
    dotb = Circle(self.b, TBASE/2)
    doti = Circle(self.i, TBASE/2)
    return [dota,dotb,doth,doti]

  def five_dots(self):
    d1 = self.four_dots()
    d2 = self.one_dot()
    return d1+d2
  
  def six_dots(self):
    d = self.four_dots()
    # and dots d and f
    dotd = Circle(self.d, TBASE/2)
    dotf = Circle(self.f, TBASE/2)
    d.extend([dotd,dotf])
    return d

  def seven_dots(self):
    d1 = self.six_dots()
    d2 = self.one_dot()
    return d1+d2
    

  def eight_dots(self):
    d1 = self.six_dots()
    d2 = self.two_dots()
    return d1 + d2
  
  #just for testing
  def all_dots(self):
    self.eight_dots()
    self.one_dot()

# simulate the moves along the "path"; path holds the sequence of all
# puzzle states from start to solution; the value of path is retrieved
# from the a .pickle file; 

def run_path(pickle_file):
  frompickle = open(pickle_file, "rb")
  path = pickle.load(frompickle)
  frompickle.close()
  
  count = 1
  for state in path[:-1]:
    init1to8 = bestfirst_astar_search.make_1to8_init_list(state)
    print "Step %d. init state with %s" % (count,init1to8)
    count += 1
    tiles1to8 = Tiles1to8_Frame(None,init1to8)
    tiles1to8.draw()
    time.sleep(1.5)
    tiles1to8.undraw()
  # draw last state and quit
  init1to8 = bestfirst_astar_search.make_1to8_init_list(path[-1])
  print "Step %d. init state with %s" % (count,init1to8)
  count += 1
  tiles1to8 = Tiles1to8_Frame(init1to8,init1to8)
  tiles1to8.draw()
  tiles1to8.is_solved()
  return
    
if __name__ =='__main__':
                     
  dowhat = raw_input("Play(Y) or Pickle(P)? ")

  if dowhat == "Y" or dowhat == 'y':

    # Solve the puzzle in interactive game ...
    win = GraphWin("The Eight-Puzzle", WIN_MAX_X, WIN_MAX_Y)
    
    my1to8 = Tiles1to8_Frame([1,2,3,8,0,4,7,6,5])
    my1to8.draw()

    my1to8.random_start(5)

    click = win.getMouse()
    
    for i in range(100):
      my1to8.make_move()
      if my1to8.is_solved():
        print "THE 8-PUZZLE IS SOLVED :-)"
        break
    
    click = win.getMouse()
    win.close()

  elif dowhat == "P" or dowhat == "p":

    # Demonstrate a pickled solution path

    pf = raw_input("Name of the .pickle file: ")
    pf = pf + '.pickle'

    win = GraphWin("The Eight-Puzzle", WIN_MAX_X, WIN_MAX_Y)
    run_path(pf)

    click = win.getMouse()
    win.close()

  else:
    print "Invalid Selection"

  
    
    
    
  
  
    



    





    
    






    
    




      




      

  
    

  
    
    
        
