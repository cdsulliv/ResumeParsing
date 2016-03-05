import os
from utilities import getFiles

def pdfToXML(inputfilepath="", outdir=""):
    filename, file_extension = os.path.splitext(os.path.basename(inputfilepath))
    print filename
    command = "pdftohtml -i -xml '" + inputfilepath + "' '" + outdir + filename +".xml'"

    os.system(command)


def convertAll(dirpath="", outdir=""):
    filepaths = [dirpath + f for f in os.listdir(dirpath)]
    for filepath in filepaths:
        if filepath[-4:] == ".pdf":
            pdfToXML(filepath, outdir)

if __name__ == "__main__":
    
    dirpath = "/Users/colin/Dropbox/Resume-audit/Scraping Project/Career Builder Resumes/Parsing Files/AllPDFs/"
    outdir = "/Users/colin/Dropbox/Resume-audit/Scraping Project/Career Builder Resumes/Parsing Files/XML/"
    convertAll(dirpath, outdir)
    