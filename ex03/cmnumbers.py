'''--------------------------------------------------------------------------
 Carmichael Number Generator
--------------------------------------------------------------------------
 Explanation:
    generates carmichael numbers (runs in parallel)

 How this code works 
    refere to doc, p.XX
    
    
 Notes / Convention:
    One part uses multiple cores to try to crack the encryption
    basic idea for multicore implementation from this site:
    http://www.doughellmann.com/PyMOTW/multiprocessing/communication.html#multiprocessing-queues
 
--------------------------------------------------------------------------
 Rafael Kueng
    v1 basic implementation with multicore support
 
 BUGS / TODO:
    spawning for each number it's own task may produce much overhead... check for this... see bench at bottom
 
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
            if answer[0]: 
                #print 'answer', answer
                self.result_queue.put(answer[1])
        return


class Task_cm_check(object):
    def __init__(self, id, num):
        self.id = id
        self.num = num

    def __call__(self):
        #time.sleep(0.1) # pretend to take some time to do the work
        #print 'id', self.id
        
        if isprime(self.num):
            return [False, self.num]

        copri = coprimes(self.num)

        for i in range (len(copri)):
            if pow(copri[i],self.num-1,self.num) != 1:
                return [False, self.num]

        return [True, self.num]


        while r < self.range[1]:
            #print r
            if pow(self.msg, r, self.pubkey[0]) == 1:
                #print 'Result', r
                return r
            r += 1
        return -1
    def __str__(self):
        return string.join(['id', `self.id`, 'num', `self.num`])




def genCM(n_mc_numbers, processes=0):
    '''Uses multiple cores to try generate [n_mc_numbers] carmichael numbers
    using [processes] cores (processes = 0: auto detection of num cores)
    basic idea for multicore implementation from this site:
    http://www.doughellmann.com/PyMOTW/multiprocessing/communication.html#multiprocessing-queues
    '''
    
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start workers
    if processes == 0:
        if multiprocessing.cpu_count() == 1: # single processor machine
            num_workers = 1
        else:
            num_workers = multiprocessing.cpu_count() - 1 # give one to the os...
    else:
        num_workers = processes

    print '\n---------------------------------------------------------------------'
    print 'Starting Carmichael Number generation'
    print '---------------------------------------------------------------------'
    print '\n                             ...creating %d workers\n' % num_workers
    workers = [ Worker(tasks, results) for i in xrange(num_workers) ]
    for w in workers:
        w.start()


    loop_cnt = 0
    taskcnt = 0
    aborted = False
    
    
    print 'Searching for', n_mc_numbers,'Carmichael Numbers...'
    
    while results.qsize() < n_mc_numbers: # check from time to time whether there's a result or empty queue
        if taskcnt > 20000: # abort anyways after cnt checked numbers
            aborted = True #implement handle for this later
            break
        if tasks.qsize() < num_workers * 2: # fill up queue if it's running low
            for i in range(num_workers):
                tasks.put(Task_cm_check(taskcnt,taskcnt+1)) # each task is checking a number, with offset 1..
                if taskcnt%1000 == 0:
                    print '   ... checking range: ', taskcnt+1, '-', taskcnt+1000
                taskcnt += 1
        loop_cnt += 1
        #sleep(0.1) # suspend loop, free up some cpu time for workers, don't do this here, workers are waiting for jobs else...


    # Add a poison pill for each Worker
    print '\nsending kill signal to processes....'
    for i in xrange(num_workers):
        tasks.put(None)
    print '                                    ...done'

    
    # calm down (let some old tasks finish running)
    print 'cleaning up processes and queues...'
    while tasks.qsize() > 0:
        sleep(0.5)
    print '                                    ...done'

    # Wait for all of the tasks to finish
    print 'waiting for processes to shutdown....'
    tasks.join()
    print '                                    ...done'

    
    print 'extracting results...'
    r = []
    while results.qsize():
        r.append(results.get(True, 0.1)) # trow away additional solutions
    print '                                    ...done'


    print '\n\n------------------------------------------------'
    print ' Final Result: '
    print '------------------------------------------------'
    for i, ele in enumerate(r):
        print 'CM Numer #:', i+1, 'is:', ele
    print '------------------------------------------------'
    print 'stats:'
    print '   spawned tasks:', taskcnt
    print '   loop counter :', loop_cnt
    print '------------------------------------------------'

    return True



def gcd(a, b):
    if a < b: a,b = b,a
    while a%b != 0:
        a,b = b,a%b
    return b


def coprimes(n):
    '''get the coprimes of n'''
    coprimes=[]

    for a in range(1,n):
        if(gcd(a,n) == 1):
            coprimes.append(a)         
    return coprimes


def isprime(n):
    '''test if its prime, based on this description
    http://pythonism.wordpress.com/2008/05/04/looking-at-prime-numbers-in-python/
    '''
    n*=1.0
    if n%2==0 and n!=2 or n%3==0 and n!=3:
        return False
    for b in range(1,int((n**0.5+1)/6.0+1)):
        if n%(6*b-1)==0:
            return False
        if n %(6*b+1)==0:
         return False
    return True



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


if __name__ == '__main__':
    genCM(8) # use genCM(#number, #worker) to manually set the number of parallel workers
    #don't excagerate, on a 8 core (7 workers) 2ghz machine,
    # Some benches
    # getting 6 takes 13 sec
    # getting 7 takes 24 sec
    # getting 8 takes 34 sec ...
    # getting 8 with 4 workers takes 40.5 sec ...
    # getting 8 with 7 workers takes 34 sec ...
    # getting 8 with 16 workers takes 31.5 sec ...
    #   so indeed look like too much cpu overhead from generating task classes...