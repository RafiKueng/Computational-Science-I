'''
Calculates pi with machin's formula
input:
		n=3:	number of 3er sets of digis after komma; n=2 ==> [3][141][593]
return:
		pi: pi
--------------------------------------------------------------------------
Machines Formula:
pi / 4 = 4 * arctan(1/5) - arctan(1/239)

--------------------------------------------------------------------------
Rafael Kueng
v1-2011.09.29-00:10 basic calculation
v2-2011.09.29-20.05 finished extension for arbitrary many digits, int mode

BUGS / TODO:
- there are overflows occuring at line 155 for to many digitgroups (~>20)
- check in div whether rounding is accurate...
--------------------------------------------------------------------------
'''

from numpy import *


def machin():
    # the main program part

    # init arrays
    atan5 = array(zeros(ndigitp+1), dtype=int32) #set up result list, n entries containing each base digits
    atan239 = array(zeros(ndigitp+1), dtype=int32) #least significant digits first,
                #+1 for de non decimal 3 of pi
    
    #get the atangenses
    atan5 = atan(atan5,5)
    atan239 = atan(atan239,239)
    
    # put them together
    mult(atan5,16)
    if debug_p: print 'arctan5*16', atan5[::-1]
    mult(atan239,4)
    if debug_p: print 'arctan239*4', atan239[::-1]
    sub(atan5,atan239) #sub atan239 to atan5
    
    if debug_p: atan5[::-1]
    
    return atan5[::-1] #return result, most significant first (reoder from last to first)

    

def atan(arr, arg):
    if debug_t: print '\n---------------------------------\nStarting atang calc'
    if debug_t: print 'got array', arr[::-1], 'and arg', arg
    
    # calcs the arctan(arg)
    sum = array(zeros(ndigitp+1), dtype=int32)
    part = array(zeros(ndigitp+1), dtype=int32)
    
    if debug_t: print 'after init'
    if debug_t: print '	sum',sum[::-1],'\n	part',part[::-1]
    
    # 1st step, 1/x
    part[ndigitp-1] = 1*base # set unity
    part = div(part,arg)
    sum = add(part, sum) #use built in add function, we're sure there'll be no overflow
    
    if debug_t: print 'after 1st step'
    if debug_t: print '	sum',sum[::-1],'\n	part',part[::-1]
    
    vfactor = 1 # vorfactor (kind of loop counter)
    c_debug = 0 #debug counter
    while vfactor<1000: #loop forever
        c_debug +=1
        if debug_t: print '\n--------------------\nafter step',c_debug,' - beginning of loop'
        if debug_t: print '	sum',sum[::-1],'\n	part',part[::-1],'\n		addit. data:', vfactor, arg

        mult(part,vfactor) # multiply with old vorfactor
        if debug_t: print 'after step',c_debug,' - after multi with',vfactor
        if debug_t: print '	sum ',sum[::-1],'\n	part',part[::-1],'\n		addit. data:', vfactor, arg

        vfactor += 2
        div(part,arg*arg*vfactor)
        if debug_t: print 'after step',c_debug,' - after div by', arg*arg*vfactor
        if debug_t: print '	sum ',sum[::-1],'\n						part',part[::-1],'\n		addit. data:', vfactor, arg
        if debug_t: print '		part.sum',part.sum(),'sign',(((vfactor-1)/2)%2) * (-2) +1, '(', ((vfactor-1)/2)%2,')\n'

        if part.sum()==0: # check if part of sum is below resolution
            if debug_t: print 'after step',c_debug,' - BREAK - due reached prec.'
            if debug_t: print '	sum',sum[::-1],'\n	part',part[::-1],'\n		addit. data:', vfactor, arg
            break
        if ((vfactor-1)/2)%2 == 0: # vorfaktor ist 1, 5, 9, ...
            if debug_t: print 'after step',c_debug,' - summing part to sum'
            if debug_t: print '	befor: sum',sum[::-1],'\n	      part',part[::-1]
            add1(sum, part) # add part to sum
            if debug_t: print '	after: sum',sum[::-1],'\n	      part',part[::-1],'\n		addit. data:', vfactor, arg
        else: # vorfaktor ist 3, 7, 11, ...
            if debug_t: print 'after step',c_debug,' - substracting part from sum'
            if debug_t: print '	befor: sum',sum[::-1],'\n	      part',part[::-1]
            sub(sum, part) #substract part from sum
            if debug_t: print '	after: sum',sum[::-1],'\n	      part',part[::-1],'\n		addit. data:', vfactor, arg
        
    if debug_t: print '\n'
    if debug_t: print 'END - after',c_debug,'steps, returning'
    if debug_t: print '	sum',sum[::-1],'\n	part',part[::-1],'\n		addit. data:', vfactor, arg
    if debug_t: print '\n'
        
    return sum	

