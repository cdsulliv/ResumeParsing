# Resume-Parsing

Step by step process to parse resume:

 
0. LibreOffice 
Convert from Word docs to PDF using LibreOffice command line. (Script). This code is not currently in the directory - need to find it elsewhere.

1. scripts/pdf_to_xml_v2.py 
Convert PDF to XML.
Set the values of input directory path (PDF directory) and output directory path (where you want your XML files to be stored) in the code. Run the script by typing in commandline "python pdf_to_xml_v2.py"

2. After-Oct-2015/splitting_xml.py
Note: out_edu_split_v does not yet exist, so comment out line 264, 281-EVERYTHING WITH GRAD_DATE, and 373-374 (those variables don't exist). Run this code with those lines commented out, then re-run the whole code after obtaining grad information in later step. 

Once you have the XML files, run this script to generate a Csv that has resume parts categorised into some fields. The Csv can be found at Data/split.csv . The script needs to be provided XML directory path before running it. Run it by "python splitting_xml.py". Need to update locations to local machine. This will output several CSV files to make them small enough to process in later stages.

Note: Need to run find_all_possible_headings.py and find_set_of_headings.py to create the all_headings.txt files that get read into POSSIBLE_HEADINGS. Code then compares against this list of possible headings to identify any missed headings.

NOTE:  preprocessor.py
Fix the preprocessor to run prior to splitting.

TO DO: 
(a) Fix the preprocessing code to run before splitting
(b) Write a separate file to identify resume criteria AFTER splitting and other steps are complete. This should alleviate the need to comment out this file and run it multiple times.
(c) Figure out how to use the headings files, and why we need to create a separate list. Suspect we can 

3. After-Oct-2015/parsing_from_split.py
Parse the bio section and the education section.
Requires Stanford Tagger (NER). Need to update line 284 to reflect location of .jar file on local machine.
Update line 362 to reflect location of files in local machine.

Output: New text file containing JSON information on bio and education for all files in the input CSV list.

4. Leader Exp.py
Parse Leadership experience section.
Calls on the sports list and identifies frats, sports, clubs & orgs

Right now, only reads the sample. Need to update to pull from CSV with Leadership section.
No output, only prints to screen.

5. Experience parse.py
Input: CSV 
line 238 hardcodes the files it needs to read.
Output: Writes new CSV file for each CSV input file



utilities.py - contains a useful function to get all the files

Data from Outside Sources
sports-list.txt - list of sports for identifying sports participation
states.csv - list of states
position_list.txt - contains the most common job titles on Glassdoor
