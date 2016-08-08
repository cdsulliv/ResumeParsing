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
import pandas as pd
import difflib
import subprocess

############   Set variables to local machine   #############
xml_loc = "/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Sovren/Penn Clubs Output/All xml files/"
folders = ["GM Output", "MARC Output", "MUSE Output", "Networking Lunch Output", "Wharton Alliance Output", "WUCC Output"]
fileset = [xml_loc + f for f in os.listdir(xml_loc)]
filenames = [f for f in os.listdir(xml_loc)]
outputloc = "/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output"
outputfile = outputloc+"/Sovren-Parse-Data.csv"
extdataloc = '/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Data Sources'
exp_file = '/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output/AllPennJobs.csv'
exp_data_file = '/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output/AllPennJobs_wdata.csv'
xml_path = '/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Sovren/Penn Clubs Output/All xml files/'
R_file = '/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output/ReshapeJobs_wLoc.R'
work_exp_file = '/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output/work_exp_only.csv'
#############################################################

#LISTS FOR IDENTIFYING LEADERSHIP SECTION
leadership = ["leadership", 'community', 'extracurricular', 'extracurriculars', 'activities', 'activites', 'organizations']
headings = ["education", "objective", "experience", 
"work", "certifications", 
"skills", "coursework", "coursework", 'awards', "additional", 'interests',"experience", "employment", 'career', 'history', 'work']
job_list = ['Volunteer', 'President', 'Vice-President', 'VP', 'Captain', 'Treasurer'] 


#Determines if a text tag contains text or is blank/doesn't exist
def exists(soup):
    if soup is None:
        return "Not Listed"
    else:
        return soup.get_text().encode('ascii', 'replace')

#HELPER FUNCTION FOR PARSE_XML
#Returns a list of locations for jobs
def find_loc(soup):
    locations = []
    jobs = soup.find_all('positionhistory')
    
    for job in jobs:
        area = exists(job.find('municipality'))
        state = exists(job.find('region'))
        
        locations.append(area + ', ' + state)
    
    while len(locations) < 10:
        locations.append("Not Listed")
    return locations

#HELPER FUNCTION FOR PARSE_XML
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


#HELPER FUNCTION FOR PARSE_XML
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

#HELPER FUNCTION FOR PARSE_XML
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

#HELPER FUNCTION FOR PARSE_XML
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

# HELPER FUNCTION FOR PARSE_XML
def find_qualifications(soup):
    q_sum = soup.find_all("qualificationsummary")
    
    if len(q_sum) != 1:
        return ["Not Listed"]
    else:
        return q_sum[0].get_text().encode('ascii', 'replace')

#HELPER FUNCTION FOR PARSE XML
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


#STEP 1: PARSES THE SOVREN OUTPUT XML FILES
def parse_xml():
    
     # Get list of files for iteration
    XMLSet = [f for f in fileset if f.endswith(".xml")]
    XMLNames = [f for f in filenames if f.endswith(".xml")]
    assert len(XMLSet) == len(XMLNames) 
    xmlset = set()
    
    with open (outputfile, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['FILE', 'SCHOOL', 'DEGREE', 'GPA', 'JOBCOMPANY1', 'JOBTITLE1', 'JOBLOC1', 'JOBDESCRIPTION1', 'JOBSTARTDATE1', 'JOBENDDATE1', 'JOBCOMPANY2', 'JOBTITLE2', 'JOBLOC2', 'JOBDESCRIPTION2', 'JOBSTARTDATE2', 'JOBENDDATE2', 'JOBCOMPANY3', 'JOBTITLE3', 'JOBLOC3', 'JOBDESCRIPTION3', 'JOBSTARTDATE3', 'JOBENDDATE3', 'JOBCOMPANY4', 'JOBTITLE4', 'JOBLOC4', 'JOBDESCRIPTION4', 'JOBSTARTDATE4', 'JOBENDDATE4', 'JOBCOMPANY5', 'JOBTITLE5', 'JOBLOC5', 'JOBDESCRIPTION5', 'JOBSTARTDATE5', 'JOBENDDATE5', 'JOBCOMPANY6', 'JOBTITLE6', 'JOBLOC6', 'JOBDESCRIPTION6', 'JOBSTARTDATE6', 'JOBENDDATE6', 'JOBCOMPANY7', 'JOBTITLE7', 'JOBLOC7', 'JOBDESCRIPTION7', 'JOBSTARTDATE7', 'JOBENDDATE7', 'JOBCOMPANY8', 'JOBTITLE8', 'JOBLOC8', 'JOBDESCRIPTION8', 'JOBSTARTDATE8', 'JOBENDDATE8', 'JOBCOMPANY9', 'JOBTITLE9', 'JOBLOC9', 'JOBDESCRIPTION9', 'JOBSTARTDATE9', 'JOBENDDATE9', 'JOBCOMPANY10', 'JOBTITLE10', 'JOBLOC10', 'JOBDESCRIPTION10', 'JOBSTARTDATE10', 'JOBENDDATE10', 'QUALIFICATIONS', 'ACHIEVMENTS', 'ASSOCIATIONS'])
    
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
            locs = find_loc(soup)
    
            row = [xml_filename, Edu[0], Edu[1], Edu[2], exp[0][0], exp[0][1], locs[0], dscrpt[0], dates[0][0], dates[0][1], exp[1][0], exp[1][1], locs[1], dscrpt[1], dates[1][0], dates[1][1], exp[2][0], exp[2][1], locs[2], dscrpt[2], dates[2][0], dates[2][1], exp[3][0], exp[3][1], locs[3], dscrpt[3], dates[3][0], dates[3][1], exp[4][0], exp[4][1], locs[4], dscrpt[4], dates[4][0], dates[4][1], exp[5][0], exp[5][1], locs[5], dscrpt[5], dates[5][0], dates[5][1], exp[6][0], exp[6][1], locs[6], dscrpt[6], dates[6][0], dates[6][1], exp[7][0], exp[7][1], locs[7], dscrpt[7], dates[7][0], dates[7][1], exp[8][0], exp[8][1], locs[8], dscrpt[8], dates[8][0], dates[8][1], exp[9][0], exp[9][1], locs[9], dscrpt[9], dates[9][0], dates[9][1], qual, act[0], act[1]]
    
            csvwriter.writerow(row)


