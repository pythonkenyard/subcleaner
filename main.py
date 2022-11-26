import re
from tkinter import filedialog as fd
from fuzzywuzzy import fuzz

#TODO - 

#select and read file
subtitles_file_location = fd.askopenfilename()
print(subtitles_file_location)
with open (subtitles_file_location) as file:
    subtitle_lines = file.readlines()

#analyse for text.
sentencenumber = 1
sentencelist = []
print("checking for text")
for line in subtitle_lines:
    sentence = f"sentence_{sentencenumber}"
    output_sentence = re.search("[A-Za-z,;?\.\)\('\"\s]+",line)
    try:
        output_sentence = output_sentence.group(0)
        if len(output_sentence)>1:
            #print(output_sentence)
            sentencelist.append([sentencenumber,output_sentence])
    except:
        pass
    sentencenumber +=1

#compare sequential lines for similarity
print("comparing lines")
total_sentences = len(sentencelist)
current_sentence = 0
deletion_marker = []
try:
    while total_sentences > current_sentence:
        next_sentence = current_sentence+1
        similarity_value = fuzz.ratio(sentencelist[current_sentence][1], sentencelist[next_sentence][1])
        print(str(similarity_value))
        if similarity_value >48:
            print('value: ' + str(similarity_value))
            deletion_marker.append(sentencelist[current_sentence][0])
        current_sentence+=1
except:
    pass

#cleanup

#TODO
###Deletion marker list has a list of lines that need to be removed.
###Find the previous time indicator by splitting by -->
###find the next time indicator similarly.
###remove all content between these.
###need to track how many lines have been removed. subtitle_lines will be shortened by this amount so next loop through deletion indicator will need to consider this.
###loop through every iterator of deletion marker.

deletedlines = 0

for line in deletion_marker:
    #check previous line
    try:
        back_a_line = line -1
        previous_line = subtitle_lines[back_a_line]
        if "-->" in previous_line:
            first_splitline = previous_line.split("-->")[0]
        else:
            raise
    except:
      #check 2 lines back
        try:
            back_a_line = back_a_line -1
            previous_line = subtitle_lines[back_a_line]
            if "-->" in previous_line:
                first_splitline = previous_line.split("-->")[0]
            else:
                raise
        except:
          #check 3 lines back
            try:
                back_a_line = back_a_line -1
                previous_line = subtitle_lines[back_a_line]
                if "-->" in previous_line:
                    first_splitline = previous_line.split("-->")[0]
                else:
                    raise
            except:
                print("failed to find time indicator")



#TODO - save new file
