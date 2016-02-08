import re
import csv
import numpy as np

# Define time regexes and location regexes
months = "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
seasons = "Spring", "Summer", "Fall", "Autumn", "Winter"

with open('StateAbbreviations.csv', 'rb') as f:
    states = np.array([row for row in csv.reader(f.read().splitlines())])
abbrevs = states[1:,1]

def isdate(txt):
    ismonth = (True in [i in txt for i in months] )
    isyear = re.search(re.compile('20..'), txt) is not None
    isseason = (True in [i in txt for i in seasons])
    return (ismonth or isyear or isseason)

def islocation(txt):
    txt = ''.join(e for e in txt if e.isalnum())
    return (txt in abbrevs)

def iscompany(txt):
    return (re.search("Inc|Corp|Ltd|LLC", txt) is not None)


# Main splitting function. Splits text at delimiters, without splitting dates, locations, or company names
def textsplit(txt):
    nosplit = []
    # Split the text into separate sections. Identify all delimiters here
    delims = '-|,'
    splitted = re.split(delims,txt)
    dellist = [x for i, x in enumerate(txt) if x in [',', '-']]

    # Identify the index of locations, dates, and company names that should not be split
    # Locations
    locs = [islocation(x) for x in splitted]
    if True in locs:
        nosplit = [locs.index(True) - 1]

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
    if True in comps:
        nosplit.append(comps.index(True) - 1)

    # Re-join select elements, and keep a list of them
    joined = [dellist[idx].join(e for e in splitted[idx:(idx+2)]) for idx in nosplit]
    used = [i+1 for i in nosplit] + nosplit

    notjoined = [j for idx, j in enumerate(splitted) if idx not in used]

    output = joined + notjoined

    return(output)