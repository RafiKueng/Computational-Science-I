# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex08: Halton sequence
-------------------------------------------------------------------------------
Explanation:
    halton sequence produces quasi random numbers
    
    compared to pseudo rng, these are more evenly distributed
    and some problems arise with higher primes, ex. 17, 19:
    the first 16 points have perfect linear correlation...
    
    
    
    
    
How this code works:
    to produce N q-rand-nr:
    - select a prime base p
    - for each int(i) in range(N)
        - rewrite in base p
        - reoder the digits (abcdef. -> .fedcba)
        - convert this nr back to dec.sys
    
    

Notes / Convention:



-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-18   basic implementation
    v2 2012-01-09   added real random nr
 
BUGS / TODO:



LICENSE:
    none
    
-------------------------------------------------------------------------------
"""

from os import sys
from numpy import *
import matplotlib as mp
import pylab as pl
from random import random


def halton(index, base):
    result = 0
    f = 1 / float(base)
    i = index
    while (int(i) > 0):
        #print i
        digit = i%base        
        result = result + f * digit    
        i = i / base
        f = f / base
    return result


def main():
    N=1000
    print 'Input base 1:'
    base1 = input()
    print 'input base 2:'
    base2 = input()
    
    halt_x = [halton(x,base1) for x in range(N)] 
    halt_y = [halton(x,base2) for x in range(N)]
    
    rand_x = [random() for _ in range(N)]
    rand_y = [random() for _ in range(N)]
    
    pl.subplot(221)
    pl.plot(halt_x,halt_y,'rx')
    #pl.plot(halt_x[0:512],halt_y[0:512],'rx')
    pl.plot(rand_x,rand_y,'gx')
    pl.title("Halton (quasi)[red] vs. Pseudo[green] Random numbers\n(use red/gren 3d glasses :) )")

    pl.subplot(223)
    pl.plot(halt_x,halt_y,'rx')
    pl.title("Halton Numbers / Quasi Random")
    
    pl.subplot(224)
    pl.plot(rand_x,rand_y,'gx')
    pl.title("Pseudo Random Nr")
    
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
    print 'call main()'
    

        
if __name__ == '__main__':
    sys.exit(cmdmain(*sys.argv))
else:
    classmain()