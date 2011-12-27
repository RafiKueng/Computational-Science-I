# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex12: Great Circle / Flight Path / SLERP
-------------------------------------------------------------------------------

Explanation:
    This program uses quaternions and slerp (spherical linear interpolation)
    to calculate the great circle between two points


    
How this code works:


    

Notes / Convention:




-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    va 2011-12-14   basic outline of program, gui and stuff
    v1 2011-12-15   calculations, finished
 
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

real = (int, float, long)
arrlst = ndarray #(ndarray, list)


class quat(object):
    '''
    Represents a quaternion q = (w, x, y ,z)
    '''
    
    def __init__(self, *args): #x0=0, x1=0, x2=0, x3=0):
        '''init an quaternion, either using:
        quat(w,x,y,z):
        quat(array[w,x,y,z]):
            defining the 4 components in an array
        quat(float(omega), array([vx, vy, vz])):
        quat(abs, float(omega), array([vx, vy, vz])):
            using versor form, with omega: angle and v = (vx, vy, vz) unit vector
            q = cos(omega) + v * sin(omega)
            this describes also a rotation around v with 2*omega
        '''
        if len(args) == 1 and isinstance(args[0], arrlst) and len(args[0]) == 4:
            self.w, self.x, self.y, self.z = self.q = args[0]
            
            self.v=array([self.x, self.y, self.z])
            
            self.abs = linalg.norm(self.q)
            self.o = arccos(self.w/self.abs)
            self.nx, self.ny, self.nz = self.n = self.v/self.abs
                        
        elif len(args) == 4:
            self.__init__(array(args))
            
        elif len(args) == 2 and isinstance(args[0], real) and isinstance(args[1], arrlst):
            self.__init__(linalg.norm(args[1]), *args)
        
        elif (len(args) == 3 and
                isinstance(args[0], real) and
                isinstance(args[1], real) and
                isinstance(args[2], arrlst)):
            self.vx, self.vy, self.vz = self.v = args[2]    
            #TODO check if this is right, when a versor with non unit length is added
            self.abs = args[0]
            self.o = args[1]
            self.nx, self.ny, self.nz = self.n = self.v/linalg.norm(self.v) #make sure its normvector
            
            self.w = cos(self.o)
            self.x, self.y, self.z = self.n*sin(self.o)
            self.q = array([self.w, self.x, self.y, self.z])
        
        else:
            print 'wrong arguments @ init quat', args
            raise TypeError

    def __mul__(self, other):
        '''def of a*b'''
        if isinstance(other, type(self)):
            a,b=(self,other)
            return quat(a.w*b.w - a.x*b.x - a.y*b.y - a.z*b.z,
                    a.w*b.x + a.x*b.w + a.y*b.z - a.z*b.y,
                    a.w*b.y - a.x*b.z + a.y*b.w + a.z*b.x,
                    a.w*b.z + a.x*b.y - a.y*b.x + a.z*b.w)
        elif isinstance(other, (int, float, long)):
            print 'Multiplikation quat * x, x in R not implemented'
            raise TypeError
        elif isinstance(other, type(array([]))) and len(other)==3: #scaling the quat with vector
            return quat(self.w, self.x+other[0], self.y+other[1], self.z+other[2])
        else:
            print 'Multiplikation quat with',type(other),'not implemented'
            raise TypeError            

    def __add__(self, other):
        if isinstanceof(other, type(self)):
            return quat(self.q+other.q)
            
        elif isinstanceof(other, type(array([]))) and len(other)==3:
            return quat(self.q + array([0,other[0], other[1], other[2]]))      
            
        else:
            print 'add quat with',type(other),'not implemented'
            raise TypeError
        
    def __repr__(self):
        str  = 'Quaternion: cart : [%4.2f, %4.2fi, %4.2fj, %4.2fk]\n'%(self.w, self.x, self.y, self.z)
        str += '            polar: abs: %4.2f, angle: %4.2f, n=[%4.2f, %4.2f, %4.2f]'%(self.abs, self.o, self.nx, self.ny, self.nz)
        return str
        
    def __invert__(self):
        '''retuns the inverted of the quaternion'''
        return self.conj()/self.norm()**2
            
    def __div__(self, other):
        if isinstance(other,type(self)):
            raise TypeError
        elif isinstance(other,(int,float,long)):
            return quat(self.q/other)
        
    def __pow__(self, other):
    
        if isinstance(other, (int,float,long)):
            return quat(self.abs**other, self.o*other, self.v)
        else:
            print 'can only versor**float, got instead t=',other, type(other)
            raise TypeError
    

    #def scale(self, s):
    #use __mul__(quat,array) instead
    #    '''scales the x,y,z components of quat with s[0], s[1] and s[2]'''
    #    x = self.q
    #    return quat(x[0],x[1]*s[0],x[2]*s[1],x[3]*s[2])
        
    def norm2(self):
        x=self.q
        return x[0]*x[0]+x[1]*x[1]+x[2]*x[2]+x[3]*x[3]
        
    def norm(self):
        return sqrt(self.norm2())
    
    def conj(self):
        '''returns a new, conjugated quat q' '''
        x = self.q
        return quat(x[0],-x[1],-x[2],-x[3])

    T = property(conj)

    def rot_by(self, other):
        '''returns new rotated quat, rotated by other'''
        return other*self*~other

    #def addV(self, vec):
    #use __add__(self, vec) instead
    #    '''Adds a vector to self'''
    #    for i in range(3):
    #        self.q[i+1]+=vec[i]

            


