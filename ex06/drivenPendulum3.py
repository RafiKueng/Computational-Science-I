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
        
        p' = -dH/dq = a sin(q)+b sin(q-t)
        q' = dH/dp = p

How this code works:
    

    

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
from numpy import sin, cos, arange, array, pi, arctan2, linspace
import pylab as pl
import scipy.integrate.odepack as oiL
import random as rnd



def derivative(y, t):
    '''
    Right hand side of the differential equation.
    Here y = [q, p].

    return: [q', p']
    q' = dH/dp = p
    p' = -dH/dq = a sin(q)+b sin(q-t)

    '''
    
    #constants
    a = 0.025
    b = 0.025 
    
    q, p = y
    
    return array([p, -a*sin(q) - b*sin(q-t)])
                
    
    



def main():
    
    n_traj = 50
    
    t = arange(0.0, 100.0, 2*pi/10.)
    t_ = t[0::10] #select every 10th, there t=2*pi*n
    
    pl.figure()
    pl.subplot(311)
    pl.xlabel('t')
    pl.ylabel('q')
    pl.subplot(312)
    pl.xlabel('q')
    pl.ylabel('p')
    pl.subplot(313)
    pl.xlabel('q @t=2*pi*n (every 10th)')
    pl.ylabel('p @t=2*pi*n (every 10th)')
    
    for i in range(n_traj): #compute n_traj trajectories
        q_init = 0
        p_init = linspace(-2,2,n_traj)[i] #rnd.random()*4-2
        
        x_init = array([q_init, p_init])
        
        x = oiL.odeint(derivative, x_init, t)
        
        q = [arctan2(sin(i[0]),cos(i[0])) for i in x]
        #q = [i[0] for i in x]
        p = [i[1] for i in x]
        
        #print x[0,:]
        #print x[-1,:]
    
        pl.subplot(311)
        pl.plot(t, q, '.')

        pl.subplot(312)
        pl.plot(q,p,'.')

        pl.subplot(313)
        pl.plot(q[0::10], p[0::10], '.') #only plot evert 10th item, there t=2pi*n

    

    
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