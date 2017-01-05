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
    
def getMyHeuristic(nodePrime, finalPrime):
    str1 = str(nodePrime)
    str2 = str(finalPrime)
    diffs = 0
    i = 1
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += i
        i += 1
    return diffs

def getOurHeuristic(nodePrime, finalPrime):
    str1 = str(nodePrime)
    str2 = str(finalPrime)
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    ret = abs((finalPrime - nodePrime)/ finalPrime) + diffs
    return ret

def getHeuristic(nodePrime, finalPrime):
    str1 = str(nodePrime)
    str2 = str(finalPrime)
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs

def getPossActionHeur(currentPrime, finalPrime):
    listact = getPossibleActions(currentPrime)
    primeListsort = []
    for x in listact:
        a = x
        b = getHeuristic(x,finalPrime)
        primeListsort.append((a,b))
    return [i[0] for i in sorted(primeListsort, key=lambda x: x[1])]

def getOurPossActionHeur2(currentPrime, finalPrime):
    listact = getPossibleActions(currentPrime)
    primeListsort = []
    for x in listact:
        a = x
        b = getOurHeuristic(x,finalPrime)
        primeListsort.append((a,b))
    return [i[0] for i in sorted(primeListsort, key=lambda x: x[1])]


def getOurPossActionHeur(currentPrime, finalPrime):
    listact = getPossibleActions(currentPrime)
    primeListsort = []
    for x in listact:
        a = x
        b = getHeuristic(x,finalPrime)
        for y in primeListsort:
            if b == y[1]:
                b += 1
        primeListsort.append((a,b))
    return [i[0] for i in sorted(primeListsort, key=lambda x: x[1])]


def getOurPath(startingPrime, finalPrime):
    q = [(startingPrime, [startingPrime])]
    visited = set()
    while (len(q) > 0):
        (curr, currpath) = q.pop(0)
        visited.add(curr)
        if (curr == finalPrime):
            return currpath
        for prime in getOurPossActionHeur(curr, finalPrime):
            if prime not in visited:
                visited.add(prime)
                q.append((prime, currpath + [str(prime)]))
    return []


def getOurPath2(startingPrime, finalPrime):
    q = [(startingPrime, [startingPrime])]
    visited = set()
    while (len(q) > 0):
        (curr, currpath) = q.pop(0)
        visited.add(curr)
        if (curr == finalPrime):
            return currpath
        for prime in getOurPossActionHeur2(curr, finalPrime):
            if prime not in visited:
                visited.add(prime)
                q.append((prime, currpath + [str(prime)]))
    return []


def getPath(startingPrime, finalPrime):
    q = [(startingPrime, [startingPrime])]
    visited = set()
    while (len(q) > 0):
        (curr, currpath) = q.pop(0)
        visited.add(curr)
        if (curr == finalPrime):
            return currpath
        for prime in getPossActionHeur(curr, finalPrime):
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