def add1(sum,arr):
    # defines the addition for the list, adds arr to sum (no return value)
    if debug_a: print '\n	/-------- summing arr to sum ----'
    if debug_a: print '	| init: sum',sum[::-1],'\n	|	arr',arr[::-1],'\n	|'

    carry = 0;
    
    for i in range(ndigitp+1): #go thou all array elements, starting with the less significant
        if debug_a_il: print '	|	loop iter',i
        if debug_a_il: print '	|		start	: arr', arr[i],'sum',sum[i],'c:', carry, 'b', base
        sum[i] = sum[i] + arr[i] + carry# 
        carry = sum[i] // base #
        sum[i] = sum[i] % base # 
        if debug_a_il: print '	|		end	: arr', arr[i],'sum',sum[i],'carry', carry,'b', base
    
    if debug_a: print '	|	\n	| end: sum',sum[::-1],'\n	|	arr',arr[::-1]
    if debug_a: print '	\\--------- END SUM ----------\n'
    return 1

def sub(sum,arr):
    # substracts arr from sum (no return value)
    # TODO suffers from severe rounding errors - Sure?

    if debug_s: print '\n	/-------- substracting arr from sum ----'
    if debug_s: print '	| init: sum',sum[::-1],'\n	|	arr',arr[::-1],'\n	|'

    carry = 0;
    
    for i in range(ndigitp+1): #go thou all array elements, starting with the less significant
        if debug_s_il: print '	|	loop iter',i
        if debug_s_il: print '	|		start	: arr', arr[i],'sum',sum[i],'c:', carry, 'b', base
        sum[i] = sum[i] - carry - arr[i] + base
        carry = 1 - sum[i]//base
        sum[i] = sum[i] % base
        if debug_s_il: print '	|		end	: arr', arr[i],'sum',sum[i],'carry', carry,'b', base

    if debug_s: print '	|	\n	| end: sum',sum[::-1],'\n	|	arr',arr[::-1]
    if debug_s: print '	\\--------- END SUBSTR ----------\n'
    return 1

def div(arr,divisor):
    # defines the division for the list
    # TODO suffers from severe rounding errors!! This one really does
    if debug_d: print '\n	/-------- division of arr by divisor ----'
    if debug_d: print '	| array', arr[::-1], '\n	| with divisor:', divisor,'\n	|'
    
    #init
    carry = 0;

    for i in reversed(range(ndigitp+1)): #go thou all array elements, starting with the most significant
        if debug_d_il: print '	|	loop iter:', i
        if debug_d_il: print '	|	start: arr[i]', arr[i],'c', carry,'d',divisor,'b',base
        
        arr[i] += carry * base # add the left over from previous div to next lower valued group
        carry = arr[i] % divisor #get the left over
        arr[i] = arr[i] // divisor # do the div, ADD INTELIIGENTER ROUNDING HANDLING
        
        if debug_d_il: print '	|	end: arr[i]', arr[i],'c', carry,'d',divisor,'b',base
        
    if debug_d: print '	|	\n	| end: res.arr:',arr[::-1]
    if debug_d: print '	\\--------- END DIV ----------\n'
        
    return arr

    
def mult(arr,multi):
    # defines the division for the list
    # TODO suffers from severe rounding errors... DOES IT??? no?

    if debug_m: print '\n	/-------- multipl of arr with multi ----'
    if debug_m: print '	| array', arr[::-1], '\n	| with multi:', multi,'\n	|'

    #init
    carry = 0;
    
    #main loop
    for i in range(ndigitp+1): #go thou all array elements, starting with the most insignificant

        if debug_m_il: print '	|	loop iter:', i
        if debug_m_il: print '	|	start: arr[i]', arr[i],'c', carry,'m',multi,'b',base

        arr[i] = arr[i] * multi + carry
        carry = arr[i] // base 
        arr[i] = arr[i] - carry*base # 

        if debug_m_il: print '	|	end: arr[i]', arr[i],'c', carry,'m',multi,'b',base

    if debug_m: print '	|	\n	| end: res.arr:',arr[::-1]
    if debug_m: print '	\\--------- END MULTI ----------\n'

    return arr
    
#debug settings
debug_a = False # print what add1 does
debug_a_il = False # print what add1 does in inner loop
debug_s = False # print what sub does
debug_s_il = False # print what sub does in inner loop
debug_m = False # print what mult does
debug_m_il = False # print what mult does in inner loop
debug_d = True # print what div does
debug_d_il = True # print what div does in inner loop
debug_t = False # print what tan does
debug_p = False # print what main/machin does


# init const / settings
ndigitperp = 3 # each digitpacket in the result list has ndigitperp digits 
ndigitp = 20 	# number of digitpackets, each with ndigitperp digits
                            #(ndigitperp*ndigitp = tot number of digits)
base = 10**ndigitperp #base for each packet

pi = machin()

print '\n\nResultat:'
print pi