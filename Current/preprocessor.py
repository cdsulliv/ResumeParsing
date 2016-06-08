# # Preprocessing

# In[454]:
from bs4 import BeautifulSoup
from string import replace
import re
from bs4 import NavigableString

from collections import Counter
# Merge single letters with the following line
def merge_sletters(soup):
    #Grab all text tags from the soup
    textLines = soup.find_all('text')

    #Create list of key value pairs mapping each tag to its inner text
    texts = []
    for tag in textLines:
        texts.append((tag, tag.get_text()))

    to_join = []
    join_next = False
    #Iterate over the pairs
    for tag, text in texts:  
        #If we have a single character that needs joining, add the next tag to the list of tags to join
        if join_next:
            to_join.append(tag)


            #If the next tag is not a single character, join the tags into one and reset to_join and join_next
            if len(get_chars(text)) != 1:
                
                join(to_join)
                
                join_next = False
                to_join = []
        #If the tag contains only one character, add it to the to_join list and set join_next to true
        if len(get_chars(text)) == 1 and join_next == False:
            to_join.append(tag)
            join_next = True


def join(to_join):
    #Single letter tag
    first_tag = to_join[0]

    #Inner text of the single letter
    new_text = first_tag.get_text()
    wid = int(first_tag['width'])
    
    #Add each subsequent tag's text and delete each tag
    for tag in to_join[1:]:
        new_text = new_text + tag.get_text().strip()
        wid = wid + int(tag['width'])
        tag.decompose()

    #Edit the original tag
    inner = first_tag.contents
    if is_bold(first_tag) or is_italic(first_tag):
        inner[0].string = new_text
    elif is_bold_italic(first_tag):
        inner[0].contents[0].string = new_text
    else:
        first_tag.string = new_text
        
    first_tag['width'] = wid

#Finds all letters in a string
def get_chars(text):
    ret = "".join(re.findall("[a-zA-Z]+", text))
    return ret

#Deletes all tags consisting of only spaces
def remove_spaces(soup):
    textLines = soup.find_all('text')
    for tag in textLines:
        if tag.get_text() == " ":
            tag.decompose()


# In[330]:
#Merge multiple lines with same top height
def merge_lines(soup):
    bottom_map = {}
    #Create dictionary of tags at each bottom value
    for tag in soup.find_all('text'):
        bottom = int(tag['top']) + int(tag['height'])
        #Automatically add the first tag
        if len(bottom_map.keys()) == 0:
            bottom_map[bottom] = [tag]

        else:
            #Check if the bottom (or close enough) is already in the map, add if so
            exists = False
            for key in iter(bottom_map):
                if not exists and bottom in range(key - 2, key + 2):
                    bottom_map[key].append(tag)
                    exists = True
            #If not in the keyset already, add the bottom value
            if not exists:
                bottom_map[bottom] = [tag]

    #Join all appropriate tags' inner content
    for bottom in iter(bottom_map):
        num_tags = len(bottom_map[bottom])
        
        if num_tags != 1:
            tags = bottom_map[bottom]
            l = len(tags)
            #If there are more than one tags with a given bottom value, iterate over them and join, 
            #preserving inner bold/italic tags 
            for i in range(0, l):
                tag = tags[i]
                next_index = i + 1

                if next_index < l:
                    nexttag = tags[next_index]
                    end = int(tag['left']) + int(tag['width']) 
                    nextstart = int(nexttag['left'])
                    
                    # check that the beginning of each tag is within the range of other one's ending
                    if nextstart in range(end - 2, end + 3):

                        #Check if the entire tag is bold/italic/both/none
                        #If the current tag and the next have the same formatting, join them
                        if is_bold_italic(tag) and is_bold_italic(nexttag):
                            line_join(tag, nexttag, True)
                            #delete the old tag
                            nexttag.decompose()
                            #update the next tag to the combined version
                            tags[next_index] = tag

                        elif (is_bold(tag) and is_bold(nexttag)) or (is_italic(tag) and is_italic(nexttag)):
                            line_join(tag, nexttag, False)
                            nexttag.decompose()
                            tags[next_index] = tag

                        #If both the current and next tags are not bold or italic, join them
                        elif not is_italic(nexttag) and not is_bold(nexttag):
                            clean_join(tag, nexttag)
                            tags[next_index] = tag




