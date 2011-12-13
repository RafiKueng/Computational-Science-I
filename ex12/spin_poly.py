# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex12: Spinning Polygon
-------------------------------------------------------------------------------
Explanation:
    this is an implementation of a real time physics / graphics engine
    (your cpu speed doen't matter, nor should any additional cpuload,
    it's always the same speed in rads/sec!)
    
    ideas / concepts from "Introduction to Computergraphics", fs10
    http://www.ifi.uzh.ch/vmml/teaching/lectuces/30-computer-graphics-minf4226.html

    
    to let it rotate around a fixed axis change this line (around 188):
        rot.fromRot(self.angle, array([1,sin(self.angle),0.25]))
            
    to this:                    ___rotaxis___
        rot.fromRot(self.angle, array([1,1,0]))
    
How this code works:

    

Notes / Convention:
    Sooooorry, its way to much, i know... but i always wanted to try to
    implement my own graphics engine :)



-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-12-12   basic implementation
 
BUGS / TODO:



LICENSE:
    none
    
-------------------------------------------------------------------------------
"""



from Tkinter import *
from numpy import *
from numpy.linalg import norm
import exceptions
import time
import random as rnd

class quat(object):
    '''
    Represents a quaternion q = (w, x, y ,z)
    stripped down version, only works for usage in computer graphics,
    mathematically not correcly/completly implemented!
    '''
    
    def __init__(self, x0=0, x1=0, x2=0, x3=0):
        self.q = array([x0,x1,x2,x3])
        #print 'init quat:', self.q
    
    def fromRot(self, angle, vec):
        '''
        create quaternion describing rot around vec with angle
        '''
        s = sin(angle/2)
        vec = vec / norm(vec) #make sure vec is unit vec
        #print 'normed vec', vec
        self.q = array([cos(angle/2),
                        s*vec[0],
                        s*vec[1],
                        s*vec[2] ])
                        
    def getP(self):
        '''returns a 3d vector'''
        return array([self.q[1],self.q[2],self.q[3]])

    def __mul__(a, b):
        '''def of a*b'''
        x=a.q
        y=b.q
        return quat(x[0]*y[0]-x[1]*y[1]-x[2]*y[2]-x[3]*y[3],
                    x[0]*y[1]+x[1]*y[0]+x[2]*y[3]-x[3]*y[2],
                    x[0]*y[2]-x[1]*y[3]+x[2]*y[0]+x[3]*y[1],
                    x[0]*y[3]+x[1]*y[2]-x[2]*y[1]+x[3]*y[0])

    def __add__(x,y):
        return quat(*list(x.q + y.q))
        
    def __repr__(self):
        return 'Quat with w=%4.2f, x=%4.2f, y=%4.2f, z=%4.2f'%(self.q[0],self.q[1],self.q[2],self.q[3])
        
    def __invert__(self):
        '''retuns the inverted of the quaternion, i.e. ~q = q^-1
        assumes that q is a unit quaternion!!!
        '''
        return self.conj()
        #conj=self.conj()
        #if self.norm2()==1: # if unit quaternion, q^-1 = q'
        #    return conj
        #else:
        #    return quat(*list((self.q/self.norm()).conj()))
            #raise NotImplementedError
            
    def scale(self, s):
        '''scales the x,y,z components of quat with s[0], s[1] and s[2]'''
        x = self.q
        return quat(x[0],x[1]*s[0],x[2]*s[1],x[3]*s[2])
        
    def norm2(self):
        x=self.q
        return x[0]*x[0]+x[1]*x[1]+x[2]*x[2]+x[3]*x[3]
        
    def norm(self):
        return sqrt(self.norm2())
    
    def conj(self):
        '''returns a new, conjugated quat q' '''
        x = self.q
        return quat(x[0],-x[1],-x[2],-x[3])
        
    def rot(self, rotquat):
        '''returns new rotated quad, rotated by rotquat'''
        return rotquat*self*~rotquat
        
        
    
        
        
class drawable(object):
    '''Abstract class of an drawable object'''
    def __init__(self):
        raise NotImplementedError
    def register(self):
        raise NotImplementedError
    def draw(self):
        ''' initial drawing '''
        raise NotImplementedError
    def update(self, dt):
        '''update this figure'''
        raise NotImplementedError


class SpinningCube(drawable):
    def __init__(   self,
                    points=[quat(0,-1,-1,-1), quat(0,-1,-1,+1),
                        quat(0,-1,+1,-1), quat(0,-1,+1,+1),
                        quat(0,+1,-1,-1), quat(0,+1,-1,+1),
                        quat(0,+1,+1,-1), quat(0,+1,+1,+1) ],
                    v_rot=0.2, #rotation veolcity in rads / sec
                    rotdir=array([1,0,0]) #rotation direction (unit vector)
                    ):
        self.points = points
        self.v_rot = v_rot
        
        self.rotdir = rotdir
        self.rotdirfn = None
        self.trans = quat(0,0,0,0)
        self.scl = array([1,1,1])
        
        self.lines = [0 for i in range(12)]
        self.linecolor = ['black' for i in range(12)]
        self.linedash = [() for i in range(12)]
        self.x = [0 for i in range(8)]
        self.y = [0 for i in range(8)]
        
        #line nr index consists of points [i,j]
        self.point2line = [ [0,1],[2,3],[6,7],[4,5],
                            [1,5],[3,7],[2,6],[0,4],
                            [0,2],[4,6],[5,7],[1,3] ]
                            
        #point nr k is edge of lines [i,j,k]
        self.line2points = [[0,7,8],
                            [0,4,11],
                            [1,6,8],
                            [1,5,11],
                            [3,7,9],
                            [3,4,10],
                            [2,6,9],
                            [2,5,10] ]
        
        #neighbouring points, for occlusion check
        self.pnt2tri = [[1,2,4],
                        [0,3,5],
                        [0,3,6],
                        [1,2,7],
                        [0,5,6],
                        [1,4,7],
                        [2,4,7],
                        [3,5,6] ]
        self.angle=0.0

    def register(self, cam, canv):
        self.camera = cam
        self.canvas = canv

    def cp(self,x,y):
        '''this is the simplified crossp'''
        return x[0]*y[1]-x[1]*y[0]	#collision detection
        
    def isIn(self,p0,p1,p2,p3):
        '''checks whether p0 is inside p1,p2,p3'''
        
        #print 'isin',p0,p1,p2,p3
        P=p0#.getP()
        A=p1#.getP()
        B=p2#.getP()
        C=p3#.getP()


        if self.cp(P-A,C-A)//self.cp(B-A,P-A)>=0:
            if self.cp(P-B,A-B)//self.cp(C-B,P-B)>=0:
                return True
        return False
        
        """if self.cp(p0-p1,p3-p1)//self.cp(p2-p1,p0-p1)>=0:
            if self.cp(p0-p2,p1-p2)//self.cp(v-p2,p0-p2)>=0:
                return True
        return False        """
        
    def update(self, dt):

        self.angle += self.v_rot*dt
        if not self.rotdirfn==None:
            self.rotdir = self.rotdirfn(self.angle)
        #print 'updating', self.angle, self.v_rot, dt
        
        transp = self.transform(self.points)
        pp = map(self.camera.project, transp)
        
        #check if visible
        self.linecolor = ['black' for i in range(12)]
        self.linedash = [() for i in range(12)]

        for i,p in enumerate(pp):
            if self.isIn(p,pp[self.pnt2tri[i][0]],pp[self.pnt2tri[i][1]],pp[self.pnt2tri[i][2]]):
                if p[2]>(pp[self.pnt2tri[i][0]][2]+pp[self.pnt2tri[i][1]][2]+pp[self.pnt2tri[i][2]][2] )/3.: #depth check, dirty hack, only works with cam in z dir...
                    for k in range(3):
                        self.linecolor[self.line2points[i][k]] = 'grey'
                        self.linedash[self.line2points[i][k]] = (4,4)
            
        
        for n, (i,j) in enumerate(self.point2line):
            #print n,i,j,self.lines[n]
            self.canvas.coords(self.lines[n], pp[i][0],pp[i][1],pp[j][0],pp[j][1])
            self.canvas.itemconfig(self.lines[n], fill=self.linecolor[n], dash=self.linedash[n])
            
        pcross = map(self.camera.project, self.transform(self.cross))
        self.canvas.coords(self.pcrosslist[0], pcross[0][0], pcross[0][1], pcross[1][0], pcross[1][1])
        self.canvas.coords(self.pcrosslist[1], pcross[0][0], pcross[0][1], pcross[2][0], pcross[2][1])
        self.canvas.coords(self.pcrosslist[2], pcross[0][0], pcross[0][1], pcross[3][0], pcross[3][1])

        self.canvas.update()
        
    def transform(self,points):
        #print '   transforming ', self.angle
        res = []
        scl = self.scl
        rot = quat()
        rot.fromRot(self.angle, self.rotdir)
        trans = self.trans
        
        #for p in points:
        #    tmp = p.scale(s)
        #    print 'scale',tmp
        #    tmp = rot*(tmp)*~rot
        #    print 'rot',tmp
        #    tmp = tmp + trans
        #    print 'trans',tmp
        #    res.append(tmp)
        #return res
        
        return [(rot*(p.scale(scl))*~rot) + trans for p in points]
        
    def drawCordCross(self):
        p0 = quat(0,0,0,0)
        px = quat(0,1,0,0)
        py = quat(0,0,1,0)
        pz = quat(0,0,0,1)
        self.cross = [p0,px,py,pz]
        pcross = map(self.camera.project, self.transform(self.cross))
        #print pcross
        self.pcrosslist = [0,0,0]
        self.pcrosslist[0] = self.canvas.create_line(list(pcross[0][0:2]), list(pcross[1][0:2]),fill='red')
        self.pcrosslist[1] = self.canvas.create_line(list(pcross[0][0:2]), list(pcross[2][0:2]),fill='green')
        self.pcrosslist[2] = self.canvas.create_line(list(pcross[0][0:2]), list(pcross[3][0:2]),fill='blue')
    
        
    def draw(self):
        self.drawCordCross()
        #x0,y0 = self.camera.project(p0)
        #x1,y1 = self.camera.project(p1)
        #print 'draw', x0,y0,x1,y1
        #self.lines.append(self.canvas.create_line([0,0,10,20],fill='red'))
      
        pp = map(self.camera.project, self.transform(self.points))
        #print self.points
        #print pp
        
        for n,(i,j) in enumerate(self.point2line):
            self.lines[n] = self.canvas.create_line(pp[i][0],pp[i][1],pp[j][0],pp[j][1],fill='black')
        #self.lines.append(self.canvas.create_line(x[],y[],x[],y[],fill='red'))
        #self.lines.append(self.canvas.create_line(x[],y[],x[],y[],fill='red'))


class Camera(object):
    '''Implements a arbitrary camera, with:
       postition, look at direction and up vector, screen is in dist
       
       It's not fully implemented, canonical direction and up direction are assumed
       '''
    def __init__(   self,
                    dist=500, #distance of screen/view/projectionplane in pixels
                    screen=(800,600), #screen dimensions in pixels
                    pos=-10,#array([0,0,0]), #position of the camera
                    dir=array([0,0,1]),  #direction the camera is pointing to
                    up=array([0,1,0]) #upwards direction of camera
                    ):
        self.dist = dist
        self.screen = screen
        self.pos = pos
        self.dir = dir
        self.up = up
        self.initProjectionMatrix()
        
    def initProjectionMatrix(self):
        d = float(self.dist)
        self.M = matrix( ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,1/d,0)) )

    def project(self,quat):
        #p = matrix( (point[0], point[1], point[2], 1) )
        #return array((self.M*p.T).T)[0][0:3]
        
        #for this task do a simple projection from p along z axis with upvetor along y
        x,y,z = quat.getP()
        d=self.dist
        p=self.pos
        res = array([ x*d/(z-p), -y*d/(z-p), z ]) + array([self.screen[0],self.screen[1],0])/2
        #print 'project',x,y,z,d, 'res:', res
        return res

        
        
class MyEngine:
    def __init__(self, screen = (800,600)):
        self.myParent = Tk()
        
        width, height = screen

        self.camera = Camera()#50, screen)
        self.objects = []
        self.time = 0
        
       
        # ----------------
        # set up gui
        
        self.canvas = Canvas(self.myParent, width=width, height=height)
        self.canvas.grid(row=1, column=1)
        self.canvas.pack()
        
        self.myContainer1 = Frame(self.myParent)
        self.myContainer1.grid(row=2, column=1)
        self.myContainer1.pack()

        self.button1 = Button(self.myContainer1, command=self.button1Click)
        self.button1.configure(text="Start DrawLoop", background= "green")
        self.button1.pack(side=LEFT)
        self.button1.focus_force()

        self.button2 = Button(self.myContainer1, command=self.button2Click)
        self.button2.configure(text="Increase v_rot", background="yellow")
        self.button2.pack(side=LEFT)
        
        self.button3 = Button(self.myContainer1, command=self.button3Click)
        self.button3.configure(text="Decrease v_rot", background="yellow")
        self.button3.pack(side=LEFT)
        
        self.button4 = Button(self.myContainer1, command=self.button4Click)
        self.button4.configure(text="Quit", background="red")
        self.button4.pack(side=LEFT)

        self.myParent.bind("<Escape>", self.escexit)
       
    def addObject(self, obj):
        obj.register(self.camera, self.canvas)
        obj.draw()
        self.objects.append(obj)

    def draw(self, args):
        dt = time.time() - self.time # calc real delta t
        self.time = time.time()
        for obj in self.objects:
            obj.update(dt)
            #obj.draw()
        
        if args[0]%100==0:
            print 'frame: %5.0f, av. fps: %5.1f' % (args[0], 100.0/(time.time()-self.time1))
            self.time1=time.time()
            
        #print "IDLE", 
        
        if self.running:
            self.canvas.after(20,self.draw, [args[0]+1])
        
    def button1Click(self):
        print "start"
        if self.button1["background"] == "green":
            self.button1["background"] = "yellow"
            self.button1["text"] = "Stop DrawLoop"
            self.running = True
            self.canvas.after_idle(self.draw, [0]) #start drawing as soon as finished loading
            self.time = time.time()
            self.time1 = time.time()
        else:
            self.button1["background"] = "green"
            self.button1["text"] = "Start DrawLoop"
            #self.canvas.after(2000)
            self.running = False
            
    def button2Click(self):
        print "incr. v-rot"
        self.objects[0].v_rot += pi/10
        
        #self.myParent.destroy()    

    def button3Click(self):
        print "decr. v-rot"
        self.objects[0].v_rot -= pi/10
        #self.myParent.destroy()  
    
    def button4Click(self):
        print "Exit"
        self.myParent.destroy()

    def escexit(self, event):
        self.button4Click()
        
    def go(self):
        self.myParent.mainloop()
        
    def __call__(self):
        self.myParent.mainloop()

    def start(self):
        self.myParent.mainloop()






def main():
    mySim = MyEngine()
    
    cube1 = SpinningCube()
    cube1.trans = quat(0,0,0,0)
    cube1.v_rot = 0.5
    cube1.rotdir = array([1,0.5,0.25])

    cube2 = SpinningCube()
    cube2.trans = quat(0,-4,0,0)
    cube2.v_rot = 1.0
    cube2.rotdirfn = lambda x: array([sin(x), 0.5*cos(x), 0.25])

    cube3 = SpinningCube()
    cube3.trans = quat(0,+4,0,0)
    cube3.v_rot = -2.0
    #cube3.rotdirfn = lambda x: array([rnd.random(), rnd.random(), rnd.random()])*.2
    
    mySim.addObject(cube1)
    mySim.addObject(cube2)
    mySim.addObject(cube3)

    mySim()
        
    
    
def cmdmain(*args):
    try:
        main()
    except:
        raise
        # handle some exceptions
    else:
        return 0 # exit errorlessly     
        

def classmain():
    print 'call main()'
    

        
if __name__ == '__main__':
    sys.exit(cmdmain(*sys.argv))
else:
    classmain()