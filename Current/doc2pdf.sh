# Change to directory with all resumes
cd "/Users/colin/Dropbox/Resume-audit/Scraping Project/Career Builder Resumes"

#unoconv --listener &
for i in *.doc *.docx; do 
unoconv -f pdf -o "/Users/colin/Dropbox/Resume-audit/Scraping Project/Career Builder Resumes/Parsing Files/WordPDFs" "$i"; 
done 

# Rename with a _doc at the end to distinguish from similarly named PDFs
FILES="/Users/colin/Dropbox/Resume-audit/Scraping Project/Career Builder Resumes/Parsing Files/WordPDFs"
for i in "$FILES"/*; do echo "$i"; 

name="${i%.*}"; 
mv "$i" "${name}_doc${i#$name}"; 

done
