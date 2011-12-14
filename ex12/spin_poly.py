# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex12: Spinning Polygon
-------------------------------------------------------------------------------

Explanation:

    This is an implementation of a real time physics / graphics engine
    (your cpu speed doen't matter, nor should any additional cpuload,
    it's always the same speed in rads/sec!)
    
    Use the buttons to start / stop
    quit with exit
    
    ideas / concepts from "Introduction to Computergraphics", fs10
    http://www.ifi.uzh.ch/vmml/teaching/lectuces/30-computer-graphics-minf4226.html

    to use it, create an instance of myEngine, create a few objects to be drawn
    (inherit drawable, implement nessecairy functions __init__, draw,
    update) and add them to the engine with myEngine.addObject(myObject)
    then start the eninge with a call myEngine() (or myEngine.go(),
    myEngine.start())

    
How this code works:

    This project consits of 3 basic elements:
    myEngine, camera, drawableObjects.
    
    all points and vectors are assumed to be quaternions (quat)
    
    There are 3 coodinate systems:
    *   model coordinate system (mcs, 3d, in arb. units)
    *   world coordinate system (wcs, 3d, in arb. units)
    *   screen coordinate system (scs, pseudo 3d: 2d pixel value and assigned
        depth on screen in arb. units)
    
    there are 2 transformation steps involed:
    *   mcs ---> wcs:
        the model is scaled, rotated, translated into 3d wcs. the models points
        never change, only transform matrices do! this is done by the object
        itself (drawable.update(), expecially SpinningCube.transform())

    *   wcs ---> scs:
        (in contrast to actual graphics engines) this is done by the drawable
        object itself, also in drawable.update(), but with help of the
        reference to the camera, and the use of the camera.project(point)
        
    
    MyEngine:
        this is the global manager and timer. it does NOT do any depth check
        and ordering, it draws everything, does not matter whether in viewing
        cone or behind some other objects. it draws in order of registration,
        so newer registered objects will overpaint older ones...
        Strange things happend when objects are behind the camera, so beware!
        
    *   __init__()
            sets up the screen, the camera (projection matrix) and
            the basic gui.
    *   addObject()
            adds a drawable object to the list of the to be drawn objects
            and registers the camera and the canvas at the object. It also
            calls the objects draw (drawable.draw()) for a initialisation and
            first drawing of the object. (later, the objects are NOT redrawn, but
            only existing objects are manipulated)
    *   draw():
            this is the main drawing loop.
            First, the elapsed time is calculated, and then the update fn for
            each drawable object is called (passing the elapsed time) to let
            the object redrawn itself.
            At the end, it adds a call to itself again to the Tk.mainloop
            event queue, as soon the program is idle (aka finished drawing the
            previous frame and handling all user inputs)
            To start the animation, set self.running to true and call draw()
            once. (Don't call it directly, add a call to it to the event queue,
            best in myEngine.__init__() using
                self.canvas.after_idle(self.draw, [0])
            )
            or after pressing a button. So the animation is started as soon as
            everything else is loaded.
    * div. handels:
            for this task, there are some buttons and handles implemented, to start
            / stop the engine, modify some properties of the objects and exit the
            program.
            
    Camera():
        This it the camera, it defines the camera in space (position and
        orientation), projection plane distance and screen size.
    
        (this class is not completly implemented, only uses canonical camera
        orientation, pointing in direction +z axis, with upvector pointing
        in +y direction)

    *   project(point):
        This transforms the 3d world coordinates of point p (of class quat: a
        quaternion) to the projection plane, aka pixel coordinates on screen
        window and a depth value z.
        
            
    drawable():
        abstract class of object, that the engine can handle.
        objects draw them self the first time, using draw(), afterwards
        only update() is called, so the object can redrawn itself or update
        existing lines, polygons ect. update expects the elapsed time dt since
        the last time it got painted, to be able to calculate it's new
        position.
        
        Each drawable has a link to the camera and to the canvas, on which it
        has to paint itself. (these are assigned to them when they are
        registered with the engine, by calling register(cam, canvas) )
        
    SpinningCube(drawable):
        8 edges/points P and 12 lines L defined and connected as following:
        (see self.point2line, line2points)
    
                        P2+-----------------------+P6
                         /|         L06          /|   
                        / |                     / |   
                    L01/  |L08              L02/  |   
                      /   |                   /   | 
                     /    |    L05           /    |L09   
                  P3+-----------------------+P7   |
                    |     |                 |     |
                    |     |                 |L10  |
                    |     |          L07    |     |
                    |   P0+-----------------|-----+P4
                 L11|    /                  |    /
                    |   /                   |   /
                    |  /L00                 |  /L03
                    | /                     | /
                    |/        L04           |/
                  P1+-----------------------+P5       
           
        To check whether a line is visilbe, it checks whether point P is inside
        the triangle spanned by the neighbouring points (in the scs) 
        (eg. P0: is P0 inside P1, P2, P4; check self.pnt2tri)
        with the function isIn(P0, P1, P2, P4)
        
        If it is, and if the depth value of P0 is bigger than the average of
        P1, P2 and P4; the lines connecting to P0 are hidden.
        
        
    

Notes / Convention:
    Sooooorry, its way to much, i know... but i always wanted to try to
    implement my own graphics engine :)



