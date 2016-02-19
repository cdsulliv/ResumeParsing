"""
This script reads headings from xml files and writes them to a text file

"""

__author__ = "Shreya Pandey"

from utilities import getFiles 
from splitting_xml import ParseText 

def writeHeadings():
    f = open("all_headings_other_without.txt", 'w')
    fileset = getFiles("/home/shreya/Wharton/NEW/Other/ONLY_XML")
    for filepath in fileset:
        index = filepath.index(".") 
        if "xml" in filepath[index:]:
            print filepath
            pt = ParseText(filepath)
            content = pt.readXmlToString()
            #print content
            content_list = pt.readTextToList()     
            heading_indexes, headings = pt.findHeadings(content, content_list, [])
            #print headings
            for heading in headings:
                f.write(heading.encode('ascii', 'ignore') + "\n")
            

    f.close()
                

if __name__ == "__main__":
    writeHeadings()