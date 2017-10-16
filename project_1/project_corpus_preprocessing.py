import nltk, os, re
from bs4 import BeautifulSoup

PATH_TO_CORPUS = "/home/feasinde/Escritorio/reuters_corpus/"

list_of_files = []
# stopwords = ['april', 'with', 'is', 'from', 'its', 'at', 'dlrs', 'by', "'s", 'mln', 'on', 'usa', '>', '<', 'for', 'march', 'it', 'and', 'said', 'a', 'of', 'in', 'to', '.', 'reuter', ',', '-', 'reute', 'f', 'the']
# stopwords = ['current', 'record', 'because', 'month', 'board', 'when', 'six', 'financial', 'years', 'february', 'canada', 'added', 'into', 'rate', 'foreign', 'june', 'ltd', 'against', 'prices', 'could', 'total', 'week', 'president', 'agreement', 'due', 'oil', 'securities', 'five', 'price', 'unit', 'their', 'debt', 'expected', 'per', 'there', 'we', 'all', 'london', 'interest', 'loss', 'some', 'today', 'if', 'qtr', 'japan', 'shr', 'government', 'under', 'acq', 'three', 'told', 'group', 'sales', 'than', 'washington', 'no', 'shares', 'exchange', 'over', 'b', 'international', 'other', 'trade', 'dlr', 'after', 'share', 'more', 'first', 'blah', 'vs', 'been', 'd', 'may', 'co', 'york', 'cts', 'they', 'market', 'stock', 'or', ')', 'had', 'about', '(', 'two', 'billion', 'up', 'also', 'have', 'u.s.', 'one', 'earn', 'last', 'were', 'are', 'would', '``', "''", 'bank', 'this', 'net', 'but', 'not', 'which', 'he', 'corp', 'company', 'as', 'inc', 'was', 'r', 'has', 'that', 'an', 'year', 'pct', 'new', 'be', 'will', 'u', 'april', 'with', 'is', 'from', 'its', 'at', 'dlrs', 'by', "'s", 'mln', 'on', 'usa', '>', '<', 'for', 'march', 'it', 'and', 'said', 'a', 'of', 'in', 'to', '.', 'reuter', ',', '-', 'reute', 'f', 'the']
## Load the stemmer from nltk

stemmer = nltk.PorterStemmer()
for file in os.listdir(PATH_TO_CORPUS):

## Gather all corpus file locations
	if file.endswith(".sgm"): list_of_files.append(PATH_TO_CORPUS+file)

for file in list_of_files:
	n=1
	## Each file gatheredi in the previous block is converted into
	## a BeautifulSoup object for parsing and extraction
	with open(file) as corpus_file:
		file_soup = BeautifulSoup(corpus_file,'html.parser')
	
	## Write each processed corpus file to another file, labelled as such
	with open(file+"_tokenised.txt","a") as tokens_file:
		articles = file_soup.find_all("reuters")
		for document in articles:
			## Gather the text and the docID using BS
			doc_text = document.text.strip()
			doc_ID = document["newid"]
			## Tokenise the text and finally write to file
			tokens = set(nltk.word_tokenize(doc_text))
			for token in tokens:
				# if not token in stopwords:
				# if not re.match(".*\d.*",token):
				## Stemming, case folding, and HES removal are performed here
				if not re.match(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]',token):
					tokens_file.write(str((stemmer.stem(token.lower()),doc_ID))+"\n")

## A final operation is required involving the 
## concatenation of the resulting files into one
## big preprocessed corpus file
