"""
-------------------------------------------------------------------------------
 
-------------------------------------------------------------------------------
Explanation:


How this code works:
    as a strating point, i used this paper:
    http://www.physik.tu-dresden.de/~baecker/papers/python.pdf
    and this site for reference on solving coupled ode:
    http://www.scipy.org/Cookbook/LoktaVolterraTutorial
    

Notes / Convention:
    
 
-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-02   basic implementation

BUGS / TODO:
    

LICENSE:
    none
-------------------------------------------------------------------------------
"""

# imports
import sys
from numpy import sin, cos, arange, array
import pylab as pl
import scipy.integrate.odepack as oiL


def derivative(y, t):
    """
    Right hand side of the differential equation.
    Here y = [p(t), q(t)].
    """
    a=b=0.025
    return array([-a*sin(y[1])+b*sin(y[1]-t), y[0]])
                
    
    
def compute_trajectory(y0):
    """
    Integrate the ODE for the initial point y0 = [phi_0, v_0]
    """
    t = arange(0.0, 100.0, 0.1) # array of times
    y_t = oiL.odeint(derivative, y0, t) # integration of the equation
    return y_t # return arrays for phi and v






def main():
    # compute and plot for two different initial conditions:
    
    data = [1,2]    
    data[0] = compute_trajectory([1.0, 0.1])
    data[1] = compute_trajectory([0.0, 10.0])
    
    #print data[0]
    
    for d in data:
        print d,'\n\n'
        pl.plot(d[:,0], d[:,1])

    pl.xlabel(r"p")
    pl.ylabel(r"q")
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