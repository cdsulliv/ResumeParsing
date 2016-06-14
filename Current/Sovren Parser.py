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
outputfile = outputloc+"/Sovren-Parse-Data.csv"
#############################################################


#Returns a list of educational information [School_Name, Degree, GPA]
def find_Edu(soup):
    School_Name = soup.find("schoolname")
    Degree = soup.find("degreename")
    GPA = soup.find("measurevalue")

    #If GPA isn't listed, output "Not Listed"
    if GPA is None:
        GPA = "Not Listed"
    else:
        GPA = GPA.get_text().strip('\n')

    print [School_Name.get_text(), Degree.get_text(), GPA]
    return [School_Name.get_text(), Degree.get_text(), GPA]


#Returns a list of Work Experience information [[Job1Company, Job1Position, Internship], [Job2Company, Job2Position, Internship]]
def find_workExp(soup):
    jobList = []
    jobNumber = len(soup.find_all('positionhistoryuserarea'))

    CompanyNames = soup.find_all('employerorgname')
    PositionNames = soup.find_all('title')

    for Company, Position in zip(CompanyNames, PositionNames):
        jobList.append([Company.get_text(), Position.get_text()])
    
    if jobNumber < 5:
        while len(jobList) < 5:
            jobList.append(['Not Listed', 'Not Listed'])

    print jobList
    return jobList


if __name__ == "__main__":

     # Get list of files for iteration
    XMLSet = [f for f in fileset if f.endswith(".xml")]
    XMLNames = [f for f in filenames if f.endswith(".xml")]
    assert len(XMLSet) == len(XMLNames) 

    xmlset = set()

    with open (outputfile, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['FILENAME', 'SCHOOL', 'DEGREE', 'GPA', 'JOB 1 COMPANY', 'JOB 1 TITLE', 'JOB 2 COMPANY', 'JOB 2 TITLE', 'JOB 3 COMPANY', 'JOB 3 TITLE', 'JOB 4 COMPANY', 'JOB 4 TITLE'])

        for xml_filename, xml_filepath in zip(XMLNames, XMLSet):
            print "filename: ", xml_filename

            handler = open(xml_filepath).read()

            soup = BeautifulSoup(handler, "html.parser")

            Edu = find_Edu(soup)
            exp = find_workExp(soup)

            row = [xml_filename, Edu[0], Edu[1], Edu[2], exp[0][0], exp[0][1], exp[1][0], exp[1][1], exp[2][0], exp[2][1], exp[3][0], exp[3][1], exp[4][0], exp[4][1]]

            csvwriter.writerow(row)
            
            
            
            
            
            

