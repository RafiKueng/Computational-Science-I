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

    def __init__(self, N1, N2, n_tries, n_bins):
        self.N1 = N1
        self.N2 = N2
        self.n_tries = n_tries
        self.n_bins = n_bins
        gcd_ = gcd(N1, N2)
        self.steplength1 = N2/gcd_ #1. / (1.*N1) * (N1+N2)
        self.steplength2 = -N1/gcd_ #-1. / (1.*N2) * (N1+N2)
        
        
        
    def __call__(self):
        self.nWalks()
        
        bins = linspace(0,1,self.n_bins)
        prob_histo = array(histogram(self.maxdist)[0]) / (1.*self.n_tries)

        print bins
        print prob_histo
        
        pl.bar(bins, prob_histo)
        pl.show()
        
        #self.genHistogram()
        #self.plot()
        
        
        
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
        print '\n nWalk maxdist', self.maxdist
        
    def genHistogram(self):
        max_dist = max(self.result_dist)
        max_element = max( [max(self.result_element[i]) for i in range(self.dim)] )#total max in all dimensions
        n_events = len(self.result_dist)*1.0
            
            
        #print max_dist, self.n_bins
        
        if self.grid_with == None:
            dist_bin, dist_d_bin = linspace(0, max_dist, self.n_bins, retstep=True)
            element_bin, element_d_bin = linspace(-max_element, max_element, self.n_bins, retstep=True)
        else:
            # this part still has some bugs
            offset = (self.n_steps%2)/2.
            element_d_bin = dist_d_bin = self.grid_with*2
            dist_bin = arange(0, dist_d_bin*(self.n_steps+1), dist_d_bin) - (0.5+offset)*dist_d_bin
            
            element_bin  = arange(-self.grid_with*(self.n_steps),
                                    self.grid_with*(self.n_steps+2+(0.5-offset)),
                                    element_d_bin) - (0.5+offset)*element_d_bin
       
        
        
        dist_hist = histogram(self.result_dist, dist_bin)[0] / n_events
        
        element_hist = [[] for i in range(self.dim)]
        for i in range(self.dim):
            element_hist[i] = histogram(self.result_element[i], element_bin)[0] / n_events 


        print element_d_bin
        print '\n'
        print element_bin
        print '\n'        
        #print element_hist[0]
        #print '\n'   

        
        self.dist_bin = dist_bin
        self.dist_d_bin = dist_d_bin
        self.dist_hist = dist_hist
        
        self.element_bin = element_bin
        self.element_d_bin = element_d_bin
        self.element_hist = element_hist
        
        
    def plot(self, plot_distr = True):
        """
        plots the results
        plot_distr = True plots the theoretical results with a red line..
        """
        #print 'plot:', self.dist_bin[:-1],self.dist_hist
        
        pl.figure()
        pl.subplot(self.dim+1,1,1)
        pl.bar(self.dist_bin[:-1],self.dist_hist, width=self.dist_d_bin)
        
        if plot_distr:
            distrange = linspace(self.dist_bin[0], self.dist_bin[-1], 1000)
            elementrange = linspace(self.element_bin[0], self.element_bin[-1], 1000)
            
            maxwell = 2*distrange/float(self.n_steps)*exp(-distrange**2/float(self.n_steps))
            gauss = 1/(pi*self.n_steps)*exp(-elementrange**2/float(self.n_steps))
            
            pl.plot(distrange, maxwell, 'r:')
            
        
        for i in range(self.dim):
            pl.subplot(self.dim+1,1,i+2)
            pl.bar(self.element_bin[:-1],self.element_hist[i], width=self.element_d_bin)
            pl.xlim(self.element_bin[0], self.element_bin[-1])
            
            if plot_distr:
                pl.plot(elementrange, gauss, 'r:')

        pl.show()
            
        

def main():

    N1 = 24
    N2 = 36
    n_tries = 3
    n_bins = 10

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