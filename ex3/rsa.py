#--------------------------------------------------------------------------
# RSA encrypt / decrypt / brute force crack
#--------------------------------------------------------------------------
# Explanation:
#   
#
# How this code works 
#
#
# Notes / Convention:
#
#--------------------------------------------------------------------------
# Rafael Kueng
# v1
# 
# BUGS / TODO:
#
#--------------------------------------------------------------------------

from random import choice, seed
from numpy import sqrt

#--------------------------------------------------------------------------
# SETTINGS
#--------------------------------------------------------------------------

def encrypt(msg, priv_key):
	return pow(msg, priv_key[1], priv_key[0])


def decrypt(msg, pub_key):
	return pow(msg, pub_key[1], pub_key[0])


def encode(plain_word):
	enc_word = 0
	for i, c in enumerate(plain_word):
		if c < "a" or c > "z": c = "{"
		enc_word += (ord(c) - 96)*32**i
	return enc_word


def decode(enc_word):
	plain_word = ""
	while enc_word > 0:
		c = chr(enc_word % 32 + 96)
		if c < "a" or c > "z": c = " "
		plain_word += c
		enc_word /= 32
	return plain_word


def gen_key(rnd_init, max):

	seed(rnd_init)
	primes = primelist(max)
	
	while True:
		p = choice(primes)
		q = choice(primes)
		if p*q >= max:
			break
	#p = 11
	#q = 13
	
	totient = (p - 1) * (q - 1)
	
	while True:
		e = choice(primes[0:100]) #choose one of the first 100 primes, should be sufficant
		#e = 23
		if e<totient and ggt(e,totient)==1:
			break
	
	k, d = bizout(totient, e)
	
	if d<0:
		tmp = d
		d = k
		k = tmp
	
	print "p", p, "q", q, "N", p*q, "Tot", totient, "e", e, "d", d, "k", k
	
	return [[p*q, e],[p*q, d]] #return [public key pair, private key pair]
	
def ggt(a, b):
	if a < b: a,b = b,a
	while a%b != 0:
		a,b = b,a%b
	return b
	
def primelist(max):
# copy from sieve.py, ex2
	primes = list()
	multiples = [False] * (max+1) #is this nr a multiple of any other value?
	
	for i in range(2,int(sqrt(max+1))+1): #+1 to account for rounding errors
		if multiples[i]: continue
		for j in range(i*i,max+1,i):
			multiples[j]=True

	for n in range(1,len(multiples)):
		if not multiples[n]: primes.append(n)
	
	return primes
	
def bizout(a, b):
	if b == 0:
		return (1, 0)
	q = a / b
	r = a - q * b
	x, y = bizout(b, r)
	return (y, x - q * y)


def hack():
	return 0