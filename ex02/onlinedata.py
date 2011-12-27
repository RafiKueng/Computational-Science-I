# basic html parser, prepared to get all tables and put in in list structres

from HTMLParser import HTMLParser
from urllib2 import urlopen
from pylab import bar, xlabel, ylabel, show

class table:
	rows = list()
	
	def addRow(self, ele):
		self.rows.append(ele)
		


# uses a stack, every time a starting tabletag is found, put its coordinates onto
class getTables(HTMLParser):
	tables = list()
	tablestack = list()
	currTable = list()
	currRow = list()
	currData = ''
	lookFor = ''
	interestingTables = list()
	colspan =1
	rowspan = list()
	lastrowspan = list()

	def __init__(self, data, str):
		HTMLParser.__init__(self)
		self.lookFor = str
		self.feed(data)
		
	def handle_starttag(self, tag, attrs):
		if tag == 'table':
			#print "found table start at pos:", self.getpos()[1]
			self.tablestack.append(self.currTable)
			self.currTable = list()
			
		if tag == 'tr':
			#print 'row'
			self.lastrowspan = self.rowspan
			self.rowspan = list()
			self.currRow = list()
			
		if tag == 'td':
			#print 'col'
			self.currData = ''
			if attrs and attrs[0][0]=='colspan': #quick and dirty, only checks if this atrribute is in first place...
				self.colspan = int(attrs[0][1])
			else:
				self.colspan = 1
			if attrs and attrs[0][0]=='rowspan': #can't handle more than two
				self.rowspan.append(len(self.currRow))# int(attrs[0][1])

				
	def handle_endtag(self, tag):
		if tag == 'table':
			#print "found table end at pos:", self.getpos()[1]
			self.tables.append(self.currTable)
			self.currTable = self.tablestack.pop()

		if tag == 'tr':
			#print 'row'
			while self.lastrowspan:
					self.currRow.insert(self.lastrowspan.pop(0),'')
			self.currTable.append(self.currRow)
			
			
		if tag == 'td':
			#print 'col'
			while self.colspan>=1:
				self.currRow.append(self.currData.strip(' '))
				self.colspan-=1
			
			
			
	def handle_data(self, data):
		self.currData = ''.join([self.currData,data])
		#if data!=[]:
		#	print '||', data, '||', self.getpos()[1]
			
		if data == self.lookFor:
			#print 'found keyword', self.lookFor, 'at pos', self.getpos(),'in table', len(self.tables), len(self.tablestack)
			self.interestingTables.append(len(self.tables))


			
		
		
#does what it says
def removeLinefeed(str):
	str = str.replace('<br>', ' ')
	return str.replace('\n',' ')
		
def removeWhitespaces(str):
	str = str.strip(' ')
	pos = str.find('  ')
	if pos == -1:
		return str
	return ''.join([str[0:pos],' ', removeWhitespaces(str[pos+2:])])
		
		
		
# main
		
data = urlopen('http://worldweather.wmo.int/087/c00312.htm')
src_string = data.read()
#src_string = 'this is  a   test	.	bla'

# remove linefeeds, tabs and multiples spaces
src_string = removeLinefeed(src_string)
src_string = src_string.expandtabs(1)
src_string = removeWhitespaces(src_string)

a = getTables(src_string, 'Month')

tab = a.tables[a.interestingTables[0]]

#print tab

for i in range(4):
	tmp = list()
	for j in range(12):
		tmp.append(float(tab[j+2][i+1]))
	bar(range(12), tmp, width = 1)
	xlabel("Month number")
	if tab[1][i+1]:
		str = ''.join([tab[0][i+1],' / ',tab[1][i+1]])
	else:
		str = tab[0][i+1]
	ylabel(str)
	show()