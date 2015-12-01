# Resume-Parsing

Step by step process to parse resume:

1. scripts/pdf_to_xml_v2.py 

Set the values of input directory path (PDF directory) and output directory path (where you want your XML files to be stored) in the code. Run the script by typing in commandline "python pdf_to_xml_v2.py"

2. After-Oct-2015/splitting_xml.py

Once you have the XML files, run this script to generate a Csv that has resume parts categorised into some fields. The Csv can be found at Data/split.csv . The script needs to be provided XML directory path before running it. Run it by "python splittig_xml.py"

3.
 