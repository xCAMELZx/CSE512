'''
# Brandon Saunders
# 3/17/2016
# Implementation of the a STRIPS representation operator that will move blocks
# in a "3-block-world"
# STRIPS instance is a quadruple <P,O,I,G>

P is a set of conditions (i.e., propositional variables);
O is a set of operators (i.e., actions); each operator is itself a quadruple \langle \alpha, \beta, \gamma, \delta \rangle, each element being a set of conditions. These four sets specify, in order, which conditions must be true for the action to be executable, which ones must be false, which ones are made true by the action and which ones are made false;
I is the initial state, given as the set of conditions that are initially true (all others are assumed false);
G is the specification of the goal state; this is given as a pair \langle N,M \rangle, which specify which conditions are true and false, respectively, in order for a state to be considered a goal state.
Reference: Wikipedia - https://en.wikipedia.org/wiki/STRIPS
'''
import random
# Anything to the right of floor will be a block on the floor.
# Right to left represents top to bottom. Unless the floor is positioned between blocks.
# Then the block closes to the floor is on the virtual floor. 
blocks2 = [ 'c', 'b', 'a', 'floor' ]
blocks = [ 'c', 'floor', 'b', 'a' ]


class STRIPS_OP():
	def __init__(self, p=[], a=[], d=[], nm=""):
		self.preconds = p
		self.adds = a
		self.dels = d
		self.name = nm

	def __str__(self):
		outstr ="%s:\n" % self.name
		outstr += "pres: %s\n" % self.preconds
		outstr += "adds: %s\n" % self.adds
		outstr += "dels: %s\n" % self.dels
		return outstr

	def apply(self, op, blocks):
		operation = op
		preconditions = operation.preconds
		add = operation.adds
		deletes = operation.dels
		name = operation.name
		block_state = blocks[:]
		print("\n")
		print("Applying: ", operation.name)
		print("Precondition: ", preconditions)
		print("Adds: ", add)
		print("Deletes: ", deletes)
		print("Name: ", name)

		name_array = name.split("_")
		print("Operation being called: ", name_array)

		number = 0
		for name in name_array:
			print(number, name)
			number += 1

		print("Before: ", block_state)

		# Check the preconditions
		if len(block_state) >= 4:
			print("Checking location of operation")

			index_of_blk_a = block_state.index(name_array[1])
			index_of_position_b = block_state.index(name_array[3])
			index_of_position_c = block_state.index(name_array[5])
			index_of_floor = block_state.index('floor')

			# on_y_x ("x is on y") and clear_x ("x is clear on top")	
			if index_of_blk_a - index_of_position_b == 1 and index_of_floor == index_of_blk_a - 1:
				print("Block ", name_array[1] ," is on block ", name_array[3] ," -----------------------------------------------------")
				print("Block ", name_array[1] ," is is clear on top")
				print("Moving ",  name_array[1], " to position ",  name_array[5])
				temp = block_state[index_of_floor]
				block_state[index_of_floor] = block_state[index_of_blk_a]
				block_state[index_of_blk_a] = temp

			# clear_z ("z is clear on top")
			if index_of_position_c - index_of_floor == 1:
				print("Position z is clear on top")

		print("After: ", block_state, "\n")
		return block_state
	


# Generate operator "move x from y to z"
# x is a block, y and z are blocks or floor
def generate_STRIPS_op(x,y,z): 
	pres = generate_pres(x,y,z)
	adds = generate_adds(x,y,z)
	dels = generate_dels(x,y,z)
	name = generate_name(x,y,z)
	return STRIPS_OP(pres,adds,dels,name)

def print_STRIPS_op(op):
	print("Operation:")
	print(op)
	print("\n")

def generate_name(x,y,z):
	nm = "move_%s_from_%s_to_%s" % (x,y,z)
	return nm
	
def generate_pres(x, y, z):
	p1 = "on_%s_%s" % (y,x)
	p2 = "clear_%s" % x
	p3 = "clear_%s" % z
	return [p1,p2,p3]

def generate_adds(x, y, z):
	a1 = "clear_%s" % y
	a2 = "on_%s_%s" % (z,x)
	return [a1,a2]

def generate_dels(x, y, z):
	d1 = "on_%s_%s" % (y,x)
	d2 = "clear_%s" % z
	return [d1,d2]

# generates a dictionary data structure for all moves
# that are possible for the blocks in 'blocks';
# e.g., call: all_ops(['a','b','c'])
def all_ops(blocks):
	all = {}
	operations = []
	for b1 in blocks:
		for b2 in blocks + ['floor']:
			for b3 in blocks + ['floor']:
				if b1 != b2 and b1 != b3 and b2 != b3:
					op = generate_STRIPS_op(b1,b2,b3)
					operations.append(op)
					all[op.name] = op
	return operations



def shuffle(x):
    x = list(x)
    random.shuffle(x)
    return x



strip = STRIPS_OP()
op = generate_STRIPS_op('a','b','floor')
print(op)
strip.apply(op,blocks)
all_operations = all_ops(blocks)

for i in all_operations:
	new_strip = STRIPS_OP()
	random_blocks = shuffle(blocks)

	new_strip.apply(i, random_blocks)
	print(i.name)
	
