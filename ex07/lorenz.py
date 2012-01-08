"""
-------------------------------------------------------------------------------
 Lorenz attractor screen saver
-------------------------------------------------------------------------------
Explanation:
    PAY ATTENTION
    you will not be able to close the screensaver, once run..
    ...except with alt+f4 (tested only on win)
    for some reason the keybinds don't work...
    welll actually, the reason is the painting doesn't happen in
    the screen.mainloop(), but before. eventhandling (working on the event
    queue) only starts in the mainloop...
    
    ODE's
    X' = sigma*(Y - X)
    Y' = r*X - Y - XZ
    Z' = XY - b*Z

How this code works:
    

Notes / Convention:
    maybe it would be better, to do this event driven? use timer /
    alarmclock event... so the key bindings would actually work...
 
-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-10   basic implementation

BUGS / TODO:
    - alt f4 only way to kill the screensaver

LICENSE:
    none
-------------------------------------------------------------------------------
"""

# imports
import sys
from numpy import sin, cos, arange, array, matrix, pi
import pylab as pl
import scipy.integrate.odepack as oiL
from Tkinter import *
import random as rnd



class LorenzODE(object):
    def __init__(self, const, init, timing):
        """
        sigma, r, b = const
        t_start, t_end, dt = timing
        """

        self.s, self.r, self.b = const
        self.t_start , self.t_end, self.dt = timing
        
        self.t = self.t_start
        self.init = self.state = array(init, dtype = float)
    
    def derr(self, val, t):
        x, y, z = val
        return [self.s*(-x + y), (self.r-z)*x-y-x*z, y*x-self.b*z]

    def solve(self):
        return oiL.odeint(self.derr, self.init, arange(self.t_start, self.t_end, self.dt))
        
    def next_step(self):
        #print self.state, [self.t, self.t + self.dt]
        
        newstate = oiL.odeint(self.derr, self.state, [self.t, self.t + self.dt])

        self.state = newstate[1]
        self.t += self.dt
        finished = self.t >= self.t_end
            
        return [ self.state, finished ]
        




def main():
    screen = Tk()
    screen.overrideredirect(1) #dont draw the windowmanager stuff
    wd = screen.winfo_screenwidth()
    ht = screen.winfo_screenheight()
    screen.geometry("%dx%d+0+0"%(wd, ht))
    canv = Canvas(screen, height = ht, width = wd, background ="black")
    canv.focus_set() # <-- move focus to this widget
    #screen.bind("<<draw>>", draw)
    canv.bind("<Escape>", lambda e: e.widget.quit())
    canv.bind("<Button-1>", lambda e: e.widget.quit())
    canv.pack()
    
    const = [10.0, 28.0, 8/3.]
    
    rnd.seed(42) # so we are not really random... remove for real random pictrues :) but i wanted to be sure it looks good ;) 
    
    #mainloop, never ends, draws all the time
    while True:
        init = array([rnd.uniform(-15, 15) for x in range(3)])
        t_end = rnd.randint(20,40) * 1.0
        color = rnd.choice(["red","green","blue","brown","gold","orange",
            "maroon","magenta","orchid","RoyalBlue1","SkyBlue3","LightSkyBlue3",
            "PaleTurquoise1","DarkSeaGreen1","LightYellow4","chocolate1"])
        alpha, beta = array([rnd.random() for x in range(2)])*pi
        zoom = rnd.uniform(5., 50.)
        
        rotx = matrix([[ 1,0,0],
                       [0,cos(alpha),-sin(alpha)],
                       [0,sin(alpha),cos(alpha)]])
        rotz = matrix([[cos(beta),-sin(beta),0],
                       [sin(beta),cos(beta),0],
                       [ 0,0,1]])
        
        lorenz = LorenzODE(const,init, [0, t_end, 0.005])
        oldP = rotz*rotx*matrix(init).T
        oldSP = screenP(oldP, wd, ht, zoom) #back to array
        finished = False
        
        canv.delete(ALL)

        p0 = screenP(rotz*rotx*matrix(array([0.,0.,0.])).T, wd, ht, zoom) #origin
        px = screenP(rotz*rotx*matrix(array([1.,0.,0.])).T, wd, ht, zoom) #xaxis
        py = screenP(rotz*rotx*matrix(array([0.,1.,0.])).T, wd, ht, zoom) #yaxis
        pz = screenP(rotz*rotx*matrix(array([0.,0.,1.])).T, wd, ht, zoom) #zaxis
        
        for i, p in enumerate([px, py, pz]):
            canv.create_line(p0[0], p0[1], p[0], p[1], fill=["red","green","blue"][i])
        
        
        # mainloop for drawing one curve
        while not finished:
            newP, finished = lorenz.next_step()
            newSP = screenP((rotz*rotx*matrix(newP).T), wd, ht, zoom)
            #print oldSP, newSP
            canv.create_line(oldSP[0], oldSP[1], newSP[0], newSP[1], fill=color)
            canv.update()
            
            oldSP = newSP
            
            
    screen.mainloop()

        
def screenP(pnt, wd, ht, zoom):
    pnt = pnt.T.getA()[0] #get rid of nested lists, get a simple array
    #zoom the already rotated result and put it in the middle of the screen
    return array([pnt[0]*zoom+wd//2, pnt[1]*zoom+ht//2], dtype=int)
    




def cmdmain(*args):
    try:
        #print "Starting Program"
        main()
        #print "ending programm"
    except:
        raise
        # handle some exceptions
    else:
        return 0 # exit errorlessly     
        

def classmain():
    print 'screensaver function only workes, when called in commandline...'
    print 'you can however use the LorenyODE class, I\'ll show you how:'
    print """
    const = [10.0, 28.0, 8/3.]      # [sigma, b, r]
    init = array([rnd.uniform(-15, 15) for x in range(3)])   # x0, y0, z0
    timing = [0, 30, 0.005]         # t_start, t_end, delta_t
    
    lode = LorenzODE(const,init, timing)
    
    # get the solution with
    for i in arange(*timing):
        coord, done = lode.next_step()

    # or the "it's done when it's done" way
    done = False
    while not done:
        coord, done = lode.next_step()
        
    #or all in one    
    solution = lode.solve()
    """
    

        
if __name__ == '__main__':
    sys.exit(cmdmain(*sys.argv))
else:
    classmain()