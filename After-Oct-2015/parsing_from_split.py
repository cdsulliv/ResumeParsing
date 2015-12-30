
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
#java_path = "C:/Program Files/Java/jdk1.8.0_65/bin/java.exe"
#os.environ['JAVAHOME'] = java_path

import numpy as np
import csv
from collections import Counter


# For sending text message
import smtplib


# In[2]:

possible_headers = ["EDUCATION", "EXPERIENCE", "PROFESSIONAL" , "ORGANIZATIONS", "MEMBERSHIPS", "LANGUAGE", "SKILLS", "HOBBIES","COMPUTER", "ACTIVITIES","INTERESTS"]


# In[3]:

EDU_KEYWORDS = ["university", "school", "college", "UC"]
#helper function to check the keywords from the user made list
def keyword_present(words):
    for word in words:
        if word.strip(',.') in [kw.capitalize() for kw in EDU_KEYWORDS ] + [kw.upper() for kw in EDU_KEYWORDS]:
            return True
    return False


# In[4]:

def get_gpa(arr):
    text = [ele.text for ele in arr]
    gpa = [re.findall("\d+.\d+", line) for line in text if re.search("GPA|Grade Point Average|G.P.A.", line)]
    if gpa:
        return gpa[0][0]
    else:
        return "No GPA found"


# In[5]:

def get_deanslist(arr):
    text = [ele.text for ele in arr]
    deans = bool([re.match("Dean's List|Deans List|Dean's list|dean's list", line) for line in text])
    return deans


# In[6]:

# Modularize this function - should collect all univ info using separate functions

def extract_edu_info_new_xml(soup,stagger):
    #print soup
    arr = soup.findAll("text")
    #Cross verification step : First element should have education

    #if "EDUCATION" not in arr[0].text:
    #    return "Error: Education section not present"

    #arr.pop(0) #Removing heading which was 'education'
    univ_list = {}
    arr_ind = 0;
    for ele in arr:
        text = ele.text
        # print text
        words = text.split(" ")

        if (keyword_present(words) or st_tag_present(words,stagger)):
            univ_list[text] = {"arr_pos" : arr_ind}; #Storing the position in the array in order to help in Date finding

        arr_ind = arr_ind +1;
    #Once we find all the university list, we iterate over the keys and find the nearest date found.
    #print univ_list
    for key in univ_list:
        val = univ_list[key]
        pos = val["arr_pos"]
        # print pos
        for item in arr[pos:len(arr)]:
            #print item.text
            item = item.text
            date = re.findall(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December|Sept)\s\d{4}', item)
            date_text = ""
            if date:
                date_text = date[0]
                exist_val = univ_list[key]
                exist_val["associated_date"] =  date_text
                univ_list[key] = exist_val
                break #Go to the next university to find its associated date

    gpa = get_gpa(arr)
    deanslist = get_deanslist(arr)
    return [univ_list, {"gpa": gpa}, {"deanslist": deanslist}]


# In[7]:

def extract_edu_info_alt(soup):
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

    f = open("states.csv").read()
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
            if date:
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

st = StanfordNERTagger('/Users/sajal/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','/Users/sajal/stanford-ner-2014-06-16/stanford-ner.jar')


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


# # Extract data from all resumes



#CODE START FROM HERE

with open('split_v3.csv', 'rb') as f:
    reader = csv.reader(f)
    data = [row for row in reader]
datanp = np.array(data)



# Drop useless resumes!
droplist = "|".join(['FILENAME', 'Wichita State University'])
boolz = [not bool(re.match(droplist, x[0])) for x in datanp]
subs = np.where(boolz)
datanp = datanp[subs]


# ### Check analysis of bio data


biosoups = [BeautifulSoup(row) for row in datanp[:,2]]
preprocessed = [preprocess(row) for row in biosoups]
allbiodata = np.array([extract_person_info(soup, st) for soup in preprocessed])
filename = [row for row in datanp[:,0]]

# np.save("bioparsed", allbiodata)
# print allbiodata

i = 0

file_o = open("out_bio.txt","wb")
for entry in allbiodata:
    file_o.write(filename[i] + "\t\t" + str(entry))
    file_o.write("\n\n")
    i +=1



