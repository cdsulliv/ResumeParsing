"""
This script splits the xml version of resume into major categories

"""

__author__ = "Shreya Pandey"

import re
from bs4 import BeautifulSoup
from utilities import getFiles 
import csv

HEAD_PATTERN = "\S[A-Z \d / : ]+$" 
#PROBABLE_HEADINGS = ["education", "objective", "experience", "work experience", "certifications", "organizations and activites"]

def getAllHeadings(filename=""):
    f = open(filename, "r")
    lines = f.readlines()
    headings = [line.strip() for line in lines]
    return headings

class ParseText(object):
    """docstring for ParseTextme"""
    def __init__(self, filepath=""):
        self.filepath = filepath

    def findHeadings(self, content, PROBABLE_HEADINGS):
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
                '''heading = re.match(HEAD_PATTERN, line)
                 
                if heading and len(line) > 5:
                    print "heading1: ", line
                    #print "bold:", bold
                    headings.append(line)
                    start_index = content.index(str(bold))
                    heading_indexes.append(start_index)
                '''
                #print "!!!", line.strip()
                prob_head = line.strip().lower() 
                if prob_head in PROBABLE_HEADINGS and line not in headings:
                    print "heading2: ", line
                    headings.append(line)
                    start_index = content.index(str(bold))
                    heading_indexes.append(start_index)
                                      
        return heading_indexes, headings
    
    def find_bio(self, content, headings, heading_indexes):
        if heading_indexes:
            end_bio_ind = min(heading_indexes)
            bio = content[:end_bio_ind]
            if bio:
                return bio

        return "NOT FOUND"

    def find_this(self, content, head, headings, heading_indexes):
        if headings:
            for h in range(len(headings)):
                heading = headings[h]
                if head in heading.lower():
                    start_index = heading_indexes[h]
                    if h+1 <= len(heading_indexes)-1:
                        next_index = heading_indexes[h+1]
                        edu = content[start_index:next_index]     
                    else:
                        edu = content[start_index:]

                    return edu        

        return "NOT FOUND"        

    def readFile(self):
        out = file(self.filepath, "r").read()            
        return out

    def writeToCsv(self, filename=""):
        with open (filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, dialect='excel')
            csvwriter.writerow(['bio'])
    

if __name__ == "__main__":
    PROBABLE_HEADINGS = getAllHeadings("set_of_headings.txt")
    fileset = getFiles("/home/shreya/Wharton/XML")
    with open ("split_v3.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['FILENAME', 'HEADINGS', 'BIO', 'EDUCATION', 'EXPERIENCE' ])
        for filepath in fileset:
            index = filepath.index(".") 
            if "xml" in filepath[index:]:
                print filepath
                row = []
                last_index =filepath.rfind("/")+1
                filename = filepath[last_index:]
                pt = ParseText(filepath)
                content = pt.readFile()     
                heading_indexes, headings = pt.findHeadings(content, PROBABLE_HEADINGS)
                bio = pt.find_bio(content, headings, heading_indexes)
                print "BIO: ", bio
                print "HEADINGS: ",  headings
                edu = pt.find_this(content, "education", headings, heading_indexes)
                exp = pt.find_this(content, "experience", headings, heading_indexes)
                print "EDUCATION: ", edu
                print "EXPERIENCE: ", exp 
                row.append(filename)
                row.append(headings)    
                row.append(bio)    
                row.append(edu)
                row.append(exp)        
                csvwriter.writerow(row)

    '''filepath = "/home/shreya/Wharton/1.xml"
    pt = ParseText(filepath)
    content = pt.readFile()     
    #pt.findHeadings(content) 
    print pt.find_bio(content)
    #print "a"
    '''