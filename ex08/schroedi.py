"""
General Numerical Solver for the 1D Time-Dependent Schrodinger's equation.
 Written by Jake VanderPlas, December 2009
  email: vanderplas@astro.washington.edu
  website: http://www.astro.washington.edu/users/vanderplas

 Feel free to use and modify this code, but please leave this doc string
 intact!  I originally wrote this as a homework assignment for a graduate
 level intro to quantum mechanics at the University of Washington. After
 finishing the assignment, I spent a couple hours cleaning it up and
 speeding it up.

 For a discussion of the solution algorithm, please see the writeup that
 accompanies this code at
   http://www.astro.washington.edu/users/vanderplas/code
"""

import numpy
import pylab
from scipy.fftpack import fft,ifft

class schrodinger(object):
    """
    Class which implements a numerical solution of the time-dependent
    Schrodinger equation for an arbitrary potential
    """
    def __init__(self,x,psi_x,V_x,k0 = None,hbar=1,m=1,t0=0.0):
        """
        Parameters:
        ==========
          x     : a length-N array of evenly-spaced values
          psi_x : a length-N array giving the position-space
                  wave-function at time t0
          V_x   : a length-N array giving the potential at x
          k0    : the minimum value of k.  Note that, because of the
                  workings of the fast fourier transform, the momentum
                  wave-number will be defined in the range
                    k0 < k < 2*pi/dx
                  where dx = x[1]-x[0].  If you expect nonzero momentum
                  outside this range, you must modify the inputs
                  accordingly.
                  If not specified, k0 will be calculated such that the
                  range is [-k0,k0]
          hbar  : value of planck's constant
          m     : particle mass
          t0    : initial time
        """
        self.hbar = hbar
        self.m = m
        self.t = t0
        self.dt_ = None

        self.N = len(x)

        self.x = x
        self.dx = self.x[1]-self.x[0]
        self.V_x = V_x

        self.dk = 2*numpy.pi /(self.N * self.dx)
        if k0 == None:
            self.k0 = -0.5*self.N * self.dk
        else:
            self.k0 = k0
        self.k = self.k0 + self.dk*numpy.arange(self.N)

        self.set_psi_x(psi_x)
        self.compute_k_from_x()

        #evolution functions
        self.x_evolve_half = None
        self.x_evolve = None
        self.k_evolve = None

        #attributes used for dynamic plotting
        self.psi_x_line = None
        self.psi_k_line = None
        self.V_x_line = None

    def set_psi_x(self,psi_x):
        self.psi_mod_x = psi_x * numpy.exp(-1j * self.k[0] * self.x) * self.dx/numpy.sqrt(2*numpy.pi)

    def get_psi_x(self):
        return self.psi_mod_x * numpy.exp(1j * self.k[0] * self.x)* numpy.sqrt(2*numpy.pi)/self.dx

    def set_psi_k(self,psi_k):
        self.psi_mod_k = psi_k * numpy.exp(1j * self.x[0] * \
                                           self.dk * numpy.arange(self.N))

    def get_psi_k(self):
        return self.psi_mod_k * numpy.exp(-1j * self.x[0] * \
                                           self.dk * numpy.arange(self.N))
    
    def set_dt(self,dt):
        if dt!=self.dt_:
            self.dt_ = dt
            self.x_evolve_half = numpy.exp(-0.5*1j*self.V_x/self.hbar * dt )
            self.x_evolve = self.x_evolve_half**2
            self.k_evolve = numpy.exp(-0.5*1j*self.hbar/self.m*(self.k**2)*dt)
    
    psi_x = property(get_psi_x,set_psi_x)
    psi_k = property(get_psi_k,set_psi_k)
    dt = property(lambda self: self.dt_,set_dt)

    def compute_k_from_x(self):
        self.psi_mod_k = fft(self.psi_mod_x)

    def compute_x_from_k(self):
        self.psi_mod_x = ifft(self.psi_mod_k)

    def time_step(self,dt,Nsteps = 1):
        """
        Perform a time-step via the time-dependent Schrodinger Equation

        Parameters
        ==========
          dt     : the small time interval over which to integrate
          Nsteps : the number of intervals to compute.  The total change
                   in time will be dt*Nsteps
        """
        self.set_dt(dt)
        if Nsteps>0:
            self.psi_mod_x *= self.x_evolve_half
        for i in xrange(Nsteps-1):
            self.compute_k_from_x()
            self.psi_mod_k *= self.k_evolve
            self.compute_x_from_k()
            self.psi_mod_x *= self.x_evolve
        self.compute_k_from_x()
        self.psi_mod_k *= self.k_evolve
        self.compute_x_from_k()
        self.psi_mod_x *= self.x_evolve_half
        self.compute_k_from_x()

        self.t += dt*Nsteps

    def plot_psi_x(self,
                   evalfunc = abs,
                   plotfunc = pylab.plot,*args,**kwargs):
        """
        use matplotlib to plot psi_x on the current axis.
        Parameters
        ==========
          evalfunc : specify a function which will be applied to the
                     wave-function.
                     The plot will be of evalfunc(psi_x) vs x
                     default is evalfunc = abs
          plotfunc : specify the plotting function to use: e.g.
                       pylab.plot, pylab.loglog, etc.
                     extra arguments and keywords will be passed to this
                     function.
        """
        self.psi_x_eval = evalfunc
        self.psi_x_line = plotfunc(self.x,evalfunc(self.psi_x),*args,**kwargs)[0]

    def plot_psi_k(self,
                   evalfunc = abs,
                   plotfunc = pylab.plot,*args,**kwargs):
        """
        use matplotlib to plot psi_k on the current axis.
        Parameters
        ==========
          evalfunc : specify a function which will be applied to the
                     wave-function.
                     The plot will be of evalfunc(psi_k) vs k
                     default is evalfunc = abs
          plotfunc : specify the plotting function to use: e.g.
                       pylab.plot, pylab.loglog, etc.
                     extra arguments and keywords will be passed to this
                     function.
        """
        self.psi_k_eval = evalfunc
        self.psi_k_line = plotfunc(self.k,evalfunc(self.psi_k),*args,**kwargs)[0]

    def plot_V_x(self,
                 evalfunc = lambda y:y,
                 plotfunc = pylab.plot,*args,**kwargs):
        """
        use matplotlib to plot V_x on the current axis.
        Parameters
        ==========
          evalfunc : specify a function which will be applied to the
                     wave-function.
                     The plot will be of evalfunc(V_x) vs x
                     default is evalfunc = lambda y:y
          plotfunc : specify the plotting function to use: e.g.
                       pylab.plot, pylab.loglog, etc.
                     extra arguments and keywords will be passed to this
                     function.
        """
        self.V_x_eval = evalfunc
        self.V_x_line = plotfunc(self.x,evalfunc(self.V_x),*args,**kwargs)[0]

    def update_psi_x(self):
        """
        update the most recently plotted psi_x line
        """
        self.psi_x_line.set_data( self.x,self.psi_x_eval(self.psi_x) )

    def update_psi_k(self):
        """
        update the most recently plotted psi_k line
        """
        self.psi_k_line.set_data( self.k,self.psi_k_eval(self.psi_k) )

    def update_V_x(self):
        """
        update the most recently plotted V_x line
        """
        self.V_x_line.set_data( self.x,self.V_x_eval(self.V_x) )

    def update_all(self):
        self.update_psi_x()
        self.update_psi_k()
        self.update_V_x()
        pylab.draw()


