"""
This script reads headings from xml files and writes them to a text file

"""

__author__ = "Shreya Pandey"

from utilities import getFiles 
from splitting_xml import ParseText 

def writeHeadings():
    f = open("all_headings.txt", 'w')
    fileset = getFiles("/home/shreya/Wharton/XML")
    for filepath in fileset:
        index = filepath.index(".") 
        if "xml" in filepath[index:]:
            print filepath
            pt = ParseText(filepath)
            content = pt.readFile()     
            heading_indexes, headings = pt.findHeadings(content)
            for heading in headings:
                f.write(heading.encode('ascii', 'ignore') + "\n")
    

    f.close()
                

if __name__ == "__main__":
    writeHeadings()