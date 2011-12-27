
from math import sqrt, log
from pylab import plot, xlabel, ylabel, show

# from wiki: http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

#To find all the prime numbers less than or equal to a given integer n by Eratosthenes' method:

#    Create a list of consecutive integers from 2 to n: (2, 3, 4, ..., n).
#    Initially, let p equal 2, the first prime number.
#    Starting from p, count up in increments of p and mark each of these numbers greater than p itself in the list. These numbers will be 2p, 3p, 4p, etc.; note that some of them may have already been marked.
#    Find the first number greater than p in the list that is not marked; let p now equal this number (which is the next prime).
#    If p is less than n, repeat from step 3. Otherwise, stop.

#When the algorithm terminates, all the numbers in the list that are not marked are prime.

#As a refinement, it is sufficient to mark the numbers in step 3 starting from p2, as all the smaller multiples of p will have already been marked at that point. This means that the algorithm is allowed to terminate in step 5 when p2 is greater than n. This does not appear in the original algorithm.[4]

#Another refinement is to initially list odd numbers only (3, 5, ..., n), and count up using an increment of 2p in step 3, thus marking only odd multiples of p greater than p itself. This refinement actually appears in the original description.[5] This can be generalized with wheel factorization, forming the initial list only from numbers coprime with the first few primes and not just from odds, i.e. numbers coprime with 2.[6]



# supposed to have many optimations, but not completed, the others are sufficiently fast
def sieve(max):
	primes = list()
	multiples = [False] * int(((max+1)-3)//2) #is this nr a multiple of any other value?
			#only listing odd numbers, starting from 3
			#multiples[i] = True means that the number i*2+3 is NOT prime
	
	num = 0
	for i in range(len(multiples)):
		if multiples[i]: continue
		num = i*2+3
		for j in range(num*num,max+1,num): multiples[(j-3)//2]=True
	
	primes.append(1)
	primes.append(2)
	for n in range(len(multiples)):
		if not multiples[n]: primes.append(n*2+3)
	
	return primes

#basic version, with some optimation
def sieve1(max):
	primes = list()
	multiples = [False] * (max+1) #is this nr a multiple of any other value?
	
	for i in range(2,int(sqrt(max+1))+1): #+1 to account for rounding errors
		if multiples[i]: continue
		for j in range(i*i,max+1,i):
			multiples[j]=True

	for n in range(1,len(multiples)):
		if not multiples[n]: primes.append(n)
	
	return primes


#basic version, without optimation
def sieve2(max):
	primes = list()
	multiples = [False] * (max+1) #is this nr a multiple of any other value?
	
	for i in range(2,max+1):
		if multiples[i]: continue
		for j in range(2*i,max+1,i):
			multiples[j]=True


	for n in range(1,len(multiples)):
		if not multiples[n]: primes.append(n)
	
	return primes
	
# ------- M A I N --------

primes=sieve1(30000000)
len(primes)

kln = list()
for i in range(len(primes)):
	kln.append((i+1)*log(primes[i]))

plot(primes, kln, 'r.')
xlabel("p_k")
ylabel("k * ln(p_k)")
show()
	
#print len(primes), len(kln)

#print p1[:3]
#print p2[:3]

#print p1[-3:]
#print p2[-3:]