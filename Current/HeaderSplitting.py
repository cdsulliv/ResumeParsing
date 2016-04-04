"""
This script splits the xml and text version of resume into major categories
and saves it into a csv

"""

__author__ = "Shreya Pandey"

import re
import os
import io
from bs4 import BeautifulSoup
import csv
import ast
from preprocessor import preprocess 
import fileinput
import string


############   Set variables to local machine   #############
xml_loc = "/Users/colin/Dropbox/Resume-audit/Scraping Project/Career Builder Resumes/Parsing Files/XML/"
fileset = [xml_loc + f for f in os.listdir(xml_loc)]
filenames = [f for f in os.listdir(xml_loc)]
headloc = "/Users/colin/Documents/ResumeParsing/Resume-Parsing/Current/Headings"
outputloc = "/Users/colin/Dropbox/Resume-audit/Scraping Project/Output"
outputfile = "HeaderSplitData.csv"
#############################################################

HEAD_PATTERN = "\S[A-Z \d / : ]+$" 
PROBABLE_HEADINGS = ["education", "objective", "experience", "work experience", "certifications", "organizations and activites", 
                    "extracurricular activities", "leadership experience", "volunteer experience", "skills", "coursework", 
                     "education and coursework"]
NEVER_HEADINGS = "university|institute"


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
        # headings is a list containing the headings. heading_index is a list of the starting indices of each heading.
        # Function will guarantee the two lists are of equal length, or will throw an error.
        heading_indexes = []
        headings = []
        content_new = ''.join(content_list) 
        soup = BeautifulSoup(content_new)
        #soup = preprocess(p_soup)
        bolds = soup.find_all('b')
        for bold in bolds:
            line = bold.string
            if line:
                prob_head = line.strip().lower()  
                
                prob_head = filter(lambda x: x in set(string.letters).union(set(' ')), prob_head).strip()
                
                exclude = set(string.punctuation)
                prob_head = ''.join(ch for ch in prob_head if ch not in exclude)                        
                
                if (prob_head in PROBABLE_HEADINGS) and (line not in headings):
                    #print "heading2: ", line
                    headings.append(line)
                    start_index = content_new.index(str(bold))
                    heading_indexes.append(start_index)
        
        print "OLD HEADINGS: ", headings
        print "HEADING index: ", heading_indexes        
        if len(headings)<2:            
            texts = soup.find_all("text")
            # All CAPS:
            for t in texts:
                line = t.text
                if line: 
                    if (line.isupper() and not re.search("GPA|G.P.A", line) and len(line)>5):
                        # CDS: Need to correct the encoding here - .encode('ascii', 'replace')
                        headings.append(str(line))
                        start_index = content_new.index(str(line))
                        heading_indexes.append(start_index)
                        if len(heading_indexes) != len(headings):
                            print content_new.index(str(line))

                            print "Error is CAPS heading indexes (%d) doesn't match length of headings (%d)." % (len(heading_indexes), len(headings))
                        print "The error is in UPPER"
            print "CAPS headings: ", headings
            print "CAPS heading_indexes: ", heading_indexes

        if len(headings)<2:            
            # Underline
            texts = soup.find_all("text")
            for t in texts:
                line = t.text
                if line:     
                    try:
                        # Search for underscore used as underline, and line contains alphabet character
                        if re.search('___', line) and len(line) > 5 and re.search('[a-zA-Z]', line):
                            headings.append(line)
                            start_index = content_new.index(str(line))
                            heading_indexes.append(start_index)

                        # If line doesn't contain alphabet character, take the NEXT line as header
                        if re.search('___', line) and len(line) > 5 and not re.search('[a-zA-Z]', line):
                            headings.append("This contains a horizontal rule with no text")
                    except:
                        print "the error is in Underline"                

            #print content
            print "Underline headings: ", headings
            print "Underline heading_indexes: ", heading_indexes        
 
        assert len(heading_indexes) == len(headings)
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
                
        return None

    def find_this(self, content, content_list, head, avoid, headings, heading_indexes):
        ''' Searches for any of a list of strings (head) in headings. Returns the information associated with that heading
                if a string from head is matched and a string from avoid is not matched.
        '''
        if self.isXml:
            if headings:
                for h in range(len(headings)):
                    heading = headings[h]
                    heading = heading.replace(" ", "")
                    # 
                    if (any([txt in heading.lower() for txt in head]) and not any([txt in heading.lower() for txt in avoid])) :
                        start_index = heading_indexes[h]
                        if h+1 <= len(heading_indexes)-1:
                            next_index = heading_indexes[h+1]
                            edu = content[start_index:next_index]     
                        else:
                            edu = content[start_index:]

                        return edu, self.isXml        
        else:
             if headings:
                for h in range(len(headings)):
                    heading = headings[h]
                    if (any([txt in heading.lower() for txt in head]) and not any([txt in heading.lower() for txt in avoid])) :
                        start_index = heading_indexes[h]
                        if h+1 <= len(heading_indexes)-1:
                            next_index = heading_indexes[h+1]
                            edu_list = content_list[start_index:next_index]     
                        else:
                            edu_list = content_list[start_index:]


                        return ''.join(edu_list), self.isXml                       
        
        return None, self.isXml        

    def readXmlToString(self):
        out = file(self.xml_filepath, "r").read()            
        return out

    def readXMLToList(self):
        out = file(self.xml_filepath, "r").readlines()            
        return out
            
    def readTextToList(self):
        try:
            out = file(self.text_filepath, "r").readlines()
        except:
            out = []                
        return out


    def writeToCsv(self, filename=""):
        with open (filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, dialect='excel')
            csvwriter.writerow(['bio'])

