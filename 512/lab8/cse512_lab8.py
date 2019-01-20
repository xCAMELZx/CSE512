# cse512_lab8.py
# KV, Mar 2018, solution for lab8 and beyond

import copy
import itertools  # just to try it out; used once, see below
import random

CLS = [['notP', 'notQ', 'R'],  ['P', 'R'], ['Q', 'R'], ['notR']]

# set up to prove that H2CO3 by contradicting notH2CO3
CHEM = [['notCO2', 'notH2O','H2CO3'], ['notC', 'notO2', 'CO2'],\
        ['notMgO', 'notH2', 'Mg'], ['notMgO', 'notH2','H2O'],
        ['MgO'], ['H2'], ['O2'], ['C'], ['notH2CO3']]

# CHEM with positive H2CO3 ... resolve should terminate with
# failure to find contradiction
CHEM2 = [['notCO2', 'notH2O','H2CO3'], ['notC', 'notO2', 'CO2'],\
        ['notMgO', 'notH2', 'Mg'], ['notMgO', 'notH2','H2O'],
        ['MgO'], ['H2'], ['O2'], ['C'], ['H2CO3']]

def is_neg(x):
  if len(x) >= 4 and x[:3] == 'not':
    return True
  return False

def complements(x,y):
  if is_neg(x) and not is_neg(y):
    if x[3:] == y:
      return (x,y)
    else:
      return  None
  elif not is_neg(x) and is_neg(y):
    if x == y[3:]:
      return (x,y)
    else:
      return None
  else:
    return None

# does lst1 contain variable that has complement in lst1
def have_complements(lst1, lst2):
  for x in lst1:
    for y in lst2:
      comps = complements(x,y)
      if comps != None:
        return comps
  return None
        
def contains_comps(lst):
  if len(lst) <= 1:
    return False
  pairs = itertools.combinations(lst,2)
  for (x,y) in pairs:
    if complements(x,y):
      return True
  return False

def is_same(lst1, lst2):
  if len(lst1) != len(lst2):
    return False
  return len(set(lst1).intersection(set(lst2))) == len(lst1)

# true if lst contains a member that is_same as x
def member(x, lst):
  for y in lst:
    if is_same(x,y):
      return True
  return False

# call this function to APPLY RESOLUTION

def resolve (cls):
  thecls = copy.deepcopy(cls)
  random.shuffle(thecls)
  steps = 1
  n = len(cls)
  while True:
    oldn = n
    for i in range(len(thecls)-1):
      res_found = False
      for j in range(i,len(thecls)):
        c1 = thecls[i][:] # copy
        c2 = thecls[j][:] # copy
        #print "TRYING %s and %s" % (c1,c2)

        comps = have_complements(c1,c2)
    
        if comps == None:
          continue

        # c1 and c2 are complements
        # combine c1 and c2 into c3 minus x and cx
        (x,cx) = comps
        c3 = c1
        for y in c2:
          if not y in c3:
            c3.append(y)

        #print "c3 before removal of comps: %s" % c3
        c3.remove(x)
        c3.remove(cx)
        #print "c3 after removal of comps: %s" % c3

        if c3 == []:
          print "%d. %s with %s ==> []" % (steps,thecls[i],thecls[j])
          return  'UNSATISFIABLE -- CONTRADICTION'

        if contains_comps(c3):
          #print "c3 contains complements -- ignore"
          continue
        
        if member(c3,thecls):
          #print "c3 already exists in thecls -- ignore"
          #print "thecls: %s" % thecls
          continue
        
        thecls.append(c3)
        print "%d. %s with %s ==> %s" % (steps,thecls[i],thecls[j],c3) 
        n += 1
        steps += 1
        res_found = True
        break # from inner for-loop
      if res_found:
        break # from outer for-loop
      
    if n == oldn:
      return 'SATISFIABLE -- NO CONTRADICTION'
    





    
  
  










  
  
    
  
    
    
