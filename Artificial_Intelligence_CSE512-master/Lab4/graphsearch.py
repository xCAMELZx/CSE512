# CSE 512 Lab 4
# This lab will be to solve the standard 8-puzzle. 
# Will need to represent of an 8-puzzle state. 
# Testing of whether a given puzzle state is in the goal state.
# Test all possible successor states to the given puzzle state.
# Evaluate the numeric "goodness" score for a given puzzle
from random import randint

#Blank space in the puzzle
B = "B"

# Dictionary of the form (row,col):<tile_no>
puzzle = { (1,1):1, (1,2):2, (1,3):5, (2,1):7, (2,2):B, (2,3):6, (3,1):3, (3,2):4, (3,3):8 }
d = dict(puzzle)

# Global position names for easier readability.
zero = puzzle[(1,1)]
one = puzzle[(1,2)]
two = puzzle[(1,3)]
three = puzzle[(2,1)]
four = puzzle[(2,2)]
five = puzzle[(2,3)]
six = puzzle[(3,1)]
seven = puzzle[(3,2)]
eight = puzzle[(3,3)]

'''
for item in puzzle.keys():
	print(item,puzzle[item])
	if (puzzle[item] == B):
		print("Found a blank space.")
	'''

# Prints out the index positions of the game board.
def printExampleGameBoard():
	print("Example game board:")
	print("*---------*")
	print(0,1,2)
	print(3,4,5)
	print(6,7,8)
	print("*---------*")

# Prints out the current puzzle as is.
def printPuzzle():
	print("\n")
	print("Current game board:")
	print("*---------*")
	print(zero,one,two)
	print(three,four,five)
	print(six,seven,eight)
	print("*---------*")
	print("\n")

'''
for key,value in puzzle:
	print(key,value)

'''
# Function to swap two places on the game board.
def swap(entry_A, entry_B):
	global puzzle
	print("Swapping values", entry_A, entry_B)
	tempA = entry_A
	tempB = entry_B
	tempA_key = ""
	tempB_key = ""

	for item in puzzle.keys():
		#print(item,puzzle[item])
		if (puzzle[item] == tempA):
			tempA_key = item
		if (puzzle[item] == tempB):
			tempB_key = item

	tempA_value = puzzle[tempA_key]
	puzzle[tempA_key] = puzzle[tempB_key]
	puzzle[tempB_key] = tempA_value


# Returns a list of puzzle positions that are not in the goal game state.
def evaluationFunction(mapValue):
	eval = list()

	if (mapValue[(1,1)] != 1): 
		eval.append('zero')

	if (mapValue[(1,2)] != 2):
		eval.append('one')

	if (mapValue[(1,3)] != 3):
		eval.append('two')

	if (mapValue[(2,1)] != 4):
		eval.append('three')

	if (mapValue[(2,2)] != 'B'):
		eval.append('four')

	if (mapValue[(2,3)] != 5):
		eval.append('five')

	if (mapValue[(3,1)] != 6):
		eval.append('six')

	if (mapValue[(3,2)] != 7):
		eval.append('seven')

	if (mapValue[(3,3)] != 8):	
		eval.append('eight')

	return eval


	
# Will allow moving of games pieces using the swap function after the evaluation function.
def Move(mapValue, start_position, end_position, possible_positions, open_positions):
	

	'''
	for item in mapValue.keys():
		#print(item,puzzle[item])
		if (mapValue[item] == B):
			print("Found a blank space.")
			print(item)
	'''




# Checks for the hardcoded goal game state.
def testForGoalState(mapValue):
	if (mapValue[(1,1)] == 1 and mapValue[(1,2)] == 2 and mapValue[(1,3)] == 3/
		mapValue[(2,1)] == 4 and mapValue[(2,2)] == 'B' and mapValue[(2,3)] == 5/
		mapValue[(3,1)] == 6 and mapValue[(3,2)] == 7 and mapValue[(3,3)] == 8):
		return True
	else:
		return False

# Identifies all possible moves on the game board from the perspectice of the blank space.
def possibleMoves(mapValue):
	northernMove = 0
	southernMove = 0
	easternMove = 0
	westernMove = 0
	possibleMove = list()

	if (zero == "B"):
		southernMove = 1
		easternMove = 1
		print("zero")
	elif (one == "B"):
		southernMove = 1
		easternMove = 1
		westernMove = 1
		print("Current blank space: one")
	elif (two == "B"):
		easternMove = 1
		southernMove = 1
		print("Current blank space: two")
	elif (three == "B"):
		northernMove = 1
		easternMove = 1
		southernMove = 1
		print("Current blank space: three")
	elif (four == "B"):
		easternMove = 1
		westernMove = 1
		southernMove = 1
		northernMove = 1
		print("Current blank space: four")
	elif (five == "B"):
		westernMove = 1
		northernMove = 1
		southernMove = 1
		print("Current blank space: five")
	elif (six == "B"):
		northernMove = 1
		easternMove = 1
		print("Current blank space: six")
	elif (seven == "B"):
		easternMove = 1
		northernMove = 1 
		westernMove = 1
		print("Current blank space: seven")
	elif (eight == "B"):
		northernMove = 1
		westernMove = 1
		print("Current blank space: eight")

		possibleMove.append(northernMove)
		possibleMove.append(southernMove)
		possibleMove.append(easternMove)
		possibleMove.append(westernMove)

	return(northernMove,southernMove,easternMove,westernMove)


def makeDecision(puzzle):
	TheMap = puzzle
	# Test for incorrect positions
	incorrectPositions = evaluationFunction(TheMap)
	print("Incorrect Positions: ", incorrectPositions)

	# Possible places to move to
	directions = possibleMoves(TheMap)

	print("Can move to: (north,south,east,west): ", directions)

	randomMove = randint(1,4)
	print("Random move: ", randomMove)

	if (incorrectPositions == 'two'):
		print("two")
		pass




def main():

	printExampleGameBoard()


	for _ in range(5):
		printPuzzle()

		'''
		
		print("Pieces not in the correct place: ")
		print("Positions: ", evaluationFunction(puzzle))
		print("\n")

		print("Possible Moves: ")
		print("Directions: ", possibleMoves(puzzle))
		print("\n")

		'''

		if(testForGoalState(puzzle) == False):
			makeDecision(puzzle)
			print("Need to move")





if __name__ == "__main__":
    main()

