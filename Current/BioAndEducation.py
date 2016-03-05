
# coding: utf-8

# In[1]:

from __future__ import division
import os
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import FreqDist
import math
import re
import collections
import codecs
from bs4 import BeautifulSoup
from nltk.tag.stanford import StanfordNERTagger
#import nltk.tag.stanford as st

import os

import numpy as np
import sys
import csv
from collections import Counter
import dateutil.parser 

############   Set variables to local machine   #############
taggerloc_gz ='/Users/colin/Downloads/stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz'
taggerloc_jar ='/Users/colin/Downloads/stanford-ner-2015-04-20/stanford-ner.jar'
datasplit = '/Users/colin/Documents/ResumeParsing/Resume-Parsing/HeaderSplitData.csv'
statesfile = '/Users/colin/Documents/ResumeParsing/Resume-Parsing/Data/OutsideSources/states.csv'

# Writes 2 files:
# 1) education_raw.txt holds the raw education data as dictionaries for each education entry. This can be used for troubleshooting.
education_raw = '/Users/colin/Documents/ResumeParsing/Resume-Parsing/Data/edu/education_raw.txt'
# 2) EducationData.csv holds the clean data in CSV format. Decision rules have been introduced to get uniqueness.
EducationData = '/Users/colin/Documents/ResumeParsing/Resume-Parsing/Data/edu/EducationData.csv'
#############################################################

csv.field_size_limit(sys.maxsize)

EDU_KEYWORDS = ["university", "school", "college", "UC"]
#helper function to check the keywords from the user made list
def keyword_present(words):
    for word in words:
        if word.strip(',.') in [kw.capitalize() for kw in EDU_KEYWORDS ] + [kw.upper() for kw in EDU_KEYWORDS]:
            return True
    return False


def get_gpa(arr):
    text = [ele.text for ele in arr]
    gpa = [re.findall("\d+.\d+", line) for line in text if re.search("GPA|Grade Point Average|G.P.A.", line)]
    if gpa:
        return gpa[0][0]
    else:
        return "No GPA found"


def get_deanslist(arr):
    text = [ele.text for ele in arr]
    deans = any([re.match("Dean's List|Deans List|Dean's list|dean's list", line) for line in text])
    return deans


def extract_edu_info(soup):
    #print soup
    arr = soup.findAll("text")
    
    univ_list = {}
    arr_ind = 0;
    for ele in arr:
        text = ele.text
        # print text
        words = text.split(" ")
    
        if (keyword_present(words)):
            univ_list[text] = {"arr_pos" : arr_ind}; #Storing the position in the array in order to help in Date finding

        arr_ind = arr_ind +1;

    f = open(statesfile).read()
    lines = f.split("\n")
    abbr_st = []
    full_st = []

    for line in lines:
        pair = line.split(",")
        abbr_st.append(pair[0])
        full_st.append(pair[1])


    #Once we find all the university list, we iterate over the keys and find the nearest date found.
    #print univ_list
    for key in univ_list:
        val = univ_list[key]
        pos = val["arr_pos"]
        # print pos
        #Checking dates
        for item in arr[pos:len(arr)]:
            #print item.text
            item = item.text


            date = re.findall(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December|Sept)\s\d{4}', item)
            date_text = ""
            print date
            if date:
                if len(date)==2:
                    date_text = date[1]
                else:    
                    date_text = date[0]
                exist_val = univ_list[key]
                exist_val["associated_date"] =  date_text
                univ_list[key] = exist_val
                break #Go to the next university to find its associated date

        #Checking GPA
        for item in arr[pos:len(arr)]:
            #print item.text
            item = item.text
            gpa = re.findall(r'(GPA|Grade Point Average|G.P.A)[\s|:|-]*(\d+.?\d*)',item);
            if gpa:
                gpa_text = gpa[0][1]
                exist_val = univ_list[key]
                exist_val["GPA"] = gpa_text
                univ_list[key] = exist_val
                break

        #Checking Location

        for item in arr[pos:len(arr)]:
            #print item.text
            item = item.text
            for a,b in zip(abbr_st,full_st):
                if " "+a in item or "," +a in item or ", "+a in item or b in item: #so that error cases like "GPA" is not interpreted as PA
                    st_name = ""
                    if a in item:
                        ind = abbr_st.index(a)
                        st_name = full_st[ind]
                    if b in item:
                        st_name = b

                    exist_val = univ_list[key]
                    exist_val["loc"] = st_name
                    univ_list[key] = exist_val
                    break;




    #Misc Items from here
    deanslist = get_deanslist(arr)
    univ_list["Misc"] = {"deanslist":deanslist}

    return univ_list



    # gpa = get_gpa(arr)

    # return [{'UniversityList': univ_list}, {"gpa": gpa}, {"deanslist": deanslist}]


# In[8]:

### Should make this robust to mistakes. For instance, if tagged is empty this returns errors

def extract_name(soup,st):
    arr = soup.findAll("text")

    for ele in arr:
        text = ele.text;
        words = text.split(" ")
        words = [w.strip(",.") for w in words]
        tagged = st.tag(words)
        for tup in tagged: # CDS CHANGED: for tup in tagged[0]:
            if tup[1] == "PERSON": #If any of the tuple is person, return all the words
                return text.encode("UTF-8")

    return "No Name Found"


# In[9]:

#CDS: Changed both functions from re.match() to re.search to find matches in the middle of lines

