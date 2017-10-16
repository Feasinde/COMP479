from nltk import PorterStemmer
from ast import literal_eval as makeTuple

## Load dictionary into memory
dictionary = {}
print("Loading index…")
with open("dictionary", "r") as dict_file:
	for line in dict_file:
		term = makeTuple(line)
		dictionary[term[0]] = term[1]

## Load stemmer
stemmer = PorterStemmer()

## OR flag to determine whether query contains
## a disjunction
QUERY = ""

while True:
	intersect = []
	isOR = False
	## list of postings of each query term
	query_postings = []
	print("Enter ':q' to quit")
	QUERY = input("Input query: ")
	if QUERY == ":q": break

	## default querying is taken to be and
	if not "OR" in QUERY:
		split_query = QUERY.split()
	else:
		isOR = True
		split_query = QUERY.split("OR")
		for i in range(len(split_query)):
			split_query[i] = split_query[i].strip()

	## stemming and case folding
	for i in range(len(split_query)):
		split_query[i] = stemmer.stem(split_query[i])

	## get postings form dictionary
	for term in split_query:
		if term in dictionary:
			query_postings.append(dictionary[term])

	## AND queries
	if not isOR:
		if len(query_postings) > 1:				
			intersect = set(query_postings[0]).intersection(query_postings[1])
			query_postings.pop(0)
			query_postings[0] = intersect
			while len(query_postings) != 1:
				intersect = set(query_postings[0]).intersection(query_postings[1])
				query_postings.pop(0)
				query_postings[0] = intersect
		elif len(query_postings) == 1:
			intersect = set(query_postings[0])
		else: print("Query not found.")
	## OR queries	
	else:
		for term in split_query:
			if term in dictionary:
				query_postings.append(dictionary[term])
		if query_postings != []:
			for posting in query_postings:
				intersect = intersect + posting
			intersect = set(intersect)
		else: print("Query not found.")

	print("\n",intersect, "\n\nNumber of hits:", len(intersect))
