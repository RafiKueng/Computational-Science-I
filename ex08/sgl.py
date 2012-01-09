# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex08: Schroedinger Equation
-------------------------------------------------------------------------------
Explanation:
    1d sgl:
    i * d phi / dt = -1/2 * d^2 phi / d x^2 + V(x) phi
    
    using fft:
    phi~(k) = int _-inf ^inf [ exp(ikx) * phi(x) dx ]

    one gets:
    i * d phi~ / dt = -1/2 * k^2 * phi~ + int _-inf ^inf [ exp(ikx) * V * phi(x) dx ]
    
    Since time evo can be written as exp(-i*t*H), with H = A+B and
    Baker-Campell-Hausdorff ident:
        exp(1/2*t*i*A) exp(t*i*B) exp(1/2*t*i*A) = exp(t*i*H)

    its basically done like this:
        psi *= exp(1j*V*delta_t/2)
        psi_k = fft(psi)
        psi_k = concatenate(( psi_k[N/2:N], psi_k[0:N/2]))
        psi_k *= exp(1j*K*K*delta_t)
        psi_k = concatenate(( psi_k[N/2:N], psi_k[0:N/2]))
        psi = ifft(psi_k)
        psi *= exp(1j*V*delta_t/2)

        
How this code works:
   

Notes / Convention:
    i suppose there are still a few bug in here, strange resulat...
 


-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-18   basic implementation
    v2 2012-01-09   rewrite with help from solution
 
BUGS / TODO:
    still looks quite strange...


LICENSE:
    none
    
-------------------------------------------------------------------------------
"""

from os import sys
from numpy import array, pi, sqrt, exp, arange, abs, concatenate
from scipy.fftpack import fft,ifft
import matplotlib as mp
import pylab as pl
import time



class sgl(object):
    def __init__(self, N, R, initFunc, V, dt, t0):
        """
        N: # of points on the x axis
        R: length of the x axis
        """
        
        self.dt = dt
        self.t = t0
        
        self.dx = 2.*R/N
        self.x = (array(range(N)) - N/2)*self.dx
        self.n = N
        
        self.k = 2*pi*(array(range(N))-N/2)/self.dx
        
        self.phi_x = initFunc(self.x)

        self.V_fn = V #potential function
        self.V = V(self.x)
        
                        
    def convert_x_to_k(self):
        tmp = fft(self.phi_x)
        self.phi_k = concatenate((tmp[self.n/2:self.n], tmp[0:self.n/2]))

    def convert_k_to_x(self):
        self.phi_k = concatenate((self.phi_k[self.n/2:self.n], self.phi_k[0:self.n/2]))
        self.phi_x = ifft(self.phi_k)
        
    def calc_step(self):
    
        # phi(x, t+dt) = phi(x,t) * exp(-iV(x)dt/h_bar/2)
        self.phi_x = self.phi_x * exp(-1j*self.V*self.dt/2)
        self.convert_x_to_k()
        
        #phitilde(k, t+dt) = phitilde(k, t) * exp(  -i h_bar k k dt / 2m )
        self.phi_k = self.phi_k * exp(1j*self.k*self.k*self.dt)
        self.convert_k_to_x()

        self.phi_x = self.phi_x * exp(-1j*self.V*self.dt/2)
                
        self.t += self.dt

        
        
    def paint(self):
    
        pl.figure()
        self.linehandle_psi_x = pl.plot(self.x, abs(self.phi_x))[0]
        pl.plot(self.x, self.V)
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
    
    N = 2**10
    R = 50
    #initFunc = gauss(4,-50,-100.0)
    initFunc = lambda x: exp(-0.5*(x-1)**2/2.) +0j
    #V = barrier(10,1000000,0)
    V = lambda x: 0.5*abs(x-1.0)**2
    
    dt = 0.0000005
    t0 = 0
    t_max = .0001
    
    
    sgl1 = sgl(N, R, initFunc, V, dt, t0)
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