def extract_email(soup):
    arr = soup.findAll("text")

    for ele in arr:
        a = re.search('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',ele.text.strip().encode("UTF-8")) 
        if(a):
            return a.group(0)
    return "No Email Found"

def extract_phone(soup):
    re1 = "(\()*\d{3}(\)| |-|\.)*\d{3}(-| |\.)*\d{4}"
    arr = soup.findAll("text")
    for ele in arr:
        a = re.search(re1,ele.text.strip().encode("UTF-8")) #Combining Regexes
        if(a):
            return a.group(0)
    return "No Phone Found"


# In[10]:

def extract_person_info(soup,st):
    info_map = {}
    #Extracting Email
    email = extract_email(soup)
    info_map["email"] = email;

    #Extracting Phone Number:
    phone_no = extract_phone(soup)
    info_map["phone"] = phone_no;

    #Extracting Name:
    name = extract_name(soup,st)
    info_map["name"] = name;

    return info_map


# In[11]:

st = StanfordNERTagger(taggerloc_gz, taggerloc_jar)


# # Preprocessing

# In[454]:

def merge_sletters(soup):
    # Merge single letters with the following line
    jointext = ""
    s_set = set([])
    for line in soup.findAll("text"):
        if(jointext): 
            if(bool(line.contents)):

                if(line.contents[0].string):
                    fixed_text = jointext+line.contents[0].string
                    line.contents[0].replace_with(fixed_text)   
            jointext = ""
        if(len(line.text)==1):
            # print line.text
            s_set.add(line["top"])
            jointext = line.text
        else:
            if(line["top"] in s_set):
                s_set.remove(line["top"])
    return soup,s_set


# In[330]:

def merge_toplines(soup,s_set):
    #Merge multiple lines with same top height
    tops = [line['top'] for line in soup.findAll('text')]

    tops_red = []

    for x in tops:
        if x in s_set:
            tops_red.append(x)
    print tops_red
    topcounts = { key:value for key,value in Counter(tops_red).items() if value>1 }
    ctr = {key:1 for key in topcounts}
    texts = {key:"" for key in topcounts}
    last_text=''

    for line in soup.findAll("text"):
        cur_top = line['top']

        if(str(cur_top) in topcounts):
            if(ctr[str(cur_top)] == topcounts[str(cur_top)]):
                fixed_text = unicode(line.text).replace(line.text, texts[str(cur_top)]+line.text)
                if(line.contents):
                    line.contents[0].replace_with(fixed_text)   
                #last_text = ""
            elif(ctr[str(cur_top)] < topcounts[str(cur_top)]):
                texts[str(cur_top)] = texts[str(cur_top)]+line.text
                line.extract()
                ctr[str(cur_top)] = ctr[str(cur_top)]+1
    return soup


# In[434]:

# Change this: should only merge_toplines on lines that had single-letter changes
def preprocess(soup):
    soup,s_set = merge_sletters(soup)
    print s_set
    merge_toplines(soup,s_set)
  
    return soup


### Extract education data from all resumes                
with open(datasplit, 'rb') as f:
    reader = csv.reader(f)
    datanp = np.array([row for row in reader])

#filename = [row for row in datanp[:,0]]
#filename = []
#for i in range(len(datanp)):
#    filename.append(datanp[i][0]) 

#prepedu = []
#for i in range(len(datanp)):
#    prepedu.append(BeautifulSoup(datanp[i][3]))

filenames = [row[0] for row in datanp]
assert len(filenames) == datanp.shape[0]

#prepedu = [preprocess(BeautifulSoup(row)) for row in datanp[:,3]]

# Extract education data into a list of dictionaries. Add the filename as a dictionary element 
edudata = np.array([extract_edu_info(BeautifulSoup(row[3])) for row in datanp])
for rowdata, filename in zip(edudata, filenames):
     rowdata['filename'] = filename


# Write all raw education data to txt file for records.
file_o = open(education_raw,"wb")
i = 0 #counter over filenames
for entry in edudata:
    file_o.write(filenames[i] + "\t\t" + str(entry))
    file_o.write("\n\n")
    i +=1

# Convert raw education data into clean CSV

with open(EducationData,'w') as out_file:
    csvwriter = csv.writer(out_file, delimiter=',')
    csvwriter.writerow(['FILENAME', 'Graduation Year', 'Degree Type', 'Major', 'GPA', 'Deans List', 'Flag: two dates'])


    for adic in edudata[1:]:

        # Get all education dictionaries within the dictionary, and capture information
        list_of_schools = []; gpas = []; graddates = []
        for key, value in adic.iteritems() :
            if key not in ['Misc', 'filename']:
                list_of_schools.append([key])
                if 'GPA' in value:
                    gpas.append(value['GPA'])
                if 'associated_date' in value:
                    graddates.append(value['associated_date'])

        # Collect year from different possible graduation dates
        gradyears = [dateutil.parser.parse(date).year for date in graddates]
        twodatesflag = (len(graddates) > 1)

        # Decision rules: use MAXIMUM GPA and MAXIMUM graduation date
        try:
            gradyear = max(gradyears)
        except:
            gradyear = None

        try:
            GPA = max(gpas)
        except:
            GPA = None

        filename = adic['filename']
        degreetype = "DEGREE PLACEHOLDER"
        major = "MAJOR PLACEHOLDER"
        deanslist = adic['Misc']['deanslist']

        row = [filename, gradyear, degreetype, major, GPA, deanslist, twodatesflag] 
        csvwriter.writerow(row)








