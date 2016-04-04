import re
import csv
import numpy as np

############   Set variables to local machine   #############
stateabbrevfile = '/Users/colin/Documents/ResumeParsing/Resume-Parsing/Data/OutsideSources/StateAbbreviations.csv'
#############################################################


# Define time regexes and location regexes
months = "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
seasons = "Spring", "Summer", "Fall", "Autumn", "Winter"

with open(stateabbrevfile, 'rb') as f:
    states = np.array([row for row in csv.reader(f.read().splitlines())])
abbrevs = '|'.join(['^' + x + '$' for x in states[1:,1]])
fullstate = '|'.join(['^' + x.title() + '$' for x in states[1:,0]])

def islocation(txt):
    txt = ''.join(e for e in txt if e.isalnum())
    regx = re.search(re.compile(abbrevs),txt)
    return (regx is not None)


def isdate(txt):
    ismonth = (True in [i in txt for i in months] )
    isyear = re.search(re.compile('20..'), txt) is not None
    isseason = (True in [i in txt for i in seasons])
    ispresent = re.search('Present|present', txt) is not None
    return (ismonth or isyear or isseason or ispresent)


def iscompany(txt):
    return (re.search("Inc|Corp|Ltd|LLC", txt) is not None)


# Main splitting function. Splits text at delimiters, without splitting dates, locations, or company names
def textsplit(txt):
    nosplit = []
    # Split the text into separate sections. Identify all delimiters here
    delims = "-|,|\(|\)|u'\u2013'"
    splitted = re.split(delims,txt)
    dellist = [x for i, x in enumerate(txt) if x in [',', '-', '(', ')', u'\u2013']]

    # Identify the index of locations, dates, and company names that should not be split
    # Locations
    locs = [islocation(x) for x in splitted]

    if True in locs and dellist:
        nosplit = [locs.index(True) - 1]
    print(nosplit)
    # Dates
    aredates = [isdate(x) for x in splitted]
    dateindices = [i for i, x in enumerate(aredates) if x == True]
    if len(dateindices)>1:
        if dateindices[1] == dateindices[0] + 1:
            nosplit.append(dateindices[0])
            joined = '-'.join(e for e in splitted[dateindices[0]:dateindices[1]+1])
            print(joined)
    # Company Names
    comps = [iscompany(x) for x in splitted]
    if True in comps and dellist:
        nosplit.append(comps.index(True) - 1)

    # Re-join select elements, and keep a list of them
    joined = [dellist[idx].join(e for e in splitted[idx:(idx+2)]) for idx in nosplit]
    used = [i+1 for i in nosplit] + nosplit

    notjoined = [j for idx, j in enumerate(splitted) if idx not in used]

    output = joined + notjoined

    return(output)