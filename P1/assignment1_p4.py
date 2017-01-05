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
    q1 = [(startingPrime, [startingPrime])]
    q2 = [(finalPrime, [finalPrime])]
    visited = set()
    visited2 = set()
    while (len(q1) > 0 and len(q2) > 0):
        (curr1, currpath1) = q1.pop(0)
        (curr2, currpath2) = q2.pop(0)
        if curr1 == curr2:
            return ([curr1], [curr2])
        visited.add(curr1)
        visited2.add(curr2)
        for x1 in q1:
            for x2 in q2:
                if x1[0] == x2[0]:
                    return (x1[1], x2[1])
        for prime1 in getPossibleActions(curr1):
            if prime1 not in visited:
                visited.add(prime1)
                q1.append((prime1, currpath1 + [prime1]))
        for prime2 in getPossibleActions(curr2):
            if prime2 not in visited2:
                visited2.add(prime2)
                q2.append((prime2, currpath2 + [prime2]))
    return ([], [])


def main():
    for line in sys.stdin:
        primes = str(line).split()
        (forward, back) = getPath(primes[0].lstrip("0"), primes[1].lstrip("0"))
        if (len(forward) > 0 and len(back) > 0):
            print ' '.join(forward) + "\n" + ' '.join(back)
        else:
            print "UNSOLVABLE"

if __name__ =='__main__':
    main()