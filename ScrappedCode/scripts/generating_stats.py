from __future__ import division
import os
import collections

INPUT_RESUMES = "/home/sajal/Wharton/resumes/txts"

WORDS_TO_CHECK = ["Education","Experience"] #Add words in this list to get its statistics

def get_all_files(directory):
    return os.listdir(directory)


if __name__ == "__main__":

    word_to_map ={}
    for word in WORDS_TO_CHECK:
        l = get_all_files(INPUT_RESUMES)
        file_path = [INPUT_RESUMES + "/" + file for file in l]
        cnt_upper = 0;
        cnt_lower =0;
        cnt_none =0;
        cnt_proper =0;
        file_cnt = len(file_path)
        for file in file_path:
             file_text = open(file,"r").read()
             c =collections.Counter(file_text.split())
             if(c[word.upper()] != 0):
                 cnt_upper = cnt_upper + 1
             elif(c[word.title()] != 0):
                 cnt_proper = cnt_proper + 1
             elif(c[word.lower()] != 0):
                 cnt_lower = cnt_lower +1
             else:
                 cnt_none = cnt_none+1
        inner_map = {"Proper Case " : cnt_proper, "Upper Case " : cnt_upper, "Lower Case " : cnt_lower, "Not found" : cnt_none}
        word_to_map[word] = inner_map

    print word_to_map