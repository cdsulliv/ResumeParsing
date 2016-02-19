# Python Web Scraping Summer 2015 assignment 1
# Ian Masters

# Scraping 20 resumes into spreadsheet from http://www.indeed.com/resumes
# /information-technology-support/in-Philadelphia-PA?from=mrs&subfrom=4_5

from bs4 import BeautifulSoup
import requests
import re
import csv

r = requests.get('http://www.indeed.com/resumes/information-technology-support/in-Philadelphia-PA?from=mrs&subfrom=4_5')
if r.status_code > 299:
    raise Exception('Bad Reqest')
root = BeautifulSoup(r.text)
rootRefRaw = root.find_all(class_='sl link savelink anon', limit=20)
rootRef = [x.get('data-rez') for x in rootRefRaw]
print(rootRef)

with open('Scrape1.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, dialect='excel')
    csvwriter.writerow(['Search Rank', 'Name',
                        'Employer 1', 'Roll 1', 'Job Duration 1',
                        'Employer 2', 'Roll 2', 'Job Duration 2',
                        'Employer 3', 'Roll 3', 'Job Duration 3',
                        'School 1', 'Degree 1', 'School Duration 1',
                        'School 2', 'Degree 2', 'School Duration 2',
                        'School 3', 'Degree 3', 'School Duration 3',
                        'Duration', 'Resume Body'])

    for i, ref in enumerate(rootRef):
        spreadRow = []

        tempRequest = requests.get('http://www.indeed.com/r/' + ref)
        if tempRequest.status_code > 299:
            raise Exception('Resume not found')
        tempSoup = BeautifulSoup(tempRequest.text)
        tempDict = {}
        nameTag = tempSoup.find('h1', {'id': 'resume-contact'})
        tempDict['name'] = nameTag.getText()
        tempDict['rank'] = i
        spreadRow.append(i)
        spreadRow.append(nameTag.getText())

        # EMPLOYMENT
        rollTagList = tempSoup.find_all(class_="work_title title", limit=3)
        rollList = [rollTag.getText() for rollTag in rollTagList]
        employerTagList = tempSoup.find_all(class_="work_company", limit=3)
        employerList = [employerTag.getText() for employerTag in employerTagList]
        empDatesTagList = tempSoup.find_all(class_="work_dates", limit=3)
        empDatesList = [empDatesTag.getText() for empDatesTag in empDatesTagList]
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
        tempDict['rollList'] = rollList
        tempDict['employerList'] = employerList
        tempDict['empDatesList'] = empDatesList

        # EDUCATION
        schoolTagList = tempSoup.find_all(class_="edu_school", limit=3)
        schoolList = [schoolTag.getText() for schoolTag in schoolTagList]
        degreeTagList = tempSoup.find_all(class_="edu_title", limit=3)
        degreeList = [degreeTag.getText() for degreeTag in degreeTagList]
        eduDatesTagList = tempSoup.find_all(class_="edu_dates", limit=3)
        eduDatesList = [eduDatesTag.getText() for eduDatesTag in eduDatesTagList]
        for n in range(3):
            if n > len(schoolList) - 1:
                spreadRow.append('N/A')
            else:
                spreadRow.append(schoolList[n])
            if n > len(degreeList) - 1:
                spreadRow.append('N/A')
            else:
                spreadRow.append(degreeList[n])
            if n > len(eduDatesList) - 1:
                spreadRow.append('N/A')
            else:
                spreadRow.append(eduDatesList[n])
        tempDict['schoolList'] = schoolList
        tempDict['degreeList'] = degreeList
        tempDict['eduDatesList'] = eduDatesList

        # EMP total duration
        datesFull = tempSoup.find_all(class_="work_dates")
        startYearRaw = datesFull[-1].getText()
        startYear = int(re.search(r'\b\d{4}\b', startYearRaw).group())
        spreadRow.append(2015 - startYear)
        tempDict['empDuration'] = 2015 - startYear
        bodyTag = tempSoup.find(id='resume_body')
        body = bodyTag.getText()
        body.replace('*', ' ')
        body = body.encode("utf-8", errors="ignore")
        spreadRow.append(body)

        # write to the spreadsheet
        csvwriter.writerow(spreadRow)
