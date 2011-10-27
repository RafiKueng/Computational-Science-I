"""
-------------------------------------------------------------------------------
 Class for handling Polynomials
-------------------------------------------------------------------------------
Explanation:
    Derrived from the work done in the legendrepolynoial task..

How this code works:
    

Notes / Convention:
    * the poly class doesn't yet implement all operations, 
    it implements at the moment:
    
        * (creator): with either a numer (for degree) or a list containing the
        coefficents
        
        * (*): with same class object (results in a function)
        
        * (*): with some number (int, float) (if the other object isn't of the
        same type, it expects it to be a number!
        
        * (-=): with other object of same class (can have different length)
        
        * (call()): an instance can be called, it returns:        
            * with no argument: the array of coefficents
            * with a number argumentx : the value of the function at x
            
        * (element access []): the coefficents of an instance i can directly
        be acceessed and modified using i[key]

 
-------------------------------------------------------------------------------
Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
v1 2011-10-25   basic implementation (legendrepoly.py) 
v2 2011-10-27   copy to polynomials, strip down to very basic stuff to be
                usable as class to be imported
 
BUGS / TODO:
    * implement all operators for the polynimial class

LICENSE:
    
-------------------------------------------------------------------------------
"""

# imports
import numpy as np
import sys

class poly(object):
    """Class representing a Polynomial"""

    def __init__(self, arg=None):
        """
        The allmighty creator
        arg can be:
        - None: same as arg = 0: a constant, with c0 = NaN
        - a number (the degree of the polynomial, the coefficents will be set to NaN
        - a list of numbers (the coefficents, the degree is set automaticly)
        """
        
        self.numtype = float # it's not supposed to be changed, except manually...
        
        if arg == None:
            self.n = 0
        else:
            try:
                (x for x in arg) # check if arg is a list (is iterable) 
                self.coef = np.array(arg, dtype=self.numtype)
            except TypeError: # if not, expect it to be an int!
                self.n = arg

    
    def eval(self, x=0):
        """Evaluate this Polynom at a particulat value x"""
        n = len(self.coef) - 1
        sum = self.coef[-1]
        for k in range(n, 0,-1) :
            sum = x * sum + self.coef[k-1]
        return sum

    # Basic customization
    # -------------------------------------------------------
    # let this class behave like a regular list and a function at the same time, 
    # depending whether a arg x is provided...
        
        
    def __repr__(self):
        return ''.join(['P: deg: %d c: ' % (self.n-1), '; '.join(map(lambda x:'{: .2f}'.format(x),self.coef))])
        
    def __str__(self):
        #return ''.join(['P%d has coef: ' % (self.n-1), '; '.join(map(lambda x:"%.2f"%x,self.coef))])
        return ''.join(['Poly of degree: %d; has coefs: ' % (self.n-1), '; '.join(map(lambda x:'{: .3f}'.format(x),self.coef))])


        
    # Emulating callable objects
    # -------------------------------------------------------
    # let this class behave like a regular list and a function at the same time, 
    # depending whether a arg x is provided...
    def __call__(self, x = None):
        """
        if a instance I of this class is caled like a function then:
        * with no argument: return the np.array containing the coefficents
        * with one float argument x: evaluate the Polynom at x
        """
        if x == None:
            return self._coef
        else:
            return self.eval(x)
            
 
 
    # Emulating container types
    # -------------------------------------------------------
    # slicing not implemented properly, just returns the coefs instead of new
    # polynomials with everthing set to 0 except the indices in key...
    def __len__(self):
        return len(self._coef)
        
    def __getitem__(self,key):
        return self._coef[key]
        
    def __setitem__(self, key, value):
        self._coef[key] = value
        
    def __iter__(self):
        return self._coef
 

 
    # Emulating numeric types
    # -------------------------------------------------------
    # implement operators
    def __mul__(self, other): # *
        """
        If other is a polynom:
            Returns a funcion, ready to be evaluated
            math: Pn(x) * Pm(x) -> python usage: (Pm*Pn)(x)
            maybe change this behavour later to return a new polynom...
        else: (assumed other is int or float!!)
            return a LGP with element wise multiplied coefficients
        """
        if isinstance(other, type(self)):
            return lambda x: self.eval(x) * other.eval(x)
        else:
            return LGP(self.coef*other)

    def __div__(self, other): # /
        """
        If other is a polynom:
            do element wise div (same length is assumed, otherwise error)
        else if other is a int/float:
            return a LGP with each coefficent div'ed by other
        """
        if isinstance(other, type(self)):
            try:
                return LGP(self.coef / other.coef)
            except ValueError:
                print 'You tried to element wise div two polys that don\'t have the same length!'
                raise
        else:
            return LGP(self.coef/float(other))
            
    def __isub__(self, other): # -=
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
    
    def __idiv__(self, other): # /=
        """should handle div by number and element wise div of coef (unchecked)"""
        try: #assume its a int or float
            self._coef /= self.numtype(other)
            return self
        except TypeError: #this failed, so assume its a polynom (or np.array) of same length
            try:
                self._coef /= other
                return self
            except ValueError:
                print "polynomial: Error with /= operator:\n    other is not a number, nor a np.array of same length"
                raise
                
        
    # override default setter / getter
    # -------------------------------------------------------
    
    @property
    def n(self):
        """The degree of the Polynom"""
        return self._n
        
    @n.setter
    def n(self, n):
        """
        if de degree changes, every coefficent will be re initialised
        TODO: add later dynamic growth and shrinking of polynimials if needed
        """
        self._n = n
        self._coef = np.array([np.NaN]*(n+1), dtype=self.numtype)
        
    @property
    def coef(self):
        """The coefficents of the Polynom"""
        #print 'get coef'
        return self._coef
        
    @coef.setter
    def coef(self, coef):
        #print 'set coef'
        self._coef = np.array(coef, dtype=self.numtype)
        self._n = len(coef)





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
    print 'Imported polynomials.py'
    pass

        
if __name__ == '__main__':
    sys.exit(main(*sys.argv))
else:
    classmain()