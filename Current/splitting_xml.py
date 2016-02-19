"""
This script splits the xml and text version of resume into major categories
and saves it into a csv

"""

__author__ = "Shreya Pandey"

import re
from bs4 import BeautifulSoup
from utilities import getFiles 
import csv
import ast
from preprocessor import preprocess 

HEAD_PATTERN = "\S[A-Z \d / : ]+$" 
#PROBABLE_HEADINGS = ["education", "objective", "experience", "work experience", "certifications", "organizations and activites"]

def getAllHeadings(filename=""):
    f = open(filename, "r")
    lines = f.readlines()
    headings = [line.strip() for line in lines]
    return headings

class ParseText(object):
    """docstring for ParseTextme"""
    def __init__(self, xml_filepath="", text_filepath = ""):
        self.xml_filepath = xml_filepath
        self.text_filepath = text_filepath
        self.isXml = True

    def findHeadings(self, content, content_list, PROBABLE_HEADINGS):
        heading_indexes = []
        headings = []
        #print content
        content_new = ''.join(content_list) 
        #print "content: ", content 
        soup = BeautifulSoup(content_new)
        #soup = preprocess(p_soup)
        bolds = soup.find_all('b')
        #print "bolds: ", bolds
        for bold in bolds:
            #print "bold: ", bold
            line = bold.string
            #print "heading:", line 
            #print "heading3:", line
            if line:
                '''print "line: ", line              
                heading = re.match(HEAD_PATTERN, line)
                 
                if heading and len(line) > 5:
                    print "heading1: ", line
                    #print "bold:", bold
                    headings.append(line)
                    start_index = content.index(str(bold))
                    heading_indexes.append(start_index)
                '''
                #print "!!!", line.strip()
                prob_head = line.strip().lower() 
                if prob_head in PROBABLE_HEADINGS and line not in headings:
                    #print "heading2: ", line
                    headings.append(line)
                    start_index = content_new.index(str(bold))
                    heading_indexes.append(start_index)
        
        print "OLD HEADINGS: ", headings
        print "HEADING index: ", heading_indexes        
        if len(headings)<2:
            print "new method"
            # Here is the setup. The resume should be in beautiful soup form.
            
            texts = soup.find_all("text")
            # All CAPS:
            for t in texts:
                line = t.text
                if line: 
                    try: 
                        if (line.isupper() and not re.search("GPA|G.P.A", line) and len(line)>5):    
                            #headings = [x.text for x in texts if (x.text.isupper() and not re.search("GPA|G.P.A", x.text))]
                            headings.append(str(line))
                            #print "t: ", t
                            #print "str(t): ", str(t)
                            #print "content: ", content_new
                            '''if str(line) in content_new:
                                print "OK"
                            else:
                                print "THIS IS THE ERROR!" 
                            '''       
                            #start_index = content_new.index(str(t))
                            start_index = content_new.index(str(line))
                            #print "Start index: ",start_index    
                            heading_indexes.append(start_index)
                            #print "CAPS heading_indexes: ", heading_indexes
                    except:
                        print "The error is in UPPER"
            print "CAPS headings: ", headings
            print "CAPS heading_indexes: ", heading_indexes

        if len(headings)<2:            
            # Underline
            texts = soup.find_all("text")
            for t in texts:
                line = t.text
                if line:     
                    try:
                        if re.search('___', line) and len(line) > 5:
                            headings.append(line)
                            #headings = [x.text for x in texts if re.search('___', x.text)]
                            #print "Underline headings: ", headings            
                            #start_index = content_new.index(str(t))
                            start_index = content_new.index(str(line))
                            heading_indexes.append(start_index)
                            #print "Underline heading_indexes: ", heading_indexes
                    except:
                        print "the error is in Underline"                
            #print content
            print "Underline headings: ", headings
            print "Underline heading_indexes: ", heading_indexes        
        '''if not headings:
            self.isXml = False
            for line in content_list:
                #print line
                prob_head = line.strip().lower()
                if prob_head in PROBABLE_HEADINGS and line not in headings:
                    print "heading3: ", line
                    headings.append(line)
                    start_index = content_list.index(line)
                    heading_indexes.append(start_index)           
        '''            
                                      
        return heading_indexes, headings
    
    def find_bio(self, content, content_list, headings, heading_indexes):
        if self.isXml:
            if heading_indexes:
                end_bio_ind = min(heading_indexes)
                bio = content[:end_bio_ind]
                if bio:
                    return bio
        else:
            if heading_indexes:
                end_bio_ind = min(heading_indexes)
                bio_list = content_list[:end_bio_ind]
                if bio_list:
                    return ''.join(bio_list)
                
        return None

    def find_this(self, content, content_list, head, headings, heading_indexes):
        if self.isXml:
            if headings:
                for h in range(len(headings)):
                    heading = headings[h]
                    heading = heading.replace(" ", "")
                    if head in heading.lower():
                        start_index = heading_indexes[h]
                        if h+1 <= len(heading_indexes)-1:
                            next_index = heading_indexes[h+1]
                            edu = content[start_index:next_index]     
                        else:
                            edu = content[start_index:]

                        return edu, self.isXml        
        else:
             if headings:
                for h in range(len(headings)):
                    heading = headings[h]
                    if head in heading.lower():
                        start_index = heading_indexes[h]
                        if h+1 <= len(heading_indexes)-1:
                            next_index = heading_indexes[h+1]
                            edu_list = content_list[start_index:next_index]     
                        else:
                            edu_list = content_list[start_index:]


                        return ''.join(edu_list), self.isXml                       
        
        return None, self.isXml        

    def readXmlToString(self):
        out = file(self.xml_filepath, "r").read()            
        return out

    def readXMLToList(self):
        out = file(self.xml_filepath, "r").readlines()            
        return out
            
    def readTextToList(self):
        try:
            out = file(self.text_filepath, "r").readlines()
        except:
            out = []                
        return out


    def writeToCsv(self, filename=""):
        with open (filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, dialect='excel')
            csvwriter.writerow(['bio'])
    
