from nltk import PorterStemmer
from ast import literal_eval as makeTuple
import math, operator

## Load dictionary into memory
dictionary = {}
print("Loading index…")
with open("dictionary", "r") as dict_file:
	for line in dict_file:
		term = makeTuple(line)
		dictionary[term[0]] = term[1]

## Load preprocessed corpus
corpus = {}
print("Loading preprocessed corpus…")
with open("corpus", "r") as corpus_file:
	for line in corpus_file:
		doc = makeTuple(line)
		corpus[doc[0]] = doc[1]

## compute average document length
accum = 0
for key in corpus:
	accum += len(corpus[key])
L_av = accum/len(corpus)



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

		## Begin ranking phase
		k = 1.2
		b = 0.75
		## list that holds the idf of all
		## query terms
		inverse_doc_freq_list = []
		
		doc_ranks = {}

		## compute idf of all query terms
		for query_term in split_query:
			if query_term in dictionary:
				d = len(dictionary[query_term])
			inverse_doc_freq_list.append(math.log10(len(corpus)/d))
		
		## compute RSV for each query-doc pair
		for doc in corpus:
			Ld = len(corpus[doc])
			## accumulate RSV values for each
			## term in query
			rank = 0
			for n in range(len(split_query)):
				## variables used are term_freq, inverse_doc_freq
				## parameters used are k, b, Ld, and L_av

				term_freq = corpus[doc].count(split_query[n])
				inverse_doc_freq = inverse_doc_freq_list[n]
				rank += inverse_doc_freq*(k+1)*term_freq/(k*((1-b)*b*Ld/L_av)+term_freq)

			doc_ranks[doc] = rank
		## sort RSV values and print top 10
		## docIDs 
		ranked_docs = sorted(doc_ranks.items(), key=operator.itemgetter(1), reverse=True)
		while i < 10 and i < len(ranked_docs):
			print(ranked_docs[i])
			i+=1
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
