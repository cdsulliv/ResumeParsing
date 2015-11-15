import re
from bs4 import BeautifulSoup

HEAD_PATTERN = "\S[A-Z \d]+$"

class ParseText(object):
    """docstring for ParseTextme"""
    def __init__(self, filepath=""):
        self.filepath = filepath

    def findHeadings(self, content):
        heading_indexes = []
        #print content
        soup = BeautifulSoup(content)
        bolds = soup.find_all('b')
        #print "bolds: ", bolds
        for bold in bolds:
            #print "bold: ", bold
            line = bold.string
            #print "heading1:", line 
            
            heading = re.match(HEAD_PATTERN, line)
            #print "heading1:", heading 
            if heading:
                print "heading: ", line
                #print "bold:", bold
                start_index = content.index(str(bold))
                heading_indexes.append(start_index)

        return heading_indexes
    
    def find_bio(self, content):
        heading_indexes = self.findHeadings(content)
        end_bio_ind = min(heading_indexes)
        return content[:end_bio_ind]

    def readFile(self):
        out = file(self.filepath, "r").read()            
        return out


if __name__ == "__main__":
    filepath = "/home/shreya/Wharton/1.xml"
    pt = ParseText(filepath)
    content = pt.readFile()     
    #pt.findHeadings(content) 
    print pt.find_bio(content)
    #print "a"