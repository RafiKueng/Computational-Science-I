"""LegendrePoly.py assignments from week 4
Program generates the first n legendre polynomials using orthogonality relation
"""
__author__ = "Marion Baumgartner (marion.baumgartner@uzh.ch)"
__date__ = "$Date: 18/10/2011 $"
 
from NewtonCotes import fivepoint
from scipy import *
from matplotlib import *
from pylab import *
 
def evalp(c,x):
    """evaluate a polinomial at x
    @param c array with the coefficient of the polinomial
    @param x value at with te polynomial is evaluated
    """
    sum=0
    for k in range(len(c),0,-1):
        sum=x*sum+c[k-1]
    return sum
 
def ansatz(n):
    """generate an ansaz for the coefficients of the first n polynomials.
    The function returnes a List of arrays, where the arrays contain the coefficients of the polinomials.
    The coefficinets are all set to one
    """
    P=[]
    for i in range(1,n+1,1):
        q=ones(i,float)
        P.append(q)
    return P
 
def normalise(P):
    """normalise a polinomial
    @parem P array containig the coefficients of the polynomial
    """
    for j in range(len(P)):
        P/=fivepoint(lambda x:evalp(P,x)**2,-1,1,10)**0.5
    return P
 
def gramsmitd(n):
    """generate n polynumials using the gram-smidt orthonormal method for plynomials
    @param n the amunt of polinomials to be generated
    """
    #P array containig all the polinomial coefficients
    P=ansatz(n)
    for m in range(len(P)):
        #q=ones(m,float)
        #P.append(q)
        for j in range(len(P[m])):
            for i in range(len(P[j])):
                #compute the i-the Polinomial P[i]: projects the Polinomials P[j<i] orthogonally onto the subspace U generated by P[1], ..., P[i-1].
                #The vector P[i] is then defined as the difference between vP[j<1]
                #The projection guarantees to be orthogonal to all of the vectors in the subspace U.
                P[m][i]-=fivepoint(lambda x:evalp(P[m],x)*evalp(P[j],x),-1,1,10)*P[j][i]
        #normalisation of the polinomial (create orthogonal polynomials)
        P[m]=normalise(P[m])
    return P
 
def legendre(n):
    """ generate the first n legendre polinomials using the integral normalisation kriteria of the legendre polynomials
    """
    P=gramsmitd(n)
    for i in range(len(P)):
        P[i]=1/(float(i)+1/2.0)**0.5*P[i]
    return P
 
if __name__ == '__main__':
    Coeffs=legendre(5)
    x=arange(-1,1,0.01)
    for i in range(len(Coeffs)):
        y=[]
        for j in range(len(x)):
            y.append(evalp(Coeffs[i],x[j]))
        plot(x,y)
    show()