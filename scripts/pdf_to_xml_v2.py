import os
from utilities import getFiles

def pdfToXML(inputfilepath="", outdir=""):
	file_name_last_index = inputfilepath.rfind(".")
	file_name_first_index = inputfilepath.rfind("/")
	filename = inputfilepath[file_name_first_index: file_name_last_index]
	print filename
	#print outdir
	command =  "pdftohtml -xml" + " " + inputfilepath.replace(' ', '\ ') + " " + outdir + filename.replace(' ', '\ ')+".xml"
	#print command
	os.system(command)


def convertAll(dirpath="", outdir=""):
	filepaths = getFiles(dirpath)
	for filepath in filepaths:
		print filepath
		if filepath[-4:] == ".pdf":
			pdfToXML(filepath, outdir)

if __name__ == "__main__":
	#filepath = "/home/shreya/Wharton/1.pdf"
	#pdfToXML(filepath)

	dirpath = "/home/shreya/Wharton/NEW/NEW_PDF"
	outdir = "/home/shreya/Wharton/NEW/NEW_XML"
	convertAll(dirpath, outdir)