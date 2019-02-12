# Yousef Jarrar - CSE 512 - Winter 2019 
# Water Jug Problem, with the use of bestfirst_astar_search_lab4.py 
# Implementation comes from puzz8

from bestfirst_astar_search_lab4 import *

# first define goal -- 0 liters in 3l jug, 2 liters in 4l jug
# we represent state as a simple 2-element list
GOAL = [0, 2]


# checking for goal is quite obvious
def goal_fct(jugs, goal):
	if jugs == goal:
		return True
	else:
		return False


# score is a distance from goal in liters (in both directions)
def eval_fct(jugs, goal):
	return abs(jugs[0]-goal[0]) + abs(jugs[1]-goal[1])


def successor_fct(jugs):
	moves = []

	left, right = jugs  # amount in left and right jugs

	# non-empty left jug means we can empty it
	if left > 0:
		moves.append([0, right])
	# non-full left jug means we can fill it
	if left < 3:
		moves.append([3, right])
		# or pour from non-empty right jug
		if right > 0:
			moves.append([min(3, left + right), max(0, left + right - 3)])

	# same as for left jug
	if right < 4:
		moves.append([left, 4])
		if left > 0:
			moves.append([min(3, left + right), max(0, left + right - 4)])
	if right > 0:
		moves.append([left, 0])

	return moves


# again, printer is pretty simple
def compact(position):
	print "%d | %d" % (position[0], position[1])


def main():
	print "Best-first solution. "
	# run
	BESTFIRST_SOLN = BEST_FIRST_SEARCH_FCT([0, 0], GOAL, goal_fct,
		successor_fct, eval_fct, compact)

	# and print. it all fits in one line, so no need for loops or something
	print BESTFIRST_SOLN

	print "\nAstar solution."
	# repeat for A-star
	ASTAR_SOLN = ASTAR_SEARCH_FCT([0, 0], GOAL, goal_fct,
		successor_fct, eval_fct, compact)

	print BESTFIRST_SOLN


if __name__ == '__main__':
	main()
