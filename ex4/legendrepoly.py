"""
--------------------------------------------------------------------------
 Legendre Polinomial Generator
--------------------------------------------------------------------------
Explanation:
    Generates the legendre Polynomials using the orthogonality relation
    I generate a polynomial like class, for easy operation with polynomials
    now and later on, maybe it's usefull one day.
    i know its quite a overkill...

How this code works:
    

Notes / Convention:
    * the LGP class (polynomial class) doesn't yet implement all operations, 
      it implements at the moment:
        * (creator): with either a numer (for degree) or a list containing the coefficents
        * (*): with same class object (results in a function)
        * (*): with some number (int, float) (if the other object isn't of the same type, it expects it to be a number!
        * (-=): with other object of same class (can have different length)
        * (call()): an instance can be called, it returns:
            * with no argument: the array of coefficents
            * with a number argumentx : the value of the function at x
        * (element access []): the coefficents of an instance i can directly be acceessed and modified using i[key]

 
--------------------------------------------------------------------------
Rafael Kueng
v1 basic implementation
 
BUGS / TODO:
    * implement all operators for the polynimial class LGP

--------------------------------------------------------------------------


"""


from derrint import derriveIntegrator
import numpy as np
import matplotlib as mp
import pylab as pl


class LGP(object):
    """Class representing a Legendre Polynomial"""

    def __init__(self, arg=None):
        """
        The allmighty creator
        arg can be:
        - None: same as arg = 0: a constant, with c0 = NaN
        - a number (the degree of the polynomial, the coefficents will be set to NaN
        - a list of numbers (the coefficents, the degree is set automaticly)
        """
        if arg == None:
            self.n = 0
        else:
            try:
                (x for x in arg) # check if arg is a list (is iterable) 
                self.coef = np.array(arg, dtype=float)
            except TypeError: # if not, expect it to be an int!
                self.n = arg

    
    def eval(self, x=0):
        """Evaluate this Polynom at a particulat value x"""
        n = len(self.coef) - 1
        sum = self.coef[-1]
        for k in range(n, 0,-1) :
            sum = x * sum + self.coef[k-1]
        return sum

    def __repr__(self):
        return ''.join(['LGP: deg: %d; coef: ' % (self.n-1), ', '.join(map(str,self.coef))])
        
    def __str__(self):
        #return ''.join(['P%d has coef: ' % (self.n-1), '; '.join(map(lambda x:"%.2f"%x,self.coef))])
        return ''.join(['P%d has coef: ' % (self.n-1), '; '.join(map(lambda x:'{: .3f}'.format(x),self.coef))])

# let this class behave like a regular list
    def __call__(self, x = None):
        """
        if a object of this class is caled like a function then
        * with no argument: return the array containing the coefficents
        * with one float argument x: evaluate the Polynom at x
        """
        if x == None:
            return self._coef
        else:
            return self.eval(x)
        
    def __getitem__(self,key):
        return self._coef[key]
        
    def __setitem__(self, key, value):
        self._coef[key] = value
        
    def __mul__(self, other):
        """
        If other is a LGP:
            Returns a funcion, ready to be evaluated
            math: Pn(x) * Pm(x) -> python usage: (Pm*Pn)(x)
        else if other is a int:
            return a LGP with element wise multiplied coefficients
        """
        if isinstance(other, type(self)):
            return lambda x: self.eval(x) * other.eval(x)
        else:
            return LGP(self.coef*other)

    def __div__(self, other):
        """
        If other is a LGP:
            do element wise div (same length is NOT checked)
        else if other is a int/float:
            return a LGP with each coefficent div'ed by other
        """
        if isinstance(other, type(self)):
            return LGP(self.coef / other.coef)
        else:
            return LGP(self.coef/float(other))
            
    def __isub__(self, other):
        """
        Definition of the -= operator
        it also works with different sized polynomials
        """
        
        if self.n == other.n:
            self.coef-=other.coef
        else:
            lmin = min(len(self.coef), len(other.coef))
            lmax = max(len(self.coef), len(other.coef))
            tmp = np.array([0]*lmax, dtype=float)
            for i in range(lmin):
                tmp[i]=self.coef[i]-other.coef[i]
            if len(self.coef) < len(other.coef):
                for i in range(lmin, lmax):
                    tmp[i] -= other[i]
            else:
                for i in range(lmin, lmax):
                    tmp[i] += self[i]
            self.coef = tmp
        return self
    
    def __idiv__(self, other):
        """should handle div by number and element wise div of coef (unchecked)"""
        try:
            #print '        idiv:', self, 'other:', other
            self._coef /= float(other)
            #print '        idiv:', self, 'other:', other
            return self
        except:
            print "something went wrong with the /= op, maybe not a number or not a vector of same size for element wise div..."
            raise
        
