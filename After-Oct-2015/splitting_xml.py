"""
This script splits the xml version of resume into major categories

"""

__author__ = "Shreya Pandey"

import re
from bs4 import BeautifulSoup
from utilities import getFiles 
import csv

HEAD_PATTERN = "\S[A-Z \d]+$"
PROBABLE_HEADINGS = ["education", "objective", "experience", "work experience", "certifications", "organizations and activites"]

class ParseText(object):
    """docstring for ParseTextme"""
    def __init__(self, filepath=""):
        self.filepath = filepath

    def findHeadings(self, content):
        heading_indexes = []
        headings = []
        #print content
        soup = BeautifulSoup(content)
        bolds = soup.find_all('b')
        print "bolds: ", bolds
        for bold in bolds:
            #print "bold: ", bold
            line = bold.string
            #print "heading:", line 
            #print "heading3:", line
            if line:
                heading = re.match(HEAD_PATTERN, line)
                 
                if heading:
                    print "heading1: ", line
                    #print "bold:", bold
                    headings.append(line)
                    start_index = content.index(str(bold))
                    heading_indexes.append(start_index)
                
                #print "!!!", line.strip()
                prob_head = line.strip().lower() 
                if prob_head in PROBABLE_HEADINGS and line not in headings:
                    print "heading2: ", line
                    headings.append(line)
                    start_index = content.index(str(bold))
                    heading_indexes.append(start_index)
                                      
        return heading_indexes, headings
    
    def find_bio(self, content):
        heading_indexes, headings = self.findHeadings(content)
        if heading_indexes:
            end_bio_ind = min(heading_indexes)
            return content[:end_bio_ind], headings
        return None, headings    

    def readFile(self):
        out = file(self.filepath, "r").read()            
        return out

    def writeToCsv(self, filename=""):
        with open (filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, dialect='excel')
            csvwriter.writerow(['bio'])
    

if __name__ == "__main__":
    fileset = getFiles("/home/shreya/Wharton/XML")
    with open ("split.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['filename', 'bio', 'headings'])
        for filepath in fileset:
            index = filepath.index(".") 
            if "xml" in filepath[index:]:
                print filepath
                row = []
                last_index =filepath.rfind("/")+1
                filename = filepath[last_index:]
                pt = ParseText(filepath)
                content = pt.readFile()     
                bio, headings = pt.find_bio(content)
                print bio, headings
                if bio:
                    row.append(filename)
                    row.append(bio)
                    row.append(headings)
                else:
                    row.append(filename)
                    row.append("NOT FOUND")
                    row.append(headings)
                    
                csvwriter.writerow(row)

    '''filepath = "/home/shreya/Wharton/1.xml"
    pt = ParseText(filepath)
    content = pt.readFile()     
    #pt.findHeadings(content) 
    print pt.find_bio(content)
    #print "a"
    '''