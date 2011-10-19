# multiprocessoring test

from multiprocessing import Process, Queue, Lock, current_process
from Queue import Empty
from time import sleep

def f(name, lock, jobs, res):
	lock.acquire()
	print name, 'starting'
	lock.release()
	
	goOn = True
	
	while goOn:
		try:
			lock.acquire()
			print name, 'getting job'
			lock.release()
			a=jobs.get(True, 1) # wait 1 sec for jobqueue to fill up again...
			
			lock.acquire()
			print name, 'starting job',a
			lock.release()
			
			if a == 5:
				res.put(a)
			
		except Empty:
			lock.acquire()
			print name, 'queue empty'
			lock.release()
			goOn = False
			
	lock.acquire()
	print name, 'quitting'
	lock.release()
	return

		
		
if __name__ == '__main__':
	n = 2
	Workers = []
	
	jobs = Queue()
	res = Queue()
	lock = Lock()
	
	for i in range(n):
		worker = Process(target=f, args=(i,lock,jobs,res,))
		Workers.append(worker)
	

	
	for each in Workers:
		each.start()


	goOn = True
	cnt = 0
	
	while True:
		sleep(0.5)
		if cnt >= 20: break
		try:
			r=res.get(False)
			lock.acquire()
			print '----------',r
			lock.release()
			break
		except Empty:
			print 'sz', jobs.qsize(), 'cnt', cnt
			while jobs.qsize() < n * 2 + 1:
				jobs.put(cnt)
				cnt += 1

				
	
	for each in Workers:
		each.join()
