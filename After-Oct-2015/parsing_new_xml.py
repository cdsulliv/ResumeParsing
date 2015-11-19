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
from nltk.tag.stanford import NERTagger

possible_headers = ["EDUCATION", "EXPERIENCE", "PROFESSIONAL" , "ORGANIZATIONS", "MEMBERSHIPS", "LANGUAGE", "SKILLS", "HOBBIES","COMPUTER", "ACTIVITIES","INTERESTS"]

# def extract_email(soup):
#     return  soup.pdfx.article.email.string
#
# def extract_person_from_list(st,list_words):
#     found_flag = 0
#     list_ner = st.tag(list_words)
#     person = None
#     for tup in list_ner[0]:
#         if(tup[1] == "PERSON" and found_flag == 0):
#             person = tup[0]
#             found_flag = 1
#         elif(tup[1] == "PERSON" and found_flag == 1):
#             person = person +" " +tup[0]
#         elif(tup[1] != "PERSON" and found_flag == 1):
#             return person
#
#     return person


# def extract_possible_names(soup,st):
#
#     person_name = None
#     #First check the tile as name is found in the title
#     s = soup.pdfx.article.find('title-group').find('article-title').string
#     person_name = extract_person_from_list(st,s.split())
#     if person_name != None:
#         return person_name
#
#     #If name not found, then keep checking to the next sub header till the name is found
#     list_outsiders = soup.pdfx.article.find_all('outsider')
#     for word in list_outsiders:
#         # print "!!" + word.text
#         person_name = extract_person_from_list(st,word.text.split())
#         if person_name != None:
#             return person_name
#
#     return "NOT FOUND"

# def extract_edu(soup,st): #Will return a dict
#     edu_dict ={}
#     soup = soup.pdfx.article
#     text = soup.getText()
#     words = re.split(' |\n',text)
#     capital_words = []
#     for word in words:
#         if word.isupper():
#             capital_words.append(word.encode("UTF-8"))
#
#     i = -1
#     try:
#         i = capital_words.index("EDUCATION")
#     except:
#         return "NOT FOUND"
#     ll = capital_words[i+1:len(capital_words)-1]
#
#
#     next_word = None
#     for word in ll:
#         # print words
#         if word in possible_headers:
#             next_word = word
#             break
#
#     # print next_word
#     start_i = text.index("EDUCATION")
#     end_i = len(text)-1
#     if(next_word != None):
#         end_i = text.index(next_word)
#
#     list_ner = st.tag(text[start_i:end_i].split(" "))
#     print list_ner
#     univ = "" #Finding list of universities
#     found_flag = 0
#     cnt = 1
#     for tup in list_ner[0]:
#         if(tup[1] == "ORGANIZATION" and found_flag == 0):
#             univ = tup[0]
#             found_flag = 1
#         elif(tup[1] == "ORGANIZATION" and found_flag == 1):
#             univ = univ +" " +tup[0]
#         elif(tup[1] != "ORGANIZATION" and found_flag == 1):
#             new_edu = {}
#             new_edu["Name"] = univ
#             edu_dict[cnt] = new_edu
#             cnt = cnt+1
#             univ = ""
#             found_flag = 0
#
#     return edu_dict
    # return text[start_i:end_i]

    # print re.find("EDUCATION")
    # print words
    # print capital_words


EDU_KEYWORDS = ["university", "school"]
#helper function to check the keywords from the user made list
def keyword_present(words):
    for word in words:
        if word.strip(',.') in EDU_KEYWORDS:
            return True
    return False

# helper function to detect university using stanford nlp tagger
def st_tag_present(words,stagger):
    words = [word.strip(',.') for word in words]
    tagged_words = stagger.tag(words)
    print tagged_words
    for tup in tagged_words[0]:
        if tup[1] == "ORGANIZATION":
            return True
    return False
        # if(tups)
    pos = [y  for (x,y) in tagged_words if (x,y)]
    print pos
    if ("ORGANIZATION" in pos):
        return True
    return False


