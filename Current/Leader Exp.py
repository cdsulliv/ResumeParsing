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

def extract_leadership(soup):
    lead_dict = {} #Keys : frat = [] , sports = [], sports captain = [], clubs and orgs = []

    arr = soup.findAll("text")
    print arr[16]
    frat_arr = []
    club_arr = []
    sports_arr = []
    sports_capt = []

    frat_regex = "\\b(pi|sigma|alpha|phi|omega|fraternity|delta|rho|kappa|beta|tau|epsilon|upsilon|psi|zeta|chi)\\b" #\b = word boundary
    club_regex = "\\b(club|org|organization)\\b"
    captatin_regex =  "\\b(captain|head)\\b"
    f = open("sports-list.txt").readlines()
    print f[7];
    sports = f[7:];
    sports[0] = "Baseball" #Handling one case which has not coming neatly
    sports = [x.strip("\\\n").lower() for x in sports]

    print sports


    for ele in arr:
        text = ele.text.lower()
        #Fraternity
        val = bool(re.search(frat_regex,text))
        if val:
            frat_arr.append(text)

        #Clubs and Organization
        val = bool(re.search(club_regex,text))
        if val:
            club_arr.append(text)


        #sports and sports captain
        val = False
        val_c = False
        for s in sports:
            if s in text:
                val = True
                val_c = bool(re.search(captatin_regex,text)) #If any sports is found, check if he/she was captain
                break  #Assuming the resume mentions one sports on single line
        if val:
            sports_arr.append(text)
        if val_c:
            sports_capt.append(text)



    #Putting all arrays into the dict
    lead_dict["frat"] = frat_arr
    lead_dict["club"] = club_arr
    lead_dict["sports"] = sports_arr
    lead_dict["sports_cap"] = sports_capt

    return lead_dict;



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


def preprocess(soup):
    soup,s_set = merge_sletters(soup)
    merge_toplines(soup,s_set)

    return soup





f = open("leader_exp_sample.txt").read()

samples = f.split("\n\n")


leadersoup = [BeautifulSoup(row) for row in samples]

preprocessed = [preprocess(row) for row in leadersoup]



print extract_leadership(preprocessed[3])