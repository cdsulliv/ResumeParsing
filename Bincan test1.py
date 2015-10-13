from lxml import html
import requests
page = requests.get('http://www.indeed.com/resumes/information-technology-support/in-Philadelphia-PA?from=mrs&subfrom=4_5')
tree_main = html.fromstring(page.text)
head = "http://www.indeed.com"
allPage = tree_main.xpath('//div[@class="app_name"]/a/@href')
file1 = open("outPutFile", 'w+')
for i in range(0,19):
	print head + allPage[i]
	page = requests.get(head + allPage[i])
	tree  =  html.fromstring(page.text)
	#value = tree.xpath('//div[@id="workExperience-EeUPwXM3WbOCfipAlk2Pyg"]/descendant::*/text()')
	name = tree.xpath('//h1[@id="resume-contact"]/text()')
	ContactInformation = tree.xpath('//p[@id="headline_location"]/text()') #only has geographical location, for privacy? ')#'

	Role1 = tree.xpath('((//div[@class="work-experience-section " or @class="work-experience-section last"])/div[position() < 2]/p[@class = "work_title title"]/text())[1]')
	Employer1 = tree.xpath('((//div[@class="work-experience-section " or @class="work-experience-section last"])/div[position() < 2]/div[@class = "work_company"]/span/text())[1]')
	Duration1 = tree.xpath('((//div[@class="work-experience-section " or @class="work-experience-section last"])/div[position() < 2]/p[@class = "work_dates"]/text())[1]')
	Role2 = tree.xpath('((//div[@class="work-experience-section " or @class="work-experience-section last"])/div[position() < 2]/p[@class = "work_title title"]/text())[2]')
	Employer2 = tree.xpath('((//div[@class="work-experience-section " or @class="work-experience-section last"])/div[position() < 2]/div[@class = "work_company"]/span/text())[2]')
	Duration2 = tree.xpath('((//div[@class="work-experience-section " or @class="work-experience-section last"])/div[position() < 2]/p[@class = "work_dates"]/text())[2]')
	Role3 = tree.xpath('((//div[@class="work-experience-section " or @class="work-experience-section last"])/div[position() < 2]/p[@class = "work_title title"]/text())[3]')
	Employer3 = tree.xpath('((//div[@class="work-experience-section " or @class="work-experience-section last"])/div[position() < 2]/div[@class = "work_company"]/span/text())[3]')
	Duration3 = tree.xpath('((//div[@class="work-experience-section " or @class="work-experience-section last"])/div[position() < 2]/p[@class = "work_dates"]/text())[3]')

	undergraduateDegree = tree.xpath('//div[@class="edu_school"]/descendant::*/text() ') #use reg match? differ advanced?
	copyAllText = tree.xpath('//div[@id="resume_body"]/descendant::*/text() ')
	out = (["\n name: "] + name + ["\n"]
		+ ["ContactInformation: "] + ContactInformation + ["\n"]
		+ Role1 + ["\n"]
		+ Employer1 + ["\n"]
		+ Duration1 + ["\n"]
		+ Role2 + ["\n"]
		+ Employer2 + ["\n"]
		+ Duration2 + ["\n"]
		+ Role3 + ["\n"]
		+ Employer3 + ["\n"]
		+ Duration3 + ["\n"]
		+ ["Education: "] + undergraduateDegree + ["\n\n"])
	outString = ""
	for j in range(0, len(out) - 1):
		outString += out[j]
	file1.write(outString)
file1.close
#Length of total employment history

#print copyAllText

