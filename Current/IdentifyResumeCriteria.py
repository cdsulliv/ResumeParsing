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
eduloc = '/Users/colin/Documents/ResumeParsing/Resume-Parsing/Data/edu/' 
#############################################################


if __name__ == "__main__":
    with open('HeaderSplitData.csv','rU') as in_file, open(eduloc+'EducationData.csv', 'r') as edudata, open("ResCriteria.csv", 'w') as out_file:
        csvwriter = csv.writer(out_file, delimiter=',')
        csvwriter.writerow(['FILENAME', 'HEADINGS', 'EDUCATION', 'EXPERIENCE', 'Leadership', 'Volunteer', 
            'Has Education', 'Has Work', 'Has Leadership or Volunteer', 'Has education, work, and leadership', 'Grad Date'])

        csvreader = csv.reader(in_file, delimiter=',')
        edureader = csv.reader(edudata)

        for line,eduline in zip(csvreader, edureader):
            if line[0] == 'FILENAME': continue # Don't write the column names again

            # Filenames must match between the two files
            assert line[0] == eduline[0]

            filename = line[0]
            headings = line[1]

            WorkExp = line[4]
            hasWorkExp = bool(WorkExp)

            LeadExp = line[5]
            VoluntExp = line[6]
            hasLeadership = bool(LeadExp or VoluntExp)

            edu = line[3]
            hasEdu = bool(edu)
   
            hasAll = bool(hasWorkExp and hasLeadership and hasEdu)

            gradDate = eduline[1]
                    
            row = [filename, headings, edu, WorkExp, LeadExp, VoluntExp, hasEdu, hasWorkExp, hasLeadership, hasAll, gradDate]
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
    