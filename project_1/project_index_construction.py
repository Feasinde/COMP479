##########################
## COMP 479 Project 1   ##
## Andrés Lou, 27142374 ##
##########################

import os,nltk,sys,json
from ast import literal_eval as makeTuple
from collections import OrderedDict

MEMORY_SIZE = 2

## open preprocessed corpus file, which contains
## all tokens found in the corpus
tokenised_corpus = open("tokenised_corpus_final")

## counter for the total number of blocks to be
## merged after SPIMI is done
file_block_n = 1

## nextToken() extracts and returns the 
## next token from the corpus to be added
## to the dictionary
def nextToken():
	str_token = tokenised_corpus.readline()
	if str_token == "": return ""
	token = makeTuple(str_token)
	return token

## Enter block size in MB
def SPIMI_Invert(block_size_B):
	block_size = block_size_B*1000000
	global file_block_n
	dictionary = {}
	while sys.getsizeof(dictionary) <= block_size:
		token = nextToken()
		if token == "": return False
		if token[0] not in dictionary: 
			dictionary[token[0]] = []
			dictionary[token[0]].append(token[1])
		else:
			dictionary[token[0]].append(token[1])
	sorted_dictionary = sorted(dictionary.items())
	with open("dict_block_"+str(file_block_n)+".txt", "w") as file_block:
		for tup in sorted_dictionary:
			file_block.write(str(tup)+"\n")
		file_block_n+=1
	return True
## Function that merges two blocks and produces a file containing 
## their index information 
def mergeBlocks(file_handle1, file_handle2, index_file_name):
	file_name = str(index_file_name)
	index = open(file_name,"w")
	buffer1 = []
	buffer2 = []
	eof1 = False
	eof2 = False
	for i in range(1000):
		term = file_handle1.readline()
		buffer1.append(makeTuple(term))
		term = file_handle2.readline()
		buffer2.append(makeTuple(term))
	while eof1==False or eof2==False:
				
		# begin term comparison. The lowest term is written to disc and
		# popped from the buffer
		if buffer2 != [] and buffer1 != []:
			if buffer1[0][0] < buffer2[0][0]:
				index.write(str(buffer1.pop(0))+"\n")
			elif buffer1[0][0] > buffer2[0][0]:
				index.write(str(buffer2.pop(0))+"\n")
			elif buffer1[0][0] == buffer2[0][0]:
				combined_postings = buffer1[0][1] + buffer2[0][1]
				merged_term = (buffer1[0][0],combined_postings)
				index.write(str(merged_term)+"\n")
				buffer1.pop(0)
				buffer2.pop(0)
		# if buffer1 is empty add all entries of buffer2 to disc
		# and vice versa
		elif buffer1 == [] and buffer2 != []:
			while buffer2 != []: index.write(str(buffer2.pop(0))+"\n")
		elif buffer2 == [] and buffer1 != []:
			while buffer1 != []: index.write(str(buffer1.pop(0))+"\n")

		# check if buffers are empty and refill them if so
		if buffer1 == []:
			for i in range(1000):
				term = file_handle1.readline()
				if term != "": 
					buffer1.append(makeTuple(term))
		if buffer1 == []: 
			print("buffer1 is empty")
			eof1 = True
		if buffer2 == []:
			for i in range(1000):
				term = file_handle2.readline()
				if term != "": 
					buffer2.append(makeTuple(term))
		if buffer2 == []: 
			print("buffer2 is empty")
			eof2 = True
	print(eof1,eof2)

	index.close()
########################
## Begin main program ##
########################

cont = SPIMI_Invert(MEMORY_SIZE)
while cont:
	cont = SPIMI_Invert(MEMORY_SIZE)

tokenised_corpus.close()

# Begin block merging

# list that stores the buffers of all the
# files to be opened
list_of_files = []

## dictionary for sorted entries from buffer
buffer_dict = {}

## list of buffers for each block to be merged
list_of_buffers = []

## get the current working directory and the list
## of blocks to be merged
cwd = os.getcwd()
for file in os.listdir(cwd):
	if file.endswith(".txt"): list_of_files.append(cwd+"/"+file)

for i in range(len(list_of_files)): print(list_of_files[i])

# Open all files
for i in range(len(list_of_files)):
	list_of_files[i] = open(list_of_files[i])

# Perform the merging. n is a counter used
# to name the dictionary as it progressively
# increases
n = 1
mergeBlocks(list_of_files[0],list_of_files[1],n)
list_of_files.pop(0)
list_of_files[0] = open(str(n))
while len(list_of_files) != 1:
	n+=1
	mergeBlocks(list_of_files[0],list_of_files[1],n)
	list_of_files.pop(0)
	list_of_files[0] = open(str(n))


