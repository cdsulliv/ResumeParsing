from bs4 import BeautifulSoup
import requests
import re
import csv

STATUS_OK = 200
STATUS_NOT_FOUND = 404

class ParseWebsite(object):
    """this class has all the needed information to parse resume from a website"""
    def __init__(self, url='', num=0): #constructor of the class
        self._url = url
        self._num = num

    #@property    
    def url(self):
        return self.url
 
    #@property
    def num(self):
        return self.num

    def parse_website(self):   #Abstract method, defined by convention only
        raise NotImplementedError("Subclass must implement abstract method")

class Indeed(ParseWebsite):

    def parse_website(self):
        home_page = self.url
        num_of_pages_to_parse = self.num
        print num_of_pages_to_parse
        print home_page 
        rootRef = []
        for i in range(num_of_pages_to_parse):
            r = requests.get(home_page + str(i * num_of_pages_to_parse))
            
            # failsafe to ensure above url returns authentic link
            if r.status_code != STATUS_OK:
                raise Exception('Bad Request')
            root = BeautifulSoup(r.text)
            
            # 'limit=50' looks at first 50 items that match specified class below
            # rootRef captures the specific link extension of each resume on the page
            rootRefRaw = root.find_all(class_='sl link savelink anon', limit=50)
            rootRef.extend([x.get('data-rez') for x in rootRefRaw])

            # There must exist a .csv file with the name specified below in the same directory as this script
        with open ('target.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, dialect='excel')

            # the order items are appended below to spreadRow must match the order given here
            csvwriter.writerow(['Search Rank', 'Name',
                                'School 1', 'School Location 1', 'Degree 1', 'School Duration 1',
                                'School 2', 'School Location 2', 'Degree 2', 'School Duration 2',
                                'School 3', 'School Location 3', 'Degree 3', 'School Duration 3',
                                'Employer 1', 'Roll 1', 'Job Duration 1', 'Job Location 1',
                                # the excess work experiences are to compensate for not having a
                                # more effective way of only grabbing the most relevent bullets
                                'Work Experience 11', 'Work Experience 12', 'Work Experience 13',
                                'Work Experience 14', 'Work Experience 15', 'Work Experience 16',
                                'Work Experience 17', 'Work Experience 18', 'Work Experience 19',
                                'Employer 2', 'Roll 2', 'Job Duration 2', 'Job Location 2',
                                'Work Experience 21', 'Work Experience 22', 'Work Experience 23',
                                'Work Experience 24', 'Work Experience 25', 'Work Experience 26',
                                'Work Experience 27', 'Work Experience 28', 'Work Experience 29',
                                'Employer 3', 'Roll 3', 'Job Duration 3', 'Job Location 3',
                                'Work Experience 31', 'Work Experience 32', 'Work Experience 33',
                                'Work Experience 34', 'Work Experience 35', 'Work Experience 36',
                                'Work Experience 37', 'Work Experience 38', 'Work Experience 39',
                                'Duration', 'Resume Body'])

            for i, ref in enumerate(rootRef):
                spreadRow = []

                tempRequest = requests.get('http://www.indeed.com/r/' + ref)
                if tempRequest.status_code != STATUS_OK:
                    raise Exception('Resume not found')
                
                tempSoup = BeautifulSoup(tempRequest.text)
                nameTag = tempSoup.find('h1', {'id': 'resume-contact'})
         
                spreadRow.append(i)
                spreadRow.append(nameTag.getText())

                # EDUCATION
                degreeTagList = tempSoup.find_all(class_="edu_title", limit=3)
                degreeList = [degreeTag.getText() for degreeTag in degreeTagList]
                
                eduDatesTagList = tempSoup.find_all(class_="edu_dates", limit=3)
                eduDatesList = [eduDatesTag.getText() for eduDatesTag in eduDatesTagList]
                
                #tests if degree contains the term "Bachelor" and the year "2015", skips to next resume if not
                if any('achelor' in deg for deg in degreeList):
                    if any('15' in str(yr) for yr in eduDatesList):

                        schoolTagList = tempSoup.find_all(class_="edu_school", limit=3)
                        schoolList = [schoolTag.getText() for schoolTag in schoolTagList]
                        
                        locationTagList = tempSoup.find_all(class_={"edu_school", "inline-block"}, limit = 3)
                        locationList = [locationTag.getText() for locationTag in locationTagList]

                        for n in range(3):
                            if n > len(schoolList) - 1:
                                spreadRow.append('N/A')
                            else:
                                spreadRow.append(schoolList[n])
                            if n > len(locationList) - 1:
                                spreadRow.append('N/A')
                            else:
                                spreadRow.append(locationList[n])
                            if n > len(degreeList) - 1:
                                spreadRow.append('N/A')
                            else:
                                spreadRow.append(degreeList[n])
                            if n > len(eduDatesList) - 1:
                                spreadRow.append('N/A')
                            else:
                                spreadRow.append(eduDatesList[n])

                        # EMPLOYMENT
                        rollTagList = tempSoup.find_all(class_="work_title title", limit=3)
                        rollList = [rollTag.getText() for rollTag in rollTagList]
                        
                        locationTagList = tempSoup.find_all(class_={"work_company", "inline-block"}, limit = 3)
                        locationList = [locationTag.getText() for locationTag in locationTagList]
                        
                        employerTagList = tempSoup.find_all(class_="work_company", limit=3)
                        employerList = [employerTag.getText() for employerTag in employerTagList]
                        
                        empDatesTagList = tempSoup.find_all(class_="work_dates", limit=3)
                        empDatesList = [empDatesTag.getText() for empDatesTag in empDatesTagList]
                        
                        workExpTagList = tempSoup.find_all(class_='work_description', limit=3)
                        workExpList = [workExpTag.getText() for workExpTag in workExpTagList]



                        # creates a temporary dictionary that allows the script to search through multiple bullets
                        # per work experience as opposed to only one
                        tempDict = {}
                        length = []
                        for j, section in enumerate(workExpList):
                            tempExpList = {}

                            # Attempts to replace the commonly occuring characters that begin work experiences with a common
                            # character that can be used as a delimiter to parse them into separate line items
                            temp = section.replace('*', '~').replace('•', '~').replace('\xa0ß','~')\
                                   .replace('\xa0-', '~').replace('\xa0\xa0', '~').replace('.','~')
                            
                            tempExpList['section'+str(j)] = temp.split('~')

                            # attempts to reconcile the fact that most people start their Work Experience section with
                            # the word "Responsibility" or "Experience" by deleting the first item
                            del tempExpList['section'+str(j)][0]
                            length.append(len(tempExpList['section'+str(j)]))
                            
                            for k in range(length[j]):
                                tempDict['workExp'+str(j)+str(k)] = tempExpList['section'+str(j)][k]
                                
                                            
                        

                        for n in range(3):
                            if n > len(employerList) - 1:
                                spreadRow.append('N/A')
                            else:
                                spreadRow.append(employerList[n])
                            if n > len(rollList) - 1:
                                spreadRow.append('N/A')
                            else:
                                spreadRow.append(rollList[n])
                            if n > len(empDatesList) - 1:
                                spreadRow.append('N/A')
                            else:
                                spreadRow.append(empDatesList[n])
                            if n > len(locationList) - 1:
                                spreadRow.append('N/A')
                            else:
                                spreadRow.append(locationList[n])
                            # range is set to take 9 bullets worth of information to ensure at least 3 are viable
                            if n > len(workExpList) - 1:
                                for m in range(9):
                                    spreadRow.append('N/A')
                            else: 
                                for m in range(9):
                                    if m > length[n] - 1:
                                        spreadRow.append('N/A')
                                    else:
                                        spreadRow.append(tempDict['workExp'+str(n)+str(m)])
                                        
                        print('\n', nameTag.getText(), str(i))

                        # EMPLOYMENT total duration
                        datesFull = tempSoup.find_all(class_="work_dates")
                        if len(datesFull) > 0:
                            startYearRaw = datesFull[-1].getText()
                            startYear = int(re.search(r'\b\d{4}\b', startYearRaw).group())
                            spreadRow.append(2015 - startYear)


                        # Resume Body
                        bodyTag = tempSoup.find(id='resume_body')
                        body = bodyTag.getText()
                        body.replace('*', ' ')
                        body = body.encode("utf-8", errors="ignore")
                        spreadRow.append(body)
                        
                        spreadRowEncode = [str(i).encode("utf-8", errors="ignore") for i in spreadRow]

                        # write to the spreadsheet
                        csvwriter.writerow(spreadRowEncode)

if __name__ == "__main__":
    indeed_home_page = 'http://www.indeed.com/resumes/in-New-York-NY?co=US&rb=dt%3Aba%2Cyoe%3A1-11&start='
    num_of_pages_to_parse = 0
    obj = ParseWebsite(indeed_home_page, num_of_pages_to_parse)
    print obj.
    ind = Indeed(obj)
    ind.parse_website()

    