"""
This parses the skills section of all resumes into individual bullet points
"""

__author__ = "Colin Sullivan"

import numpy as np
import csv
from bs4 import BeautifulSoup
import re
import itertools

### Set location of input file: CSV of resumes split by section ###
datasplit = '/Users/colin/Documents/ResumeParsing/Resume-Parsing/Current/HeaderSplitData.csv'

# Function to flatten irregular list 
def flatten(foo):
    for x in foo:
        if hasattr(x, '__iter__'):
            for y in flatten(x):
                yield y
        else:
            yield x

def extract_skills(soup):
	texts = soup.findAll("text")
	return [t.text.encode('utf8') for t in texts if re.search('[a-zA-Z]', t.text)]


### Extract skills data from all resumes                
with open(datasplit, 'rb') as f:
    reader = csv.reader(f)
    datanp = np.array([row for row in reader])

# Log filename and skill set in a list of lists with differing lengths; flatten each element

skillz1 = [list(flatten([row[0], extract_skills(BeautifulSoup(row[7]))])) for row in datanp]
skillz2 = [[row[0], extract_skills(BeautifulSoup(row[7]))] for row in datanp]

# Write variable names 
maxvars = max([len(x) for x in skillz1])
varnames = ["Skill"+str(i) for i in range(1, maxvars)]
skillz1[0] = list(flatten(['FILENAME', varnames]))

print skillz1

with open('SkillData.csv', 'wb') as f: 
    w = csv.writer(f, delimiter=',')
    w.writerows(skillz1)


with open('SkillData_alt.csv', 'wb') as f: 
    w = csv.writer(f, delimiter=',')
    w.writerows(skillz2)
