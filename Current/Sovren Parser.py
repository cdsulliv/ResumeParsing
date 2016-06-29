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
xml_loc = "/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Sovren/Penn Clubs Output/All xml files/"
folders = ["GM Output", "MARC Output", "MUSE Output", "Networking Lunch Output", "Wharton Alliance Output", "WUCC Output"]
fileset = [xml_loc + f for f in os.listdir(xml_loc)]
filenames = [f for f in os.listdir(xml_loc)]
outputloc = "/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output"
outputfile = outputloc+"/Sovren-Parse-Data.csv"
Arts = 0
Sciences = 0
#############################################################

def exists(soup):
    if soup is None:
        return "Not Listed"
    else:
        return soup.get_text().encode('ascii', 'replace')


#Returns a list of educational information [School_Name, Degree, GPA]
def find_Edu(soup):
    School_Name = exists(soup.find("schoolname"))
    Degree = exists(soup.find("degreemajor"))
    GPA = exists(soup.find("measurevalue"))
    Degree_name = exists(soup.find("degreename"))

    
    if "concentration" in Degree.lower() or "intended" in Degree.lower():
        Degree = exists(soup.find("degreename"))
    
    if "in" in Degree_name:
        Degree = Degree_name

    #print [School_Name.get_text(), Degree.get_text(), GPA]
    return [School_Name, Degree, GPA]


#Returns a list of Work Experience information [[Job1Company, Job1Position], [Job2Company, Job2Position]]
def find_workExp(soup):
    jobList = []
    jobNumber = len(soup.find_all('positionhistoryuserarea'))
    orgNames = soup.find_all('employerorg')

    for organization in orgNames:
        allPositions = organization.find_all('positionhistory')
        for position in allPositions:
            PositionName = exists(position.find('title'))
            CompanyName = exists(position.find('organizationname'))

            if CompanyName.strip('') == '':
                CompanyName = exists(organization.find('employerorgname'))
                #print "Name is: " + CompanyName
                if CompanyName.strip('') == '':
                    CompanyName = 'Not Listed'

            jobList.append([CompanyName, PositionName])

    if jobNumber < 10:
        while len(jobList) < 10:
            jobList.append(['Not Listed', 'Not Listed'])

    #print jobList
    return jobList

#Returns the start and end dates for each job in the job_list
def find_dates(soup):
    startDates = []
    endDates = []

    jobs = soup.find_all("positionhistory")

    for job in jobs:
        startDates.append(exists(job.find("startdate")))
        endDates.append(exists(job.find('enddate')))

    dateList = zip(startDates, endDates)

    if len(dateList) < 10:
        while len(dateList) < 10:
            dateList.append(('Not Listed', 'Not Listed'))

    return dateList

def find_descriptions(soup):
    
    descriptions = []
    
    jobs = soup.find_all("positionhistory")
    
    # Commented Out for now due to ascii issues
    for job in jobs:
        description = job.find("description")
        descriptions.append(description.get_text().encode('ascii', 'replace'))
    
    if len(descriptions) < 10:
        while len(descriptions) < 10:
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

def classify_majors(sample_major):
    global Arts, Sciences
    
    col_majors = open("/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/CollegeMajors.txt", 'r')
    c_major_list = col_majors.read().split(',')

    eng_majors = open("/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/EngineeringMajors.txt", 'r')
    e_major_list = eng_majors.read().split(',')

    wha_majors = open("/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/WhartonMajors.txt", 'r')
    w_major_list = wha_majors.read().split(',')
    
    all_majors = [c_major_list, e_major_list, w_major_list]
    
    for school in all_majors:
        for major in school:
            if major in sample_major:
                if school == c_major_list or w_major_list:
                    Arts = Arts + 1
                    print major
                elif school == e_major_list:
                    Sciences = Sciences + 1
                    print major

if __name__ == "__main__":
    
     # Get list of files for iteration
    XMLSet = [f for f in fileset if f.endswith(".xml")]
    XMLNames = [f for f in filenames if f.endswith(".xml")]
    assert len(XMLSet) == len(XMLNames) 
    xmlset = set()
    
    with open (outputfile, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['FILENAME', 'SCHOOL', 'DEGREE', 'GPA', 'JOBCOMPANY1', 'JOBTITLE1', 'JOBDESCRIPTION1', 'JOBSTARTDATE1', 'JOBENDDATE1', 'JOBCOMPANY2', 'JOBTITLE2', 'JOBDESCRIPTION2', 'JOBSTARTDATE2', 'JOBENDDATE2', 'JOBCOMPANY3', 'JOBTITLE3', 'JOBDESCRIPTION3', 'JOBSTARTDATE3', 'JOBENDDATE3', 'JOBCOMPANY4', 'JOBTITLE4', 'JOBDESCRIPTION4', 'JOBSTARTDATE4', 'JOBENDDATE4', 'JOBCOMPANY5', 'JOBTITLE5', 'JOBDESCRIPTION5', 'JOBSTARTDATE5', 'JOBENDDATE5', 'JOBCOMPANY6', 'JOBTITLE6', 'JOBDESCRIPTION6', 'JOBSTARTDATE6', 'JOBENDDATE6', 'JOBCOMPANY7', 'JOBTITLE7', 'JOBDESCRIPTION7', 'JOBSTARTDATE7', 'JOBENDDATE7', 'JOBCOMPANY8', 'JOBTITLE8', 'JOBDESCRIPTION8', 'JOBSTARTDATE8', 'JOBENDDATE8', 'JOBCOMPANY9', 'JOBTITLE9', 'JOBDESCRIPTION9', 'JOBSTARTDATE9', 'JOBENDDATE9', 'JOBCOMPANY10', 'JOBTITLE10', 'JOBDESCRIPTION10', 'JOBSTARTDATE10', 'JOBENDDATE10', 'QUALIFICATIONS', 'ACHIEVMENTS', 'ASSOCIATIONS'])
    
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
    
            row = [xml_filename, Edu[0], Edu[1], Edu[2], exp[0][0], exp[0][1], dscrpt[0], dates[0][0], dates[0][1], exp[1][0], exp[1][1], dscrpt[1], dates[1][0], dates[1][1], exp[2][0], exp[2][1], dscrpt[2], dates[2][0], dates[2][1], exp[3][0], exp[3][1], dscrpt[3], dates[3][0], dates[3][1], exp[4][0], exp[4][1], dscrpt[4], dates[4][0], dates[4][1], exp[5][0], exp[5][1], dscrpt[5], dates[5][0], dates[5][1], exp[6][0], exp[6][1], dscrpt[6], dates[6][0], dates[6][1], exp[7][0], exp[7][1], dscrpt[7], dates[7][0], dates[7][1], exp[8][0], exp[8][1], dscrpt[8], dates[8][0], dates[8][1], exp[9][0], exp[9][1], dscrpt[9], dates[9][0], dates[9][1], qual, act[0], act[1]]
    
            csvwriter.writerow(row)
