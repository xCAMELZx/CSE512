#!/bin/py
# Brandon Saunders
# 3/10/2016
# The greedy variant of the greedy separate and conquer algorithm.

import numpy
import copy

# Method 1 of representing the table
TABLE_NAME = [{'INDIVIDUAL': 1,'APPRAISAL': 1,'RATING': 0,'INCOME': 0, 'BALANCE': 1, 'LOAN_OK': 0},\
			  {'INDIVIDUAL': 2,'APPRAISAL': 0,'RATING': 0,'INCOME': 1, 'BALANCE': 0, 'LOAN_OK': 0},\
			  {'INDIVIDUAL': 3,'APPRAISAL': 1,'RATING': 1,'INCOME': 0, 'BALANCE': 1, 'LOAN_OK': 1},\
			  {'INDIVIDUAL': 4,'APPRAISAL': 0,'RATING': 1,'INCOME': 1, 'BALANCE': 1, 'LOAN_OK': 1},\
			  {'INDIVIDUAL': 5,'APPRAISAL': 0,'RATING': 1,'INCOME': 1, 'BALANCE': 0, 'LOAN_OK': 0},\
			  {'INDIVIDUAL': 6,'APPRAISAL': 1,'RATING': 1,'INCOME': 1, 'BALANCE': 0, 'LOAN_OK': 1},\
			  {'INDIVIDUAL': 7,'APPRAISAL': 1,'RATING': 1,'INCOME': 1, 'BALANCE': 1, 'LOAN_OK': 1},\
			  {'INDIVIDUAL': 8,'APPRAISAL': 1,'RATING': 0,'INCOME': 1, 'BALANCE': 0, 'LOAN_OK': 0},\
			  {'INDIVIDUAL': 9,'APPRAISAL': 1,'RATING': 1,'INCOME': 0, 'BALANCE': 0, 'LOAN_OK': 0}]

# Method 2 of representing the table
TABLE_DATA = {'INDIVIDUAL': [1,2,3,4,5,6,7,8,9], 
			  'APPRAISAL:': [1,0,1,0,0,1,1,1,1], 
			  'RATING': [0,0,1,1,1,1,1,0,1],
			  'INCOME': [0,1,0,1,1,1,1,1,0], 
			  'BALANCE': [1,0,1,1,0,0,1,0,0], 
			  'LOAN_OK':[0,0,1,1,0,1,1,0,0]}


ATTRIBS = ['APPRAISAL', 'RATING', 'INCOME', 'BALANCE']


def learnRules():
	dtab =  copy.deepcopy(TABLE_NAME)
	rules = []
	while not all_pos_covered(rules,dtab):
		nextrule = learn_next_rule(dtab)
		if not nextrule in rules:
			rules.append(nextrule)
			dtab = removeRuleCovers(nextrule, dtab)
		else:
			print("No further rules to be learned")
			break
	return rules

# Rules represented as a list of form [[a1,a2], [a3,a4,a5],...]
# Where all are attributes form ATTRIBS
def all_pos_covered(rules,dtab):
	for inst in dtab:
		if pos_instance(inst):
			cov = False 
			for r in rules:
				if covers_instance(r,inst):
					cov = True
					break
			if cov == False:
				return False
	return True


def covers_instance(rule,inst):
	if rule == []:
		return True  # most general rule cover all instances
	for at in rule:
		print("Looking at: ", at, inst[at])
		if not inst[at] == 1:
			print("covers_instance, return False")
			return False
	return True

def pos_instance(inst):
	return inst['LOAN_OK'] == 1


def covers_neg(rule, dtab):
	if rule == []:
		print("covers_neg, rule == []")
		return True
	for inst in dtab:
		print("covers_neg, looking at: ", inst)
		if covers_instance(rule,inst) and inst['LOAN_OK'] == 0:
			return True
	return False


def candidate_rules(rule, attrs):
	cands = []
	for a in attrs:
		cr = rule[:]
		cr.append(a)
		cands.append(cr)
	return cands



def learn_next_rule(dtab):
	attrs = ATTRIBS[:] # copy of attributes
	rule = [] # most general rule "everything is ok"
	while covers_neg(rule, dtab):
		# current rule with new attribute added on
		testrules = candidate_rules(rule, attrs)
		maxratio = -100000
		bestrule = None
		for tr in testrules:
			# compute ratio and keep track of largest
			ratio = comp_ratio(tr,dtab)
			if ratio > maxratio:
				bestrule = tr
				maxratio = ratio
			print("Bestrule: ", bestrule)
			print("Maxratio: ", maxratio)
		print("Attributes: ", attrs)
		attrs.remove(bestrule[-1])
		rule = bestrule
	return rule

def comp_ratio(rule, dtab):
	poscv,allcv = num_pos_all_covered(rule,dtab)
	if (allcv == 0):
		return 0
	return float(poscv)/allcv

def num_pos_all_covered(rule,dtab):
	posnum = 0
	allnum = 0
	for inst in dtab:
		if covers_instance(rule,inst):
			allnum += 1
			if inst['LOAN_OK'] == 1:
				posnum += 1
	return posnum,allnum

	

def removeRuleCovers(rules, dtab):
	l1 = []
	l2 = []
	l3 = []
	l4 = []
	n = 0
	for i in range(0,len(rules)):
		for j in dtab:
			l1.append(j[rules[i]])
	for i in dtab:
		for j in i:
			if j == 'LOAN_OK':
				l1.append(i[j])
	k = (len(l1)/(len(rules)+1))
	for i in range(0,k):
		l2.append(l1[i::9])
	for x in l2:
		n += 1
		if all(x):
			l4.append(n)
	for x in l4:
		for y in dtab:
			if x == y['INDIVIDUAL']:
				dtab.remove(y)
	return dtab



	


print("Rules Learned: ",learnRules())