if __name__ == "__main__":
    PROBABLE_HEADINGS = getAllHeadings(headloc+'/set_of_headings_1.txt')
    print "OLD LEN: ", len(PROBABLE_HEADINGS)
    PROBABLE_HEADINGS.extend(getAllHeadings(headloc+'/set_of_headings_boston.txt'))
    PROBABLE_HEADINGS.extend(getAllHeadings(headloc+'/set_of_headings_newyork.txt'))
    PROBABLE_HEADINGS.extend(getAllHeadings(headloc+'/set_of_headings_other.txt'))
    
    PROBABLE_HEADINGS = list(set(PROBABLE_HEADINGS))
    PROBABLE_HEADINGS = [x for x in PROBABLE_HEADINGS if not re.search(NEVER_HEADINGS, x)]

    # Get list of files for iteration
    XMLSet = [f for f in fileset if f.endswith(".xml")]
    XMLNames = [f for f in filenames if f.endswith(".xml")]
    assert len(XMLSet) == len(XMLNames) 
    
    xmlset = set()
                
    with open (outputfile, 'w') as csvfile:

        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['FILENAME', 'HEADINGS', 'BIO', 'EDUCATION', 'EXPERIENCE', 'LEADERSHIP', 'VOLUNTEER', 'SKILLS', 'LANGUAGES'])
        
        #print i, file_year    
        for xml_filename, xml_filepath in zip(XMLNames, XMLSet):
            isLead = False
            isVolunt = False
         
            print "filename: ", xml_filename

            text_filepath = outputloc + xml_filename + ".txt"
                
            pt = ParseText(xml_filepath, text_filepath)
            content = pt.readXmlToString()
            content_list = pt.readXMLToList()
            if content in xmlset: continue # Skip duplicates
            xmlset.add(content)

            try: # CDS: Eventually, should remove this "try". Right now, allows you to keep going despite errors.
                heading_indexes, headings = pt.findHeadings(content, content_list, PROBABLE_HEADINGS)
            except:
                headings = 'ERROR: ENCODING'
                print "fix headings"
            #assert len(heading_indexes) == len(headings)


            bio = pt.find_bio(content, content_list, headings, heading_indexes)
            '''
            if not bio:
                bio = content
            '''    
            #print "BIO: ", bio
            #print "HEADINGS: ",  headings
            edu, isXml = pt.find_this(content, content_list, ["ducation", "ducaton"], [], headings, heading_indexes)
            exp, isXml = pt.find_this(content, content_list, ["xperience", "mployment", 'areer', 'istory', 'rofessional', 'work'], ['bjective', 'ourse'], headings, heading_indexes)

            leadExp, x = pt.find_this(content, content_list, ["eadership", 'ommunity', 'xtracurricular', 'ctivities', 'rganizations'], [], headings, heading_indexes)
            
            skills, isXml = pt.find_this(content, content_list, ["kills"], [], headings, heading_indexes)
            languages, isXml = pt.find_this(content, content_list, ["languages", 'foreign'], ['omputer', 'programming'], headings, heading_indexes)

            if leadExp: isLead  = "TRUE"
           

            volunExp, y = pt.find_this(content, content_list, ["olunteer"], [], headings, heading_indexes)
            if volunExp: isVolunt = "TRUE"

            volOrLead = False
            if isLead or isVolunt: volOrLead = "TRUE"

            if not headings: isXml = "NULL"
                
            
            # Write a row of data to CSV
            row = [xml_filename, headings, "BIO EXCLUDED", edu, exp, leadExp, volunExp, skills, languages]      
            
            csvwriter.writerow(row)

    # Remove duplicates from the file in place
