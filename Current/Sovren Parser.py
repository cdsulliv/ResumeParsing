'''
This script processes the XML files output by Sovren, and scrapes Education,
Work Experience, and Skills
'''

import re
import os
import io
from bs4 import BeautifulSoup
import csv
import ast
import fileinput
import string
from HeaderSplitting import ParseText

############   Set variables to local machine   #############
xml_loc = "/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Sovren/Test XML/"
fileset = [xml_loc + f for f in os.listdir(xml_loc)]
filenames = [f for f in os.listdir(xml_loc)]
outputloc = "/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output"
outputfile = "Sovren-Parse-Data.csv"
#############################################################

def find_Edu(soup):
    Edu_info = soup.find_all("SchoolName")
    
    for info in Edu_info:
        print info.get_text()

if __name__ == "__main__":

     # Get list of files for iteration
    XMLSet = [f for f in fileset if f.endswith(".xml")]
    XMLNames = [f for f in filenames if f.endswith(".xml")]
    assert len(XMLSet) == len(XMLNames) 

    xmlset = set()

    with open (outputfile, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['FILENAME', 'HEADINGS', 'HEADINGS_CLEAN', 'BIO', 'EDUCATION', 'EXPERIENCE', 'LEADERSHIP', 'VOLUNTEER', 'SKILLS', 'LANGUAGES'])

        for xml_filename, xml_filepath in zip(XMLNames, XMLSet):
            print "filename: ", xml_filename
            
            handler = open(xml_filepath).read()

            soup = BeautifulSoup(handler, "html.parser")
            
            find_Edu(soup)
            
            
            
            
            
            

