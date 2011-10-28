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



def genChebzshevPoly(n_poly = 3):
    integr = iL.FivePointIntegrator(10, [-1,1])
    polys = []

    print '\nGenerating Legendre Polynomials using GramSchmidt\n'
    
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

        polys[n] = Tn
        for m, Tm in enumerate(polys):
            norm = np.sqrt(integr(lambda x:(Tn(x) * Tn(x)) / np.sqrt(1.0-x*x)))
            Tn /= norm


    polys[0] = polys[0] * np.sqrt(np.pi)
    for id in range(1,len(polys)):
        polys[id] = polys[id] * np.sqrt(np.pi/2.)
    
        
    return polys    
    

def norm1(polys):
    pass
    
    
    
    
    
    
def plotPolys(data):
    x = np.arange(-1, 1, 0.01)
    for d in data:
        print d
        y = map(d.eval, x)
        pl.plot(x,y)
    pl.show()


def main(*args):
    ChebyGS = genChebzshevPoly(5)
    
    
    plotPolys(ChebyGS)
    
    
    
    
    return 0 # exit errorlessly     
        

def classmain():
    print 'Imported chebyp.py inline... run it directly'
    pass

        
if __name__ == '__main__':
    sys.exit(main(*sys.argv))
else:
    classmain()