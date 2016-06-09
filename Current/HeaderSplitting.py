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
xml_loc = "/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Penn Clubs XML/"
fileset = [xml_loc + f for f in os.listdir(xml_loc)]
filenames = [f for f in os.listdir(xml_loc)]
headloc = "/Users/cutlerreynolds/git/ResumeParsing/Current/Headings"
outputloc = "/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output"
outputfile = "HeaderSplitData-testPre.csv"
#############################################################

HEAD_PATTERN = "\S[A-Z \d / : ]+$" 
PROBABLE_HEADINGS = ["education", "objective", "experience", "work experience", "certifications", "organizations and activites", 
                    "extracurricular activities", "leadership experience", "volunteer experience", "skills", "coursework", 
                     "education and coursework"]
NEVER_HEADINGS = "university|institute"

def readableClean(list):
    return [item.get_text() for item in list]

#Reads in list of headings from the text file in the data folder
def getAllHeadings(filename=""):
    f = open(filename, "r")
    lines = f.readlines()
    headings = [line.strip() for line in lines]
    return headings

#Overarching object for parsing the XML
class ParseText(object):
    """docstring for ParseTextme"""
    def __init__(self, xml_filepath="", text_filepath = ""):
        self.xml_filepath = xml_filepath
        self.text_filepath = text_filepath
        self.isXml = True

    #Function to find headings within an XML Resume by comparing with the list from the text files
    def findHeadings(self, PROBABLE_HEADINGS, soup):
        heading_indexes = []
        headings = []


        #Search through all text for 'b' tags, most likely indicator of a heading
        bolds = soup.find_all('b')
        for bold in bolds:
            line = bold.get_text()
            if line:
                prob_head = line.strip().lower()

                prob_head = filter(lambda x: x in set(string.letters).union(set(' ')), prob_head).strip()

                exclude = set(string.punctuation)
                prob_head = ''.join(ch for ch in prob_head if ch not in exclude)                        

                #Check if the text of the bold tag matches a header in the probable headers list
                for head in PROBABLE_HEADINGS:
                    if head == prob_head:
                        #Set the "header" attribute to "Y" so it is easy to find in the Soup
                        bold.parent['header'] = 'Y'
                        headings.append(bold.parent)

        #Search for Uppercase headers if not enough bold ones are found
        if len(headings)<2:            
            texts = soup.find_all("text")
            for t in texts:
                line = t.text
                if line: 
                    if (line.isupper() and not re.search("GPA|G.P.A", line) and len(line)>5):

                        t['header'] = 'Y'

                        headings.append(t)

        #If not enough bold tags were found search for underlined headers 
        #(not sure about this logic, but left it in because it was there before - haven't checked if 
        #it ever actually finds anything)
        if len(headings)<2:
            texts = soup.find_all("text")
            for t in texts:
                line = t.text
                if line:     
                    try:
                        # Search for underscore used as underline, and line contains alphabet character
                        if re.search('___', line) and len(line) > 5 and re.search('[a-zA-Z]', line):
                            headings.append(t)
                            t['header'] = 'Y'
                        # If line doesn't contain alphabet character, take the NEXT line as header
                        if re.search('___', line) and len(line) > 5 and not re.search('[a-zA-Z]', line):
                            headings.append("This contains a horizontal rule with no text")
                    except:
                        print "the error is in Underline"  
        
        #If still not enough headers, search for keywords (EDUCATION, LEADERSHIP, etc...) 
        if len(headings)<2:
            texts = soup.find_all("text")
            for t in texts:
                if t.get_text().lower().strip() in PROBABLE_HEADINGS:
                    headings.append(t)
                    t['header'] = 'Y'

        return headings

    #Function to locate the bio section, as far as I can tell it is never called but I left it 
    #as a precaution
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

    ''' 
    Searches for any of a list of strings (head) in headings. Returns the information associated 
    with that heading if a string from head is matched and a string from avoid is not matched.
    '''
    def find_this(self, soup, head, avoid):

        headings = list(soup.find_all('text', {'header' : 'Y'}))

        if headings:
            for h in headings:
                #For each heading check whether any match the header or avoid lists
                if (any([txt in h.get_text().lower() for txt in head]) and not 
                    any([txt in h.get_text().lower() for txt in avoid])) :
                    texts = list(soup.find_all('text'))
                    ret = ''
                    add = False
                    #Go through all tags, add them to the return if they are after the proper header
                    #but before the next header
                    for text in texts:
                        if h.get_text() in text.get_text():
                            add = True

                        for n in [he for he in headings if he != h]:
                            if n.get_text() in text.get_text():
                                add = False

                        if add:
                            ret = ret + text.encode()

                    #I believe the self.isXml variable is useless, but have not fully tested without it
                    #so I am leaving it for now
                    return ret, self.isXml
        return None, self.isXml        

    #Functions for reading in the xml/text files and writing out the csv output
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
    #Assemble list of probable headings
    PROBABLE_HEADINGS = getAllHeadings(headloc+'/set_of_headings_1.txt')
    print "OLD LEN: ", len(PROBABLE_HEADINGS)
    PROBABLE_HEADINGS.extend(getAllHeadings(headloc+'/set_of_headings_boston.txt'))
    PROBABLE_HEADINGS.extend(getAllHeadings(headloc+'/all_headings_newyork.txt'))
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
        csvwriter.writerow(['FILENAME', 'HEADINGS', 'HEADINGS_CLEAN', 'BIO', 'EDUCATION', 'EXPERIENCE', 'LEADERSHIP', 'VOLUNTEER', 'SKILLS', 'LANGUAGES'])

        for xml_filename, xml_filepath in zip(XMLNames, XMLSet):

            isLead = False
            isVolunt = False

            print "filename: ", xml_filename

            text_filepath = outputloc + xml_filename + ".txt"

            pt = ParseText(xml_filepath, text_filepath)
            content = pt.readXmlToString()

            #content_list variable is not used anymore, but is still used in the getBio code that I left so I left this here too
            #content_list = pt.readXMLToList()
            if content in xmlset: continue # Skip duplicates
            xmlset.add(content)

            soup = BeautifulSoup(content, "html.parser")

            #Preprocess using preprocessor.py
            preprocess(soup)

            #Get headings
            headings = pt.findHeadings(PROBABLE_HEADINGS, soup)
            headingsclean = [h.get_text() for h in headings]
            
            #bio = pt.find_bio(content, content_list, headings, heading_indexes)


            #Use find_this function to find edu, exp, leadership, skills, languages, volunteer
            edu, isXml = pt.find_this(soup, ["education", "educaton"], [])
            exp, isXml = pt.find_this(soup, ["experience", "employment", 'career', 'history', 'professional', 'work'], ['objective', 'course'])
            leadExp, x = pt.find_this(soup, ["leadership", 'community', 'extracurricular', 'activities', 'organizations'], [])
            skills, isXml = pt.find_this(soup, ["kills"], [])
            languages, isXml = pt.find_this(soup, ["languages", 'foreign'], ['computer', 'programming'])

            if leadExp: isLead  = "TRUE"

            volunExp, y = pt.find_this(soup, ["volunteer"], [])
            if volunExp: isVolunt = "TRUE"

            volOrLead = False
            if isLead or isVolunt: volOrLead = "TRUE"

            if not headings: isXml = "NULL"


            # Write a row of data to CSV
            row = [xml_filename, headings, headingsclean, "BIO EXCLUDED", edu, exp, leadExp, volunExp, skills, languages]      

            csvwriter.writerow(row)
