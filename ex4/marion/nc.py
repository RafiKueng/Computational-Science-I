"""NewtonCotes.py Problem 1
 
This program numericaly integrates a function (f(x)) using the open 5-point Newton Cotes formula.
The integration is correct for polynoms up to 4th degree
"""
__author__ = "Marion Baumgartner (marion.baumgartner@uzh.ch)"
__date__ = "$Date: 2011/10/17 $"
 
from numpy import *
from scipy.linalg import *
from fractions import Fraction
 
def f(x,n):
    """function calculates the nth power of x"""
    return pow(x,n)
 
def intf(n,bound1,bound2):
    """returne the integration between bound1 and bound2 of the above function f"""
    fun=1.0/(n+1)*(pow(bound2,(n+1))-pow(bound1,(n+1)))
    return fun
 
def genA(a,b):
    """generate the matrix A to calculate the coefficients for the open Newton Cotes fromula
    @param a lower integration bound
    @param b upper integration bound"""
    x1,x2,x3,x4,x5=genNodes(a,b)
    A=array([[f(x1,0),f(x2,0),f(x3,0),f(x4,0),f(x5,0)],[f(x1,1),f(x2,1),f(x3,1),f(x4,1),f(x5,1)],[f(x1,2),f(x2,2),f(x3,2),f(x4,2),f(x5,2)],[f(x1,3),f(x2,3),f(x3,3),f(x4,3),f(x5,3)],[f(x1,4),f(x2,4),f(x3,4),f(x4,4),f(x5,4)]])
    return A
 
def genb(a,b):
    """generate the vector b to calculate the coefficients for the open Newton Cotes fromula
    @param a lower integration bound
    @param b upper integration bound"""
    bound1=a
    bound2=b
    b=array([intf(0,bound1,bound2),intf(1,bound1,bound2),intf(2,bound1,bound2),intf(3,bound1,bound2),intf(4,bound1,bound2)])
    return b
 
def genNodes(a,b):
    """generate the nodes (stuetzstellen) for speccified boundaries a and b"""
    bound=array(range(1,10,2))
    bound=bound*(b-a)/10.0+a
    return bound
 
def solves(a,b):
    """solve the linear system of equations A*x=b, to finde the integration coeficients contained in x
    @param a lower integration bound
    @param b upper integration bound
    this functions returnes the coefficients for a 5-point open Newton Cotes formaula for any integration boundaries a and b
    the coefficients are returned as decimals as well as in from of fractions"""
 
    #solve the equation
    A=genA(a,b)
    B=genb(a,b)
    xdec=solve(A,B)
 
    #convert the decimal solutions in to fractions
    c0 = xdec[0]
    c1 = xdec[1]
    c2 = xdec[2]
    c3 = xdec[3]
    c4 = xdec[4]
 
    c0fr = Fraction(c0).limit_denominator(1000) # c0 = 335/96
    c1fr = Fraction(c1).limit_denominator(1000) # c2 = 125/144
    c2fr = Fraction(c2).limit_denominator(1000) # c4 = 1375/
    c3fr = Fraction(c3).limit_denominator(1000) # c2 = 125/144
    c4fr = Fraction(c4).limit_denominator(1000) # c4 = 1375/
 
    xfrac =array([c0fr,c1fr,c2fr,c3fr,c4fr])
 
    return [xdec,xfrac]
 
def fivepoint(f,a,b,B=1):
    """Comput \int(f(x)) from a to b
    using B blocks of the 5-point integrator
    divide up the bounds into B parts, integrate over them and sum them"""
    i=1
    bound=[a]
 
    while(i<=B):
        bound.append(i*float(b-a)/float(B)+a)
        i+=1
 
    count=0
    for j in range(len(bound)-1):
        tmp = integration(f,bound[j],bound[j+1])
        count+=tmp
    return count   
 
def integration(f,a,b):
    "numericaly integrats a function (f(x)) from a to b; using the coefficients from the 5-point Newton Cotes fromula"
    x0,x1,x2,x3,x4=genNodes(a,b)
    #generate coefficients
    c=solves(a,b)[0]
    integr=c[0]*f(x0)+c[1]*f(x1)+c[2]*f(x2)+c[3]*f(x3)+c[4]*f(x4)
    return integr
 
def fun(x):
    """function depending on x to be integrated"""
    return pi*exp(-tan(pi/2*x)*tan(pi/2*x))/(2*cos(pi/2*x)*cos(pi/2*x))
 
if __name__ == '__main__':
    #Problem 1
 
    print'The coefficients for the boundary [-5,5] are:'
    print solves(-5,5)
 
    #testing the fivepoint function:
    print'testing the 5-point function with 1,x^2 and x^4'
 
    print 'int(1)',fivepoint(lambda x: 1, -5, 5) #should equal 10
    print 'int(1)',fivepoint(lambda x: x*x, -5, 5) #should equal 83.333
    print 'int(1)',fivepoint(lambda x: x*x*x*x, -5, 5) #should equal 1250
 
    #Problem 2
    # exp(-x^2) from -inf to +inf; using substitution x=tan(pi/2*y)
    print 'integrating exp^(x^2)'
    approx = fivepoint(fun, -1, 1, 10)
    print 'approximation using B=10',approx
    real = sqrt(pi)
    print "copare the error with the analyical solution: ",abs(approx-real)*100,"% "