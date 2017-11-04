import nltk, os, re
from bs4 import BeautifulSoup

PATH_TO_CORPUS = ""
PATH_TO_CORPUS_FILE = ""

list_of_files = []

corpus_file = open(PATH_TO_CORPUS_FILE, "a")

for file in os.listdir(PATH_TO_CORPUS):
	if file.endswith(".sgm"): list_of_files.append(PATH_TO_CORPUS+file)

for file in list_of_files:
	with open(file) as corpus_file:
		file_soup = BeautifulSoup(corpus_file, 'html.parser')
		articles = file_soup.find_all("reuters")
		for document in articles:
			tokens_no_hes = []
			doc_text = document.text.strip()
			doc_ID = document["newid"]
			tokens = nltk.word_tokenize(doc_text))
			for token in tokens:
				if not re.match(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]',token):
					tokens_no_hes.append(token)
			corpus_file.write(str(doc_ID)+str(tokens_no_hex))
