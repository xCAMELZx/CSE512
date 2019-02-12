import fileinput

for line in fileinput.input():
    num = int(line)
    if num%3 == 0:
        print "fizz",
    if num%5 == 0:
        print "buzz",
    if num%3 != 0 and num%5 != 0:
        print num,
    print
