"""
-------------------------------------------------------------------------------
 Class for integrating
-------------------------------------------------------------------------------
Explanation:
    Derrived from the work done in the derrint.py assignment..

How this code works:
    

Notes / Convention:

 
-------------------------------------------------------------------------------
Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
v1 2011-10-xx   basic implementation (derrint.py)
v3 2011-10-26   copied to legendrepoly.py for assignment 
v2 2011-10-27   put everything together as a easy importable class
 
BUGS / TODO:
    * maybe make bounds changeable...
    * better integration of former standalone methode/function
      __derriveIntegrator into the class: don't need to pass that
      many values, use instance values...

LICENSE:
    
-------------------------------------------------------------------------------
"""

import sys
import numpy as np

class BasicIntegrator(object):
    """
    Basic class for an integrator, the other inherit from this one...
    """
    
    def __init__(   self,
                    max_degree=2,
                    n_points=3,
                    boundaries=[-1,1],
                    incl_bounds = True,
                    is_sym = True,
                    n_pieces = 1):

        self.dtype = float #not meant to be changed from outside...

        self.max_degree = max_degree
        self.n_points = n_points
        self.bounds = np.array(boundaries, dtype=self.dtype)
        self.incl_bounds = incl_bounds
        self.is_sym = is_sym
        self.n_pieces = n_pieces

        self.coef = []
        self.pnts = []

        a = self.bounds[0]
        b = self.bounds[1]
        B = self.n_pieces
        
        delta = (b-a)/float(B)
        for i in range(B):
            #print delta, np.array([a+i*delta,a+(i+1)*delta])
            c, pnt = self.derriveIntegrator( max_degree,
                                        n_points,
                                        np.array([a+i*delta,a+(i+1)*delta]),
                                        incl_bounds,
                                        is_sym)
            self.coef.append(c)
            self.pnts.append(pnt)


    def __call__(self, f):
        integral = 0
        for i in range(self.n_pieces):
            for k in range(5):
                integral += self.coef[i][k] * f(self.pnts[i][k])
        return integral

    def integrate(func, lowbound, upbound):
        print 'not implementet... yet...'
        
        
    def derriveIntegrator(  self,
                            max_degree=2,
                            n_points=3,
                            boundaries=np.array([-1,1]),
                            incl_bounds = True,
                            is_sym = True):

        """ Derrives a n-point integrator ala newton, simpson, ...
        (if no arguments are given, a simpson integrator is returned)
        
        @param max_degree: up to which degree should the integrator be accurate?
        @param n_points: number of points to evaluate the integral at
        @param boundaries: integrate from boundaries[0] to boundaries[1]
        @param incl_bounds: evaluate the integral at boundaries?
        @param is_sym Is this symmetric?
        @return: Integrator-Class
        """
        
        b_range = boundaries[1] - boundaries[0]
        delta = (b_range + incl_bounds) / float(n_points) # this does the same as the if below would do...
        #if incl_bounds:
        #	delta = (b_range + 1) / n_points
        #else:
        #	delta = b_range / n_points	

        degrees = range(0, max_degree+1, 1+is_sym) # if this is symetric (is_sym = true = 1), take only even degrees
        
        #generate the points inbetween..
    # the last term shifts the points half a delta to the right if the
            # boundaries are NOT included
        points = np.array(
            np.linspace(boundaries[0], boundaries[1], n_points, incl_bounds)
            + delta / 2.0 * (not incl_bounds), dtype=float)
            
        
        #if its symetric, we only need the points >=0
        if is_sym:
            points = points[points>=0]
            n_points = len(points)
        
        #status report
        #print '\nStatus:'
        #print 'Deg:', degrees, '( max:', max_degree, '; num:',len(degrees),')'
        #print 'Bounds:', boundaries, '( rng:',b_range,'; delta:', delta, ')'
        #print 'Points:', points, '( tot:', n_points,')'
        
        f = np.zeros([len(degrees),n_points], dtype=np.float)
        res = np.zeros(len(degrees), dtype=np.float)
        
        for i_d, deg in enumerate(degrees):
            for i_x, x in enumerate(points):
                f[i_d,i_x] = self.eval_poly(x, [deg])
                if is_sym and i_x!=0:
                    f[i_d,i_x] *= 2
            res[i_d] = self.eval_int(boundaries, [deg])

        #Status report
        #print '\nThe coefficents:'
        #print f
        #print '\nThe integrals:'
        #print res
        
        try:
            sol = np.linalg.solve(f, res)
            #print '\nFound a possible Integrator:'
            #print sol
            #print '\nExit integrator generator\n'
            return [sol, points]
        except np.linalg.LinAlgError:
            #print '\nCan\'t solve this task, because the resulting matrix is not sqaure..\nCheck your values!'
            #print '\nExit integrator generator\n'
            print 'Integration.py Error:\n    Could not solve the matrix equation, mismatch in dimensions.'
            return False

        
    def eval_poly(self, x, degrees):
        """
        evaluates the polynomial function f(x) with degree degrees (a list!)
        
        @param: x Parameter, the polynom is evaluated at
        @param: degrees List of degrees the function contains
        @return: The value of the function
        
        TODO:   quite ugly like this, change to better style proposed in script
                p.16, 4.20: summing up and don't use a list for degrees...
                but its only for intern use, polynomials.py has a better eval function..
        """
        value = 0
        for i in degrees:
            value += pow(x,i)
        
        #print 'evaluating polynom with degrees', degrees, 'at pos x=', x, 'equals f(x)=', value
        return value

        
    def eval_int(self, bounds, degrees):
        """
        evaluates the integral of a polynom f(x) = sum over(degrees) (x^degree)
        
        @param: bounds list of len=2 with the boundaries of the Integral
        @param: degrees List of degrees the function contains
        @return: The integral of the polynom
        """
        value = 0
        for x in reversed(bounds):
            for i in degrees:
                value += pow(x,i+1) * 1 / float(i+1)
            value *= -1
        #print 'evaluating int of poly with degrees', degrees, 'at pos x=', x, 'equals f(x)=', value
        return value
    

class FivePointIntegrator(BasicIntegrator):
    """
    A derrived wrapper class for integrating using a fife point integrator
    on B pieces of the intervall
    
    basically uses stuff generated in derrint.py
    A instance I can be used to integrate a function f like: int = I(f)
    """

    def __init__(self, n_pieces = 1, boundaries=np.array([-1,1])):
        super(FivePointIntegrator, self).__init__(4,5,boundaries,False,False, n_pieces)


class SimpsonIntegrator(BasicIntegrator):
    def __init__(self, n_pieces = 1, boundaries=np.array([-1,1])):
        super(SimpsonIntegrator, self).__init__(2,3,boundaries,True,True, n_pieces)



class BoolIntegrator(BasicIntegrator):
    def __init__(self, n_pieces = 1, boundaries=np.array([-1,1])):
        super(BoolIntegrator, self).__init__(4,5,boundaries, True, True, n_pieces)



def main(*args):
    try:
        print "direct call, print some demo"
        # some code here
    except:
        raise
        # handle some exceptions
    else:
        return 0 # exit errorlessly     
        

def classmain():
    print 'Imported integration.py'
    pass

        
if __name__ == '__main__':
    sys.exit(main(*sys.argv))
else:
    classmain()