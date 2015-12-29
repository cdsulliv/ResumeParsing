def writeSetHeadings():
	f_read = open("all_headings.txt", "r")
	lines = f_read.readlines()
	lower_lines = [line.lower() for line in lines ]
	set_lines = set(lower_lines)
	f_write = open("set_of_headings.txt", "w")
	for line in list(set_lines):
		f_write.write(line )

if __name__ == "__main__":
	writeSetHeadings()
