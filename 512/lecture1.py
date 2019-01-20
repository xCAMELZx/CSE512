Python 2.7.14 (default, Dec 11 2017, 14:52:53) 
[GCC 7.2.1 20170915 (Red Hat 7.2.1-2)] on linux2
Type "copyright", "credits" or "license()" for more information.
>>> y = x *2

Traceback (most recent call last):
  File "<pyshell#0>", line 1, in <module>
    y = x *2
NameError: name 'x' is not defined
>>> x = [1,2,3,4,5]
>>> y = x*2
>>> 
>>> y
[1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
>>> print(len(x))
5
>>> print(len(y))
10
>>> print(len(x)-1)
4
>>> x[-1]
5
>>> x
[1, 2, 3, 4, 5]
>>> w = [:]
SyntaxError: invalid syntax
>>> w = x[:]
>>> w
[1, 2, 3, 4, 5]
>>> bsasket = {}
>>> basket = {}
>>> basket['apple'] = 5
>>> basket
{'apple': 5}
>>> basket['orange'] = 4
>>> basket
{'orange': 4, 'apple': 5}
>>> basket['kiwi'] = 8
>>> basket
{'orange': 4, 'kiwi': 8, 'apple': 5}
>>> #Above is the dictionary(in Python) or Map (C++) data structure
>>> 
>>> 
>>> #Printing out by interating of the basket
>>> basket.keys()
['orange', 'kiwi', 'apple']
>>> 
>>> 
>>> 
>>> 
>>> #Better way to iterate
>>> for k in basket.keys()
SyntaxError: invalid syntax
>>> for k in basket.keys():
	print "%s: %d" % (k, basket[k])

	
orange: 4
kiwi: 8
apple: 5
>>> for k in basket.keys():
	print ("%s: %d" % (k, basket[k]))

	
orange: 4
kiwi: 8
apple: 5
>>> 
>>> 
>>> 
>>> 
>>> list(strx)

Traceback (most recent call last):
  File "<pyshell#41>", line 1, in <module>
    list(strx)
NameError: name 'strx' is not defined
>>> list(x)
[1, 2, 3, 4, 5]
>>> 
>>> 
>>> 
>>> x = [2,6,8,3,5]
>>> x
[2, 6, 8, 3, 5]
>>> 
>>> y = []
>>> for n in x:
	y.append(n+1)

	
>>> 
>>> y
[3, 7, 9, 4, 6]
>>> 
>>> 
>>> z = map(lambda n: n+1, x)
>>> 
>>> z
[3, 7, 9, 4, 6]
>>> # The z is doing the same thing that the y [] did with appending 1 to each\
>>> # value within the x list.
>>> 
>>> 
>>> b = map(lambda n: n+2, x)
>>> b
[4, 8, 10, 5, 7]
>>> 
>>> #Extra practice with the lambda function
>>> 
>>> nxt next_digits(3, 123)
SyntaxError: invalid syntax
>>> 
