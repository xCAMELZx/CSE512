# donkey.py
# Kerstin Voigt, Feb 2018
# for CSE 512

# code to solve the "Red Donkey" problem
# with graphsearch (best-first and A-star)

# FIRST TASK: settle on a data structure

START = {1:[(0,1),(2,3)], 2:[(0,0),(2,1)], 3:[(0,3),(2,4)],\
         4:[(2,0),(4,1)], 5:[(2,1),(3,3)], 6:[(2,3),(4,4)],\
         7:[(3,1),(4,2)], 8:[(3,2),(4,3)], 9:[(4,0),(5,1)],\
         0:[(4,3),(5,4)]}


def donkey_hash(pz):
  hval = 0
  for k in pz.keys():
    [(x1,y1),(x2,y2)] = pz[k]
    hval += (x1+y1) * (x2*y2)
  return hval

# true if tile of puzz covers cell (x,y)

def covered_by(puzz,tile,xy):
  x = xy[0]
  y = xy[1]
  [(x1,y1),(x2,y2)] = puzz[tile]
  if x >= x1 and x < x2 and\
     y >= y1 and y < y2:
    return True
  return False

# print out the puzzle

def show_puzz(pz):
  for x in range(5):
    for y in range(4):
      # which tiles if any covers (x,y)?
      found = False
      for ti in pz.keys():
        if covered_by(pz,ti,(x,y)):
          print ti,
          found = True
          break
      if not found:
        print '~',
      #print "(%d,%d)" % (x,y),
    print  ""
  #print "\n"
  return

# in puzzle pz, tile is free on its right side

def clear_on_right(pz,tile):
  [(x1,y1),(x2,y2)] = pz[tile]
  if y2 == 4:
    return False
  for otherti in pz.keys():
    if otherti != tile:
      [(ox1,oy1),(ox2,oy2)] = pz[otherti]
      if (oy1 == y2 and ox1 >= x1 and ox1 < x2) or\
         (oy1 == y2 and ox2 <= x2 and ox2 > x1):
        return  False
  return True

# tile is free on its left side

def clear_on_left(pz,tile):
  [(x1,y1),(x2,y2)] = pz[tile]
  if y1 == 0:
    return False
  for otherti in pz.keys():
    if otherti != tile:
      [(ox1,oy1),(ox2,oy2)] = pz[otherti]
      if (oy2 == y1 and ox1 >= x1 and ox1 < x2) or\
         (oy2 == y1 and ox2 <= x2 and ox2 > x1):
        return  False
  return True

# tile is free below

def clear_below(pz,tile):
  [(x1,y1),(x2,y2)] = pz[tile]
  if x2 == 5:
    return False
  for otherti in pz.keys():
    if otherti != tile:
      [(ox1,oy1),(ox2,oy2)] = pz[otherti]
      if (ox1 == x2 and oy1 >= y1 and oy1 < y2) or\
         (ox1 == x2 and oy2 <= y2 and oy2 > y1):
        #print "tile %d is below tile %d" % (otherti,tile)
        return False
  return True

# tile is free above

def clear_above(pz,tile):
  [(x1,y1),(x2,y2)] = pz[tile]
  if x1 == 0:
    return False
  for otherti in pz.keys():
    if otherti != tile:
      [(ox1,oy1),(ox2,oy2)] = pz[otherti]
      if (ox2 == x1 and oy1 >= y1 and oy1 < y2) or\
         (ox2 == x1 and oy2 <= y2 and oy2 > y1):
        return  False
  return True

# just for code development, report which tiles
# are clear where

def report(pz):
  for ti in pz.keys():
    clears = 0
    if clear_on_right(pz,ti):
      print "Tile %d clear on right" % ti
      clears += 1
    if clear_on_left(pz,ti):
      print "Tile %d clear on left" % ti
      clears += 1
    if clear_above(pz,ti):
      print "Tile %d clear above" % ti
      clears += 1
    if clear_below(pz,ti):
      print "Tile %d clear below" % ti
      clears += 1
    if clears == 0:
      print "Tile %d boxed in" % ti
  return
  

# move tile of puzzle pz up, down, left,
# and right by 1 unit; no change if move
# cannot be done;

def move_up(pz,tile):
  if not clear_above(pz,tile):
    return pz
  newpz = pz.copy()
  [(x1,y1),(x2,y2)] = newpz[tile]
  newpz[tile] = [(x1-1,y1),(x2-1,y2)] 
  return newpz

def move_down(pz,tile):
  if not clear_below(pz,tile):
    return pz
  newpz = pz.copy()
  [(x1,y1),(x2,y2)] = newpz[tile]
  newpz[tile] = [(x1+1,y1),(x2+1,y2)] 
  return newpz

def move_right(pz,tile):
  if not clear_on_right(pz,tile):
    return pz
  newpz = pz.copy()
  [(x1,y1),(x2,y2)] = newpz[tile]
  newpz[tile] = [(x1,y1+1),(x2,y2+1)] 
  return newpz
  
def move_left(pz,tile):
  if not clear_on_left(pz,tile):
    return pz
  newpz = pz.copy()
  [(x1,y1),(x2,y2)] = newpz[tile]
  newpz[tile] = [(x1,y1-1),(x2,y2-1)] 
  return newpz  

# simply game loop 
def donkey():
  pz = START
  show_puzz(pz)
  while not solved(pz):
    what = raw_input("Move which tile? [0-9] ")
    how = raw_input("Which direction? [l,r,u,d] ")
    tile = int(what)
    if how == 'l':
      pz = move_left(pz,tile)
    elif how == 'r':
      pz = move_right(pz,tile)
    elif how == 'u':
      pz = move_up(pz,tile)
    elif how == 'd':
      pz = move_down(pz,tile)
    else:
      pass
    show_puzz(pz)
    bc = blocking2(pz)
    ev = donkey_eval(pz)
    print "(ev: %d, bc: %d)\n" % (ev,bc)
  return 

# puzzle solved when donkey (tile 1) can get out;

def solved(pz):
  [(x1,y1),(x2,y2)] = pz[1]
  return x1 == 3 and y1 == 1 and \
         x2 == 5 and y2 == 3


def donkey_goal(pz, target = None):
  return solved(pz)

def donkey_successors(pz):
  succ = []
  for ti in pz.keys():
    if clear_on_right(pz,ti):
      newpz = move_right(pz,ti)
      succ.append(newpz)
    if clear_on_left(pz,ti):
      newpz = move_left(pz,ti)
      succ.append(newpz)
    if clear_above(pz,ti):
      newpz = move_up(pz,ti)
      succ.append(newpz)
    if clear_below(pz,ti):
      newpz = move_down(pz,ti)
      succ.append(newpz) 
  return succ

def donkey_eval(pz, other = None, target = None):
  [(x1,y1),(_,_)] = pz[1]
  return abs(3-x1) + abs(1-y1)


def donkey_compact(pz):
  show_puzz(pz)
  




  





      
    
    
      

      
  
  
