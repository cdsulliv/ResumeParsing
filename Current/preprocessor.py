# # Preprocessing

# In[454]:

from collections import Counter

def merge_sletters(soup):
    # Merge single letters with the following line
    jointext = ""
    s_set = set([])
    for line in soup.findAll("text"):
        if(jointext): 
            if(bool(line.contents)):

                if(line.contents[0].string):
                    fixed_text = jointext+line.contents[0].string
                    line.contents[0].replace_with(fixed_text)   
            jointext = ""
        if(len(line.text)==1):
            # print line.text
            s_set.add(line["top"])
            jointext = line.text
        else:
            if(line["top"] in s_set):
                s_set.remove(line["top"])
    return soup,s_set


# In[330]:

def merge_toplines(soup,s_set):
    #Merge multiple lines with same top height
    tops = [line['top'] for line in soup.findAll('text')]

    tops_red = []

    for x in tops:
        if x in s_set:
            tops_red.append(x)
    #print tops_red
    topcounts = { key:value for key,value in Counter(tops_red).items() if value>1 }
    ctr = {key:1 for key in topcounts}
    texts = {key:"" for key in topcounts}
    last_text=''

    for line in soup.findAll("text"):
        cur_top = line['top']

        if(str(cur_top) in topcounts):
            if(ctr[str(cur_top)] == topcounts[str(cur_top)]):
                fixed_text = unicode(line.text).replace(line.text, texts[str(cur_top)]+line.text)
                if(line.contents):
                    line.contents[0].replace_with(fixed_text)   
                #last_text = ""
            elif(ctr[str(cur_top)] < topcounts[str(cur_top)]):
                texts[str(cur_top)] = texts[str(cur_top)]+line.text
                line.extract()
                ctr[str(cur_top)] = ctr[str(cur_top)]+1
    return soup


# In[434]:

# Change this: should only merge_toplines on lines that had single-letter changes
def preprocess(soup):
    soup,s_set = merge_sletters(soup)
    #print s_set
    merge_toplines(soup,s_set)
  
    return soup