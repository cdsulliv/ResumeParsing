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
    Degree = soup.find("degreemajor")
    GPA = soup.find("measurevalue")

    #If GPA isn't listed, output "Not Listed"
    if GPA is None:
        GPA = "Not Listed"
    else:
        GPA = GPA.get_text().strip('\n')

    #print [School_Name.get_text(), Degree.get_text(), GPA]
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

    #print jobList
    return jobList

#Returns the start and end dates for each job in the job_list
def find_dates(soup):
    startDates = []
    endDates = []

    jobs = soup.find_all("employerorg")

    for job in jobs:
        startDates.append(job.find("startdate").get_text())
        endDates.append(job.find('enddate').get_text())

    dateList = zip(startDates, endDates)

    if len(dateList) < 5:
        while len(dateList) < 5:
            dateList.append(('Not Listed', 'Not Listed'))

    return dateList

def find_descriptions(soup):
    
    descriptions = []
    
    jobs = soup.find_all("employerorg")
    
    # Commented Out for now due to ascii issues
    for job in jobs:
        description = job.find("description")
        descriptions.append(description.get_text().encode('ascii', 'replace'))
    
    if len(descriptions) < 5:
        while len(descriptions) < 5:
            descriptions.append('Not Listed')

    return descriptions

def find_qualifications(soup):
    q_sum = soup.find_all("qualificationsummary")
    
    if len(q_sum) != 1:
        return ["Not Listed"]
    else:
        return q_sum[0].get_text().encode('ascii', 'replace')

def find_activities(soup):
    achiev_list = []
    assoc_list = []
    achievments = soup.find_all("achievement")
    associations = soup.find_all("association")
    
    for achievment in achievments:
        name = achievment.find("description")
        achiev_list.append(name.get_text())
    
    for association in associations:
        name = association.find("name")
        assoc_list.append(name.get_text())

    return [achiev_list, assoc_list]

if __name__ == "__main__":

     # Get list of files for iteration
    XMLSet = [f for f in fileset if f.endswith(".xml")]
    XMLNames = [f for f in filenames if f.endswith(".xml")]
    assert len(XMLSet) == len(XMLNames) 

    xmlset = set()

    with open (outputfile, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['FILENAME', 'SCHOOL', 'DEGREE', 'GPA', 'JOB 1 COMPANY', 'JOB 1 TITLE', 'JOB 1 DESCRIPTION', 'JOB 1 START DATE', 'JOB 1 END DATE', 'JOB 2 COMPANY', 'JOB 2 TITLE', 'JOB 2 DESCRIPTION', 'JOB 2 START DATE', 'JOB 2 END DATE', 'JOB 3 COMPANY', 'JOB 3 TITLE', 'JOB 3 DESCRIPTION', 'JOB 3 START DATE', 'JOB 3 END DATE', 'JOB 4 COMPANY', 'JOB 4 TITLE', 'JOB 4 DESCRIPTION', 'JOB 4 START DATE', 'JOB 4 END DATE', 'JOB 5 COMPANY', 'JOB 5 TITLE', 'JOB 5 DESCRIPTION', 'JOB 5 START DATE', 'JOB 5 END DATE', 'QUALIFICATIONS', 'ACHIEVMENTS', 'ASSOCIATIONS'])

        for xml_filename, xml_filepath in zip(XMLNames, XMLSet):
            print "filename: ", xml_filename

            handler = open(xml_filepath).read()

            soup = BeautifulSoup(handler, "html.parser")

            Edu = find_Edu(soup)
            exp = find_workExp(soup)
            dates = find_dates(soup)
            dscrpt = find_descriptions(soup)
            qual = find_qualifications(soup)
            act = find_activities(soup)

            row = [xml_filename, Edu[0], Edu[1], Edu[2], exp[0][0], exp[0][1], dscrpt[0], dates[0][0], dates[0][1], exp[1][0], exp[1][1], dscrpt[1], dates[1][0], dates[1][1], exp[2][0], exp[2][1], dscrpt[2], dates[2][0], dates[2][1], exp[3][0], exp[3][1], dscrpt[3], dates[3][0], dates[3][1], exp[4][0], exp[4][1], dates[4][0], dscrpt[4], dates[4][1], qual, act[0], act[1]]

            csvwriter.writerow(row)
            
            
            
            
            
            

