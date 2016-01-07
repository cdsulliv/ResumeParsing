"""
This script splits the xml version of work experience into major categories
and saves it into a csv

"""

__author__ = "Shreya Pandey"

import re
from bs4 import BeautifulSoup
from splitting_xml import ParseText, getAllHeadings
from utilities import getFiles 
import csv

def splitExp(exp):
    indexes = []
    italic_indexes = []
    bold_texts = []
    italic_texts = []
    
    work_exp ={}
    key = ""
    value = ""
    k_flag = False
    v_flag = False

    soup = BeautifulSoup(exp)
    bolds = soup.find_all('b')
	#print "BOLDS: ", bolds
	
    for bold in bolds:
    	text = bold.string 
    	if text:
        	bold_texts.append(text)

    italics = soup.find_all('i') 
	#print "ITALICS: ", italics
	
    for italic in italics:
    	text = italic.string
    	if text:
        	italic_texts.append(text)

    texts = soup.find_all('text')

    all_texts = []
    for text in texts:
        if text.string:
            all_texts.append(text)
    
    print all_texts
    #print texts[0].i.b.string

    for t in range(len(texts)):
        text = texts[t]
        line = text.string
        #print line
            
        if line:
            #print line
            if line in bold_texts or line in italic_texts:
            	#print t, len(texts), line
            	if t>0 and (not texts[t-1].bold and not texts[t-1].italic):  
                    #print texts[t-1].bold, texts[t-1].italic
                	key= line + "\n"
           	
            	elif t < len(texts)-1 and (not texts[t+1].bold or not texts[t+1].italic):
            		#print "KEY"
                	k_flag = True 
                else:
                	##########################################print line
                	key+=line + "\n"    	
    	    else:
                #print t, len(texts)
                #print texts[t-1].bold, texts[t-1].italic
                if t >0 and (texts[t-1].bold or texts[t-1].italic):
                	#########################################
                	print line 
                	value = line + "\n"
                elif t< len(texts)-1 and (texts[t+1].bold or texts[t+1].italic):
                    #####################################
                    print "VALUE"
                    v_flag = True 
                else:
                	#print line
                	value+=line + "\n"    
            
            '''if k_flag:        
            	print key
            '''
            if k_flag and v_flag:
            	print "HERE"
                work_exp[key] = value                

    return work_exp            

if __name__ == "__main__":
    PROBABLE_HEADINGS = getAllHeadings("set_of_headings.txt")
    fileset = getFiles("/home/shreya/Wharton/XML")
    with open ("work_exp.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['Filename', 'Company, Position, Duration', 'About Job', 'EXPERIENCE' ])
        for xml_filepath in fileset:
            index = xml_filepath.index(".") 
            if "xml" in xml_filepath[index:]:
                #print "xml: ", xml_filepath
                row = []
                first_index =xml_filepath.rfind("/")+1
                last_index = xml_filepath.rfind(".")
                filename = xml_filepath[first_index: last_index]
                #print "filename: "+filename
                text_filepath = "/home/shreya/Wharton/PDF_text/" + filename + ".txt"
                #print "text_filepath: ", text_filepath
                pt = ParseText(xml_filepath, text_filepath)
                content = pt.readXmlToString()
                content_list = pt.readTextToList()     
                heading_indexes, headings = pt.findHeadings(content, content_list, PROBABLE_HEADINGS)
                #bio = pt.find_bio(content, content_list, headings, heading_indexes)
                #print "BIO: ", bio
                #print "HEADINGS: ",  headings
                #edu = pt.find_this(content, content_list, "education", headings, heading_indexes)
                exp = pt.find_this(content, content_list, "experience", headings, heading_indexes)
                #print "EDUCATION: ", edu
                #print "EXPERIENCE: ", exp
                if not exp:
                    exp =  pt.find_this(content, content_list, "history", headings, heading_indexes)
                
                split_exp = splitExp(exp)

                for ex in split_exp:
                	print filename, ex, split_exp[ex], exp
                	row.append(filename)
                	row.append(ex)
                	row.append(split_exp[ex])
                	row.append(exp)        
                
                csvwriter.writerow(row)
                break

