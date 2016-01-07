"""
This script splits the xml and text version of resume into major categories
and saves it into a csv

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
    def __init__(self, xml_filepath="", text_filepath = ""):
        self.xml_filepath = xml_filepath
        self.text_filepath = text_filepath
        self.isXml = True

    def findHeadings(self, content, content_list, PROBABLE_HEADINGS):
        heading_indexes = []
        headings = []
        #print content
        soup = BeautifulSoup(content)
        bolds = soup.find_all('b')
        #print "bolds: ", bolds
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
                    #print "heading2: ", line
                    headings.append(line)
                    start_index = content.index(str(bold))
                    heading_indexes.append(start_index)
        
        #print content        
        if not headings:
            self.isXml = False
            for line in content_list:
                #print line
                prob_head = line.strip().lower()
                if prob_head in PROBABLE_HEADINGS and line not in headings:
                    print "heading3: ", line
                    headings.append(line)
                    start_index = content_list.index(line)
                    heading_indexes.append(start_index)           
                    
                                      
        return heading_indexes, headings
    
    def find_bio(self, content, content_list, headings, heading_indexes):
        if self.isXml:
            if heading_indexes:
                end_bio_ind = min(heading_indexes)
                bio = content[:end_bio_ind]
                if bio:
                    return bio
        else:
            if heading_indexes:
                end_bio_ind = min(heading_indexes)
                bio_list = content_list[:end_bio_ind]
                if bio_list:
                    return ''.join(bio_list)
                
        return "NOT FOUND"

    def find_this(self, content, content_list, head, headings, heading_indexes):
        if self.isXml:
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
        else:
             if headings:
                for h in range(len(headings)):
                    heading = headings[h]
                    if head in heading.lower():
                        start_index = heading_indexes[h]
                        if h+1 <= len(heading_indexes)-1:
                            next_index = heading_indexes[h+1]
                            edu_list = content_list[start_index:next_index]     
                        else:
                            edu_list = content_list[start_index:]


                        return ''.join(edu_list)                       
        
        return "NOT FOUND"        

    def readXmlToString(self):
        out = file(self.xml_filepath, "r").read()            
        return out

    def readTextToList(self):
        out = file(self.text_filepath, "r").readlines()            
        return out


    def writeToCsv(self, filename=""):
        with open (filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, dialect='excel')
            csvwriter.writerow(['bio'])
    

if __name__ == "__main__":
    PROBABLE_HEADINGS = getAllHeadings("set_of_headings.txt")
    fileset = getFiles("/home/shreya/Wharton/XML")
    with open ("split_v4.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['FILENAME', 'HEADINGS', 'BIO', 'EDUCATION', 'EXPERIENCE' ])
        for xml_filepath in fileset:
            index = xml_filepath.index(".") 
            if "xml" in xml_filepath[index:]:
                #print "xml: ", xml_filepath
                row = []
                first_index =xml_filepath.rfind("/")+1
                last_index = xml_filepath.rfind(".")
                filename = xml_filepath[first_index: last_index]
                #print "filename: "+filename
                text_filepath = "/home/shreya/Wharton/PDF_text/" + filename + ".txt"
                #print "text_filepath: ", text_filepath
                pt = ParseText(xml_filepath, text_filepath)
                content = pt.readXmlToString()
                content_list = pt.readTextToList()     
                heading_indexes, headings = pt.findHeadings(content, content_list, PROBABLE_HEADINGS)
                bio = pt.find_bio(content, content_list, headings, heading_indexes)
                #print "BIO: ", bio
                #print "HEADINGS: ",  headings
                edu = pt.find_this(content, content_list, "education", headings, heading_indexes)
                exp = pt.find_this(content, content_list, "experience", headings, heading_indexes)
                #print "EDUCATION: ", edu
                #print "EXPERIENCE: ", exp
                if not exp:
                    exp =  pt.find_this(content, content_list, "history", headings, heading_indexes)
                
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