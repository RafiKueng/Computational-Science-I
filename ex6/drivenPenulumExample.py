"""
-------------------------------------------------------------------------------
 
-------------------------------------------------------------------------------
Explanation:


How this code works:
    as a strating point, i used this paper:
    http://www.physik.tu-dresden.de/~baecker/papers/python.pdf
    

Notes / Convention:
    
 
-------------------------------------------------------------------------------
Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
v1 2011-10-25   basic implementation

BUGS / TODO:


LICENSE:
    
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
    Here y = [phi, v].
    """
    return array([y[1], sin(y[0]) + 0.25* cos(t)]) # (\dot{\phi}, \dot{v})
    
    
def compute_trajectory(y0):
    """
    Integrate the ODE for the initial point y0 = [phi_0, v_0]
    """
    t = arange(0.0, 100.0, 0.1) # array of times
    y_t = oiL.odeint(derivative, y0, t) # integration of the equation
    return y_t[:, 0], y_t[:, 1] # return arrays for phi and v






def main():
    # compute and plot for two different initial conditions:
    phi_a, v_a = compute_trajectory([1.0, 0.9])
    phi_b, v_b = compute_trajectory([0.9, 0.9])
    pl.plot(phi_a, v_a)
    pl.plot(phi_b, v_b, "r--")
    pl.xlabel(r"$\varphi$")
    pl.ylabel(r"$v$")
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