#For checking if bold/italic/both
def is_bold_italic(tag):
    inside = join_contents(tag)
    return ("<b><i>" in inside[0:6] and "</b></i>" in inside[-8:]) or ("<i><b>" in inside[0:5] and "</i></b>" in inside[-8:])
def is_bold(tag):
    inside = join_contents(tag)
    return "<b>" in inside[0:3] and "</b>" in inside[-4:]
def is_italic(tag):
    inside = join_contents(tag)
    return "<i>" in inside [0:3] and "</i>" in inside[-4:]

def join_contents(tag):
    ret = ""
    for string in tag.contents:
        ret  = ret + unicode(string)
    return ret


#Used to join two tags that are either bold, italic or both
def line_join(tag1, tag2, both):
    if tag1.get_text().endswith(" ") or tag2.get_text().startswith(' '): 
        new_text = tag1.get_text() + tag2.get_text()
    else: 
        new_text = tag1.get_text() + ' ' + tag2.get_text()
    inner = tag1.contents
    if not both:
        inner[0].string = new_text
    #If both italic and bold, must go one step deeper
    else:
        inner[0].contents[0].string = new_text

#Join two tags with no inner bold/italic tags
def clean_join(tag1, tag2):
    #works:
    #new_text = join_contents(tag1) + join_contents(tag2)
    #tag1.string = new_text
    try:
        if tag1 is not None and tag2 is not None:
            end1 = tag1.contents[-1]
            start2 = tag2.contents[0]
            if "<b>" not in end1 and "<i>" not in end1 and "<b>" not in start2 and "<i>" not in start2:
                end_text = end1.string
                tag2.contents[0].string.replace_with(end_text + tag2.contents[0].string)
                tag1.contents[-1].string.replace_with('')
                 #for tag in tag2.contents:
                tag1.append(tag2.contents[0])
                if len(tag2.contents) == 0:
                    tag2.decompose()
            else:
                for tag in tag2.contents:
                    tag1.append(tag)
                tag2.decompose()
    except Exception, e:
        print e
        print tag1
        print tag2

# In[434]:

#Merge single letters on different lines, then merge same "bottom" lines, then remove spaces.
#Important to remove spaces last
def preprocess(soup):
    merge_sletters(soup)

    merge_lines(soup)

    remove_spaces(soup)



def main():
    '''
    soup = BeautifulSoup(open('output.xml'))
    for line in soup.find_all('text'):
        print line.contents
    '''
    
    #Testing preprocessor output on sample resume
    filename = "Youakim_Sophie_Resume.xml"

    soup = BeautifulSoup(open(filename), "html.parser")
    merge_sletters(soup)

    merge_lines(soup)
    
    remove_spaces(soup)

    xml = soup.prettify("utf-8")
    with open("output.xml", "wb") as file:
        file.write(xml)
    #print soup.text

def bs_preprocess(html):
     """remove distracting whitespaces and newline characters"""
     pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
     html = re.sub(pat, '', html)       # remove leading and trailing whitespaces
     html = re.sub('\n', ' ', html)     # convert newlines to spaces
                                        # this preserves newline delimiters
     html = re.sub('[\s]+<', '<', html) # remove whitespaces before opening tags
     html = re.sub('>[\s]+', '>', html) # remove whitespaces after closing tags
     return html 
bad_resumes = ['S+Joshi(1)_docx.xml', 
                'Oliver_Baverstam_Resume.xml', 
                'WendongRui_Resume+Ver5.05(1).xml', 
                'Trevor+Parkes+Graduate+Resume+2.xml']
from_csv = ['Weidi+Shen+resume.xml',
            'WendongRui_Resume+Ver5.05(1).xml',
            'wesley+Washington+Resume+2015_docx.xml']
worse_splitting = ['Alice+Johnson+Resume+July+2015.xml', 
                    '2+Jordyn+Epstein+Resume+10_18_15.xml', 
                    '(Mayowa_Omokanwaye)_Resume+2015.xml', 
                    'Jjones+official+resume+01+02+15_docx.xml', 
                    'JJohnson_July2015_Copywriter_docx.xml',
                    '2013+resume_docx.xml']

if __name__ == "__main__":
    main()

