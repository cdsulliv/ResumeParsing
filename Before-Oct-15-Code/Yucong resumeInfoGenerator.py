import urllib2
from bs4 import BeautifulSoup
import re
import csv
import sys

baseUrl = "http://www.indeed.com"
rootUrl = baseUrl + "/resumes/information-technology-support/in-Philadelphia-PA?from=mrs&subfrom=4_5"
fileName = "resumeInfo.csv"

def getContent(tag):
	if (tag != None):
		try:
			string = str(tag.contents[0])
		except UnicodeEncodeError:
			print 'UnicodeEncodeError in: ' + str(tag)
			return 'ERROR'
		return string
	else:
		return None

def getListContent(lst):
	if (lst != None):
		result = []
		for item in lst:
			result.append(getContent(item))
		return result
	else:
		return None

def writeToCsvFile(data):
	csvFile = open('./' + fileName, 'w')
	csvWriter = csv.writer(csvFile)
	csvWriter.writerows(data)
	csvFile.close()

rootPage = urllib2.urlopen(rootUrl).read()

# page is loaded
# print rootPage

soupParseTree = BeautifulSoup(rootPage)
people = soupParseTree.findAll("a", {"class" : "app_link"})

# related tags extracted
# print people

links = []
for person in people:
	links.append(baseUrl + person['href'])

# people and their links are now in the directory
# print len(links)
# print links

def extractWorkExpList(workExps):
	result = []
	if (workExps != None):
		for i in range(0, 3):
			if (i < len(workExps)):
				workExp = workExps[i]
				workTitle = workExp.find('p', {'class':'work_title title'})
				workCompany = workExp.find('span', {'class':'bold'})
				workDate = workExp.find('p', {'class':'work_dates'})
				result.append(getContent(workTitle))
				result.append(getContent(workCompany))
				result.append(getContent(workDate))
			else:
				result += [None, None, None]
	else:
		for i in range(0, 9):
			result.append(None)
	return result

def extractEduList(edus):
	result = []
	if (edus != None):
		for i in range(0, 3):
			if (i < len(edus)):
				edu = edus[i]
				eduTitle = edu.find('p', {'class':'edu_title'})
				eduCompany = edu.find('span', {'class':'bold'})
				eduDate = edu.find('p', {'class':'edu_dates'})
				result.append(getContent(eduTitle))
				result.append(getContent(eduCompany))
				result.append(getContent(eduDate))
			else:
				result += [None, None, None]
	else:
		for i in range(0, 9):
			result.append(None)
	return result

def extractWorkYears(earliestWorkExp):
	if (earliestWorkExp != None):
		earliestWorkDate = earliestWorkExp.find('p', {'class':'work_dates'})
		if (earliestWorkDate != None):
			text = getContent(earliestWorkDate)
			match = re.search(re.compile('\d{4}'), text)
			firstWorkYear = match.group(0)
			firstWorkYear = firstWorkYear.strip()

			try:
				firstWorkYear = int(firstWorkYear)
			except ValueError:
				return [None]

			return [2015 - firstWorkYear]
		else:
			return [None]	
	else:
		return [None]

def extractPersonInfo(url):
	page = urllib2.urlopen(url).read()
	tree = BeautifulSoup(page)
	result = []

	resume = tree.find("div", {"id":"resume_body"})
	name = tree.find("h1", {"id":"resume-contact"})
	headline = tree.find("h2", {"id":"headline"})
	result.append(getContent(name))
	result.append(getContent(headline))

	workExps = tree.findAll('div', {'class':'work-experience-section'})
	result += extractWorkExpList(workExps)
	
	# undergradTitle = tree.find("p", {"class":"edu_title"}, text=re.compile("^.*(B|b)achelor.*$"))
	# undergradSchool = None
	# if (undergradTitle != None):
	# 	undergradSchool = undergradTitle.findNextSiblings('div')[0].find('span')
	# result.append(getContent(undergradTitle))
	# result.append(getContent(undergradSchool))

	edus = tree.findAll('div', {'class':re.compile('^education-section.*$')})
	result += extractEduList(edus)

	earliestWorkExp = tree.find('div', {'class':'work-experience-section last'})
	result += extractWorkYears(earliestWorkExp)

	return result

# extractPersonInfo('http://www.indeed.com/r/066dc1a15f0b69b0')

title = ['Name','Headline']
title += ['Work 1 Title', 'Work 1 Company', 'Work 1 Date']
title += ['Work 2 Title', 'Work 2 Company', 'Work 2 Date']
title += ['Work 3 Title', 'Work 3 Company', 'Work 3 Date']
title += ['Degree 1', 'Degree 1 School', 'Degree 1 Date']
title += ['Degree 2', 'Degree 2 School', 'Degree 2 Date']
title += ['Degree 3', 'Degree 3 School', 'Degree 3 Date']
title += ['Work Time (yr)']

data = [title]
for link in links:
	data.append(extractPersonInfo(link))
	sys.stdout.write('.')

writeToCsvFile(data)
print "Done."
