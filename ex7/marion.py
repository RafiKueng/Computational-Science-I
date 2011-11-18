"""Lorenz2.py week 7
 
This program greates a screen saver using Tkinter, plotting the lorenz atteraktor
"""
__author__ = "Marion Baumgartner (marion.baumgartner@uzh.ch)"
__date__ = "$Date: 10/11/2011 $"
 
from numpy import sqrt, linspace
from scipy.integrate import odeint
from pylab import plot, axis, show
from Tkinter import * 
from Canvas import *
from matplotlib import *
import random
#define global constants: sigma:scaled velocity; r: scaled temperature; b: geometric factor.
sigma=10.
r=28.
b=8./3.
#N=50000 #Number of Ponints
 
# The derivative function.
def f(w,t):
    x,y,z=w
    """ Compute the derivate of 'z' at time 't'.
        'z' is a list of four elements.
        @param w list conainig the real values for the cooardinates x, y and z
        @param t time at whih the equationo is evaluated
    """
    global sigma, r, b
    return [-sigma*x+sigma*y, (r-z)*x-y-x*z, y*x-b*z]
# Compute the ODE
 
def ode(ht,wd,scale,color,init):
    """calculation of the ODE and plotting the result on the TK canvase
    @param ht hight of the of the screen
    @param wd with of the screen
    @param scale scale factor, scales the plot
    @param color determines the colore to draw the graph
    @param init initial condition"""
 
    #determine the evaluation times   
    time=linspace(0.0,30.0, 3000)
    #solve the ODE
    res = odeint(f, init, time)
    #plot the result on Tkinter
    for i in range(len(res)-1):
        x0,y0,z0=res[i]
        x1,y1,z1=res[i+1]
        #create an offset and scale the points
        x0=x0*scale+wd/2
        y0=y0*scale+ht/2
        x1=x1*scale+wd/2
        y1=y1*scale+ht/2
        canv.create_line(x0, y0, x1, y1,fill=color)
        canv.update()
 
def screenSave(wd,ht):
    """Create a screen saver
    @param wd with oth the screen
    @param ht height of the screen
    """
    col=["red","green","blue","brown","gold","maroon"]
    while(1):
        #loop until colosed
        for i in range(len(col)):
            #plot the solution of the lorenz atractor using different colores,scaling factors and initial conditions
            canv.delete(ALL)
            #generate random initial conditionas and random scaling sizes
            scale=random.uniform(5.,25.)
            x0=random.uniform(-10,10)
            y0=random.uniform(-10,10)
            z0=random.uniform(-10,10)
            init=[x0,y0,z0]
            ode(ht,wd,scale,col[i],init)
"""def exit(event):
    global canv
    canv.quit()
   """ 
screen = Tk()
wd= screen.winfo_screenwidth()
ht=screen.winfo_screenheight()
screen.geometry("%dx%d+0+0"%(wd, ht))
canv = Canvas(screen, height = ht, width = wd, background ="black")
 
canv.pack()
screenSave(wd,ht)
 
#screen.mainloop()