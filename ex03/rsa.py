'''--------------------------------------------------------------------------
 RSA encrypt / decrypt / brute force crack
--------------------------------------------------------------------------
 Explanation:
	demonstration of a rsa implementation
		(key generator, sample encding of asci symbols, encryption, decryption)
	demonstration of a brute force attack on the public key
		(a simple, seriell version, and a pimped parallel version)

 How this code works 
	refere to doc, p.XX
	and wikipedia/rsa (both engl and german)
	
	
 Notes / Convention:
	One part uses multiple cores to try to crack the encryption
	basic idea for multicore implementation from this site:
	http://www.doughellmann.com/PyMOTW/multiprocessing/communication.html#multiprocessing-queues
 
--------------------------------------------------------------------------
 Rafael Kueng
 v1 basic implementation
 v2 multicore support
 
 BUGS / TODO:

--------------------------------------------------------------------------
'''

from random import choice, seed
from numpy import sqrt, uint64, int64, array
import multiprocessing
from time import sleep
import string


#--------------------------------------------------------------------------
# SETTINGS
#--------------------------------------------------------------------------


class Worker(multiprocessing.Process):
    
	def __init__(self, task_queue, result_queue):
		multiprocessing.Process.__init__(self)
		self.task_queue = task_queue
		self.result_queue = result_queue

	def run(self):
		proc_name = self.name
		while True:
			next_task = self.task_queue.get()
			if next_task is None:
				# Poison pill means shutdown
				#print '%s: Exiting' % proc_name
				self.task_queue.task_done()
				break
			#print '%s: (%s)' % (proc_name, next_task)
			answer = next_task()
			self.task_queue.task_done()
			#print 'answer', answer
			if answer >= 0:
				#print 'answer', answer
				self.result_queue.put(answer)
		return


class Task_r(object):
	def __init__(self, id, msg, pubkey, range):
		self.id = id
		self.msg = msg
		self.pubkey = pubkey
		self.range = range

	def __call__(self):
		#time.sleep(0.1) # pretend to take some time to do the work
		#print 'id', self.id, self.range
		r = self.range[0]
		while r < self.range[1]:
			#print r
			if pow(self.msg, r, self.pubkey[0]) == 1:
				#print 'Result', r
				return r
			r += 1
		return -1
	def __str__(self):
		return string.join(['id', `self.id`, 'msg', `self.msg`, 'pubkey', `self.pubkey`, 'range', `self.range`])

		
class Task_d(object):
	def __init__(self, id, r, pubkey, range):
		self.id = id
		self.r = r
		self.c = pubkey[1]
		self.range = range

	def __call__(self):
		#time.sleep(0.1) # pretend to take some time to do the work
		#print 'id', self.id, self.range
		
		d = self.range[0]
		r = float(self.r)
		m = 0
		while d < self.range[1]:
			m = (self.c * d - 1) / r
			if int(m) == m:
				return d
			d += 1

		return -1

	def __str__(self):
		return string.join(['id', `self.id`, 'r', `self.r`, 'pubkey', `self.c`, 'range', `self.range`])




def crack_mc(msg, pubkey):
	'''Uses multiple cores to try to crack the encryption
	basic idea for multicore implementation from this site:
	http://www.doughellmann.com/PyMOTW/multiprocessing/communication.html#multiprocessing-queues
	'''
	
	# Establish communication queues
	tasks = multiprocessing.JoinableQueue()
	results = multiprocessing.Queue()

	# Start workers (maybe even more would be good? but they tend to totally lock my win machine...
	if multiprocessing.cpu_count() == 1: # single processor machine
		num_workers = 1
	else:
		num_workers = multiprocessing.cpu_count() - 1 # give one to the os...

	print '\n---------------------------------------------------------------------'
	print 'Starting MultiCore Bruteforce attak'
	print '---------------------------------------------------------------------'
	print '\n                             ...creating %d workers\n' % num_workers
	workers = [ Worker(tasks, results) for i in xrange(num_workers) ]
	for w in workers:
		w.start()


	cnt_r = cnt_d = 0
	taskcnt_r = taskcnt_d = 0
	delta_r = 20000 # how many r's should one worker check, more = less overhead
	delta_d = 10000
	abort_r = abort_d = False
	start_r = 2 #0 # ususally = 0, except you wanna continie a previous run...
	
	taskcnt_r = (start_r-2) // delta_r
	
	print 'Searching for r...'
	
	while results.empty(): # check from time to time whether there's a result or empty queue
		if cnt_r > 20000:
			abort_r = True
			break
		if tasks.qsize() < num_workers + 2:
			for i in range(num_workers):
				tasks.put(Task_r(taskcnt_r, msg, pubkey, [taskcnt_r*delta_r+2, (taskcnt_r+1)*delta_r+2]))
				print '   ... in range: ', [taskcnt_r*delta_r+2, (taskcnt_r+1)*delta_r+2]
				taskcnt_r += 1
		cnt_r += 1
		sleep(0.1)

	r = results.get(True, 1)
	print '--> GOT IT:', r
	
	print '\ncleaning up processes and queues...'
	# calm down (let some old tasks finish running)
	while tasks.qsize() > 0:
		sleep(0.5)
	while results.qsize():
		results.get(True, 0.1) # trow away additional solutions
	print '                                    ...done'

	
	print '\nSearching for d\'...'
	while results.empty():
		if cnt_d > 100:
			abort_d = True
			break
		if tasks.qsize() < num_workers + 2:
			for i in range(num_workers):
				tasks.put(Task_d(taskcnt_d, r, pubkey, [taskcnt_d*delta_d+2, (taskcnt_d+1)*delta_d+2]))
				print '   ... in range:', [taskcnt_d*delta_d+2, (taskcnt_d+1)*delta_d+2]
				taskcnt_d += 1
		cnt_d += 1
		sleep(0.1)
		
	d = results.get(True, 1)
	print '--> GOT IT:', d, '\n'
	
	# Add a poison pill for each Worker
	print 'sending kill signal to processes....'
	for i in xrange(num_workers):
		tasks.put(None)
	print '                                    ...done'

	# Wait for all of the tasks to finish
	print 'waiting for processes to shutdown....'
	tasks.join()
	print '                                    ...done'

	print '\n\n------------------------------------------------'
	print ' Final Result: r:', r,'d\':', d
	print ' Bruteforced Private Key:', [pubkey[0], d]
	print '------------------------------------------------'
	print 'stats: spawned tasks: for r:', taskcnt_r, '; for d:', taskcnt_d
	print '       loop counter : for r:', cnt_r, '; for d:', cnt_d
	#	num_jobs -= 1
	return [pubkey[0], d]


