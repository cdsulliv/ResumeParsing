"""
This script takes CSV of resume elements and marks those meeting specific criteria.
"""

__author__ = "Colin Sullivan"

import re
from bs4 import BeautifulSoup
import csv
import ast
from preprocessor import preprocess 

############   Set variables to local machine   #############

# Location of output from education parsing
fileloc =  "/home/shreya/RA_ML/Resume-Parsing/Data/edu/Other/" 
#############################################################

def getGradDatesFromCSV(CSVname):    
    text = open(CSVname, "r").read()
    files = text.split("\n\n")
    file_year = {}
    for f in files[:-1]:          
        years = []
        file_content = f.split("\t\t")

        file_name = file_content[0].strip()

        dic = ast.literal_eval(file_content[1])    
        for univ in dic:
            value = dic[univ]
            for key in value:
                if key == 'associated_date':
                    date = value[key]
                    month_year = date.split(" ")
                    years.append(int(month_year[1]))

        if 2016 in years: 
            file_year[file_name] = 2016
        elif 2015 in years:
            file_year[file_name] = 2015    
        else:
            file_year[file_name] = None

        #break    
    return file_year



if __name__ == "__main__":
    with open('split_v.csv','rU') as in_file, open("ResCriteria.csv", 'w') as out_file:
        csvwriter = csv.writer(out_file, delimiter=',')
        csvwriter.writerow(['FILENAME', 'HEADINGS', 'EDUCATION', 'EXPERIENCE', 'Leadership', 'Volunteer', 
            'Has Education', 'Has Work', 'Has Leadership or Volunteer', 'Has education, work, and leadership'])

        csvreader = csv.reader(in_file, delimiter=',')

#        file_year = getGradDatesFromCSV(fileloc+"out_edu_split_v.txt")

        for line in csvreader:
            filename = line[0]
            headings = line[1]

            # Get grad dates - need to get from Education Parsing output

            WorkExp = line[4]
            hasWorkExp = bool(WorkExp)

            LeadExp = line[5]
            VoluntExp = line[6]
            hasLeadership = bool(LeadExp or VoluntExp)

            edu = line[3]
            hasEdu = bool(edu)
   
            hasAll = bool(hasWorkExp and hasLeadership and hasEdu)
                    
            row = [filename, headings, edu, WorkExp, LeadExp, VoluntExp, hasEdu, hasWorkExp, hasLeadership, hasAll]
            csvwriter.writerow(row)
                        
    with open('ResCriteria.csv','r') as in_file, open('ResCrit_NoDuplicates.csv','w') as out_file:
            csvreader = csv.reader(in_file, delimiter=',')
            csvwriter = csv.writer(out_file, delimiter=',')

            seen = set() 
            for line in csvreader:
                key = (line[1], line[2], line[3], line[4], line[5])

                if key not in seen:
                    csvwriter.writerow(line)
                    seen.add(key)
    