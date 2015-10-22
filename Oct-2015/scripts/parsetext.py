import re

HEAD_PATTERN = "\W"

class ParseText(self):
	"""docstring for ParseTextme"""
	def __init__(self, filepath):
		self.filepath = filepath
		

	def readText(self):
		file = open(filepath, 'r')
		lines = f.readline()
		return lines

	def parseWorkExp(self, lines=[]):
		heading_indexes = findHeadings(lines)

		for line in lines:
			if "EXPERIENCE" in line:
				start_index = lines.index(line)
				for index in heading_indexes:
					if index > start_index:
						next_index = index
						break
					else:
						next_index = length(lines)-1	

			else:
				return None

		work_exp = lines[start_index+1: next_index]		
		
		position_indexes = []
		for line in work_exp:
			if "\n\n" not in line:
				position = line			
				its_index = lines.index(line)	
				position_indexes.append(its_index) 
			else:
				next_position_index = work_exp.index(line)
				work_exp = work_exp[next_position_index+1:]	

		return position_indexes
				
	def findHeadings(self, lines=[]):
		heading_indexes = []
		
		for line in lines:
			heading = re.match(HEAD_PATTERN, line)
			if heading:
				indexOfHead = lines.index(line)
				heading_indexes.append(indexOfHead)
		
		return heading_index		


	def writeParsedWorkExp(self, all_lines=[], role_indexes = []):

		for index in range(length(role_indexes)-1):
			role_index = role_indexes[index]
			if (index+1) <length(role_indexes):
				next_role = role_indexes[index+1]
			else:
				continue	
			
			responsibilities = all_lines[role_index: next_role]


	def Controller(filepath=''):
		all_lines = readText(filepath='')
		role_indexes= parseWorkExp(lines)
		writeParsedWorkExp(all_lines, role_indexes)


def getAllFiles(directory_path=''):



if __name__ == "__main__":

			