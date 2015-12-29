import os

def getFiles(directory=""):
	fileset = []
	for path, dirs, files in os.walk(directory):
		for f in files:
			filepath = os.path.join(directory, f)
			fileset.append(filepath)
	return fileset            