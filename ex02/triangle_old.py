from Tkinter import *
import time
from numpy import array#, cross

# class Triangle:
	
	# def __init__(self, canvas, coordi):
		# global canv, coord, obj
		# canv = canvas
		# coord = list()
		# coord = coordi
		# obj = canv.create_polygon(coord)
		
	# def paint(self):
		# canv.delete(obj)
		# canv.update()

class App:

	def __init__(self, master):
		global canv
		global xo, yo
		global move_line, move_oval
		global got_edge
		
		canv = Canvas(root, width = 300, height = 300)
		canv.bind("<Button-1>", self.clicked)
		canv.bind("<B1-Motion>", self.moved)
		canv.bind("<ButtonRelease-1>", self.released)
		canv.pack()
		
		#global triangle
		#triangle = Triangle(canv, [[0,0],[50,0],[25,50]])
		
		global tri, tri_obj
		tri = [[0,0],[50,0],[25,50]]
		tri_obj = canv.create_polygon(tri)
		
		frame = Frame(master)
		frame.pack()

		self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
		self.button.pack(side=LEFT)

		self.hi_there = Button(frame, text="Hello", command=self.say_hi)
		self.hi_there.pack(side=LEFT)
		
		got_edge = 0
		move_line = 0
		move_oval = 0

	def say_hi(self):
		print "hi there, everyone!"

	def clicked(self, event) :
		global xo, yo, got_edge, move_line, move_oval
		
		tol = 40 #egde snap tolerance, in sqrt(tol) = radius
		xo = event.x
		yo = event.y
		got_edge=0
		print xo, yo
		
		
		for i in range(3):
			if (xo-tri[i][0])*(xo-tri[i][0])+(yo-tri[i][1])*(yo-tri[i][1]) < tol:
				got_edge = i+1
				print 'got edge',i
		
		if got_edge == 0:
			isInSide=self.colDet(xo,yo)
			self.ani(xo,yo,isInSide)
			#move_line = canv.create_line(xo, yo, xo, yo)
			#move_oval = canv.create_oval(xo - 6, yo - 6, xo + 6, yo + 6)
		
	#collision detection
	def colDet(self,xo,yo):
# basic idea: take crossproduct(AP, AC) and crossp(AB, AP)
# if they have the same sign, p is inside a cone
# do the same with (BP, BA) and (BC, BP)
# crossp(A,B) in 2d is simply: Ax*By-Ay*Bx
# x,y have same sign <=> x*y>0

		#this is the simplified crossp
		def cp(x,y):
			return x[0]*y[1]-x[1]*y[0]
		
		global tri
		
		#cearte some shortcuts
		A=array(tri[0])
		B=array(tri[1])
		C=array(tri[2])
		P=array([xo,yo])

		if cp(P-A,C-A)*cp(B-A,P-A)>0:
			if cp(P-B,A-B)*cp(C-B,P-B)>0:
				return True
		
		return False
	
	
# this was my first try, did'nt work, because wrong idea
# uses projections to x and y axis
	'''
		global tri, tri_obj
		liesIn = 0
		cor=tri[:]
		cor.append(tri[0])
		#cor.append(tri[1])
		rangeside = [[[],[],[]]]*2
		
		print cor
		
		for i in range(3):
			for dim in [0,1]:
				if cor[i][dim] < cor[i+1][dim]: rangeside[dim][i] = range(cor[i][dim], cor[i+1][dim])
				else: rangeside[dim][i] = range(cor[i+1][dim], cor[i][dim])
		
		range12 = range13=range23 = [[]]*2
		for dim in [0,1]:
			range12[dim] = rangeside[dim][0] +rangeside[dim][1]
			range13[dim] = rangeside[dim][0] + rangeside[dim][2]
			range23[dim] = rangeside[dim][1] + rangeside[dim][2]
		
		print range12[0], xo
		
		if xo in range12[0] or xo in range13[0] or xo in range23[0]:
			if yo in range12[1] or yo in range13[1] or yo in range23[1]:
				liesIn+=1
				print 'eine kante drin'
				return True
				
		if liesIn>=2: return True
		return False
'''


	def moved(self, event) :
		global xo, yo, got_edge, move_line, move_oval, tri, tri_obj
		#canv.delete(move_line)
		x = event.x
		y = event.y
		
		if got_edge == 0:
			canv.coords(move_line,xo,yo,x,y)
			canv.coords(move_oval,x - 6, y - 6, x + 6, y + 6)
		else:
			print tri, [x,y]
			tri[got_edge-1] = [x,y]
			print tri
			canv.delete(tri_obj)
			tri_obj = canv.create_polygon(tri)
		
	def released(self, event):
		global xo, yo, got_edge, move_line, move_oval
		if got_edge == 0:
			canv.delete(move_line)
			canv.delete(move_oval)
		got_edge = 0

	def ani(self, x,y,isOn):
		global anio
		if isOn: color="red"
		else: color = "blue"
		for i in range(25,0,-1):
			anio = canv.create_oval(x - 2*i, y - 2*i, x + 2*i, y + 2*i)
			canv.itemconfigure(anio,fill=color)
			canv.update()
			canv.after(10)
			canv.delete(anio)
			
			
	
root = Tk()
app = App(root)
root.mainloop()