def getGradDate(filename):    
    text = file(filename, "r").read()
    files = text.split("\n\n")
    file_year = {}
    for f in files[:-1]:          
        years = []
        file_content = f.split("\t\t")
        #print file_content
        file_name = file_content[0].strip()
        #print file_name
        #print file_content[1]
        dic = ast.literal_eval(file_content[1])    
        for univ in dic:
            value = dic[univ]
            for key in value:
                if key == 'associated_date':
                    date = value[key]
                    month_year = date.split(" ")
                    years.append(int(month_year[1]))

        if 2016 in years: 
            file_year[file_name] = 2016
        elif 2015 in years:
            file_year[file_name] = 2015    
        else:
            file_year[file_name] = None

        #break    
    return file_year

if __name__ == "__main__":
    PROBABLE_HEADINGS = getAllHeadings("set_of_headings_1.txt")
    print "OLD LEN: ", len(PROBABLE_HEADINGS)
    PROBABLE_HEADINGS.extend(getAllHeadings("set_of_headings_boston.txt"))
    PROBABLE_HEADINGS.extend(getAllHeadings("set_of_headings_newyork.txt"))
    PROBABLE_HEADINGS.extend(getAllHeadings("set_of_headings_other.txt"))
    
    PROBABLE_HEADINGS = list(set(PROBABLE_HEADINGS))
    print "NEW LEN: ", len(PROBABLE_HEADINGS)
    if "education:" in PROBABLE_HEADINGS:
        print "AYE!" 

    fileset = getFiles("/home/shreya/Wharton/NEW/Other/ONLY_XML")
    

    fileSet = []
    for f in fileset:
        if ".xml" == f[-4:]:
            fileSet.append(f)

    #print len(fileSet)
    for i in range(0, len(fileSet), 50):
        if (i+50)< len(fileSet):
            file_set = fileSet[i: i+50]
        else:
            file_set = fileSet[i:]   
        
        try:
            with open ("split_v" +str(i) +".csv", 'w') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                csvwriter.writerow(['FILENAME', 'HEADINGS', 'BIO', 'EDUCATION', 'EXPERIENCE', 'isXML?', 'LeadershipExp?', 'VolunteerExp?', 'Leadership Exp', 'Volunteer Exp', 'Grad(2015)', 'Grad(2016)', 'Grad(15/16)', 'Grad(15/16) AND (hasWorkExp) AND (hasLead/Volunt Exp)'])
        
                file_year = getGradDate("/home/shreya/RA_ML/Resume-Parsing/Data/edu/Other/"+"out_edu_split_v"+str(i)+".txt")
                #print i, file_year    
                for xml_filepath in file_set:
                    isLead = False
                    isVolunt = False
                    index = xml_filepath.index(".") 
                    if "xml" in xml_filepath[index:]:
                        #print "xml: ", xml_filepath
                        row = []
                        first_index =xml_filepath.rfind("/")+1
                        last_index = xml_filepath.rfind(".")
                        filename = xml_filepath[first_index: last_index]
                        print "filename: ", filename
                        #filename =  "Katie+Coyle+resume+"
                        text_filepath = "/home/shreya/Wharton/PDF_text_new/" + filename + ".txt"
                        #print "text_filepath: ", text_filepath

                        try:
                            grad_date = file_year[filename]
                            #print grad_date 
                        except:
                            grad_date = None
                            #print filename

                        grd = False

                        if grad_date == 2016:
                            grd16 = "TRUE"
                        else:
                            grd16 = False    


                        if grad_date == 2015:
                            grd15 = "TRUE"
                        else:
                            grd15 = False        
                            
                        if grd15 or grd16:
                            grd = True       
                            

                        #xml_filepath = "/home/shreya/Wharton/NEW/Other/ONLY_XML/ Katie+Coyle+resume+.xml"    

                        pt = ParseText(xml_filepath, text_filepath)
                        content = pt.readXmlToString()
                        content_list = pt.readXMLToList()
                        #content_list = pt.readTextToList()     
                        try:
                            heading_indexes, headings = pt.findHeadings(content, content_list, PROBABLE_HEADINGS)
                        except:
                            print "fix headings"

                        bio = pt.find_bio(content, content_list, headings, heading_indexes)
                        '''
                        if not bio:
                            bio = content
                        '''    
                        #print "BIO: ", bio
                        #print "HEADINGS: ",  headings
                        edu, isXml = pt.find_this(content, content_list, "ducation", headings, heading_indexes)
                        exp, isXml = pt.find_this(content, content_list, "xperience", headings, heading_indexes)
                        if not exp:
                            exp, isXml = pt.find_this(content, content_list, "mployment", headings, heading_indexes)
                            

                        #print "EDUCATION: ", edu
                        #print "EXPERIENCE: ", exp
                        if not exp:
                            exp, isXml =  pt.find_this(content, content_list, "istory", headings, heading_indexes)
                        
                        '''if not edu:
                            edu = content

                        if not exp:
                            exp = content    
                        '''    
                        leadExp, x = pt.find_this(content, content_list, "eadership", headings, heading_indexes)
                        
                        if leadExp:
                            isLead  = "TRUE"
                       

                        volunExp, y = pt.find_this(content, content_list, "olunteer", headings, heading_indexes)
                        if volunExp:
                            isVolunt = "TRUE"
            
                        volOrLead = False
                        if isLead or isVolunt:
                            volOrLead = "TRUE"

                        if not headings:
                            isXml = "NULL"
                        
                        allCriteria = False
                        if grd and exp and volOrLead:
                            allCriteria = "TRUE"
                                
                        #(2015 or 2016 grad) AND (has a career experience section) AND (has a leadership experience section or a volunteer section)

                        row.append(filename)
                        row.append(headings)    
                        row.append(bio)    
                        row.append(edu)
                        row.append(exp)
                        row.append(isXml)        
                        row.append(isLead)
                        row.append(isVolunt)
                        row.append(leadExp)
                        row.append(volunExp)
                        row.append(grd15)
                        row.append(grd16)
                        row.append(grd)
                        row.append(allCriteria)
                        csvwriter.writerow(row)
                    
        except:
            print i                
    '''filepath = "/home/shreya/Wharton/1.xml"
    pt = ParseText(filepath)
    content = pt.readFile()     
    #pt.findHeadings(content) 
    print pt.find_bio(content)
    #print "a"
    '''