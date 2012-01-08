"""
-------------------------------------------------------------------------------
Driven Pendulum
-------------------------------------------------------------------------------
Explanation:
    In this example we consider a pendulum mounted on the rim of a wheel. The
    wheel has radius r and is driven to rotate at a constant angular speed.
    The pendulum has length l and is free to swing.
    The angle of the wheel is q, the angle of the pendulum is q, with respect
    to a vertial line.
    
    Coordinates of penulum:
        x = l * sin q + r * sin t
        y = -l cos q - r * cos t
        
    using:
        a = g / l
        b = r / l
        g: gravity
        
    Hamiltonian:
        H = 1/2 * p^2 + P - a * cos(q) - b * cos(q-Q)
        with Q = t+const
        
    

How this code works:
    not at all...

    

Notes / Convention:
    
 
-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-02   basic implementation
    v2 2012-01-08   complete redesign of v1

BUGS / TODO:
    

LICENSE:
    none
-------------------------------------------------------------------------------
"""

# imports
import sys
from numpy import sin, cos, arange, array, pi, arctan2
import pylab as pl
import scipy.integrate.odepack as oiL
import random as rnd



def derivative(y, t):
    '''
    Right hand side of the differential equation.
    Here y = [q, Q, p, P].
    '''
    
    #constants
    a = 0.025
    b = 0.025 
    
    q, Q, p, P = y
    
    return array([a*sin(q) + b*sin(q-Q), b*sin(q-Q), p , 1])
    #return array([p, 1.0, a*sin(q) + b*sin(q-Q), -b*sin(q-Q)])
    #return array([p, 1.0, a*sin(q) + b*sin(q-Q), -b*sin(q-Q)])
                
    
    



def main():
    
    t = arange(0.0, 100.0, 2*pi/10.)
    t_ = t[0::10] #select every 10th, there t=2*pi*n
    
    
    
    for i in range(1): #compute 100 trajectories
        q_init = pi/4.
        Q_init = 0.0001
        p_init = 0.0001 #rnd.random()*2*pi
        P_init = 1
        
        x_init = array([q_init, Q_init, p_init, P_init])
        
        x = oiL.odeint(derivative, x_init, t)
        
        #Q = [arctan2(sin(i[1]),cos(i[1])) for i in x]
        q = [i[0] for i in x]
        Q = [i[1] for i in x]
        p = [i[2] for i in x]
        P = [i[3] for i in x]
        
        print x[0,:]
        print x[-1,:]
        pl.plot(t, q, '.')
        #pl.plot(q[0::10], p[0::10], '.') #only plot evert 10th item, there t=2pi*n
        
    pl.xlabel('q')
    pl.ylabel('p')
    
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