-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-12-12   basic implementation
    v2 2011-12-14   minor corrections and documenation
 
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
        self.q = array([x0,x1,x2,x3], dtype=float)
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

    def addV(self, vec):
        '''Adds a vector to self'''
        for i in range(3):
            self.q[i+1]+=vec[i]









class drawable(object):
    '''Abstract class of an drawable object'''
    def __init__(self):
        raise NotImplementedError
    def register(self, cam, canv):
        self.camera = cam
        self.canvas = canv
    def draw(self):
        ''' initial drawing '''
        raise NotImplementedError
    def update(self, dt):
        '''update this figure'''
        raise NotImplementedError








class UnitVectors(drawable):
    '''
    This draws the unit vectors of the wcs
    '''
    def __init__(self):
        self.length = 1
        pass

    def draw(self):
        ''' initial drawing '''
        p0 = quat(0,0,0,0)
        px = quat(0,self.length,0,0)
        py = quat(0,0,self.length,0)
        pz = quat(0,0,0,self.length)
        color = ('red','green','blue')
        self.cross = [p0,px,py,pz]

        pcross = map(self.camera.project, self.cross)

        self.pcrosslist = [0,0,0]
        for i in range(3):
            self.pcrosslist[i] = self.canvas.create_line(
                list(pcross[0][0:2]),
                list(pcross[i+1][0:2]),
                fill=color[i],
                dash=(4, 4)
                )

    def update(self, dt):
        pass