class flightpath(object):
    def __init__(self):

        self.cnt = 0
        self.hpnt = []

        self.root = Tk()
        self.root.bind("<Escape>", lambda e: e.widget.destroy())

        self.canv = Canvas(self.root, width=1000, height=500)
        
        def click(event):
            print 'click', [event.x, event.y], [event.x-500, -event.y+250]
            #print 'px2pol:', pixel2polar([event.x-500, -event.y+250])
            self.start = pixel2quat([event.x-500, -event.y+250])
            print 'start\n', self.start

        def move(event):
            print 'move', event.x-500, -event.y+250
            self.cnt += 1
            self.canv.after_idle(self.update, [self.cnt, pixel2quat([event.x-500, -event.y+250])])
            
        def release(event):
            print 'rel', event.x-500, -event.y+250
            self.cnt += 1
            self.canv.after_idle(self.update, [self.cnt, pixel2quat([event.x-500, -event.y+250])])

        
        self.root.bind("<Button-1>", click)
        self.root.bind("<B1-Motion>", move)
        #self.root.bind("<ButtonRelease-1>", release)


        self.photo = PhotoImage(file="earth.gif")
        
        self.canv.create_image([500,250], image=self.photo)
        #self.canv.create_line(0,0,500,500, fill='red')
        
        
        #label = Label(master=self.canv, image=photo, width=1000, height=500)
        #label.image = photo # keep a reference!
        #label.pack()
        self.canv.pack()
       

        
    def __call__(self):
        self.root.mainloop()

    def update(self, args):
        cnt, end = args
        print 'update', cnt
        #time.sleep(1)

        
        dt = 0.1 #modify this to alyways take equal distance steps
        tvec = arange(0,1+dt,dt)
        npnts = len(tvec)
        #tvec = [0,0.5,1]
        
        #print self.start
        #print end
        #print tvec
        
        res = [slerp(self.start,end,t) for t in tvec]
        
        #for r in res:
        #    print r
        
        points = [quat2pixel(q) for q in res]

        for h in self.hpnt:
            self.canv.delete(h)
        self.hpnt = []
        
        color = ['green' for _ in range(npnts)]
        color[0] = 'red'
        color[-1] = 'red'
        
        for i, p in enumerate(points):
            self.hpnt.append(self.canv.create_oval(point2circle(p), fill=color[i]))
        
        #if True:
        #    self.canv.after_idle(self.update, [args[0]+1])
            
    def draw(self):
        print 'draw'
        
        #delete all previous points / handles
        #draw start, end green
        #for p in self.points
        #   draw point blue
        #   store handle
        
        
def point2circle(point):
    r = 3. #radius of circles
    x, y = point
    x = x+500
    y = -y+250
    return [x-r, y-r, x+r, y+r]
        

def quat2pixel(q):
    #print 'quat2pixel: cart:', q.n
    pol = cart2polar(q.n)
    #print '            pol :', pol
    px = polar2pixel(pol)
    #print '            px  :', px
    return array(px)
    
def pixel2quat(pixel):
    #print 'pixel2quat: px  :', pixel
    pol = pixel2polar(pixel)
    #print '            pol :', pol
    cart = polar2cart(pol)
    #print '            cart:', cart
    q = quat(1,cart)
    #print q
    return q

    
def polar2cart(polar):
    '''r, psi, phi = polar TO x,y,z = cart
    psi = polar[1] = lat. (breite, NS)  [-pi/2, pi/2]
    phi = polar[2] = long. (laenge, EW)  [-pi, pi]
    def: 0N 0E -> (1,0,0), 0N 90E -> (0,1,0), 90N, XE -> (0,0,1)
    '''
    x=polar[0]*cos(polar[1])*cos(polar[2])
    y=polar[0]*cos(polar[1])*sin(polar[2])
    z=polar[0]*sin(polar[1])
    return array([x,y,z])

def cart2polar(cart):
    '''r, psi, phi = polar TO x,y,z = cart
    psi = polar[1] = lat. (breite, NS)  [-pi/2, pi/2]
    phi = polar[2] = long. (laenge, EW)  [-pi, pi]
    def: 0N 0E -> (1,0,0), 0N 90E -> (0,1,0), 90N, XE -> (0,0,1)
    '''
    r=linalg.norm(cart)
    psi=arcsin(cart[2]/r)
    phi=arctan2(cart[1], cart[0])
    return array([r,psi,phi])

def deg2rad(deg):
    return deg/180.*pi
    
def rad2deg(rad):
    return rad/pi*180.
    
def pixel2polar(pixel):
    x = pixel[0]/500.*(sqrt(2)*2.)
    y = pixel[1]/250.*sqrt(2.)
    
    u = sqrt(1-x*x/16.-y*y/4.)
    psi = arcsin(u*y)
    phi = 2.*arctan(u*x/(4.*u*u-2.)) 
    
    return array([1, psi, phi])

def polar2pixel(polar):
    psi = polar[1]
    phi = polar[2]
    
    x = 2.*sqrt(2)*cos(psi)*sin(phi/2.) / sqrt(1.+cos(psi)*cos(phi/2.))
    y = sqrt(2.)*sin(psi) / sqrt(1.+cos(psi)*cos(phi/2.))
    
    #scale, that x, y in [-1,1]
    x = x / (sqrt(2)*2.)
    y = y / sqrt(2.)
    
    #scale to pixel coordinates
    x = x*500.
    y = y*250.
    
    return array([x,y])


def slerp(q1, q2, t):
    return q1*(~q1*q2)**t







def main():
    fp = flightpath()
    fp()







   
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