# make setter / getter
    @property
    def n(self):
        """The degree of the Polynom"""
        #print 'get n'
        return self._n
        
    @n.setter
    def n(self, n):
        #print 'set n'
        self._n = n
        self._coef = np.array([np.NaN]*(n+1), dtype=float)
        
    @property
    def coef(self):
        """The coefficents of the Polynom"""
        #print 'get coef'
        return self._coef
        
    @coef.setter
    def coef(self, coef):
        #print 'set coef'
        self._coef = np.array(coef)
        self._n = len(coef)

        
class FivePointIntegrator(object):
    """
    A wrapper class for integrating using a fife point integrator on B pieces of the intervall
    basically uses stuff generated in derrint.py
    A instance I can be used to integrate a function f like: int = I(f)
    """

    def __init__(self, n_pieces = 1, boundaries=np.array([-1,1])):

        self.coef = []
        self.pnts = []
        self.n_pieces = B = n_pieces
        self.bounds = boundaries
        a = boundaries[0]
        b = boundaries[1]
        
        delta = (b-a)/float(B)
        for i in range(B):
            #print delta, np.array([a+i*delta,a+(i+1)*delta])
            c, pnt = derriveIntegrator(4,5,np.array([a+i*delta,a+(i+1)*delta]),False,False)
            self.coef.append(c)
            self.pnts.append(pnt)
    
    def __call__(self, f):
        integral = 0
        for i in range(self.n_pieces):
            for k in range(5):
                integral += self.coef[i][k] * f(self.pnts[i][k])
                
        return integral







def genLegendrePoly(n_poly = 3):
    """
    Generates the legendrepolynomials up to P_(n-poly) (degree n_poly)
    using gram smith orthogonalisation
    """
    
    polys = []
    #p0 = LGP([1])
    #polys.append(p0)
    integr = FivePointIntegrator(10)
    print '\n\n\n\n\n=============================================\n finished generating integrator...\n \nGenerating Legendre Polynomials\n'
    
    for n in range(0, n_poly+1):
        print ' - generate P%d'%n
        
        Pn = LGP([1]*(n+1)) #degree 1 has 2 coefficients, degree 2 has 3, ...
        polys.append(Pn)
        
        for m in range(len(Pn())):
            #print 'n,m',n,m
            Pm = polys[m]
            #print 'Pn', Pn
            #print 'Pm', Pm
            
            for i in range(Pm.n):
                #print '    n,m,i',n,m,i
                tmp = integr(Pn * Pm) * Pm[i]
                #print '    intgr(Pm*Pn)*Pm[i]: ' ,tmp
                Pn[i] -=  tmp
                #print '    Pn', Pn, '\n'

        #print '  old   :', Pn
        for m, Pm in enumerate(polys):
            norm = np.sqrt(integr(Pn*Pn))
            #print '  norm:', norm
            Pn /= norm
        #print '  normed:', Pn
        polys[n] = Pn

    #polys = [ (Pn * (np.array(range(len(Pn())))/2.)**0.5) for Pn in polys]
    
    for id in range(len(polys)):
        polys[id] = polys[id]*(1 / (float(id)+1/2.0)**0.5)
    
        
    return polys

 
if __name__ == '__main__':
    n_poly = 5
    polys = genLegendrePoly(n_poly)
    print '\nFinished creating %d Legendrepolynomials\n   printing the polynomials (rounded to 3 digits after comma):\n' %n_poly
    x = np.arange(-1, 1, 0.01)
    
    for p in polys:
        print p
        y = map(p.eval, x)
        pl.plot(x,y)
    pl.show()