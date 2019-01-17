# resolve.py
# Lab 7
# Brandon Saunders
<<<<<<< Updated upstream
# 2/25/2016

=======
>>>>>>> Stashed changes

import copy

# ['item', 'item'] = clause
# ['item' = literal ]
CLS = [ ['notP', 'notQ', 'R'], ['P','R'], ['Q','R'], ['notR'] ]



# c1 same as c2, if both contain the same elements, but possibly 
# in a different order; iterate over one and test whether it is 
# present in the other;
def same_clause(c1, c2):
	if not len(c1) == len(c2):
		return False
	for x in c1:
		if not x in c2:
			return False
	return True

# returns complementary literals 
def contains_compl(c1,c2):
	for x in c1:
		cx = get_compl(x)
		for y in c2:
			if y == cx:
				return (x,cx)
	return None

# return complement of x; notX if x=X, X if x=notX
def get_compl(x):
	if len(x) > 3:
		if x[:3] == 'not':
			return x[3:]
		else:
			return 'not' + x
	return 'not' + x

<<<<<<< Updated upstream
def clause_with_compl(c3):
    for i in range(len(c3)-1):
        l1 = c3[i]
        for j in range(i,len(c3)):
            l2 = c3[j]
            if l2 == get_compl(l1):
                return True
    return False

# remove all duplicates elements from list
def no_dups(lst):
    s = set(lst)
    return list(s)
            
# if c3 not contained in cls (no clause in cls is "same"), then
# add c3 to cls and return new cls; if c3 contained, return cls
# unchanged;
def add_new_clause(cls,c3):
    # test whether c3 contains complementary literals;
    if clause_with_compl(c3):
        return cls
    # remove duplicate literals if there are any
    c3 = no_dups(c3)
    # do not add if c3 already in cls
    for x in cls:
        if same_clause(x,c3):
            return cls
    # c3 is new and added
    cls.append(c3)
    print " ... added"
    return cls

def resolve(cls):
    # implement algorithm from lab7 instructions ...
    N = 0
    M = N
    count = 0
    while count < 10000:
        count += 1
        for i in range(len(cls)-1):
            c1 = cls[i]
            for j in range(i,len(cls)):
                c2 = cls[j]
                print "checking %s and %s for compl literal ..." % (c1,c2)
                compl = contains_compl(c1,c2)
                if not compl == None:
                    print "Found compl lits (%s,%s)" % compl
                    c3 = copy.deepcopy(c1)
                    cp2 = copy.deepcopy(c2)
                    c3.extend(cp2)
                    c3.remove(compl[0])
                    c3.remove(compl[1])
                    print "new clause %s" % c3

                    if c3 == []:
                        return "UNSATISFIABLE :-)"
                    # add c3 to cls if not contained already
                    cls = add_new_clause(cls,c3)
                    N += 1
        if N > M:
            M = N
        else:
            ['R', 'R', 'R']            # N has not changes; no new resolvents
            return 'No Contradiction: Satisfiable'
    return

        
            
        
                    
print(resolve(CLS))

            
                
=======

def clause_with_compl(c3):
	for i in range(len(c3)-1):
		l1 = c3[i]
		for j in range(i,len(c3)):
			l2 = c3[j]
			if l2 == get_compl(l1):
				return True
	return False

# if c3 not contained in cls (no clause in cls is "same")
# add c3 to cls and return new cls; if c3 contained, return cls
# unchanged; 
def add_new_clause(cls, c3):
	for x in cls:
		if same_clause(x,c3):
			return cls
	cls.append(c3)
	#return cls

def resolve (cls):
	#implement algorithm from lab7 instructions ...
	N = 0
	M = 0
	count = 0
	while count < 1000:
		count += 1
		for i in range(len(cls)-1):
			c1 = CLS[i]
			for j in range(i,len(cls)):
				c2 = CLS[j]
				print("Checking for compl literal", c1, c2)
				compl = contains_compl(c1,c2)
				if not compl == None:
					print("Found compl lits", compl)
					c3 = copy.deepcopy(c1)
					cp2 = copy.deepcopy(c2)
					c3.extend(cp2)
					c3.remove(compl[0])
					c3.remove(compl[1])
					print("c3")
					if c3 == []:
						print("UNSATISFIABLE")
						return "UNSATISFIABLE"

					add_new_clause(cls, c3)
					N += 1
		if N > M:
			M == N
		else:
			return "No Contradiction: Satisfiable"
						

		print("CLS",cls)
		break



print( resolve(CLS))
>>>>>>> Stashed changes