def extract_edu_info_new_xml(soup,stagger):
    arr = soup.findAll("text")
    #Cross verification step : First element should have education

    if "EDUCATION" not in arr[0].text:
        return "Error: Education section not present"

    arr.pop(0) #Removing heading which was 'education'
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
    print univ_list
    for key in univ_list:
        val = univ_list[key]
        pos = val["arr_pos"]
        # print pos
        for item in arr[pos:len(arr)]:
            print item.text
            item = item.text
            date = re.findall(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December|Sept)\s\d{4}', item)
            date_text = ""
            if date:
                date_text = date[0]
                exist_val = univ_list[key]
                exist_val["associated_date"] =  date_text
                univ_list[key] = exist_val
                break #Go to the next university to find its associated date


    return univ_list


def extract_name(soup,st):
    arr = soup.findAll("text")

    for ele in arr:
        text = ele.text;
        words = text.split(" ")
        words = [w.strip(",.") for w in words]
        tagged = st.tag(words)
        for tup in tagged[0]:
            if tup[1] == "PERSON": #If any of the tuple is person, return all the words
                return text.encode("UTF-8")


    return "No Name Found"


def extract_email(soup):
    arr = soup.findAll("text")

    for ele in arr:
        a = re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',ele.text.strip().encode("UTF-8"))
        if(a):
            return a.group(0)
    return "No Email Found"

def extract_phone(soup):
    re1 =  "^[1-9]\\d{2}-\\d{3}-\\d{4}$" # Case: 129-222-3333
    re2 =  "((\(\d{3}\) ?)|(\d{3}-))?\d{3}-\d{4}"  #Case: (234) 232-4244
    re3 = "^\D?(\d{3})\D?\D?(\d{3})\D?(\d{4})$" #Case: Both of the above two + 2324567891
    arr = soup.findAll("text")
    for ele in arr:
        a = re.match("|".join([re1, re2, re3]),ele.text.strip().encode("UTF-8")) #Combining Regexes
        if(a):
            return a.group(0)
    return "No Phone Found"





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



if __name__ == "__main__":
    # f = file("/home/sajal/Wharton/resumes/American University.xml","r").read()#Name, Univ and Email working good
    # f = file("/home/sajal/Wharton/resumes/Austin College 1.xml","r").read()#Name, Email working. Univ not able to extract
    # f = file("/home/sajal/Wharton/resumes/Bates College.xml","r").read() #Name, Univ and Email working good
    # f = file("/home/sajal/Wharton/resumes/Boise State Functional.xml","r").read() #Univ and Email working good. name not working.
    # soup = BeautifulSoup(f)
    # st = NERTagger('/home/sajal/Downloads/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','/home/sajal/Downloads/stanford-ner-2014-06-16/stanford-ner.jar')
    # email = extract_email(soup)
    # name = extract_possible_names(soup,st)
    # education = extract_edu(soup,st)
    # # print name
    # print education
    # # print email




    #New XML Parsing Starts here
    # f = file("/home/sajal/Wharton/code/After-Oct-2015/dummy_xml","r").read()
    # f = file("/home/sajal/Wharton/code/After-Oct-2015/dummy_2.xml","r").read()

    # soup = BeautifulSoup(f)
    # print soup
    # st = NERTagger('/home/sajal/Downloads/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','/home/sajal/Downloads/stanford-ner-2014-06-16/stanford-ner.jar')
    # print extract_edu_info_new_xml(soup,st)


    #Code for extracting info for heading
    f = file("/home/sajal/Wharton/code/After-Oct-2015/dummy_for_name_1.xml","r").read()
    soup = BeautifulSoup(f)
    st = NERTagger('/home/sajal/Downloads/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','/home/sajal/Downloads/stanford-ner-2014-06-16/stanford-ner.jar')
    print extract_person_info(soup,st)