prepedu = [preprocess(BeautifulSoup(row)) for row in datanp[:,3]]

edudata_alt = np.array([extract_edu_info_alt(row) for row in prepedu])

i = 0

file_o = open("out_edu_2.txt","wb")
for entry in edudata_alt:
    file_o.write(filename[i] + "\t\t" + str(entry))
    file_o.write("\n\n")
    i +=1





#
# with open('eggs.csv', 'wb') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=' ')
#     for entry in edudata_alt:
#         spamwriter.writerow(filename[i] + "\t" + str(entry))
#         i +=1


# # Issues

# * It's sooooooo slow! We need to remove the Stanford Tagger wherever possible. How can we speed up the tagger?
#     * Could try it in batches: nltk.tag.stanford.POSTagger.tag_sents()
# ## Checks:
# * Verify reliability of BIO parsing
# * Verify reliability of EDU parsing

# In[75]:

#
# server = smtplib.SMTP( "smtp.gmail.com", 587 )
# server.ehlo()
# server.starttls()
# server.login( 'cdsulliv@gmail.com', 'FL3XTH15' )
# server.sendmail( 'Colin', '3123163086@att.txt.net', 'CODE FINISHED RUNNING' )


# In[68]:



# Brown University 9 education section shouldn't contain this:
# 
#  [ {u' !Organized a black-tie fundraiser for Gulf Coast Oil Spill victims. ': {'arr_pos': 9}, u' !Courses Include: Introduction to Environmental Studies, Biology of Plants, Food and People, Foundation of Living Introduction to Environmental Studies, Biology of Plants, Food and People, Foundation of Living Introduction to Environmental Studies, Biology of Plants, Food and People, Foundation of Living ': {'arr_pos': 1, 'associated_date': u'June 2010'}, u'Los Alamitos High School, High School Diploma Los Alamitos, CA \u2013 Graduated June 2010 ': {'arr_pos': 4, 'associated_date': u'June 2010'}, u' !Provide free SAT preparatory classes for local high school students. ': {'arr_pos': 19}, u'Los Alamitos Unified School District, Teacher\u2019s Aide Los Alamitos, CA \u2013 Summer 2010 ': {'arr_pos': 14}, u'Ecofficiency.org, Intern  Costa Mesa, CA \u2013 Summer 2010  ': {'arr_pos': 8}}

# In[51]:




# In[38]:

# len(newdata)
#
#
# # In[59]:
#
# print drop2
# print newdata[178]
# bool(re.match(drop2, newdata[178]))
# #print datanp[178]
#
#
# # In[338]:
#
# # Remove files that don't contain useful information
# droplist = "|".join(['FILENAME', 'Wichita State University'])
#Error
# datanp = datanp[re.match(droplist, x) for x in datanp[:,0]]


# In[ ]:

# a= [re.match(droplist, x) for x in datanp[:,0]]
# print a


# In[176]:

#FAILED PREPROCESS STEP
# def preprocess(soup):
#     # Merge single letters with the following line
#     jointext = ""
#     for line in soup.findAll("text"):
#         if(jointext):
#             if(bool(line.contents)):
#                 fixed_text = unicode(line.text).replace(line.text, jointext+line.text)
#                 line.contents[0].replace_with(fixed_text)
#
#             jointext = ""
#         if(len(line.text)==1 and not line.text.isspace()):
#             #print line.text
#             jointext = line.text
#             line.extract()
#
#     # Merge multiple lines with same top height
#     tops = [line['top'] for line in soup.findAll('text')]
#     topcounts = { key:value for key,value in Counter(tops).items() if value>1 }
#     ctr = 1
#     last_text=""
#     for line in soup.findAll("text"):
#         cur_top = line['top']
#
#         if(str(cur_top) in topcounts):
#             if(ctr == topcounts[str(cur_top)]):
#                 fixed_text = unicode(line.text).replace(line.text, last_text+line.text)
#                 if(line.contents):
#                     line.contents[0].replace_with(fixed_text)
#                 else:
#                     line.contents.append(fixed_text)
#                 last_text = ""
#                 ctr = 1
#             elif(ctr < topcounts[str(cur_top)]):
#                 last_text = last_text+line.text
#                 line.extract()
#                 ctr = ctr+1
#
#     return soup


# In[ ]:



