# This is a program to emulate the problem of filling and emptying jugs. 
# Goal: The goals state is one jug to have 2 liters and another jug empty.
# Brandon Saunders
# 2/16/2016
# Possible solution:
# Jug A (4 liters), and Jug B (3 liters)
#	Move:							State:
#	Fill B. 						A = 0, B = 3
#	Transfer B to A					A = 3, B = 0
#	Fill B 							A = 3, B = 3
#	Transfer B to A 				A = 4, B = 2
#	Dump A 							A = 0, B = 2

import random


# goal state; 2 liters in the 4-liter jug, empty 3 liter jug.
GOAL = [0,2]

# initial state; 3- and 4-liter jugs are empty.
empty34 = [0,0]

# Six operations on jugs.
# Fill 3-liter jug; whatever it contains, after filling it contains 3 liter;
# Let jugs be a list [,] with first component the contents of the 3-liter jug.
# and the second component the contents of the 4-liter jug;
def fill_j3(jugs):
	newjugs = jugs[:]
	print("Filling the 3-liter jug", jugs)
	newjugs[0] = 3
	print(newjugs)
	return newjugs

# Fill the 4-lier jug; whatever it contains, after filling it contains 4 liters;
def fill_j4(jugs):
	newjugs = jugs[:]
	print("Filling the 4-liter jug", jugs)
	newjugs[1] = 4
	print(newjugs)
	return newjugs

# Dump the entire contents of the 3-liter jugs.
def dump_j3(jugs):
	newjugs = jugs[:]
	print("Dumping out the contents of the 3-liter jug", jugs)
	newjugs[0] = 0
	return newjugs

# Dump the entire contents of the 4-liter jug;
def dump_j4(jugs):
	newjugs = jugs[:]
	print("Dumping out the contents of the 4-liter jug", jugs)
	newjugs[1] = 0
	print(newjugs)
	return newjugs

# Pour as much as possible of the contents of the 3-liter jug into the 
# 4-liter jug; the 3-liter jug may or may not be empty after pouring;
# the 4-liter jug may or may not be full after pouring;
def pour_j3j4(jugs):
	newjugs = jugs[:]
	print ("Pouring contents of 3-liter into the 4-liter")
	# [3,4] = Placement of jugs.
	contents_of_3 = newjugs[0]
	contents_of_4 = newjugs[1]

	if (contents_of_3 > 3):
		contents_of_3 = 3
	if (contents_of_4 > 4):
		contents_of_4 = 4
	if (contents_of_4 < 0):
		contents_of_4 = 0
	if (contents_of_3 < 0):
		contents_of_3 = 0

	if (contents_of_4 <= 4 and contents_of_3 <= 3):
		contents_of_4 = contents_of_4 + contents_of_3

		if (contents_of_4 > 4):
			contents_of_3 = contents_of_4 - 4
			contents_of_4 = 4

	newjugs[0] = contents_of_3
	newjugs[1] = contents_of_4

	print(newjugs)

	return newjugs

# Pour as much of the contents of the 4-liter jug into the 3-liter jug;
def pour_j4j3(jugs):
	newjugs = jugs[:]
	print ("Pouring contents of 4-liter into the 3-liter")

	
	# [3,4] = Placement of jugs.
	contents_of_3 = newjugs[0]
	contents_of_4 = newjugs[1]

	if (contents_of_3 > 3):
		contents_of_3 = 3
	if (contents_of_4 > 4):
		contents_of_4 = 4
	if (contents_of_4 < 0):
		contents_of_4 = 0
	if (contents_of_3 < 0):
		contents_of_3 = 0

	if (contents_of_4 <= 4 and contents_of_3 <= 3):
		contents_of_3 = contents_of_3 + contents_of_4
		contents_of_4 = contents_of_4 - contents_of_4

		if (contents_of_3 > 3):
			contents_of_3 = 3
	

	newjugs[0] = contents_of_3
	newjugs[1] = contents_of_4
	

	print(newjugs)

	return newjugs

# All possible next water jug states; up to 6 possible next states depending on how many
# operations (fill, dump, pour, ...) apply;
def succesor_fct(jugs):
	succs = [fill_j3(jugs), fill_j4(jugs), dump_j3(jugs), dump_j4(jugs),\
				pour_j3j4(jugs), pour_j4j3(jugs)]
	while None in succs:
		succs.remove(None)
	return succs
	
# Place holder ; Keep this unless I can come up with a useful and *admissible* evaluation function.
# One that consistently underestimates the true cost from state to goal.
def eval_fct(jugs):
	return 0

def goal_fct(jugs):
	return jugs == GOAL


def print_jug_contents(jugs):
	print(jugs)




