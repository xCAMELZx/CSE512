#usr/bin/python
# Brandon Saunders
# Created on 3/3/2016
# CNF conversion of propositional logic.


PROP0 = [ 'P' ,'notP', ['R', '=>', 'notS'], ['A', 'and', 'B'], ['A', 'or', 'B'], ['A', '=>', 'B'] ]
PROP1 = ['notP','=>', ['R', '=>', 'notS']]
PROP2 = ['P', 'or', ['R', 'and', 'S'] ]
prop1 = ['notP', '=>', ['R','=>', 'notS']]
prop2 = ['not', ['notP', 'and', ['R','=>', 'notS']]]
prop3 = [ ['A', 'and','B'], 'or', 'C' ]
prop4 = [ ['A', 'or','B'], 'and', 'C' ]
prop5 = [ 'C', 'and', ['A', 'or','B'] ]
prop6 = [ 'C', 'or', ['A', 'and','B'] ]

def is_literal(x):
	return type(x) == str

def is_neglit(x):
	return is_literal(x) and x[:3] == 'not'

def is_and(x):
	return type(x) == list and len(x) == 3 and x[1] == 'and'

def is_or(x):
	return type(x) == list and len(x) == 3 and x[1] == 'or'

def is_imp(x):
	return type(x) == list and len(x) == 3 and x[1] == '=>'

def is_negex(x):
	return type(x) == list and len(x) == 2 and x[0] == 'not'

def flatten(lst):
	if not type(lst) == list:
		return lst
	if lst == []:
		return lst
	elif(type(lst[0]) == list):
		return flatten(lst[0]) + flatten(lst[1:])
	else:
		return [lst[0]] + flatten(lst[1:])

# Eliminates all implications from the propositional expression.
def imp_elim(x):
	#case 1: x is a literal
	if (is_literal(x)):
		return x
	#case 2: x is a disjunction (that may contain implications)
	elif (is_or(x)):
		return [imp_elim(x[0]), 'or', imp_elim(x[2])]
	#case 3: x is a conjunction (that may contain implications)
	elif (is_and(x)):
		return [imp_elim(x[0]), 'and',  imp_elim(x[2])]
	#case 4: x is a negated statement (that may contain implecations)
	elif (is_negex(x)):
		return ["not" + imp_elim(x[1])]
	#case 5: x is an implication (that may contain other implications)
	else:
		return [['not', imp_elim(x[0])], 'or', imp_elim(x[2])]


# Moves negations into the expressions so that only negated statements will be literals.
def negs_in(x):
	#case 1: x is a literal
	if(is_literal(x)):
		return x		
	#case 2: x is a disjunction (that may contain implications)
	elif(is_or(x)):
		return [negs_in(x[0]), 'or', negs_in(x[2])]
	#case 3: x is a conjunction (that may contain implications)
	elif(is_and(x)):
		return [negs_in(x[0]), 'and', negs_in(x[2])]
	#case 4: x is a negated statement (that may contain implecations)
	elif (is_negex(x)):
		if (is_literal(x[1])):
			if(is_neglit(x[1])):
				return x[1][3:]
			else:
				return 'not' + x[1]
		elif(is_negex(x[1])):
			return negs_in(x[1][1])
		
		elif(is_and(x[1])):
			left = x[1][0]
			right = x[1][2]
			return negs_in([ ['not',negs_in(left)], 'or', ['not',negs_in(right)] ])
		elif(is_or(x[1])):
			left = x[1][0]
			right = x[1][2]
			return negs_in([['not',negs_in(left)], 'and', ['not',negs_in(right)] ])
		else:
			# should not here, but if, return unchanged
			return x


# Distribute and-expressions over or-operators in order to produce an equivalent conjunction of disjunctions, which is the ultimate
# objective of the conversion.
# Conjunction of disjunctions = and's of or's
def distrib_andof(x):
	#print("x[0]", x[0])
	#print("x[1]", x[1])
	#print("x[2]", x[2])

	#case 1: x is an expression without 'and'
	if(is_and(x[1]) == False and is_and(x[0]) and is_and(x[2])):
		print("There was no and expression")
		return flatten(x)
	#case 2: x is a conjunction (that may contain and-or's)
	if(is_and(x)):
		left = x[0]
		right = x[2]
		print("and")

		#print("left", left, "right", right)
		if(is_or(left) and len(right) == 1):
			print("EX (A or B), and C")
			return([left[0], 'and',x[2][0]], 'or', [left[2], 'and', x[2][0] ] ) 

		if(is_or(right) and len(left) == 1):
			print("EX C and (A or B)")
			return([right[0], 'and',x[0]], 'or', [right[2], 'and', x[0] ] ) 

	#case 3: x is a disjunction (that may contain or produce and-or's)
	if(is_or(x)):
		left = x[0]
		right = x[2]

		if(is_and(left) and len(right) == 1):
			print("EX (A and B), or C")
			return([left[0], 'or',x[2][0]], 'and', [left[2], 'or', x[2][0]] ) 

		if(is_and(right) and len(left) == 1):
			print("EX C or (A and B)")
			return([right[0], 'or',x[0]], 'and', [right[2], 'or', x[0] ] ) 

	# Should not reach here.
	return(x)
	
prop3 = [ ['A', 'and','B'], 'or', 'C' ]
prop4 = [ ['A', 'or','B'], 'and', 'C' ]
prop5 = [ 'C', 'and', ['A', 'or','B'] ]
prop6 = [ 'C', 'or', ['A', 'and','B'] ]

val = negs_in(imp_elim(prop3))
print(val)
distributed = distrib_andof(val)
print(distributed)
