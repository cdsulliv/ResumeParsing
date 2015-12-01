import csv
import numpy as np
import ast 

def readHeadings(filename=''):
	HEADS =[]
	with open(filename, 'rb') as csvfile:
	     csvreader = csv.reader(csvfile, delimiter=',')
	     for row in csvreader:
	     	 #print row[2]	
	         headings = ast.literal_eval(row[2])
	         #print headings
	         HEADS.append(headings)
	#print HEADS
	#HEADS = np.array(HEADS)
	#HEADS = HEADS.ravel()
	#print HEADS
	HEADS = sum(HEADS, [])
	print HEADS
	'''heads = [x.lower() for x in HEADS]
	print set(heads)
	return set(heads)
	'''

def writeHeadings(headings=[]):
	f = open("headings.txt", "w")
	for heading in headings:
		f.write(heading + "\n")
	f.close()
	

def controller(filename=''):
	headings = readHeadings(filename)
	writeHeadings(headings)

if __name__ == "__main__":
	filename = "bio.csv"
	controller(filename)