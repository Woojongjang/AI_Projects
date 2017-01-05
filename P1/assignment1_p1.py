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

def getPath(startingPrime, finalPrime):
	q = [(startingPrime, [startingPrime])]
	visited = set()
	while (len(q) > 0):
		(curr, currpath) = q.pop(0)
		visited.add(curr)
		if (curr == finalPrime):
			return currpath
		for prime in getPossibleActions(curr):
			if prime not in visited:
				visited.add(prime)
				q.append((prime, currpath + [str(prime)]))
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