######################################################################
# Helper functions for gaussian wave-packets
######################################################################

def f(x,a,x0,k0):
    """
    a gaussian wave packet of width a, centered at x0, with momentum k0
    """ 
    return (a*numpy.sqrt(numpy.pi))**(-0.5) * numpy.exp(-0.5*((x-x0)*1./a)**2 + 1j*x*k0)

def psi_k(k,a,x0,k0):
    """
    fourier transform of f(x), above
    """
    return (a/numpy.sqrt(numpy.pi))**0.5 * numpy.exp(-0.5*(a*(k-k0))**2 - 1j*(k-k0)*x0)

######################################################################
# Functions to run example below
######################################################################

def theta(x):
    """
    theta function :
      returns 0 if x<=0, and 1 if x>0
    """
    x = numpy.asarray(x)
    y = numpy.zeros(x.shape)
    y[numpy.where(x>0)] = 1.0
    return y

def square_barrier(x,width,height):
    return height * (theta(x)-theta(x-width))

def make_plot(S,x0,p0,V0,m,hbar,
              xlim=None,klim=None):
    pylab.figure()
    pylab.subplot(211)
    S.plot_psi_x(lambda x:4*abs(x),
               c='r',
               label=r'$|\psi(x)|$')
    S.plot_V_x(c='k',label=r'$V(x)$')
    ymin = min(S.V_x)
    ymax = max(S.V_x)
    pylab.ylim( ymin-0.2*(ymax-ymin),
                ymax+0.2*(ymax-ymin) )
    ylim = pylab.ylim()

    S.x0 = x0
    S.v0 = p0/m
    S.x_center_line = pylab.plot(2*[x0+S.t*p0/m],ylim,':k',
                                 label = r"$x_0 + v_0t$")[0]
    
    pylab.xlim(xlim)
    pylab.ylim(ylim)
    
    pylab.legend(loc=0)

    
    pylab.subplot(212)
    S.plot_psi_k(c='r',
               label=r'$|\psi(k)|$')
    ymin = min(abs(S.psi_k))
    ymax = max(abs(S.psi_k))
    pylab.ylim( ymin-0.2*(ymax-ymin),
                ymax+0.2*(ymax-ymin) )
    ylim = pylab.ylim()
    pylab.plot(2*[-p0/hbar]+2*[p0/hbar],ylim[::-1]+ylim,
               ':k',label=r'$\pm p_0$')
    pylab.plot(2*[numpy.sqrt(2*V0)/hbar],ylim,'--k',
               label=r'$\sqrt{2mV_0}$')   
    pylab.legend(loc=0)
    pylab.xlim(klim)
    pylab.ylim(ylim)

