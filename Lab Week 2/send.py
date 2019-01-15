# send.py
# by KV for CSE 512, Winter 2018
# generate next number (as listof digits) that has
# k unique digits 0..9
'''
brute-force solution to the send-more-money puzzle;
demonstration of a puzzle solving program "without"
intelligence; ... discuss ...

set up and order so that problem becomes computatioally
more feasible for demo purposes ..
'''

#LETTERS = ['O','M','Y','E','N','D','R','S'] # (01)256789
LETTERS = ['S','E','N','D','R','Y']
CODE = {'O':0, 'M':1} # set these to cut down on effort

SEND = ['S','E','N','D']
MORE = ['M','O','R','E']
MONEY = ['M','O','N','E','Y']

def next_unique_digits(k,num):
    nxt = next_digits(k,num)
    #print nxt
    while len(set(nxt)) != k and len(set(nxt)) <= k or\
          set(nxt).intersection(set([0,1])) != set([]):
        num += 1
        nxt = next_digits(k,num)
        #print nxt
    nextnum = int(''.join(map(lambda x: str(x),nxt)))
    if nextnum >= pow(10,k):
        return ([],-1)
    return (nxt, nextnum)

# given a integer k ("number of digits") and a number
# produces a list of digits that represents the number
def next_digits(k, num):
    digs = []
    x = k-1
    while x >= 0:
        m = num / pow(10,x)
        digs.append(m)
        if m != 0:
            num = num - m * pow(10,x)
        x -= 1
    return digs

# [S,E,N,D] Sval * 10^3 + Eval * 10^2 + Nval * 10^1 + Dval * 10^0
# i = 0..3 
def word_value(wdlst,code):
    val = 0;
    for i in range(len(wdlst)):
        val += code[wdlst[i]] * pow(10,len(wdlst)-1 -i)
    return val

def solve():
    global CODE
    k = 6 # bec of preset CODE, 8 - 2 letters to encode ... 
    n = 0
    count = 1
    for i in range(pow(10,k)):
        (n1,n2) = next_unique_digits(k,n)
        if n2 == -1:
            return []
        print "%d. %s" % (count,n1)  #,n2
        count += 1
        j = 0
        for x in LETTERS:
            if x != 'O' and x != 'M':
                CODE[x] = n1[j]
                j+=1
        if word_value(SEND,CODE) + word_value(MORE,CODE) == \
            word_value(MONEY,CODE):
            return CODE
        n = n2+1
    return []

# **** alternative generation of lists of unique digits ****

def all_codes(k, digs):
    if len(digs) < k:
        return []
    if k == 1:
        return map(lambda x: [x],digs)

    codes = []
    for d in digs:
        rest = digs[:]
        rest.remove(d)
        subcodes = all_codes(k-1, rest)
        for s in subcodes:
            nextcode = [d]
            nextcode.extend(s)
            codes.append(nextcode)
    return codes
        
def alt_solve():
    letters = ['O','M','S','E','N','D','R','Y']
    allcodes = all_codes(len(letters),[0,1,2,3,4,5,6,7,9])

    k = 1
    for cd in allcodes:
        testcode = {}
        i = 0
        for x in letters:
            testcode[x] = cd[i]
            i+=1
        print "%d. %s" % (k,testcode)
        k+=1
        if word_value(SEND,testcode) + word_value(MORE,testcode) == \
            word_value(MONEY,testcode):
            return testcode
    return []


# "main" is only needed when you want to run the script
# directly be calling it by name; for our purposes, we
# will mostly want to run the program from within the
# IDE via 'Run', or by adding intended top-level function
# call to the end of the file.

solve()
print "\n"
print CODE


'''
__name__ = '__main__'

if __name__ == '__main__':
    solve()
    raw_input(\n"Any key to quit")
'''    
    
    
    
            
        
        
        

    

        
      
  
