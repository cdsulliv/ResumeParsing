#SCRAPCODE EDUCATION PARSING


# Modularize this function - should collect all univ info using separate functions
def extract_edu_info_new_xml(soup,stagger):
    #print soup
    arr = soup.findAll("text")
    #Cross verification step : First element should have education

    #if "EDUCATION" not in arr[0].text:
    #    return "Error: Education section not present"

    #arr.pop(0) #Removing heading which was 'education'
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
    #print univ_list
    for key in univ_list:
        val = univ_list[key]
        pos = val["arr_pos"]
        # print pos
        for item in arr[pos:len(arr)]:
            #print item.text
            item = item.text
            date = re.findall(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December|Sept)\s\d{4}', item)
            date_text = ""
            if date:
                date_text = date[0]
                exist_val = univ_list[key]
                exist_val["associated_date"] =  date_text
                univ_list[key] = exist_val
                break #Go to the next university to find its associated date

    gpa = get_gpa(arr)
    deanslist = get_deanslist(arr)
    return [univ_list, {"gpa": gpa}, {"deanslist": deanslist}]


# In[7]:


#
# with open('eggs.csv', 'wb') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=' ')
#     for entry in edudata_alt:
#         spamwriter.writerow(filename[i] + "\t" + str(entry))
#         i +=1


# # Issues

# * It's sooooooo slow! We need to remove the Stanford Tagger wherever possible. How can we speed up the tagger?
#     * Could try it in batches: nltk.tag.stanford.POSTagger.tag_sents()
# ## Checks:
# * Verify reliability of BIO parsing
# * Verify reliability of EDU parsing

# In[75]:

#
# server = smtplib.SMTP( "smtp.gmail.com", 587 )
# server.ehlo()
# server.starttls()
# server.login( 'cdsulliv@gmail.com', 'FL3XTH15' )
# server.sendmail( 'Colin', '3123163086@att.txt.net', 'CODE FINISHED RUNNING' )


# In[68]:



# Brown University 9 education section shouldn't contain this:
# 
#  [ {u' !Organized a black-tie fundraiser for Gulf Coast Oil Spill victims. ': {'arr_pos': 9}, u' !Courses Include: Introduction to Environmental Studies, Biology of Plants, Food and People, Foundation of Living Introduction to Environmental Studies, Biology of Plants, Food and People, Foundation of Living Introduction to Environmental Studies, Biology of Plants, Food and People, Foundation of Living ': {'arr_pos': 1, 'associated_date': u'June 2010'}, u'Los Alamitos High School, High School Diploma Los Alamitos, CA \u2013 Graduated June 2010 ': {'arr_pos': 4, 'associated_date': u'June 2010'}, u' !Provide free SAT preparatory classes for local high school students. ': {'arr_pos': 19}, u'Los Alamitos Unified School District, Teacher\u2019s Aide Los Alamitos, CA \u2013 Summer 2010 ': {'arr_pos': 14}, u'Ecofficiency.org, Intern  Costa Mesa, CA \u2013 Summer 2010  ': {'arr_pos': 8}}

# In[51]:




# In[38]:

# len(newdata)
#
#
# # In[59]:
#
# print drop2
# print newdata[178]
# bool(re.match(drop2, newdata[178]))
# #print datanp[178]
#
#
# # In[338]:
#
# # Remove files that don't contain useful information
# droplist = "|".join(['FILENAME', 'Wichita State University'])
#Error
# datanp = datanp[re.match(droplist, x) for x in datanp[:,0]]


# In[ ]:

# a= [re.match(droplist, x) for x in datanp[:,0]]
# print a


# In[176]:

#FAILED PREPROCESS STEP
# def preprocess(soup):
#     # Merge single letters with the following line
#     jointext = ""
#     for line in soup.findAll("text"):
#         if(jointext):
#             if(bool(line.contents)):
#                 fixed_text = unicode(line.text).replace(line.text, jointext+line.text)
#                 line.contents[0].replace_with(fixed_text)
#
#             jointext = ""
#         if(len(line.text)==1 and not line.text.isspace()):
#             #print line.text
#             jointext = line.text
#             line.extract()
#
#     # Merge multiple lines with same top height
#     tops = [line['top'] for line in soup.findAll('text')]
#     topcounts = { key:value for key,value in Counter(tops).items() if value>1 }
#     ctr = 1
#     last_text=""
#     for line in soup.findAll("text"):
#         cur_top = line['top']
#
#         if(str(cur_top) in topcounts):
#             if(ctr == topcounts[str(cur_top)]):
#                 fixed_text = unicode(line.text).replace(line.text, last_text+line.text)
#                 if(line.contents):
#                     line.contents[0].replace_with(fixed_text)
#                 else:
#                     line.contents.append(fixed_text)
#                 last_text = ""
#                 ctr = 1
#             elif(ctr < topcounts[str(cur_top)]):
#                 last_text = last_text+line.text
#                 line.extract()
#                 ctr = ctr+1
#
#     return soup


# In[ ]:

    # Drop useless resumes!
 #   droplist = "|".join(['FILENAME', 'Wichita State University'])
 #   boolz = [not bool(re.match(droplist, x[0])) for x in datanp]
 #   subs = np.where(boolz)
 #   datanp = datanp[subs]
    #print datanp.size
    # ### Check analysis of bio data

    '''biosoups = []
    for i in range(len(datanp)):
        biosoups.append(BeautifulSoup(datanp[i][2]))


    
    #biosoups = [BeautifulSoup(row) for row in datanp[:,2]]
    preprocessed = [preprocess(row) for row in biosoups]
    allbiodata = np.array([extract_person_info(soup, st) for soup in preprocessed])
    filename = [row for row in datanp[:,0]]

    # np.save("bioparsed", allbiodata)
    # print allbiodata

    i = 0

    file_o = open("out_bio_"+ out_filename+ ".txt","wb")
    for entry in allbiodata:
        file_o.write(filename[i] + "\t\t" + str(entry))
        file_o.write("\n\n")
        i +=1

    '''  



