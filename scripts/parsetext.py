import re
import csv

HEAD_PATTERN = "\S[A-Z \d]+$"
#"^[A-Z \d\W]+$

class ParseText(object):
	"""docstring for ParseTextme"""
	def __init__(self, filepath):
		self.filepath = filepath
		

	def readText(self):
		f = open(self.filepath, 'r')
		lines = f.readlines()
		#print lines
		return lines

	def parseWorkExp(self, lines=[]):
		heading_indexes= self.findHeadings(lines)
		print "heading_indexes ", heading_indexes
		
		headings = []
		#position_indexes = []
		work_exps = []

		for line in lines:
			#print "line: ", line 
			if "EXPERIENCE" in line:
				print "EXPERIENCE: ", line 
				headings.append(line)
				start_index = lines.index(line)
				print "start_index: ", start_index
				for index in heading_indexes:
					print "there are indexes in heading_indexes"
					if index > start_index:
						next_index = index
						print "if next_index: ", next_index
						break
					else:
						next_index = len(lines)-1	
						print "else next_index: ", next_index

			else:
				continue

			print "next_index: ", next_index	
			work_exp = lines[start_index+1: next_index]		
			#print work_exp
			#break
			work_exps.append(work_exp)
			'''for line in work_exp:
				if "\n\n" not in line:
					position = line			
					its_index = lines.index(line)	
					position_indexes.append(its_index) 
				else:
					next_position_index = work_exp.index(line)
					work_exp = work_exp[next_position_index+1:]	
			'''		
		#return position_indexes
		print "headings", headings 
		self.writeParsedWorkExp(headings, work_exps)
		#return work_exps

	def findHeadings(self, lines=[]):
		heading_indexes = []
		#headings = []

		for line in lines:
			heading = re.match(HEAD_PATTERN, line)
			if heading:
				print "heading: ", line
				#headings.append(line)
				indexOfHead = lines.index(line)
				heading_indexes.append(indexOfHead)
			
		return heading_indexes


	'''def writeParsedWorkExp(self, all_lines=[], role_indexes = []):

		for index in range(len(role_indexes)-1):
			role_index = role_indexes[index]
			if (index+1) <len(role_indexes):
				next_role = role_indexes[index+1]
			else:
				continue	
			
			responsibilities = all_lines[role_index: next_role]
			#print responsibilities 
			#break
	'''
	
	def writeParsedWorkExp(self, headings=[], work_exps = []):
		with open ('work_exp.csv', 'w') as csvfile:
			csvwriter = csv.writer(csvfile, dialect='excel')
			csvwriter.writerow(['work_exp1', 'work_exp2', 'work_exp3', 'responsibilities1', 'responsibilities2', 'responsibilities3'])
			print len(headings)
			for i in range(len(headings)):
				print headings[i], headings[i+1], headings[i+2]
				csvwriter.writerow([headings[i], headings[i+1], headings[i+2], work_exps[i], work_exps[i+1], work_exps[i+2]])
				break
            
            

	def controller(self):
		all_lines = self.readText()
		#print "controller: ", all_lines
		role_indexes= self.parseWorkExp(all_lines)
		#print "role_indexes: ", role_indexes
		#self.writeParsedWorkExp(all_lines, role_indexes)

#def getAllFiles(directory_path=''):



if __name__ == "__main__":
	filepath = "/home/shreya/Wharton/PDF/Brown University 1.txt"
	pt = ParseText(filepath)
	pt.controller()
