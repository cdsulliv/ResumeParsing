read -p "Enter the resume path: " input
# input must have full path to the directory of pdfs:  "/home/sajal/Wharton/resumes"
if [ -d "$input" ]; then
	for file in "$input"/*
	do
		if [[ $file == *.pdf ]] ;
			then 
			# mkdir -p "$input/out_txts"
			f=${file::-4}
			"pdf2txt.py" "$file" > "$f.txt"
			echo "$file"
		else
		 echo "Not a pdf file"	
		fi
	done
else
	echo "Directory entered does not exist"
fi