class SpinningCube(drawable):
    def __init__( self ):
        self.points = [quat(0,-1,-1,-1), quat(0,-1,-1,+1),
                        quat(0,-1,+1,-1), quat(0,-1,+1,+1),
                        quat(0,+1,-1,-1), quat(0,+1,-1,+1),
                        quat(0,+1,+1,-1), quat(0,+1,+1,+1) ]
        
        self.v_rot = 0.2 #rotation veolcity in rads / sec
        self.rotdir = array([1,0,0]) #rotation direction (unit vector); OR
        self.rotdirfn = None #a function returning the rotation direction for a given dt
        self.a_rot = 0.0 #rot. acceleration in rads/sec^2 NOT IMPLEMENTED
        
        self.trans = quat(0,0,0,0)      #the objects position in wcs
        self.v_trans = array([0,0,0])   #the objects velocity
        self.a_trans = array([0,0,0])   #the objects acceleration
        
        self.scl = array([1,1,1])  #the objects scaling along x, y, z axis (in mcs)
        
        self.lines = [0 for i in range(12)] #list of linehandles
        self.linecolor = ['black' for i in range(12)] #color of the lines
        self.linedash = [() for i in range(12)] #drawingstile of the line (): straigt, (4,4): dashed
        #self.x = [0 for i in range(8)]
        #self.y = [0 for i in range(8)]
        
        #line nr n has the endpoints nr [i,j]
        # [i,j] = point2line[k]
        self.point2line = [ [0,1],[2,3],[6,7],[4,5],
                            [1,5],[3,7],[2,6],[0,4],
                            [0,2],[4,6],[5,7],[1,3] ]
                            
        #point nr n is edge of lines [i,j,k]
        # [i,j,k] = line2points[n]
        self.line2points = [[0,7,8],
                            [0,4,11],
                            [1,6,8],
                            [1,5,11],
                            [3,7,9],
                            [3,4,10],
                            [2,6,9],
                            [2,5,10] ]
        
        #neighbouring points i,j,k for each point n
        #for occlusion check
        # [i,j,k] = pnt2tri[n]
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
        '''
        we want to know the engines camera to be able to project on the
        screen and the canvas, where to paint on.
        '''
        self.camera = cam
        self.canvas = canv

        
    def isIn(self,p0,p1,p2,p3):
        '''checks whether p0 is inside p1,p2,p3
        2d arrays (x,y) expected (by cp()), but being tolerant...
        
        it checkts the sign of of the crossprdct, aka the
        direction of the area normal.
        if P inside ABC, then n_area of APB should be the same as
        ACP.
        but this is also the case when P is reflected at A, so an
        additional check is needed:
        if BPC is the same dir as BAC
        
                  B
                /   \
              /       \
            /     *P    \
          /               \
        A-------------------C
        
        '''
        
        def cp(x,y):
            '''this is the simplified crossp'''
            return x[0]*y[1]-x[1]*y[0]	#collision detection

        P=p0    
        A=p1    
        B=p2    
        C=p3

        if cp(P-A,C-A)//cp(B-A,P-A)>=0:
            if cp(P-B,A-B)//cp(C-B,P-B)>=0:
                return True
        return False
        
        
    def update(self, dt):

        #update rotation
        self.angle += self.v_rot*dt
        #self.v_rot += self.a_rot*dt #not implemented
        if not self.rotdirfn==None:
            self.rotdir = self.rotdirfn(self.angle)
        
        #update position (or even better, call a function returning the new v, a..)
        self.trans.addV(self.v_trans*dt)
        self.v_trans += self.a_trans*dt
        
        #transform the points from mcs to wcs
        #put the model on the stage
        transp = self.transform(self.points)
        
        #project from wcs to scs
        #project the stage onto the screen
        pp = map(self.camera.project, transp)
        
        #check if visible
        self.linecolor = ['black' for i in range(12)] # init everything to visible
        self.linedash = [() for i in range(12)]       # ^^^
        for i,p in enumerate(pp): #check each projected point p (in scs)
            if self.isIn(p,
                        pp[self.pnt2tri[i][0]],
                        pp[self.pnt2tri[i][1]],
                        pp[self.pnt2tri[i][2]]):
                    #if p lies in the projection of the triangle spanned
                    #by p's neighbouring points, then do depth check
                        
                if p[2] > ( pp[self.pnt2tri[i][0]][2]
                            +pp[self.pnt2tri[i][1]][2]
                            +pp[self.pnt2tri[i][2]][2] )/3.:
                    #depth check, relies on correct depth values from
                    #camera's project()
                    # pp[self.pnt2tri[i][0]][2] explained:
                    #   pp[X][2]: depth value of (projected) point with index X
                    #      X = self.pnt2tri[Y][i]: index X of the i'th
                    #      neighbouring point to the point with index Y
                    
                    for k in range(3):
                        #color all the 3 lines which lead to this corner as hidden
                        self.linecolor[self.line2points[i][k]] = 'grey'
                        self.linedash[self.line2points[i][k]] = (4,4)
            
        #actually draw the points
        for n, (i,j) in enumerate(self.point2line):
            #for each line nr n with the edge points with numbers (i, j) do:
            
            self.canvas.coords(self.lines[n], pp[i][0],pp[i][1],pp[j][0],pp[j][1])
            #update the coordinates of the line nr n with handle self.lines[n]
            
            self.canvas.itemconfig(self.lines[n], fill=self.linecolor[n], dash=self.linedash[n])
            #and set the drawing style accordingly whether visible or hidden
            
        #draw the mcs unit vectors for a orientation aid.
        pcross = map(self.camera.project, self.transform(self.cross))
        self.canvas.coords(self.pcrosslist[0], pcross[0][0], pcross[0][1], pcross[1][0], pcross[1][1])
        self.canvas.coords(self.pcrosslist[1], pcross[0][0], pcross[0][1], pcross[2][0], pcross[2][1])
        self.canvas.coords(self.pcrosslist[2], pcross[0][0], pcross[0][1], pcross[3][0], pcross[3][1])

        #...
        self.canvas.update()

        
    def transform(self,points):
        '''transforms a list of points from mcs to wcs'''
        #print '   transforming ', self.angle
        scl = self.scl
        rot = quat()
        rot.fromRot(self.angle, self.rotdir)
        trans = self.trans
        
        # do the following in a compact way
        #for p in points:
        #    tmp = p.scale(s)       scale the whole thing with (not nec. equal x,y,z factors)
        #    tmp = rot*(tmp)*~rot   rotate it with quat rot
        #    tmp = tmp + trans      translate it to world coodinates trans
        #    res.append(tmp)
        
        return [(rot*(p.scale(scl))*~rot) + trans for p in points]
        
    def drawCordCross(self):
        '''init and draw unit vectors of mcs'''
        p0 = quat(0,0,0,0)
        px = quat(0,1,0,0)
        py = quat(0,0,1,0)
        pz = quat(0,0,0,1)

        self.cross = [p0,px,py,pz]

        pcross = map(self.camera.project, self.transform(self.cross))

        self.pcrosslist = [0,0,0]
        self.pcrosslist[0] = self.canvas.create_line(list(pcross[0][0:2]), list(pcross[1][0:2]),fill='red')
        self.pcrosslist[1] = self.canvas.create_line(list(pcross[0][0:2]), list(pcross[2][0:2]),fill='green')
        self.pcrosslist[2] = self.canvas.create_line(list(pcross[0][0:2]), list(pcross[3][0:2]),fill='blue')
    
        
    def draw(self):
        '''init all lines and make a fisrt quick and dirty drawing...
        the actual frame per frame drawing is done in update(), so actually
        this function should more be something like initDraw()...'''

        self.drawCordCross()

        # do mcs --> wcs --> scs in one line...
        pp = map(self.camera.project, self.transform(self.points))
        
        #initially create the lines, store the handles
        for n,(i,j) in enumerate(self.point2line):
            self.lines[n] = self.canvas.create_line(pp[i][0],pp[i][1],pp[j][0],pp[j][1],fill='black')









class Camera(object):
    '''
    Implements a arbitrary camera, with:
       postition, look at direction and up vector, screen is in dist
       
    It's not fully implemented, canonical direction and up direction are assumed
    if you change those, it has no effect...
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
        '''not yet implemented'''
        d = float(self.dist)
        self.M = matrix( ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,1/d,0)) )

    def project(self,quat):
        '''
        this transforms the 3d world coordinates to the projection plane, 
        aka pixel coordinates and a depth value z.
        '''
        #p = matrix( (point[0], point[1], point[2], 1) )
        #return array((self.M*p.T).T)[0][0:3]
        
        #for this task do a simple projection from p along z axis with upvetor along y
        x,y,z = quat.getP()
        d=self.dist
        p=self.pos
        res = array([ x*d/(z-p), -y*d/(z-p), z ]) + array([self.screen[0],self.screen[1],0])/2
        return res










class MyEngine:
    def __init__(self, screen = (800,600), camera = None):
        self.myParent = Tk()
        
        width, height = screen

        if camera == None:
            self.camera = Camera(screen=screen)
        else:
            self.camera = camera
        
        self.objects = []
        self.time = 0
        
       
        # ----------------
        #  set up gui
        # ----------------
        
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
            #self.canvas.after(20,self.draw, [args[0]+1])
            self.canvas.after_idle(self.draw, [args[0]+1])
        
    def button1Click(self):
        #print "start"
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
        #print "incr. v-rot"
        for o in self.objects:
            try:
                o.v_rot += pi/5
            except:
                pass


    def button3Click(self):
        #print "decr. v-rot"
        for o in self.objects:
            try:
                o.v_rot -= pi/5
            except:
                pass
    
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
    
    unitv = UnitVectors()
    unitv.length = 3
    
    cube1 = SpinningCube()
    cube1.trans = quat(0,0,0,0)
    cube1.v_rot = 0.5
    cube1.rotdir = array([1,0.5,0.25])

    cube2 = SpinningCube()
    cube2.trans = quat(0,-4,0,0)
    cube2.v_rot = 1.0
    cube2.rotdirfn = lambda x: array([sin(x), 0.5*cos(x), 0.25])
    cube2.v_trans = array([0,2.0,0])
    cube2.a_trans = array([0,-0.3,0])

    cube3 = SpinningCube()
    cube3.trans = quat(0,+4,0,0)
    cube3.v_rot = -2.0
    
    mySim.addObject(unitv)
    mySim.addObject(cube1)
    mySim.addObject(cube2)
    mySim.addObject(cube3)

    mySim()





def cmdmain(*args):
    try:
        main()
    except:
        # handle some exceptions
        raise
    else:
        return 0 # exit errorlessly     

def classmain():
    print 'call main()'

if __name__ == '__main__':
    sys.exit(cmdmain(*sys.argv))
else:
    classmain()