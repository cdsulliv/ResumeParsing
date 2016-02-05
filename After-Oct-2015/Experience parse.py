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
import csv
from collections import Counter
import sys
csv.field_size_limit(sys.maxsize)


def split_from_prettified(array):
    # print array
    new_arr = []
    for entries in array:
        elements = entries.split("\n")
        new_arr.append(elements)

    return new_arr

def extract_exp(soup): #Handles experience section of ONE resume
    arr_lines = soup.findAll("text")

    #Create array of array of different work experience
    temp = []
    final_arr = []
    temp_str = ""
    for lines in arr_lines:
        # print str(lines)
        if '<b>' in str(lines) or '<i>' in str(lines):
            temp_str = temp_str + lines.prettify() + "\n"
            # prettified_text = lines.prettify() #Using prettify function to draw different entities on different lines
            # temp.append(prettified_text)
        else:
            if temp_str:
                final_arr.append(temp_str)
                temp_str = ""
        #     if(lines.text.strip(" ") != ""): #Excluding empty bold tags
        #         temp.append(lines.text.strip())
        # else:
        #     if temp:
        #         final_arr.append(temp)
        #         temp = []
    # if final_arr:
    #     print final_arr[0][0].prettify()

    return final_arr

def split_more(file_exp_pair):
    a = []
    for (file,val) in file_exp_pair: #val is an array of array
        new_arr = [] #This should also be an array of array which will replace val
        print new_arr
        for entries in val: #entries is an array of strings
            ins_arr = [] #This should be array of strings
            for sing_entry in entries:
                s = re.split(',|-',sing_entry.encode('utf-8'))
                ins_arr.extend(s)
            new_arr.append(ins_arr)
        tup = (file,new_arr)
        a.append(tup)

    return a


def extract_info(new_val,inp_arr,pos_list,states):#Main logic to extract different elements given an array of mixed items of experience

    items = len(inp_arr)
    done = []

    #Finding position. If found, deleting it from the array
    ind = 0;
    flag = 0;
    for item in inp_arr:
        words = item.split(" ")
        for word in words:
            if word in pos_list:
                new_val["position"] = item
                # inp_arr.remove(item)
                done.append(ind)
                flag =1
                break;
        if (flag ==1):
            break
        ind +=1

    #Finding date. If found, deleting it from the array
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

    #If remaining item is one, put that as the company name
    # if(len(inp_arr) == 1):
    #     new_val["company"] = inp_arr[0]
    #     inp_arr.remove(inp_arr[0])

    if (items - len(set(done)) == 1): #Only one element is unmarked
        for i in range(0,items):
            if i not in done:
                new_val["company"] = inp_arr[i]
                done.append(i)
                break



def arrange_exp_data(file_exp_pair):

    #Read glassdoor position list
    pos = open("position_list.txt","r").read().split("\n")
    pos_list = []
    for x in pos:
        arr = x.split(" ")
        [pos_list.append(b) for b in arr]

    pos_list = set(pos_list)

    #Read states
    f = open("states.csv").read()
    lines = f.split("\n")
    states = []

    for line in lines:
        pair = line.split(",")
        states.append(pair[0])
        states.append(pair[1])


    # file_exp_pair_new = split_more(file_exp_pair) #Currently not executing this logic

    file_exp_dict ={}
    final_arr = [] #Containing each entry =resume in form of dict with key = file each resume

    for pair in file_exp_pair:
        resume = {pair[0] : {}}
        arr_of_arr = pair[1]
        i = 1
        for entry in arr_of_arr:
            new_val = {"company" : "UNK", "location" : "UNK", "position" : "UNK", "date" : "UNK",  "all" : entry} # rem = array of remaining elements which are not in any attributes
            extract_info(new_val,entry,pos_list,states)
            dict = resume[pair[0]]
            dict["entry"+str(i)] = new_val
            i = i+1

        final_arr.append(resume)

    return final_arr

    #This was the old logic. Commenting for referencing at any later point.
    #for sing_exp in allexpdata:
    #     found_date = False
    #     found_comp = False
    #     found_pos = False
    #     exp = {}
    #
    #     exp_company = sing_exp[0] #Assuming first entry would be company name
    #     exp["company"] = exp_company
    #     found_comp = True
    #
    #     for entry in sing_exp:
    #         print entry
    #         date = re.findall(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December|Sept)\s', entry)
    #         if(date):
    #             exp["date"] = entry
    #             found_date = True
    #         if entry in pos_list:
    #             exp["position"] = entry
    #             found_pos = True
    #
    #     exp_arr.append(exp)



