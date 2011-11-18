# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex08: Halton sequence
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



LICENSE:
    none
    
-------------------------------------------------------------------------------
"""

from os import sys
from numpy import *
import matplotlib as mp
import pylab as pl


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
    x = [halton(x,base1) for x in range(N)] 
    y = [halton(x,base2) for x in range(N)]

    pl.plot(x,y,'rx')
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