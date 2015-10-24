#By Carter Cook - "I confirm that this submission is my own work and is consistent with the Queen's regulations on Academic Integrity."
#----------IMPORTS, FUNCTIONS, AND GLOBAL VARIABLES----------#
import math #for math.sqrt() in quadraticProbe()

#initialize hashTable
m = 2477 #len(hashTable)
hashTable = []

def string_to_int(s):
	x = 37 # can be any value large enough to ensure that the maximum result is >= m. It is often a 2-digit prime number.
	sum = 0
	for c in s:
		sum = sum*x + ord(c)
	return sum

def multiplyHash(key): #using multiplicaton method
	mew = (math.sqrt(5) - 1)/2 #Knuth told me to do it
	x = (key*mew) % 1 #only keep digits after the decimal point, e.g. 0.538924...
	return int(m*x) #m = table size

def midSquareHash(key): #using mid-square method
	key = str(key**2) #square the key, convert it to a string
	length = len(key) #cant call len() on an int, hence the conversion :p
	if (length <= 4):
		return int(key) #return all the digits
	return int(key[length/2-2:length/2+2]) #grab the middle 4 digits & return

def noHash(key):
	return key

def quadraticProbe(key, c1, c2):
	hashedKey = multiplyHash(string_to_int(key)) #calculate before while() to save time
	i = 0
	while hashTable[(hashedKey + c1*i + c2*(i**2)) % m] != "": #keep searching while space is occupied
		i = i + 1
	hashTable[(hashedKey + c1*i + c2*(i**2)) % m] = key #found an empty spot! insert our key
	return i+1 #return comparisons

def doubleHash(key, hash1, hash2):
	key1 = hash1(string_to_int(key)) #calculate these before while() to save time
	key2 = hash2(string_to_int(key))
	i = 0
	while hashTable[(key1 + (key2+1)*i) % m] != "": #keep searching while space is occupied
		i = i + 1
	hashTable[(key1 + (key2+1)*i) % m] = key #found an empty spot! insert our key
	return i+1 #return comparisons

#---------MAIN PROGRAM----------#
aliases = open("top_secret_agent_aliases_2015.txt").read().splitlines() #read aliases into array

#---------QUADRATIC PROBE----------#
minComparisons = float("inf") #infinity
bestCoprimes = (0,0) #to print most effective coefficents later on
maxComparisons = -1
worstCoprimes = (0,0) #to print least effective coefficients later on
for c1 in xrange(2,31): #0 & 1 aren't prime, 31 is just an arbitrary range
	#generate coprimes of c1
	factors = [x for x in xrange(2, c1+1) if c1 % x == 0] #get all factors of c1 < 31
	coprimes = []
	for c2 in xrange(2,31): #now check for coprimes between 2-30
		i = 0
		while i < len(factors):
			if c2 % factors[i] == 0: #c2 and c1 have a common factor
				break #therefore they aren't coprime
			i=i+1
		if i == len(factors): #finished checking without breaking, therefore c2 and c1 are coprime
			#test all pairs of coprimes
			hashTable = [""]*m #initialize hashTable
			comparisons = 0
			for line in aliases: #len(aliases)==2000
				comparisons = comparisons + quadraticProbe(line, c1, c2)
			comparisons = comparisons/float(len(aliases)) #comaprisons per insert
			if comparisons < minComparisons: #store best and worst coefficients so far
				minComparisons = comparisons
				bestCoprimes = (c1, c2)
			if comparisons > maxComparisons:
				maxComparisons = comparisons
				worstCoprimes = (c1, c2)
print "Quadratic Probe:\n\tmin comparisons/insert=%f, coefficients: %d*i + %d*(i^2)\n\tmax comparisons/insert=%f, coefficients: %d*i + %d*(1^2)" % (minComparisons,bestCoprimes[0], bestCoprimes[1], maxComparisons, worstCoprimes[0], worstCoprimes[1])

#----------DOUBLE HASH----------#
minComparisons = float("inf") #infinity
bestFuncs = (0,0) #functions causing the fewest comparisons
maxComparisons = -1
worstFuncs = (0,0) # funcs causing the most comparisons
functions = [multiplyHash, midSquareHash, noHash]
for func1 in functions:
	for func2 in functions:
		if func1 == func2: #don't want to use identical functions
			continue #skip this iteration
		hashTable = [""]*m #initialize hashTable
		comparisons = 0
		for line in aliases: #len(aliases)==2000
			comparisons = comparisons + doubleHash(line, func1, func2)
		comparisons = comparisons/float(len(aliases)) #comaprisons per insert
		if comparisons < minComparisons: #store best and worst hash functions so far
			minComparisons = comparisons
			bestFuncs = (func1, func2)
		if comparisons > maxComparisons:
			maxComparisons = comparisons
			worstFuncs = (func1, func2)
print "Double Hash:\n\tcomparisons/insert=%f, functions: %s + %s*i\n\tmax comparisons/insert=%f, functions: %s + %s*i\n" % (minComparisons, bestFuncs[0].__name__, bestFuncs[1].__name__, maxComparisons, worstFuncs[0].__name__, worstFuncs[1].__name__)

print """CONLCUSIONS:
Even at its worst, double hashing is still better than quadratic probing. The results are
pretty shocking actually.

I could find no pattern in the combinations of coprimes. The only
requirement seems to be a lack of common factors. Running with different table sizes yields
different optimal coefficents every time.

Why is double hashing consistently better than quadratic probing (ignoring that fact that
it sometimes fails to halt)? I fail to see the difference between a good hash function and
a psuedo-random number generator.

Mid square method is kinda bad IMHO. Even though it yeilded the fewest collisions, it
consistently threw my tests with non-prime table sizes into infinite loops. NoHash actually
behaved very nicely, but that's because string_to_int on its own is technically a hash
function."""