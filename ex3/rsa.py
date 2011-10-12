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
from numpy import sqrt, uint64, int64, array

tp = int64

#--------------------------------------------------------------------------
# SETTINGS
#--------------------------------------------------------------------------

def encrypt(msg, publ_key):
	return pow(msg, publ_key[1], publ_key[0])


def decrypt(msg, prvt_key):
	return pow(msg, prvt_key[1], prvt_key[0])


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
		e = choice(primes[10:min(100, max)]) #choose one of the first 100 primes, should be sufficant
		#e = 23
		k, d = bizout(totient, e)
		if e < totient and ggt(e,totient) == 1 and d > 0:
			break
	
	#t, k, d = extEuklid(totient, e)
	
	#if d < 0: d = k
	
	print "p", p, "q", q, "N", p*q, "Tot", totient, "e", e, "d", d, "k", k
	
	return [p*q, e], [p*q, d] #return [public key pair, private key pair]


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
	q = a // b
	r = a - q * b
	x, y = bizout(b, r)
	return y, x - q * y


def extEuklid(a,b):
	if b == 0:
		return (a, 1, 0)
	d, s, t = extEuklid(b, a%b)
	return d, t, s - a//b*t


def hack(msg, pubkey):
	r=1
	while pow(msg, r, pubkey[0]) != 1:
		r += 1
		print r
		
	d = 1111 # something like = ( 1 + m*r ) //c
	
	return decrypt(msg, [pubkey[1], pubkey[0]*d])
	

# demo of rsa encr and decry
msg = "h"
msg_e = encode(msg)
pubkey, prikey = gen_key(10,30)#msg_e)

msg_s = encrypt(msg_e, pubkey)
msg2_e = decrypt(msg_s, prikey)

msg2 = decode(msg2_e)

print msg_s, msg2_e
print msg, msg2

# hack a msg
print decode(hack(msg_s, pubkey))

#b_pub = [1024384027, 910510237]
#msg = 100156265
#print decode(hack(msg, b_pub))