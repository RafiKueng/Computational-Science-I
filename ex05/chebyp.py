"""
--------------------------------------------------------------------------
 Chebyshev Polynomials Generator
--------------------------------------------------------------------------
Explanation:
    Generates the Chebyshev Polynomials using the orthogonality relation
    
How this code works:
    

Notes / Convention:

 
-------------------------------------------------------------------------------
Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
v1 2011-10-27   basic implementation
 
BUGS / TODO:


LICENSE:
    
-------------------------------------------------------------------------------
"""

import sys
import numpy as np
import matplotlib as mp
import pylab as pl
import integration as iL
import polynomials as pL



def genChebzshevPolyGS(n_poly = 3):
    """
    Generates Chebyshev Polynomials using GramSchmidt
    """
    integr = iL.FivePointIntegrator(10, [-1,1])
    polys = []

    print '\nGenerating Chebyshev Polynomials using GramSchmidt'
    print '-----------------------------------------------------------------------\n'

    
    for n in range(0, n_poly+1):
        print ' - generate P%d'%n
        
        Tn = pL.poly([1]*(n+1)) #degree 1 has 2 coefficients, degree 2 has 3, ...
        polys.append(Tn)
        
        for m in range(len(Tn())-1):
            Tm = polys[m]
            #print 'indices',n,m
            #print 'Tn', Tn
            #print 'Tm', Tm
            
            for i in range(Tm.n):
                #print '    n,m,i',n,m,i
                #tmp = integr(lambda x:(Tn(x) * Tm(x)) / np.sqrt(1.0-x*x))
                #print '    intgr at: ',n,m,i,"int",tmp, Tm[i]
                #Tn[i] -=  tmp * Tm[i]
                #print '    ', Tn, '\n    ',Tm
                
                Tn[i] -= integr(lambda x:(Tn(x) * Tm(x)) / np.sqrt(1.0-x*x)) * Tm[i]

        polys[n] = norm1(Tn, integr)
        
    return normFinal(polys)    
    

def norm1(Tn, integr):
    for m in range(len(Tn)):
        Tn /= np.sqrt(integr(lambda x:(Tn(x) * Tn(x)) / np.sqrt(1.0-x*x)))
    return Tn
    
    



def normFinal(polys):
    polys[0] = polys[0] * np.sqrt(np.pi)
    for id in range(1,len(polys)):
        polys[id] = polys[id] * np.sqrt(np.pi/2.) 
    return polys

    
    
    

def genChebyshevPolyGCQ(n_poly = 3, M_eval = 10):
    """
    Generates Chebyshev Polynomials using
     * Gauss-Chebyshev quadrature for integration
     * Gram Schmidt
    """
    integr = iL.GaussChebishevQuadrature(M_eval)
    polys = []

    print '\n\nGenerating Chebyshev Polynomials using Gauss-Chebyshev quadrature'
    print '-----------------------------------------------------------------------\n'
    
    for n in range(0, n_poly+1):
        print ' - generate P%d'%n
        
        Tn = pL.poly([1]*(n+1)) #degree 1 has 2 coefficients, degree 2 has 3, ...
        polys.append(Tn)
        
        for m in range(len(Tn())-1):
            Tm = polys[m]
            #print 'indices',n,m
            #print 'Tn', Tn
            #print 'Tm', Tm
            
            for i in range(Tm.n):
                #print '    n,m,i',n,m,i
                #tmp = integr(lambda x:(Tn(x) * Tm(x)) / np.sqrt(1.0-x*x))
                #print '    intgr at: ',n,m,i,"int",tmp, Tm[i]
                #Tn[i] -=  tmp * Tm[i]
                #print '    ', Tn, '\n    ',Tm
                
                Tn[i] -= integr(Tn * Tm) * Tm[i]

        polys[n] = norm2(Tn, integr)
        
    return normFinal(polys)    


def norm2(Tn, integr):
    for m in range(len(Tn)):
        Tn /= np.sqrt(integr(Tn * Tn))
    return Tn
    
    
    
    
    
    


def plotPolys(data):
    print '\n\nR E S U L T S   &   P L O T S :\n'
    x = np.arange(-1, 1, 0.01)
    for d in data:
        print d
        y = map(d.eval, x)
        pl.plot(x,y)
    pl.show()


def main(*args):

    ChebyGS = genChebzshevPolyGS(5)
    plotPolys(ChebyGS)

    ChebyGCQ = genChebyshevPolyGCQ(5,100)
    plotPolys(ChebyGCQ)
    
    
    
    return 0 # exit errorlessly     
        

def classmain():
    print 'Imported chebyp.py inline... run it directly'
    pass

        
if __name__ == '__main__':
    sys.exit(main(*sys.argv))
else:
    classmain()