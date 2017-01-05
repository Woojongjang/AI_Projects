__author__ = 'wojang@ucsd.edu,A97105059,a1heng@ucsd.edu,A11308554,sharoon@ucsd.edu,A10938989'

import sys

def getPossibleActions(currentPrime):
    setOfPrimes = set()
    index = 0
    currentPrimeString = str(currentPrime)

    # Iterate through digits
    for i in range(len(currentPrimeString)):
        # Enumerate neighbors
        start = 0
        if i == 0:
            start = 1
        for digit in range(start, 10):
            neighbor = currentPrimeString[:i] + str(digit) + currentPrimeString[i + 1:]
            if (digit != int(currentPrimeString[i]) and isPrime(int(neighbor))):
                setOfPrimes.add(neighbor)

    # Convert set to list
    listOfPrimes = list(setOfPrimes)
    return listOfPrimes

"""Simple check if number is prime"""
def isPrime(number):
	if number > 1:
		i = 2
		# Iterate up to the square root of number
		while (i * i <= number):
			if (number % i == 0):
				# IS NOT PRIME NUMBER
				return False
			i = i + 1
		# IS PRIME
		return True
	return False
	
""" (2.2) DFS (depth limit) """
def getPath2(startingPrime, finalPrime, depth, visited = set(), path = [], layer = 0):
	if startingPrime == finalPrime:
		if (layer == 0):
			return [startingPrime] + path
		return path
	elif (depth > 0):
		for prime in getPossibleActions(startingPrime):
			if prime not in visited:
				currPath = getPath2(prime, finalPrime, depth - 1, visited.union(set([startingPrime])), path + [prime], layer + 1)
				if (len(currPath) > 0):
					if (layer == 0):
						return [startingPrime] + currPath
					return currPath
	return []

def getPath(startingPrime, finalPrime):
	for depth in range(8):
		path = getPath2(startingPrime, finalPrime, depth)
		if len(path) > 0:
			return path
	return []

def main():
    for line in sys.stdin:
        primes = str(line).split()
        path = getPath(primes[0].lstrip("0"), primes[1].lstrip("0"))
        if (len(path) > 0):
            print ' '.join(path)
        else:
            print "UNSOLVABLE"

if __name__ == '__main__':
	main()
