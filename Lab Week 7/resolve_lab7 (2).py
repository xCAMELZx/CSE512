##
##Nick Chiodini
##Yousef Jarrar
##CSE 512
##HW 3
##


import copy
import itertools  
import random

CLS = [['notP', 'notQ', 'R'],  ['P', 'R'], ['Q', 'R'], ['notR']]

CLS_SAT = [['notP', 'notQ', 'R'],  ['P', 'R'], ['Q', 'R'], ['R']]

CLS_H2CO3 = [['notCO2', 'notH2O','H2CO3'], ['notC', 'notO2', 'CO2'],\
        ['notMgO', 'notH2', 'Mg'], ['notMgO', 'notH2','H2O'],
        ['MgO'], ['H2'], ['O2'], ['C'], ['notH2CO3']]



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

#check for compliments
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


def member(x, lst):
  for y in lst:
    if is_same(x,y):
      return True
  return False

#lab 7 algorithm

def resolve (cls):
  maincls = copy.deepcopy(cls)
  random.shuffle(maincls)
  steps = 1
  n = len(cls)
  while True:
    oldn = n
    for i in range(len(maincls)-1):
      res_found = False
      for j in range(i,len(maincls)):
        c1 = maincls[i][:] # make a copy
        c2 = maincls[j][:] # make a copy
       

        comps = have_complements(c1,c2)
    
        if comps == None:
          continue

        # c1 and c2 are complements
        # combine c1 and c2 into c3
        (x,cx) = comps
        c3 = c1
        for y in c2:
          if not y in c3:
            c3.append(y)

        c3.remove(x)
        c3.remove(cx)
        

        if c3 == []:
          print "%d. %s with %s -> []" % (steps,maincls[i],maincls[j])
          return  'UNSATISFIABLE AKA CONTRADICTION'

        if contains_comps(c3):
          #print "c3 contains complements -- ignore"
          continue
        
        if member(c3,maincls):
          continue
        
        maincls.append(c3)
        print "%d. %s with %s -> %s" % (steps,maincls[i],maincls[j],c3) 
        n += 1
        steps += 1
        res_found = True
        break # from inner loop
      if res_found:
        break # from outer loop
      
    if n == oldn:
      return 'SATISFIABLE AKA NO CONTRADICTION'

##print (resolve(CLS))

##print (resolve(CLS_SAT))

##print (resolve(H2CO3))
