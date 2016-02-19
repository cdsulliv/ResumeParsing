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

def extract_email(soup):
    return  soup.pdfx.article.email.string

def extract_person_from_list(st,list_words):
    found_flag = 0
    list_ner = st.tag(list_words)
    person = None
    for tup in list_ner[0]:
        if(tup[1] == "PERSON" and found_flag == 0):
            person = tup[0]
            found_flag = 1
        elif(tup[1] == "PERSON" and found_flag == 1):
            person = person +" " +tup[0]
        elif(tup[1] != "PERSON" and found_flag == 1):
            return person

    return person


def extract_possible_names(soup,st):

    person_name = None
    #First check the tile as name is found in the title
    s = soup.pdfx.article.find('title-group').find('article-title').string
    person_name = extract_person_from_list(st,s.split())
    if person_name != None:
        return person_name

    #If name not found, then keep checking to the next sub header till the name is found
    list_outsiders = soup.pdfx.article.find_all('outsider')
    for word in list_outsiders:
        # print "!!" + word.text
        person_name = extract_person_from_list(st,word.text.split())
        if person_name != None:
            return person_name

    return "NOT FOUND"

def extract_edu(soup,st): #Will return a dict
    edu_dict ={}
    soup = soup.pdfx.article
    text = soup.getText()
    words = re.split(' |\n',text)
    capital_words = []
    for word in words:
        if word.isupper():
            capital_words.append(word.encode("UTF-8"))

    i = -1
    try:
        i = capital_words.index("EDUCATION")
    except:
        return "NOT FOUND"
    ll = capital_words[i+1:len(capital_words)-1]
    print ll

    next_word = None
    for word in ll:
        # print words
        if word in possible_headers:
            next_word = word
            break

    # print next_word
    start_i = text.index("EDUCATION")
    end_i = len(text)-1
    if(next_word != None):
        end_i = text.index(next_word)

    list_ner = st.tag(text[start_i:end_i].split(" "))
    print list_ner
    univ = "" #Finding list of universities
    found_flag = 0
    cnt = 1
    for tup in list_ner[0]:
        if(tup[1] == "ORGANIZATION" and found_flag == 0):
            univ = tup[0]
            found_flag = 1
        elif(tup[1] == "ORGANIZATION" and found_flag == 1):
            univ = univ +" " +tup[0]
        elif(tup[1] != "ORGANIZATION" and found_flag == 1):
            new_edu = {}
            new_edu["Name"] = univ
            edu_dict[cnt] = new_edu
            cnt = cnt+1
            univ = ""
            found_flag = 0

    return edu_dict
    # return text[start_i:end_i]

    # print re.find("EDUCATION")
    # print words
    # print capital_words

if __name__ == "__main__":
    # f = file("/home/sajal/Wharton/resumes/American University.xml","r").read()#Name, Univ and Email working good
    # f = file("/home/sajal/Wharton/resumes/Austin College 1.xml","r").read()#Name, Email working. Univ not able to extract
    # f = file("/home/sajal/Wharton/resumes/Bates College.xml","r").read() #Name, Univ and Email working good
    f = file("/home/sajal/Wharton/resumes/Boise State Functional.xml","r").read() #Univ and Email working good. name not working.
    soup = BeautifulSoup(f)
    st = NERTagger('/home/sajal/Downloads/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','/home/sajal/Downloads/stanford-ner-2014-06-16/stanford-ner.jar')
    email = extract_email(soup)
    name = extract_possible_names(soup,st)
    education = extract_edu(soup,st)
    print name
    print education
    print email
