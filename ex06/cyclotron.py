"""
-------------------------------------------------------------------------------
(Non)Relativistic Particle in Cyclotron
-------------------------------------------------------------------------------
Explanation:
    Particle in B field and oscillation electric field:
    
    Hamiltonian with only B field:
        H = 1/2 * (px+y)^2 + 1/2 (py-x)^2
        
    non relativistic Hamiltonian with B/E field
        H = 1/2 * (px+y)^2 + 1/2 (py-x)^2 + a*x*cos(w*t)
        with resonance at w=2
        
        qx' = dH/dpx = px + qy
        qy' = dH/dpy = px - qy
        
        px' = -dH/dqx = py - qx - a cos(w*t)
        py' = -dH/dqx = -qy - px

        
        
    relativistic Hamiltonian with B/E field
        H = (1 + (px+y)^2 + (py-x)^2)^0.5 + a*x*cos(w*t)
        
        qx' = dH/dpx = ( px + qy )/s
        qy' = dH/dpy = (py - qx)/s
        
        px' = -dH/dqx = (py - qx)/s - a cos(w*t)
        py' = -dH/dqx = -(qy - px)/s

        with s = sqrt(1+(px + qy)^2+(py - qx)^2)

        
        
How this code works:


    

Notes / Convention:
    
 
-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2012-01-08   basic implementation

BUGS / TODO:
    relativistic path has a bug, can't find it

LICENSE:
    none
-------------------------------------------------------------------------------
"""

# imports
import sys
from numpy import sin, cos, arange, array, pi, sqrt, linspace
import pylab as pl
import scipy.integrate.odepack as oiL
import random as rnd

#constants
a = 1.
w = 2.


def derr_nrel(y, t):
    '''
    Right hand side of the differential equation.
    Here y = [qx, qy, px, py].
    '''
    qx, qy, px, py = y

    qx_ = px + qy
    qy_ = py - qx
    
    px_ = py - qx - a*cos(w*t)
    py_ = -px - qy 

    return array([qx_, qy_, px_, py_])

    
def derr_rel(y, t):
    '''
    Right hand side of the differential equation.
    Here y = [qx, qy, px, py].
    '''
    qx, qy, px, py = y

    s = sqrt(1 + (px + qy)**2 + (py - qx)**2)
    
    #this is dorde's solution, but it doesn't work either
    #qx_ = px/sqrt(1+px**2+py**2)-qy   #(px + qy)/s
    #qy_ = py/sqrt(1+px**2+py**2)+qx    # (py - qx)/s
    #px_ =  -(py+a*cos(w*t)) 
    #py_ = px

    #my solution, checked with tipps, but doesn't work...
    qx_ = (px + qy)/s
    qy_ = (py - qx)/s
    px_ = (py - qx)/s - a*cos(w*t)
    py_ = -1*((-px + qy)/s)

    return array([qx_, qy_, px_, py_])
                
    
    



def main():
    

    
    qx_init = 0.
    qy_init = 0.
    px_init = .50
    py_init = -.50
    
    x_init = array([qx_init, qy_init, px_init, py_init])
    
    t = linspace(0.0, 20.0, 1000)    
    x_nrel = oiL.odeint(derr_nrel, x_init, t)

    t = linspace(0.0, 20.0, 1000)
    x_rel = oiL.odeint(derr_rel, x_init, t)
    
    
    pl.plot(x_nrel[:,0], x_nrel[:,1])
    pl.plot(x_rel[:,0], x_rel[:,1])
    
    pl.show()




def cmdmain(*args):
    try:
        #print "Starting Program"
        main()
        #print "ending programm"
    except:
        raise
        # handle some exceptions
    else:
        return 0 # exit errorlessly     
        

def classmain():
    print 'not to be used as a module\nend...'
    

        
if __name__ == '__main__':
    sys.exit(cmdmain(*sys.argv))
else:
    classmain()