#STEP 2: RESHAPE DATA FROM WIDE TO LONG FORMAT
def reshape():
    #data = pd.read_csv('/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output/Sovren-Parse-Data.csv', sep=",")

    #resh = pd.wide_to_long(data, ['JOBCOMPANY', 'JOBTITLE', 'JOBLOC', 'JOBDESCRIPTION', 'JOBSTARTDATE', 'JOBENDDATE'], i="FILENAME", j="JOB" )
    #resh.to_csv(exp_file)
    
    #BE SURE TO ENSURE R FILE ALSO HAS CORRECT WORKING DIRECTORY
    subprocess.check_call(['Rscript', R_file], shell=False)


#STEP 3: SEPARATE JOB DESCRIPTIONS AND FIND OUT WHETHER WORK FOR MONEY OR NOT
def job_info():
    #LISTS FOR IDENTIFYING LEADERSHIP SECTION
    majors = pd.read_csv(extdataloc+'/ListofPennMajors.csv', sep=',')
    jobs = pd.read_csv(exp_file, sep=',')
    wfmjobs = pd.read_csv(extdataloc+'/WorkForMoneyJobs.csv', sep=',', header=None)
    topemp= pd.read_csv(extdataloc+'/TopPennEngineeringEmployers.csv', sep=',')
    
    jobs['DEGREE'] = [deg.split(' in ', 1)[-1].strip() for deg in jobs['DEGREE']]
    
    
    jobs['GuessMaj'] = [difflib.get_close_matches(x, majors['Major'], n=1)[0] if 
                        difflib.get_close_matches(x, majors['Major'], n=1) else ''
                        for x in jobs['DEGREE']]
    
    jobs = jobs.merge(majors, how='left', left_on='GuessMaj', right_on='Major')
    
    jobs['WFM'] = [any([wfm in job.lower() for wfm in[title.lower() for title in wfmjobs[0]]]) for job in jobs['JOBTITLE']]
    
    jobs = jobs.loc[(jobs.JOBCOMPANY != 'Not Listed') & (jobs.JOBTITLE != "Not Listed") & (jobs.Des1 != "Not Listed")]
    
    jobs['GuessTopJob'] = [difflib.get_close_matches(x.lower(), [y.lower() for y in topemp['TopCompany']], n=1, cutoff=0.8)[0] if 
                    difflib.get_close_matches(x.lower(), [y.lower() for y in topemp['TopCompany']], n=1, cutoff=0.8) else ''
                    for x in jobs['JOBCOMPANY']]
    
    jobs.to_csv('/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output/AllPennJobs_wdata.csv', sep=",", index=False)
    