def demo():
	# fast demo of rsa encr and decry
	msg_plain = "abc"  # dont use too lang msg, otherwise it'll take hours to produce an overflow..
		# for chars already take like minutes
	msg_encoded = encode(msg_plain)
	pubkey, prikey = gen_key(10,msg_encoded)
	msg_secure = encrypt(msg_encoded, pubkey)
	msg_decrypted = decrypt(msg_secure, prikey)
	msg_decoded = decode(msg_decrypted)

	bf_key = crack(msg_secure, pubkey)
	msg_bf_decrypted = decrypt(msg_secure, bf_key)
	msg_bf_decoded = decode(msg_bf_decrypted) # hack the encrypted msg

	# output
	print '\n\n'
	print '---------------------------------------------------------------------'
	print 'Results of the Simple Demonstration:'
	print '---------------------------------------------------------------------'
	print 'public key     :', pubkey
	print 'private key    :', prikey
	print 'bruteforced key:', bf_key
	print '---------------------------------------------------------------------'
	print "original message   :", msg_plain
	print "secure message     :", msg_secure
	print 'decrypted message  :', msg_decrypted
	print 'decoded message    :', msg_decoded
	print "bruteforced message:", msg_bf_decoded ,'\n\n'
	
	return msg_plain, msg_encoded, msg_secure, pubkey


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
	
	print '\n---------------------------------------------------------------------'
	print ' Key Generator:'
	print '---------------------------------------------------------------------'
	print "p:", p, "q:", q, "N:", p*q, "Totient:", totient, "e:", e, "d:", d, "k:", k
	#print '---------------------------------------------------------------------'

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


def crack(msg, pubkey):
	#returns a key able to crack the encryption
	r=1
	N = pubkey[0]
	c = pubkey[1]

	while pow(msg, r, N) != 1:
		r += 1
		#if r%1000000==0: print 'r', r
		
	#print '---------------\n r:', r
	
	#m=???
	#d_new = (1 + m*r) // pubkey[1] # something like = ( 1 + m*r ) //c
	d_new = 0
	r = float(r)
	while True:
		d_new += 1
		m = (c * d_new - 1) / r
		#if d_new%1000000==0: print 'd_new, m=', d_new, m
		
		if int(m) == m:
			break
	
	#print 'I got: r',r,'m',m,'d_new',d_new
	
	return [pubkey[0], d_new]
	

if __name__ == '__main__':
	# first a demo of encoding encrypting, decoding decrypting, seriell hacking
	# displys results on screen and saves the simple example for next one
	msg_plain, msg_encoded, msg_secure, pubkey = demo()
	
	
	# for testing, call the multicore cracker with simple stuff, aka results from demo
	prikey = crack_mc(msg_secure, pubkey)
	msg_dec=decrypt(msg_secure, prikey)
	print '\n\nSECRET TEXT:', decode(msg_dec),'\n\n'
	
	# now the real test, the assignment / excersice...
	
	b_pub = [1024384027, 910510237]
	msg = 100156265
	prikey = crack_mc(msg, b_pub)
	msg_dec=decrypt(msg, prikey)
	print '\n\nSECRET TEXT:', decode(msg_dec),'\n\n'
	

	
