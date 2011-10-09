from numpy import array

class Triangle:
	def __init__(self, a=array([0,0]), b=array([0,0]), c=array([0,0]), id=0):
		self.a = array(a)
		self.b = array(b)
		self.c = array(c)
		self.id = id
		self.coo = [a,b,c]
	
	def update(self):
		self.a = self._coo[0]
		self.b = self._coo[1]
		self.c = self._coo[2]
	
	def set_coo(self, arg):
		#setter, accepts either:
		# - 6 numbers
		# - a list/array of 6 numbers
		# - a list of 3 lists /arrays with coordinate pairs
		# - a array (x,y) and a id (0=a, 1=b, 2=c) to change only one point
		#   [[3,2],1] change point b to (3,2)
		#print 'setting coord', arg
		if len(arg)==6:
			#print 'one long list'
			self.coo = [array([arg[0],arg[1]]), array([arg[2],arg[3]]), array([arg[4],arg[5]])]
			self.update()
			return
		elif len(arg)==1 and len(arg[0])==6:
			#print 'list of list'
			self.coo = [array([arg[0][0],arg[0][1]]), array([arg[0][2],arg[0][3]]), array([arg[0][4],arg[0][5]])]
			self.update()
			return
		elif len(arg)==3 and len(arg[0])==2 and len(arg[1])==2 and len(arg[2])==2:
			#print 'list with coordinate pairs'
			self.coo = [array([c[0],c[1]]), array([c[2],c[3]]), array([c[4],c[5]])]
			self.update()
			return
		elif len(arg)==2 and len(arg[0])==2:
			#print 'unique coordiante pair'
			if arg[1]==0: self.a = array([arg[0][0],arg[0][1]])
			if arg[1]==1: self.b = array([arg[0][0],arg[0][1]])
			if arg[1]==2: self.c = array([arg[0][0],arg[0][1]])
			self.coo = [self.a, self.b, self.c]
			return
			
		raise Exception('Error, wrong coordinate format')
		return False

	def get_c(self):
		return list([self.a[0], self.a[1], self.b[0], self.b[1], self.c[0], self.c[1]])

	#this is the simplified crossp
	def cp(self,x,y):
		return x[0]*y[1]-x[1]*y[0]	#collision detection

	def getArea(self):
		area = self.cp(self.a-self.b,self.c-self.b)//2
		if area<0:area=area*(-1)
		return area
		
	def isIn(self, xo, yo):
	#collision detection, is point inside this figure
	# basic idea: take crossproduct(AP, AC) and crossp(AB, AP)
	# if they have the same sign, p is inside a cone
	# do the same with (BP, BA) and (BC, BP)
	# crossp(A,B) in 2d is simply: Ax*By-Ay*Bx
	# x,y have same sign <=> x*y>0 use div because of overflowss occuring
		
		#create some shortcuts
		A=array(self.a)
		B=array(self.b)
		C=array(self.c)
		P=array([xo,yo])
		
		#print self.tri.a, B, C, P
		#print type(self.tri.a), type(B), type(C), type(P) 
		
		if self.cp(P-A,C-A)//self.cp(B-A,P-A)>=0:
			if self.cp(P-B,A-B)//self.cp(C-B,P-B)>=0:
				return True
		return False