# f = open("experience_sample.txt").read()
# soup = BeautifulSoup(f)
# extract_exp(soup)

def clean_and_arrange(arr):
    ret_resume = []
    for resume in arr:
        cleaned_entry = []
        for exp_str in resume:
            b = re.split("\n|\s\s\s",exp_str) #split in three or more space or \n
            pure_b = []
            for lines in b:
                if "<b>" not in lines and "</b>" not in  lines and "<text" not in  lines and "<i>" not in  lines and "</i>" not in  lines and "/text>" not in  lines:
                    if(lines): #Dont enter empty lines
                        pure_b.append(lines.encode("utf-8").strip())
            cleaned_entry.append(pure_b)
        ret_resume.append(cleaned_entry)
    return ret_resume

#Code starts from here

files = ["split/split_v0","split/split_v50","split/split_v100","split/split_v150","split/split_v200","split/split_v250","split/split_v300","split/split_v350","split/split_v400","split/split_v450"]

for file_inp in files:
    # file_inp = "split/split_v0"
    with open(file_inp +'.csv', 'rb') as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    datanp = np.array(data)

    expsoups = [BeautifulSoup(row) for row in datanp[:,4]]
    allexpdata = np.array([extract_exp(soup) for soup in expsoups])
    filename = [row for row in datanp[:,0]]


    exp_array = clean_and_arrange(allexpdata)



    file_exp_pair = zip(filename,exp_array)


    fin_arr = arrange_exp_data(file_exp_pair)


    #Writing final output to csv file
    file_out = file_inp + "_out"
    with open(file_out+".csv", 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['filename','company-1', 'location-1','position-1','date-1', 'all-1', 'company-2', 'location-2','position-2','date-2', 'all-2', 'company-3', 'location-3','position-3','date-3', 'all-3','company-4', 'location-4','position-4','date-4', 'all-4',])
        for item in fin_arr:
            filename = item.keys()[0];
            towrite = [filename];
            if(item[filename]): #if dictionary is non empty
                val_dict = item[filename]

                if("entry1" in val_dict): #if this key is present
                    val_val_dict = val_dict["entry1"]
                    vals = [str(val_val_dict["company"]),str(val_val_dict["location"]),str(val_val_dict["position"]),str(val_val_dict["date"]),str(val_val_dict["all"])]
                    towrite.extend(vals)

                if("entry2" in val_dict): #if this key is present
                    val_val_dict = val_dict["entry2"]
                    vals = [val_val_dict["company"],val_val_dict["location"],val_val_dict["position"],val_val_dict["date"],val_val_dict["all"]]
                    towrite.extend(vals)

                if("entry3" in val_dict): #if this key is present
                    val_val_dict = val_dict["entry3"]
                    vals = [val_val_dict["company"],val_val_dict["location"],val_val_dict["position"],val_val_dict["date"],val_val_dict["all"]]
                    towrite.extend(vals)

                if("entry4" in val_dict): #if this key is present
                    val_val_dict = val_dict["entry4"]
                    vals = [val_val_dict["company"],val_val_dict["location"],val_val_dict["position"],val_val_dict["date"],val_val_dict["all"]]
                    towrite.extend(vals)

            writer.writerow(towrite)

