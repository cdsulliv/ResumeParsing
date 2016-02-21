# Resume-Parsing

Step by step process to parse resume:

 
0. LibreOffice 
Convert from Word docs to PDF using LibreOffice command line. (Script). This code is not currently in the directory - need to find it elsewhere. 

- Need to verify this step. Losing text from (Bryony+Grant) resume. Unclear if lost text is from this step or PDF to XML step.

1. scripts/pdf_to_xml_v2.py 
Convert PDF to XML.
Set the values of input directory path (PDF directory) and output directory path (where you want your XML files to be stored) in the code. Run the script by typing in commandline "python pdf_to_xml_v2.py"

2. After-Oct-2015/HeaderSplitting.py
Once you have the XML files, run this script to generate a CSV that has resume parts categorised into header fields. Must update local XML directory path before running. Run it with the command "python HeaderSplitting.py" in the terminal window.

Output: HeaderSplitData.csv

Note: Need to run find_all_possible_headings.py and find_set_of_headings.py to create the all_headings.txt files that get read into POSSIBLE_HEADINGS. Code then compares against this list of possible headings to identify any missed headings.

NOTE:  preprocessor.py
Fix the preprocessor to run prior to splitting.

TO DO: 
(a) Fix the preprocessing code to run before splitting
(b) Eliminate the need to call on find_all_possible_headings.py and find_set_of_headings.py and create extra txt files. 
(c) Correct some misidentications. Why is Araujo%2c getting the wrong header?

3. After-Oct-2015/BioAndEducation.py
Parse the bio section and the education section.
Requires Stanford Tagger (NER). Need to update line 284 to reflect location of .jar file on local machine.
Update line 362 to reflect location of files in local machine.

Output: New text file containing JSON information on bio and education for all files in the input CSV list.

Need to capture:
- Dean's List. Getting too many false negatives. Deanâ€™s List doesn't identify (Fall+2015+Resume). 
- GPA. Seem to be missing too many of them. 
- Major
- Degree (BA, BS, etc)
- Sum Cum Laude, Cum Laude, Valedictorian

Need to clean:
- location recognizer. don't embed the call to states.csv - separate, and create link in the variables at the top

4. Leader Exp.py
Parse Leadership experience section.
Calls on the sports list and identifies frats, sports, clubs & orgs

Right now, only reads the sample. Need to update to pull from CSV with Leadership section.
No output, only prints to screen.

5. Experience.py
Input: CSV 
line 238 hardcodes the files it needs to read.
Output: Writes new CSV file for each CSV input file


Need to Create:
6. Awards and Honors; Achievements. Identify any major awards, and look for Dean's List here as well.


utilities.py - Contains one function for obtaining list of file. Can be replaced with one line of code; remove it from all files and delete

Data from Outside Sources
sports-list.txt - list of sports for identifying sports participation
states.csv and StateAbbreviations.csv - list of states and their 2 letter abbrevs. Need to delete one file after removing from code
position_list.txt - contains the most common job titles on Glassdoor


RA help:
- Find examples of multi-page PDF and word docs. Are we losing information? If so, at what stage? 