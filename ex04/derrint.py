'''
--------------------------------------------------------------------------
 derrivation  of Integrators
--------------------------------------------------------------------------
 Explanation:

 How this code works 

 Notes / Convention:

 
--------------------------------------------------------------------------
 Rafael Kueng
 v1 basic implementation
 
 BUGS / TODO:

--------------------------------------------------------------------------
'''

import numpy as np
import scipy as sp
import fractions as fr


def fivepoint(f, a, b, B = 1):
	"""Computes int_a^b f(x) dx
	using B blocks of the 5-point integrator.
	"""

	#integrators = []
	delta = (b-a)/float(B)
	integral = 0.
	
	for i in range(B):
		#print delta, np.array([a+i*delta,a+(i+1)*delta])
		c, pnt = derriveIntegrator(4,5,np.array([a+i*delta,a+(i+1)*delta]),False,False)
		#print c, pnt
		#integrators.append([c, pnt])
		for k in range(5):
			integral += c[k] * f(pnt[k])
			
	return integral
		
		
	#return integrators
	
#		derriveIntegrator(
#			max_degree=5,
#			n_points=5,
#			boundaries=np.array([a+i*delta,a+(i+1)*delta]),
#			incl_bounds = False,
#			is_sym = False):



		
def eval_poly(x, degrees):
	""" evaluates the function f(x) = sum over degrees of (x^degree)
	@param: x Parameter, the polynom is evaluated at
	@param: degrees List of degrees the function contains
	@return: The value of the function
	"""
	value = 0
	for i in degrees:
		value += pow(x,i)
	
	#print 'evaluating polynom with degrees', degrees, 'at pos x=', x, 'equals f(x)=', value
	return value

def eval_int(bounds, degrees):
	""" evaluates the integral of a function f(x) = sum over(degrees) (x^degree)
	@param: bounds list of len=2 with the boundaries of the Integral
	@param: degrees List of degrees the function contains
	@return: The integral of the polynom
	"""
	value = 0
	for x in reversed(bounds):
		for i in degrees:
			value += pow(x,i+1) * 1 / float(i+1)
		value *= -1
	#print 'evaluating int of poly with degrees', degrees, 'at pos x=', x, 'equals f(x)=', value
	return value
	
def derriveIntegrator(
			max_degree=2,
			n_points=3,
			boundaries=np.array([-1,1]),
			incl_bounds = True,
			is_sym = True):

	""" Derrives a n-point integrator ala newton, simpson, ...
	(if no arguments are given, a simpson integrator is returned)
	
	@param max_degree: up to which degree should the integrator be accurate?
	@param n_points: number of points to evaluate the integral at
	@param boundaries: integrate from boundaries[0] to boundaries[1]
	@param incl_bounds: evaluate the integral at boundaries?
	@param is_sym Is this symmetric?
	@return: Integrator-Class
	"""
	
	b_range = boundaries[1] - boundaries[0]
	delta = (b_range + incl_bounds) / float(n_points) # this does the same as the if below would do...
	#if incl_bounds:
	#	delta = (b_range + 1) / n_points
	#else:
	#	delta = b_range / n_points	

	degrees = range(0, max_degree+1, 1+is_sym) # if this is symetric (is_sym = true = 1), take only even degrees
	
	#generate the points inbetween..
	points = np.array(np.linspace(boundaries[0], boundaries[1], n_points, incl_bounds)
						+ delta / 2.0 * (not incl_bounds), dtype=float)
		# the last term shifts the points half a delta to the right if the
		# boundaries are NOT included
	
	#if its symetric, we only need the points >=0
	if is_sym:
		points = points[points>=0]
		n_points = len(points)
	
	
	#print status
	print '\nStatus:'
	print 'Deg:', degrees, '( max:', max_degree, '; num:',len(degrees),')'
	print 'Bounds:', boundaries, '( rng:',b_range,'; delta:', delta, ')'
	print 'Points:', points, '( tot:', n_points,')'
	
	f = np.zeros([len(degrees),n_points], dtype=np.float)
	res = np.zeros(len(degrees), dtype=np.float)
	
	for i_d, deg in enumerate(degrees):
		for i_x, x in enumerate(points):
			#print i_x, x, ';', i_d, deg
			f[i_d,i_x] = eval_poly(x, [deg])
			if is_sym and i_x!=0:
				f[i_d,i_x] *= 2
		res[i_d] = eval_int(boundaries, [deg])

	print '\nThe coefficents:'
	print f
	print '\nThe integrals:'
	print res
	
	try:
		sol = np.linalg.solve(f, res)
		print '\nFound a possible Integrator:'
		print sol
		print '\nExit integrator generator\n'
		return [sol, points]
	except np.linalg.LinAlgError:
		print '\nCan\'t solve this task, because the resulting matrix is not sqaure..\nCheck your values!'
		print '\nExit integrator generator\n'
		return False
	#print np.linalg.solve(f, res)


