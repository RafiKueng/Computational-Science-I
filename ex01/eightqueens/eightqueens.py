#--------------------------------------------------------------------------
# Calculates all possible solutions of the eight queens problem
#--------------------------------------------------------------------------
# Explanation:
#   How do you have to arrange n queens on a n x n chessboard,
#   such that they can't attak each other.
#   How many independant, unique solutions exist?
#   (unique = one solution can't be converted to the other with rotations
#    and reflections)
#
# How this code works 
#  - creates all possible solutions (backtracking)
#    \-> stores the result in an array, where the queen in each row is
#  - converts this result to complex notation
#  - for each solution, create all possible refl, rots; look them up in 
#    the list of results and cancel them out
#
# Notes / Convention:
#   use for row, col, counters ect. logical numbers (1, 2, ..., dim)
#   shift these for access to arrays, lists ect. (eg. board[row-1][col-1])
#--------------------------------------------------------------------------
# Rafael Kueng
# v1-2011.09.29-23:10 uncomplete submitted version
# v2-2011.09.30-20:00 completed version with nice output 
# 
# BUGS / TODO:
# - non known
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# SETTINGS
#--------------------------------------------------------------------------

# print some staus reports
print_status = True # give some output at least
print_short_res = True # list the resulting unique configurations
print_pics = False # list the unique solutions and depict them
print_detailed_result = False # list all configurations (the non unique ones)


# simulation settings
dim = 8 #width of chess board
		# use dim > 1 !!! otherwise a dirty hack causes an index out of bound..
		# use dim < 12 for a runtime of a few minutes (and disable text/graphic output!)
queenNr = 3 # witch digit represents a queen
attakNr = 7 # witch digit represents a field under attak
		# empty fields use 0
		# DONT use the same for both, attakNr > queenNr


#debug settings
debug_rs = False # debug out of the recursivesolver
debug_rs_board = False #displays the placement of the queens (slow!!)
debug_sq = False # debug setqueen
debug_gs = False # debug genSolutions
debug_ge = False # debug genSimilar
debug_fl = False #debugging filterList

#--------------------------------------------------------------------------



#imports		
from numpy import *
import os #used for clear screen
import time #used for waiting a few secs

# public vars
oo = 0 # how many times the recsolver has been called
bt = 0 # counter for backtracks




def genSol():
	# generates all possible solutions, incl. simmilar
	
	if debug_gs: print 'in gensol'
	
	#init
	#iList = list(list([0] for i in range(dim))) # list of possible solutions
	iList = list() # list of possible solutions
	board = zeros([dim, dim], int)
	currSol = array(zeros(dim, int))
	
	# start the recursive magic
	recSolver(iList, board, 1, currSol)
	
	if debug_gs: print '------SOLUTIONS--------'
	if debug_gs: 
		for i in iList:
			print i
	if debug_gs: print 'found ', len(iList), 'solutions'

	return iList
	
def recSolver(iList, board, row, currSol):
	# recursive solver for the queen placement
	global oo
	global bt
	oo+=1
	if debug_rs: print 'in recsolver, ',oo,row,currSol
	
	# if at the end of the board, we found a solution
	if row > dim:
		iList.append(currSol.copy()) # add current to solutions
		if debug_rs: print 'found solution'
		if debug_rs: printBoard(board)
		return 1
	
	# small speed hack:
	# if all fields in the last or 2nd last row are under attak,
	# there's no need to continue tring to place queens
	if board[-1].sum()==dim*attakNr or board[-2].sum()==dim*attakNr:
		if debug_rs: print 'shortcut exit, one of last two rows totally under attak'
		bt+=1
		return 1
	
	for col in range(1,dim+1): #board[row-1]:
		if board[row-1][col-1]==attakNr: # this place is not possible / under attak
			continue
		else:
			if debug_rs: print 'else',row,col
			new_board = board.copy() #make a deep copy
			currSol[row-1]=col # save result
			setQueen(row,col, new_board)
			
			# output evolution of board
			if debug_rs_board:
				clearScreen()
				printBoard(new_board)
				time.sleep(0.2)
			
			recSolver(iList, new_board,row+1,currSol)
	
	return 1
	
def setQueen(row,col, board):
	# updates the board that a queen is set on row, col
	if debug_sq: print 'setting a queen at row', row, 'col', col 
	board[row-1][col-1]=queenNr #set the queen
	#mark row as attaked
	i = 0
	for crow in range(row,dim+1):
		#set straight line of attak
		if board[crow-1][col-1]==0:
			board[crow-1][col-1]=attakNr
		#set diagonals
		if col+i<=dim:
			if board[crow-1][col+i-1]==0:
				board[crow-1][col+i-1]=attakNr
		if col-i>=1:
			if board[crow-1][col-i-1]==0:
				board[crow-1][col-i-1]=attakNr
		i+=1
	return 1
	
def printBoard(board):
	#debug fn
	for row in board:
		print row
	
	return 1

def printIntSol(iElement):
	# prints a solution

	board = zeros([dim, dim], int)
	for i in range(dim):
		board[i][iElement[i]-1] = queenNr
	printBoard(board)	
	return 1
	
