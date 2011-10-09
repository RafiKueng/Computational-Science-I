from Tkinter import *
from numpy import array
from triangle import Triangle
from collections import deque

class App:
	def __init__(self, master):
		self.dim = 500
		#init vars
		self.got_edge = 0
		#self.move_line = 0
		#self.move_oval = 0
		self.anistack = deque()
		self.moveanistack = deque()

		# create paining area
		self.canv = Canvas(root, width = self.dim, height = self.dim)
		self.canv.bind("<Button-1>", self.clicked)
		self.canv.bind("<B1-Motion>", self.moved)
		self.canv.bind("<ButtonRelease-1>", self.released)
		self.canv.pack()
		
		self.tri = Triangle([50,70],[300,300],[400,100])
		self.tri.id = self.canv.create_polygon(self.tri.coo,fill='yellow')
		
		frame = Frame(master)
		frame.pack()

		self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
		self.button.pack(side=LEFT)

		self.hi_there = Button(frame, text="Reset", command=self.reset)
		self.hi_there.pack(side=LEFT)
		

	def reset(self):
		print "reset isn't yet implemented, please just restart :)"

	def clicked(self, event) :
		#global xo, yo, got_edge, move_line, move_oval
		
		tol = 40 #egde snap tolerance, in sqrt(tol) = radius
		r = 6 #radius of moving animation

		#init vars and shortcut
		self.xo = xo = event.x
		self.yo = yo = event.y
		self.p = array([xo,yo])
		self.got_edge = 0
		tri = self.tri.coo

		for i in range(3):
			if (xo-tri[i][0])*(xo-tri[i][0])+(yo-tri[i][1])*(yo-tri[i][1]) < tol:
				self.got_edge = i+1
				#print 'got edge',i
		
		# if not clicking on a edge
		if self.got_edge == 0:
			isInSide=self.tri.isIn(xo,yo) # collision detection
			self.ani(xo,yo,isInSide)
			#move_line = self.canv.create_line(xo, yo, xo, yo)
			#move_oval = self.canv.create_oval(xo - r, yo - r, xo + r, yo + r)
			#self.moveanistack.append([move_line, move_oval])
		
	#this is the simplified crossp
	def cp(self,x,y):
		return x[0]*y[1]-x[1]*y[0]	#collision detection
		
# collision detection moved to triangle class, as for each object different...
#	def colDet(self,xo,yo):
# basic idea: take crossproduct(AP, AC) and crossp(AB, AP)
# if they have the same sign, p is inside a cone
# do the same with (BP, BA) and (BC, BP)
# crossp(A,B) in 2d is simply: Ax*By-Ay*Bx
# x,y have same sign <=> x*y>0 use div because of overflowss occuring


		
		#create some shortcuts
#		A=array(self.tri.a)
#		B=array(self.tri.b)
#		C=array(self.tri.c)
#		P=array(self.p)
		
		#print self.tri.a, B, C, P
		#print type(self.tri.a), type(B), type(C), type(P) 
		
#		if self.cp(P-A,C-A)//self.cp(B-A,P-A)>=0:
#			if self.cp(P-B,A-B)//self.cp(C-B,P-B)>=0:
#				return True
#		return False


	def moved(self, event) :
		# coordinates moved to
		x = event.x
		y = event.y
		
		if self.got_edge == 0:pass
			#while len(self.moveanistack)>1:
			#	ml, mo = self.moveanistack.popleft()
			#	self.canv.delete(ml)
			#	self.canv.delete(mo)
			
			#ml, mo = self.moveanistack.pop()
			#self.canv.coords(ml,xo,yo,x,y)
			#self.canv.coords(mo,x - 6, y - 6, x + 6, y + 6)
		else:
			self.tri.set_coo([[x,y],self.got_edge-1])
			self.canv.delete(self.tri.id)
			#print '-------------\n',self.tri.coo
			area = self.tri.getArea()
			area = area*255//(self.dim*self.dim)
			if area>255:area=255
			#print '-------------\n',area
			color = "#%02x%02x%02x" % (255, 255-area, 0)
			self.tri.id = self.canv.create_polygon(self.tri.get_c(),fill=color)
		self.canv.update()
		
	def released(self, event):
		#if self.got_edge == 0:
		#	while len(self.moveanistack)>0:
		#		ml, mo = self.moveanistack.popleft()
		#		self.canv.delete(ml)
		#		self.canv.delete(mo)
		self.got_edge = 0

	def ani(self,x,y,isOn):
		#clean up the stack, delete all remaining animation artifacts
		while len(self.anistack) > 0:
			self.canv.delete(self.anistack.popleft())
		
		if isOn: color="green"
		else: color = "red"
		
		f = 1 # size factor
		
		for i in range(50,0,-1):
			ani = self.canv.create_oval(x - f*i, y - f*i, x + f*i, y + f*i)
			self.anistack.append(ani)
			self.canv.itemconfigure(ani,fill=color)
			self.canv.update()
			self.canv.after(5)
			if len(self.anistack)>0:
				self.canv.delete(self.anistack.pop())
			
			
	
root = Tk()
app = App(root)
root.mainloop()
