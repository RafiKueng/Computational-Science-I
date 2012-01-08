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


class markov(object):
    """
    Markov
    """

    def __init__(self, a, b):
        self.a = a
        self.b = b
        
        self.p = lambda x: b / (x*x-2*a*x+a*a+b*b) / (arctan((1-a)/b)-arctan((-1-a)/b))  


        
    def __call__(self):
        pass                
        
    def prob(self,a,b,x):
        #print a, b, x
        dphi = b/(x*x-2*a*x+a*a+b*b)
        a1 = arctan((1.-a)/b)
        a2 = arctan((-1.-a)/b)

        #print '   ',x, dphi, a1, a2, dphi / (a1-a2)
        return dphi / (a1-a2)
        
    def set_prob(self,a,b):
        p = 1
        for x in self.data_set:
            p *= self.prob(a,b,x)
        print p
        return p
        
    def generate_sequence(self, n_num):
        """
        """
        data_set = []
        self.p_joint = 1
        
        n = 0
        while n<n_num:
            phi = rnd.uniform(-1, 1)
            x = self.a + self.b * tan(phi)
            
            if abs(x) <= 1:
                n += 1
                data_set.append(x)
                self.p_joint *= self.p(x)
            
        self.data_set = data_set
        self.p_joint /= n
        
            
    def recover(self):
        """
        Tries to recover the parameters a sand b from the dataset
        using the Metropolis algorythm
        """

        
        a = 1
        b = 1
        pars = [[a,b]] #init a, b
        sp = self.set_prob(a,b)
        
        i = 0
        while True:
            i += 1    
            beta = rnd.random()*2*pi
            da, db = (cos(beta), sin(beta))
            
            sp_new = self.set_prob(a+da,b+db)

            if i>1000 and sp < sp_new:
                break            
            
            #print 'i:%4.0f a:%5.2f, da:%5.2f, b:%5.2f, db:%5.2f, sp:%5.4f, sp_new:%5.4f' %(i, a, da, b, db, sp, sp_new)
            if rnd.random() < sp_new/sp:
                a+=da
                b+=db
                pars.append([a,b])
                sp = sp_new
                print ' >> ',pars[-1]
                
            
            
        
        
 
        

def main():
    m = markov(-.5, .7)
    m.generate_sequence(100)
    m.recover()
   
    
    
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