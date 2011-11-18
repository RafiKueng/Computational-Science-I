# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex08: Schroedinger Equation
-------------------------------------------------------------------------------
Explanation:

    
    
How this code works:

    

Notes / Convention:



-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-18   basic implementation
 
BUGS / TODO:
    doen't really work, theres somewhere a few bugs hidden...


LICENSE:
    none
    
-------------------------------------------------------------------------------
"""

from os import sys
from numpy import array, pi, sqrt, exp, arange, abs
from scipy.fftpack import fft,ifft
import matplotlib as mp
import pylab as pl



class sgl(object):
    def __init__(self, xAxisSetup, initFunc, k0_init, V, dt, t0):
        """
        xAxisSetup: [Xmin, Xmax, dx]
        """
        
        self.V = V #potential function
        self.dt = dt
        self.t = t0
        self.xMin, self.xMax, self.dx = xAxisSetup
        self.x = arange(*xAxisSetup)
        self.n = len(self.x)
        self.phi_x = initFunc(self.x)
        
        self.dk = 2*pi /(self.n * self.dx)
        self.k0 =  -0.5*self.n * self.dk
        self.k = arange(self.n) * self.dk + self.k0
        
        self.phi_x = self.phi_x * exp(-1j * self.k[0] * self.x) * self.dx / sqrt(2*pi)
        
        self.convert_x_to_k()
        
                        
    def convert_x_to_k(self):
        self.phi_k = fft(self.phi_x)

    def convert_k_to_x(self):
        self.phi_x = ifft(self.phi_k)    
        
    def calc_step(self):
    
        # phi(x, t+dt) = phi(x,t) * exp(-iV(x)dt/h_bar)
        self.phi_x = self.phi_x * exp(-1j*self.V(self.x)*self.dt)
        self.convert_x_to_k()
        
        #phitilde(k, t+dt) = phitilde(k, t) * exp(  -i h_bar k k dt / 2m )
        self.phi_k = self.phi_k * exp(-1j*self.k*self.k*self.dt/2.)
        self.convert_k_to_x()

        self.t += self.dt

        
        
    def paint(self):
    
        pl.figure()
        self.linehandle_psi_x = pl.plot(self.x, abs(self.phi_x))[0]
        pl.plot(self.x, self.V(self.x))
        ymin = min(abs(self.phi_x))
        ymax = max(abs(self.phi_x))
        pl.ylim( ymin-0.2*(ymax-ymin),ymax+0.2*(ymax-ymin) )

        
    def repaint(self):
        self.linehandle_psi_x.set_data(self.x, abs(self.phi_x))
        pl.draw()
    



def gauss_fn(x,w,x0,k0):
    """
    gaussian wave packet of width w, center at x0, momentum k0
    """ 
    return (w*sqrt(pi))**(-0.5) * exp(-0.5*((x-x0)*1./w)**2 + 1j*x*k0)

def gauss(w,x0,k0):
    """
    gaussian wave packet of width w, center at x0, momentum k0
    """ 
    return lambda x:(w*sqrt(pi))**(-0.5) * exp(-0.5*((x-x0)*1./w)**2 + 1j*x*k0)
    
def step(limit=0):
    """classical stepfunction: is 0 for x<limit, 1 otherwise"""
    return lambda x: array(x>=limit, dtype=int)

def barrier(width=0.1, height = 1, loc = 0):
    """creates a barrier at (around) x = loc, of height and witdh"""
    return lambda x: height*( step(-width/2.0)(x-loc) * 1-step(width/2.0)(x-loc))
    
def main():

    pl.ion()
    
    #V = lambda x: 0.5*abs(x-1)**2
    
    xAxisSetup = [-100, 100, 0.01]
    initFunc = gauss(4,-50,10.0)
    k0_init = 10.
    V = barrier(5,10,0)
    dt = 0.05
    t0 = 0
    t_max = 10.
    
    sgl1 = sgl(xAxisSetup, initFunc, k0_init, V, dt, t0)
    sgl1.paint()
    
    while sgl1.t < t_max:
        sgl1.calc_step()
        sgl1.repaint()
    
    pl.show()

    
    
    
    
def cmdmain(*args):
    try:
        main()
        
    except:
        raise
        # handle some exceptions
    else:
        return 0 # exit errorlessly     
        

def classmain():
    print '[display notes if imported as a class]'
    

        
if __name__ == '__main__':
    sys.exit(cmdmain(*sys.argv))
else:
    classmain()