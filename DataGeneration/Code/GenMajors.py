"""
Generate a clean list of majors and STEM identifiers
"""

__author__ = "Colin Sullivan"

import numpy as np
import csv
import re

### Set output location
outputdir = '/Users/colin/Documents/ResumeParsing/Resume-Parsing/DataGeneration/DataFiles'

### Set location of input files: lists of CIP code majors and STEM majors ###
Majlist = '/Users/colin/Dropbox/Resume-audit/Scraping Project/Data Sources/CIPCode2010.csv'
STEMlist = '/Users/colin/Dropbox/Resume-audit/Scraping Project/Data Sources/STEMlist.csv'

### Get list of STEM majors              
with open(STEMlist, 'rU') as f:
    reader = csv.reader(f)
    reader.next()
    STEMmaj = np.array([row[1] for row in reader])

# Clean STEM majors
STEMmaj = [maj.replace(".", "") for maj in STEMmaj]   
STEMmaj = [maj.replace(", Other", "") for maj in STEMmaj]   
STEMmaj = [maj.replace(", General", "") for maj in STEMmaj]   
STEMmaj = [maj.replace("/Technicians", "") for maj in STEMmaj]   
STEMmaj = [maj.replace("/Technician", "") for maj in STEMmaj]   

STEMnp = np.unique(STEMmaj)


### Get full list of majors                
with open(Majlist, 'rU') as f:
    reader = csv.reader(f)
    reader.next()
    allmaj = np.array([row[4] for row in reader])

majorcats = [maj.title() for maj in allmaj if maj.isupper()]   

# Clean list of majors
allmaj = [maj.replace(".", "") for maj in allmaj]   
allmaj = [maj.replace(", Other", "") for maj in allmaj]   
allmaj = [maj.replace(", General", "") for maj in allmaj]   
allmaj = [maj.replace("/Technicians", "") for maj in allmaj]   
allmaj = [maj.replace("/Technician", "") for maj in allmaj]  
allmaj = [maj for maj in allmaj if not re.search("Residency", maj)]
allmaj = [maj.replace("  ", " ") for maj in allmaj]   
allmaj = [maj.title() if maj.isupper() else maj for maj in allmaj]
allmaj = [maj.replace("Management Sciences and Quantitative Methods", 
                      "Management Science and Quantitative Methods") for maj in allmaj]  


allmajnp = np.unique(allmaj)
isSTEM = [1 if maj in STEMnp else 0 for maj in allmajnp]
majors = np.vstack((allmajnp,isSTEM)).T
print majors


with open(outputdir+'/majors.csv', 'wb') as f: 
    w = csv.writer(f, delimiter=',')
    w.writerow(['Major', 'STEM'])
    w.writerows(majors)
