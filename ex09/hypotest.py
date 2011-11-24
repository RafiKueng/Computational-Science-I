# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex09: Hypothesis Testing using random Walk
-------------------------------------------------------------------------------
Explanation:

    
    
How this code works:

    

Notes / Convention:



-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-24   basic implementation
 
BUGS / TODO:



LICENSE:
    none
    
-------------------------------------------------------------------------------
"""

from os import sys
from numpy import *
import matplotlib as mp
import pylab as pl
import random as rnd
from fractions import gcd


class hypothesistesting(object):
    """
    N1, N2 must be int!
    """

    def __init__(self, N1, N2, n_tries=10000, n_bins=100):
        self.N1 = N1
        self.N2 = N2
        self.n_tries = n_tries
        self.n_bins = n_bins
        #self.gcd = gcd(N1, N2)
        self.steplength1 = N2#/self.gcd #1. / (1.*N1) * (N1+N2)
        self.steplength2 = -N1#/self.gcd #-1. / (1.*N2) * (N1+N2)
        
        
        
    def __call__(self):
        self.nWalks()
        
        '''
        bins = linspace(0,0.2,self.n_bins)
        #bins = arange(0,1,self.gcd/(10.*self.N1*self.N2))
        d_bin = bins[1]-bins[0]
        prob_histo = array(histogram(self.maxdist, bins)[0]) / (1.*self.n_tries)

        #print bins
        #print prob_histo
        
        pl.bar(bins[:-1], prob_histo, d_bin)
        pl.show()
        '''
        
        #create the ks plot... do it complicated so we don't get any mess with
        #ill spaced bins...
        
        #sort the list that the smallest is at the end and start working on
        #the list from rear to front
        
       
        x_axis = []
        y_axis = []
        
        self.maxdist.sort(reverse = True)
        
        #print self.maxdist
        
        x_old = 0
        counter = 0
        while True:
            x_new = self.maxdist.pop()
            #print x_new, x_old, counter
            if x_new == x_old:
                counter += 1
            else:
                x_axis.append(x_old)
                y_axis.append(counter)
                counter += 1
                x_old = x_new
                #print ' >>', x_old, counter
            if len(self.maxdist)==0:
                x_axis.append(x_new)
                y_axis.append(counter)
                x_axis.append(1)
                y_axis.append(self.n_tries)
                
                break
                
        y_axis = array(y_axis)/(self.n_tries*1.)
        pl.plot(x_axis, y_axis, drawstyle='steps-post')

        #theoretical curve
        x2 = linspace(0,1,1000)
        y2 = zeros(1000)
        v=sqrt(self.N1*self.N2 / (1.*self.N1+self.N2))
        mu = v + 0.12 + 0.11/v
        for k in range(100):
            y2 += (-1)**k*exp(-2*(k+1)**2*mu**2*x2**2)
        y2 = 1-2*y2 
        pl.plot(x2,y2, 'r:')
        
        pl.show()
                
        
        
    def walk(self):
        """
        one walk
        """
        n1 = self.N1
        n2 = self.N2
        X = 0
        dist = 0
        
        while n1+n2 >0:
            if rnd.random()*(n1+n2)<n1:
                #a element from n1 has been chosen
                n1 -= 1
                X += self.steplength1
            else:
                n2 -= 1
                X += self.steplength2
            #print X, dist
            dist = max([dist, abs(X)])
            
        #print dist, dist / (1.*self.N1*self.N2)
        return dist / (1.*self.N1*self.N2)
            
            
    def nWalks(self):
        self.maxdist = []
        for i in range(self.n_tries):
            self.maxdist.append(self.walk())
        #print '\n nWalk maxdist', self.maxdist
        
 
        

def main():

    N1 = 24
    N2 = 36
    n_tries = 10000
    n_bins = 100

    # hypothesis testing

    rndwk1 = hypothesistesting(N1, N2, n_tries, n_bins)
    rndwk1()
    
    
    
def cmdmain(*args):
    try:
        main()
    except:
        raise
        # handle some exceptions
    else:
        return 0 # exit errorlessly     
        

def classmain():
    print 'call main()'
    

        
if __name__ == '__main__':
    sys.exit(cmdmain(*sys.argv))
else:
    classmain()