def clearScreen():
	if os.name == "posix":
		# Unix/Linux/MacOS/BSD/etc
		tmp=os.system('clear')
	elif os.name in ("nt", "dos", "ce"):
		# DOS/Windows
		tmp=os.system('CLS')
	return

def toComplexElement(iElement):
	# converts a int representation to complex representation
	#automaticly sorted for increasing real part
	cElement = list()
	k = int((dim/2.0+0.5)*2)

	for row in range(1,dim+1):
		cElement.append(complex((2*row-k), (2*iElement[row-1]-k)))
	return cElement

def toIntElement(cElement):
	#backwards for disply
	iElement = list()
	k = int((dim/2.0+0.5)*2)

	for row in range(1,dim+1):
		iElement.append(int((cElement[row-1].imag+dim+1)//2))
	return iElement
	
	
def toComplexList(iList):
	#converts a list with regular solutions to complex solutions 

	cList = list()
	
	for iElement in iList:
		cList.append(toComplexElement(iElement))
	
	return cList

	
def sortComplexList(cList):
	# sorts each element in a cList by real part
	for pos in range(len(cList)):
		cList[pos]=sorted(cList[pos], key=lambda x: x.real) 
	return 1
		
def genSimilar(cElement):
	# generates all simmilar representations
	
	if debug_ge: print 'generating similar solutions for solution\n',cElement
	
	cList = list()
	
	rot090 = list()
	rot180 = list()
	rot270 = list()
	reflRe = list()
	reflIm = list()
	reflD1 = list() #reflection on the x-y diagonal
	reflD2 = list() #reflection on the x-(-y) diagonal
	
	for e in cElement:
		rot090.append(e*1j)
		rot180.append(e*(-1))
		rot270.append(e*(-1j))
		reflRe.append(e.conjugate())
		reflIm.append((-1)*e.conjugate())
		reflD1.append(complex(e.imag, e.real))
		reflD2.append(complex(-1*e.imag, -1*e.real))
	
	if debug_ge: print 'result\n',rot090,'\n',rot180,'\n',rot270,'\n',reflRe,'\n',reflIm
	
	cList.append(cElement)
	cList.append(rot090)
	cList.append(rot180)
	cList.append(rot270)
	cList.append(reflRe)
	cList.append(reflIm)
	cList.append(reflD1)
	cList.append(reflD2)
	
	if debug_ge: print 'cList contains:'
	if debug_ge:
		for i in cList: print i
	
	sortComplexList(cList)

	if debug_ge: print 'cList after being sorted'
	if debug_ge:
		for i in cList: print i
	
	
	return cList
	
def isIn(cElement, cList):
	# returns the pos of cElement in cList, -1 if not found
	pos = -1
	
	for pos in range(len(cList)):
		cont = True
		for i in range(dim):
			if cElement[i] != cList[pos][i]:
				cont = False
				break
		if cont: return pos
			
	return -1
	
def filterList(cList):
	#filters out all similar elements from list

	newList = list()
	filter = ones(len(cList),bool) #filter mask, set everything to true
	
	for solNr in range(len(cList)):
		#short cut, if this sol is already filtered out, theres no need to check again
		if filter[solNr]==False:
			continue
		
		#get the current solution to check, and generate similar solutions
		simSolutions = genSimilar(cList[solNr])
		#check for each simsolution, whether its in the list...
		for simSol in simSolutions:
			pos = isIn(simSol, cList)
			#...if it is, mark it not to be copied later to the new list
			if pos > -1 and solNr != pos:
				filter[pos] = False
	
	#copying elements marked to copy to new list
	for solNr in range(len(filter)):
		if filter[solNr]:
			newList.append(cList[solNr])
	
	return newList

	
	
	
	
# ------------------------
#   main
# ------------------------

if print_status:
	clearScreen()
	print '\n 8 QUEENS PROBLEM'
	print '=================='
	print '					...solving it for a',dim,'x',dim,'field\n'
	print '--- S T A R T ------------------------------------------------------------\n'

if print_status: print ' creating all possible solutions...'
iList=genSol()
if print_status: print '								...DONE'

if print_status: print ' converting solutions to complex plane'
cList = toComplexList(iList)
if print_status: print '								...DONE'

if print_status: print ' filtering results for unique solutions...'
new_list=filterList(cList)
if print_status: print '								...DONE'
if print_status: print '\n--- E N D ----------------------------------------------------------------\n'


if print_detailed_result:
	print '\nListing all possible solutions\n---------------------------------'
	for i in cList:	print toIntElement(i)
print '\nFound', len(cList),'(non unique) solutions'

if print_short_res or print_pics:
	print '\nListing unique solutions...\n---------------------------------'
	for i in range(len(new_list)):
		if print_pics:
			print '\nSolution Nr', i+1, '\n',toIntElement(new_list[i])
			printIntSol(toIntElement(new_list[i]))
		else: print toIntElement(new_list[i])
print '\nFound', len(new_list), 'unique solutions'

print '\n	(Hint: enable detailed/graphic output in code to disply the result)'