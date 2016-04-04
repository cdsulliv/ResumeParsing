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
from split_smartly import textsplit
import os
from unidecode import unidecode

import numpy as np
import csv
from collections import Counter
import sys
csv.field_size_limit(sys.maxsize)


############   Set variables to local machine   #############
inputfile = '/Users/colin/Documents/ResumeParsing/Resume-Parsing/Current/HeaderSplitData.csv'
outputfile = '/Users/colin/Documents/ResumeParsing/Resume-Parsing/Data/Leadership.csv'
dataloc = '/Users/colin/Documents/ResumeParsing/Resume-Parsing/Data/OutsideSources/'

positlist = dataloc + "leadership_positions.txt"
statelist = dataloc + "states.csv"
sportslist = dataloc + 'sports-list.txt'
#############################################################



def extract_lead(soup): #Handles leadership section of ONE resume
    arr_lines = soup.findAll("text")

    #Create array of array of different work leadership
    final_arr = []; bullet_arr = []
    temp_str = ""; bulletstr = ""
    for lines in arr_lines:
        # print str(lines)
        if '<b>' in str(lines) or '<i>' in str(lines):
            temp_str = temp_str + lines.prettify() + "\n"
            if bulletstr:
                bullet_arr.append(bulletstr)
                bulletstr = ""
        else:
            bulletstr = bulletstr + lines.prettify() + "\n"
            if temp_str:
                final_arr.append(temp_str)
                temp_str = ""

    return (final_arr, bullet_arr)


def extract_info(new_val,inp_arr):#Main logic to extract different elements given an array of mixed items of leadership

    items = len(inp_arr)
    done = []

    #Find position. If found, deleting it from the array
    #Read glassdoor position list
    pos = open(positlist,"r").read().split("\n")
    
    pos_list = [x.lower() for x in pos]

    pos_list = set(pos_list)
    ind = 0;
    flag = 0;
    for item in inp_arr:
        words = item.split(" ")
        if any([word.lower() for word in words if word.lower() in pos_list]):
            new_val["position"] = item
            # inp_arr.remove(item)
            done.append(ind)
            flag =1
            break;
        if (flag ==1):
            break
        ind +=1

    #Find date. If found, deleting it from the array
    ind = 0;
    for item in inp_arr:
        date = re.findall(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December|Sept)\s|\b(19|20)\d{2}\b', item)
        if(date):
            new_val["date"] = item
            # inp_arr.remove(item)
            done.append(ind)
            break;
        ind +=1

    #Finding location. If found, deleting it from the array
    
    #Read states
    f = open(statelist).read()
    lines = f.split("\n")
    states = []

    for line in lines:
        pair = line.split(",")
        states.append(pair[0])
        states.append(pair[1])

    
    flag = 0
    ind = 0;
    for item in inp_arr:
        for st in states:
            if(len(st) ==2): #If abbreviation
                if " "+st in item or "," +st in item or ", "+st in item:
                    new_val["location"] = item
                    # inp_arr.remove(item)
                    done.append(ind)
                    flag =1
                    break;
            else:
                if st in item:
                    new_val["location"] = item
                    # inp_arr.remove(item)
                    done.append(ind)
                    flag =1
                    break;
        if flag ==1:
            break
        ind +=1
        
    # Identify organization names
    sports = open(sportslist).read().splitlines()
    #sports = [x.lower() for x in sports]
    sports = "|".join(sports)

    greek = "\\b(Alpha|Beta|Gamma|Delta|Epsilon|Zeta|Eta|Theta|Iota|Kappa|Lambda|Mu|Nu|Xi|Omicron|Pi|Rho|Sigma|Tau|Upsilon|Phi|Chi|Psi|Omega)\\b"
   
    prob_organization = "University|College|Board|Institute|America|Fellowship|Scouts|Committee|Association|Church|Bank|Drive|Club|Organization|Students|Service|Trip|Society|Marathon|Alliance|" + greek + "|" + sports
    for item in inp_arr:    
        comp = re.findall(prob_organization, item)
        if(comp):
            new_val["organization"] = item
            break;
    
    if (items - len(set(done)) == 1): #Only one element is unmarked
        for i in range(0,items):
            if i not in done:
                new_val["organization"] = inp_arr[i]
                done.append(i)
                break



def arrange_lead_data(atuple, numbullets):
    filename = atuple[0]
    titleinfo = atuple[1]
    bullets = ['<li>' + bul + '</li>' for bul in atuple[2]]
    
    # Create a separate dictionary for bullet points. Must all be the same length (pad with empty '')
    bvarnames = ['bullet' + str(x) for x in range(1,numbullets+1)]
    vals = bullets + [''] * (numbullets - len(bullets))
    bdict = {key: val for key,val in zip(bvarnames, vals)}
    
    new_val = {"filename":filename, "organization" : "UNK", "location" : "UNK", "position" : "UNK", "date" : "UNK", 
               "all" : str(titleinfo), "bullets": str(bullets)}  
    
    new_val.update(bdict)
    
    extract_info(new_val, titleinfo)
    return(new_val)
    
    

def clean_and_arrange(arr):
    ret_resume = []
    for resume in arr:
        cleaned_entry = []
        for lead_str in resume:
            b = re.split("\n|\s\s\s",lead_str) #split in three or more space or \n
            pure_b = []
            for lines in b:

                if "<b>" not in lines and "</b>" not in  lines and "<text" not in  lines and "<i>" not in  lines and "</i>" not in  lines and "/text>" not in  lines:
                    if(lines) and len(unidecode(lines).strip()) > 1: #Dont enter empty lines and single character lines
                        #Here calling the function written by Colin
                        print(lines)
                        splitted_arr = textsplit(lines)
                        for x in splitted_arr:
                            # pure_b.append(lines.encode("utf-8").strip(" ,.-!"))
                            pure_b.append(unidecode(x).strip(" ,.-!"))
            cleaned_entry.append(pure_b)
        ret_resume.append(cleaned_entry)
    return ret_resume



### Code starts from here ###
with open(inputfile, 'rbU') as f:
    reader = csv.reader(f)
    data = [row for row in reader]
datanp = np.array(data)

leadsoups = [BeautifulSoup(row) for row in datanp[:,5]]
allleaddata = np.array([extract_lead(soup) for soup in leadsoups])
leadtitles = [x[0] for x in allleaddata]
leadbullets = [x[1] for x in allleaddata]
filename = [row for row in datanp[:,0]]

bulltext = []
for ares in leadbullets:
    res = []
    restext = [BeautifulSoup(x).findAll("text") for x in ares]
    for t in restext:
        temp = filter(None, re.split(u"\u2022|\uf0b7|\uf097|\uf0a7", ''.join([x.text.replace('\n', '') for x in t])))
        res.append([unidecode(x.strip()) for x in temp if len(unidecode(x.strip())) > 1])

    bulltext.append(res)
maxbull = len(max(bulltext,key=len))

lead_array = clean_and_arrange(leadtitles) 
    
# Create an array of tuples: (filename, work header array, bullet array) for each job
# Multiple lines for each resume if it has multiple jobs
flattened = []
for f, leadarr, bull in zip(filename, lead_array, bulltext):
    flattened.append([(f, x, b) for x,b in zip(leadarr, bull)])
flattened = [item for sublist in flattened for item in sublist]

fin_arr = [arrange_lead_data(flat, maxbull) for flat in flattened]


keys = fin_arr[0].keys()
with open(outputfile, 'wb') as csvfile:
    dict_writer = csv.DictWriter(csvfile, keys)
    dict_writer.writeheader()
    dict_writer.writerows(fin_arr)


    

    
    	