#STEP 4: SEPARATE LEADERSHIP FROM EXPERIENCE
def lead_from_exp():
    with open(exp_data_file, 'rU') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lines = list(reader)
    headers = lines[0]
    work_exp = [headers]
    headers.insert(0, "Club/Pos")
    leadership_exp = [headers]
    lines = lines[1:]
    filemap = make_map(lines)

    #Iterate over map and split up lines into exp and lead
    for fn in filemap.keys():
        print fn
        lead = get_leadership(fn)

        for exp in filemap[fn]:
            if len(exp) >= 5:
                org = exp[3].strip()
                if len(org) > 0 and org in lead:
                    if is_club(exp):
                        exp.insert(0, "TRUE")
                    else:
                        exp.insert(0, "FALSE")
                    leadership_exp.append(exp)
                else:
                    exp.insert(0, "FALSE")
                    work_exp.append(exp)

    with open('/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output/leadership_only.csv', 'wu') as f:
        wr = csv.writer(f, delimiter = ',')
        wr.writerows(leadership_exp)

    with open('/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output/work_exp_only.csv', 'wu') as f:
        wr = csv.writer(f, delimiter = ',')
        wr.writerows(work_exp)

#HELPER FUNCTION FOR LEAD_FROM_EXP
def make_map(lines):
    filemap = {}

    #Build map of each person's lines
    for line in lines:

        fn = line[0]
        #print filemap.keys()
        if fn not in filemap or filemap[fn] == None:
            filemap[fn] = [line]
        else:
            #print line
            filemap[fn].append(line)
    return filemap

#HELPER FUNCTION FOR LEAD_FROM_EXP
def get_leadership(fn):
    f = open(xml_path + fn)
    xml = f.read()
    soup = BeautifulSoup(xml)
    soup = soup.find('textresume')
    try:
        textresume = soup.get_text().encode('ascii', 'ignore')
    except Exception, e:
        print "Could not find textresume"
        return ""
    
    textresume = textresume.replace('\t', ' ')
    lines = textresume.split('\n')

    cont = True
    section = []
    for line in lines:
        words = line.split(' ')
        temp = []

        #Get rid of weird characters, making line too long - Yao_Kelly.xml
        for word in words:
            if not ((not word.isalpha()) or word == ''):
                temp.append(word)
        words = temp

        #Find probable heading rows and check if they match the keywords given
        if (len(words) <= 5 or (words[0].lower() in leadership)) and cont:
            for word in words:
                if word.lower() in leadership and cont:
                    #print "Found Section"
                    cont = False
                    section = get_section(lines[lines.index(line):])
    return section

#Helper function for lead_from_exp()
#Takes in the list of lines starting from the starting point
#Returns the list of lines up to the next header
def get_section(lines):
    cont = True
    for line in lines[1:]:
        words = line.split(' ')
        if (len(words) <= 5 or (words[0].lower() in headings)) and cont:
            for word in words:
                if word.lower() in headings and cont:
                    cont = False
                    index = lines.index(line)
    if cont: 
        index = len(lines)
    #Join lines together into one string
    ret = ''
    for line in lines[0:index]:
        ret = ret + line + '\n'

    return ret

#Helper function for lead_from_exp()
def is_club(exp):
    if 'club' in exp[3] or 'Club' in exp[3] or 'CLUB' in exp[3]:
        return True
    for job in job_list:
        if job in exp[7]:
            return True
    return False

#Step 5: Creates a separate file where work for money jobs are separated out
def work_for_money():
    with open(work_exp_file, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        jobs = list(reader)
        headers = jobs[0]
    
    f = open('/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output/WorkForMoneyJobs.csv', 'w')
    wr = csv.writer(f, delimiter = ',')
    
    wr.writerow(headers)
    
    for job in jobs[1:]:
        if job[20] == 'True':
            wr.writerow(job)
    csvfile.close()


def science_from_humanities():
    with open(work_exp_file, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        jobs = list(reader)
        headers = jobs[0]
    
    f = open('/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output/HumSoScJobs.csv', 'w')
    wr = csv.writer(f, delimiter = ',')
    j = open('/Users/cutlerreynolds/Dropbox/Resume-audit/Scraping Project/Output/ScienceJobs.csv', 'w')
    wr2 = csv.writer(j, delimiter = ',')
    
    wr.writerow(headers)
    wr2.writerow(headers)

    for job in jobs[1:]:
        if job[19] == 'Humanities' and job[20] == 'False': 
            wr.writerow(job)
        elif job[19] == 'Social Sciences' and job[20] == 'False':
            wr.writerow(job)
        elif job[19] == 'Computer Sciences/Engineering/Math' and job[20] == 'False':
            wr2.writerow(job)
        elif job[19] == 'Physical or Biological Science' and job[20] == 'False':
            wr2.writerow(job)


if __name__ == "__main__":
    parse_xml()
    print "Step 1 Complete"
    reshape()
    print "Step 2 Complete"
    job_info()
    print "Step 3 Complete"
    lead_from_exp()
    print "Step 4 Complete"
    work_for_money()
    science_from_humanities()
    print "Step 5 Complete"
            
            
            
            
            

