def nroot(a, n=2, epsilon=0.0):
	# Calculates the n-th root of a using the newton approximation
	# input:
	#		a:	n-th root of a
	#		n=2:	n-th root of a
	#		epsilon=0.0:	desired precesision of result
	# return:
	#		x = nroot(a)
	#--------------------------------------------------------------------------
	# x = nroot(a)
	# <==> a = x^n <==> 0 = x^n - a
	# def: f(x) = x^n - a and solve for x, where f(x)=0
	# using newton verfahren
	# (@x_i: tangente t an kurve f(x), schnitt t mit xachse => x_(i+1))
	# x_(i+1) = x_i - f(x) / f'(x)
	#		= xi - (xi^n - a) / (n * xi^(n-1)) = ...
	#		= (n-1) / n * xi   +   a / n * xi^(1-n)
	#		def:	k1 = (n-1) / n
	#					k2 = a / n
	#					k3 = 1 - n
	#					for faster runtime
	# abort approx at given def. precesision or at float prec.
	#--------------------------------------------------------------------------
	# Rafael Kueng v1-2011.09.28-23:10
	#--------------------------------------------------------------------------
	
	# init const / settings
	k1 = (n-1) / float(n)
	k2 = a / float(n)
	k3 = 1-n
	i = 0									# counter
	delta = 1.0						# some not zero value for first run to happen
	x = 1									# starting value for newton verfahren

	epsilon = float(epsilon)	# precission to reach, put 0.0 max. float
	
	# main loop
	while delta > epsilon:
		i = i + 1
		x_old = x
		x = k1 * x + k2 * pow(x,k3)
		delta = float(abs(x - x_old))
		
		#debug output
		#print i, x, x_old, delta
	
	# additional output on screen
	print 'Found solution to problem',n,'nd/rd/th root of',a,'(in', i, 'steps):'
	print '   ',x
	return x
	
sol = nroot(2,2)
print 'Resultat: ', sol 