def update_plot(S):
    S.update_all()
    x,y = S.x_center_line.get_data()
    S.x_center_line.set_data( 2*[S.x0+S.t*S.v0],y )
    

def animate():
    N = 2**11
    V0 = 1.5
    hbar = 1.0
    m = 1.0

    L = hbar/numpy.sqrt(2*m*V0)
    a = 3*L
    x0 = -60*L
    
    p0 = numpy.sqrt(2*m*0.2*V0)
    dp2 = p0**2 * 1./80
    d = hbar / numpy.sqrt(2*dp2)

    k0 = p0/hbar
    v0 = p0/m

    dx = 0.1
    x = dx * ( numpy.arange(N) - 0.5*N )
    V_x = square_barrier(x,a,V0)
    #V_x = 0.5*numpy.abs(x-1)**2
    psi_x = f(x,d,x0,k0)
    
    S = schrodinger(x = x,
                    psi_x = psi_x,
                    V_x = V_x,
                    hbar = hbar,
                    m = m,
                    k0=-28)

    print "   xmin =",S.x[0]
    print "   xmax =",S.x[-1]
    print "     dx =",S.x[1]-S.x[0]
    print "   kmin =",S.k[0]
    print "   kmax =",S.k[-1]
    print "     dk =",S.k[1]-S.k[0]

    make_plot(S,x0,p0,V0,m,hbar,
              xlim = [-100,100],
              klim = [-5,5])
    
    dt = 0.01
    N_steps = 50
    t_max = 120
    pylab.subplot(211)
    T = pylab.title("t = %.2f" % S.t)
    while S.t < t_max:
        S.time_step(dt,N_steps)
        T.set_text("t = %.2f" % S.t)
        update_plot(S)
    
if __name__ == '__main__':
    pylab.ion()
    animate()
    pylab.show()