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

possible_headers = ["EDUCATION", "EXPERIENCE", "PROFESSIONAL" , "ORGANIZATIONS", "MEMBERSHIPS", "LANGUAGE", "SKILLS", "HOBBIES","COMPUTER", "ACTIVITIES","INTERESTS"]

def extract_email(soup):
    return  soup.pdfx.article.email.string

def extract_possible_names(soup):
    arr =[]
    s = soup.pdfx.article.find('title-group').find('article-title').string
    arr.append(s)
    s = soup.pdfx.article.outsider
    print s
    arr.append(s)
    return arr

def extract_edu(soup):
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

    return text[start_i:end_i]

    # print re.find("EDUCATION")
    # print words
    # print capital_words

if __name__ == "__main__":
    f = file("/home/sajal/Wharton/resumes/American University.xml","r").read()
    # f = file("/home/sajal/Wharton/resumes/Austin College 1.xml","r").read()
    f = file("/home/sajal/Wharton/resumes/Bates College.xml","r").read()
    # f = file("/home/sajal/Wharton/resumes/Boise State Functional.xml","r").read()
    soup = BeautifulSoup(f)
    email = extract_email(soup)
    name = extract_possible_names(soup)
    education = extract_edu(soup)

    print name
    print email
    print education
