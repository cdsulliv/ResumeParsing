# Change to directory with all resumes
cd "/Users/colin/Dropbox/Resume-audit/Scraping Project/Career Builder Resumes"
FILES="/Users/colin/Dropbox/Resume-audit/Scraping Project/Career Builder Resumes/Parsing Files/AllPDFs"

unoconv --listener &

for i in *.doc; do 
  name="${i%.*}"; 
  if  [ ! -f "$FILES/${name}_doc.pdf" ];then
      printf "$name\n";
      unoconv -f pdf -o "$FILES/${name}_doc" "$i"; 
  fi
done 

for i in *.docx; do 
  name="${i%.*}"; 
  if [ ! -f "$FILES/${name}_docx.pdf" ];then
      printf "$name\n";
      unoconv -f pdf -o "$FILES/${name}_docx" "$i"; 
  fi 
done 
kill -15 %-

# Move files that were originally PDFs into the same directory and remove duplicates
cp *.pdf "$FILES/"
fdupes -d -N "$FILES"