def gcd(num):
	a=num[0]
	b=num[1]
	if a < b: a,b = b,a
	while a%b != 0:
		a,b = b,a%b
	return b

	
	
def simplify(fraction):
	"""Simplifies a fraction, make sure to pass only numpy arrays!!
	"""
	mygcd = gcd(fraction)
	if mygcd > 1:
		fraction = simplify(fraction//mygcd)
	return fraction


	
def float2frac(fl, steps=20):
	"""converts a float number to a rational fraction using continued fraction expansion
	to get the continued fraction representation, then summing up to get the fraction
	(if some inital test for easy fractions fail)
	
	@param flt: float to convert
	@param tol: accuracy
	@return: [num, denum], array of int, such that num / denum = flt
	"""
	
	print '\nConverting the Float to a fraction...\n   float:',fl
	
	res = None
	
	# quick check if this is a easy fraction with denom somewhere <=1000
	for i in range(2,1001):
		t = fl * i
		if int(t) == t:
			print '   found it the easy way (try and error)'
			res = simplify(np.array([t, i], dtype=int))
			break
	
	# an other idea, obsolete with the part above, but anyway nice to have:
	# quick check if tis a fraction of the form x/9
	#repcheck = ((10*fl-fl)+2-2)
	#print 'repcheck', repcheck
	#if repcheck == int(repcheck): 
	#	res = simplify(np.array([repcheck, 9], dtype=int))
	#	print res
	#	return res		
	
	if res == None:
	# so, it isn't that easy, lets do a continued fraction expanision
		cfe = [] #continued fraction expanision
	
		cnt = 0
		i = 0.0
		tmp = 0.0
		acc = 20 # be accurate up to acc (binary) digits (tot available, float: 52)
	
		while cnt<steps:
			cnt += 1
			cfe.append(int(fl))
			rest = fl - int(fl)
			#if int(rest*2)//2 == 0:
			#	break #we're finished
			fl = 1 / rest
			#print 'fl, intfl, stuff', fl, int(fl), fl+pow(2,20)-pow(2,20), fl-(fl+pow(2,20)-pow(2,20))
			
			#print 'rest',rest
			#if fl - (fl+pow(2,acc)-pow(2,acc)) == 0: #not exactly sure why/if this really work, looks like... maybe just better check if fl > 1000 or anything... actually, do this...
			if fl > 10e6:
				#print fl, fl+pow(2,acc)-pow(2,acc)
				#print 'we\'re done'
				break
		
		print '   Found the continued fraction expanision:\n   ', cfe
		print '   ... in', cnt, 'steps (max.', steps, ')'
		
		# create the nominator, denominator, rewind the recursive fraction..
		a = 1
		b = cfe[cnt-1]
		cnt-=1
		while cnt > 0:
			cnt -= 1
			#print a, b, cnt, cfe[cnt]
			#exchange a, b
			a_old=a
			a = cfe[cnt]*a + b
			b = a_old
		
		#print a/float(b), b/float(a)
		res = res = simplify(np.array([a, b], dtype=int))
	
	print '\n   Result:  ',res[0],'/', res[1]
	print '      ( built-in Fractions gives:', fr.Fraction(fl).limit_denominator(),')\n'
	
	return res


if __name__ == '__main__':
	simpson_integrate = derriveIntegrator()
	bool_integrate = derriveIntegrator(4,5,[-2,2], True, True)

	#solve task 1
	coef, pnt = derriveIntegrator(4,5,[-5,5], False, True)
	faccoef = map(float2frac, coef)
	print faccoef 
	
	#testing the fivepoint function:
	fivepoint(lambda x: x*x, -5, 5, 4) #should equal 83.333
	
	#solve task 2
	# exp(-x^2) from -inf to +inf; using substitution x=tan(pi/2*y)
	f = lambda x: np.pi*np.exp(-np.tan(np.pi/2*x)*np.tan(np.pi/2*x))/(2*np.cos(np.pi/2*x)*np.cos(np.pi/2*x))
	sol1 = fivepoint(f, -1, 1, 4)
	sol2 = np.sqrt(np.pi)
	print "error compared to solution: ",sol1/sol2*100,"% accurate"
	