#    seen = set() # set for fast O(1) amortized lookup
#    for line in fileinput.FileInput(outputfile, inplace=1):
#        if (line in seen): continue # skip duplicates

#        seen.add(line)
#        print line, # standard output is now redirected to the file  
            
            
#        csvwriter.writerow('')
#        csvwriter.writerow(['Empty count: ', '=COUNTIF(B1:B702, "[]"', '=COUNTIF(C1:C702, ""','=COUNTIF(D1:D702, ""', '=COUNTIF(E1:E702, ""', '=COUNTIF(F1:F702, ""'])
#        csvwriter.writerow(['Error count: ', '=COUNTIF(B1:B702, "*ERROR*"'])
        
            # First and biggest issue: 'ascii' codec can't encode characters in position 9-10: ordinal not in range(128)
            # Something wrong with the codec, so some characters are marked as ascii errors. These seem related to some bullet points and some horizontal rules (AChoi)
            ### Leads to different lengths beween len(heading_indexes) and len(heading). This is causing problems in May+2015+Resume.doc.

            ### CDS: Bio section is returning all the png files. I think these lines must be due to pictures included in the first part of resumes. 
            # Must exclude the png's - adds tens of thousands of rows to the output csv. Temporarily removed bio information until rectified.


            ### Need to check that duplicates are getting removed, but NOT name duplicates. Should include all unique files called "Resume.xml", for instsance.
            # After removing pure duplicates, only have 322 resumes. Is this right?

            # For Underlined headings: also look for "___" used as horizontal rule, collect line AFTER (ZHOODA.pdf)
                # This doesn't occur in any of the cases we currently have in XML. (ZHOODA doesn't get converted)


        # Remove duplicate rows from CSV file, save as SectionSplit_NoDups.csv - NOT WORKING. WRITING OUT MANY LINES OF XML        
            # About 70 lines of CSV are text, not resume entries. Example:
            # <text top=""155"" left=""54"" width=""198"" height=""17"" font=""3""><b>(SOME TEXT WITH UNRECOGNIZED CHARACTER ENCODINGS)</b></text>

#        with open('split_v.csv','r') as in_file, open('SectionSplit_NoDups.csv','w') as out_file:

#            seen = set() 
#            for line in in_file:
 #               if line in seen: continue # skip duplicate

  #              seen.add(line)
  #              csvwriter.writerow(line)
                         
    '''filepath = "/home/shreya/Wharton/1.xml"
    pt = ParseText(filepath)
    content = pt.readFile()     
    #pt.findHeadings(content) 
    print pt.find_bio(content)
    #print "a"
    '''