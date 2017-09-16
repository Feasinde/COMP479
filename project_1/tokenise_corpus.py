import os,nltk
from bs4 import BeautifulSoup

PATH_TO_CORPUS = "/home/feasinde/Escritorio/reuters_corpus/"
list_of_files = []

for file in os.listdir(PATH_TO_CORPUS):
	if file.endswith(".sgm"): list_of_files.append(PATH_TO_CORPUS+file)

for path_to_filename in list_of_files:
	print("currently at:",path_to_filename)
	with open(path_to_filename) as sgm_file:
		token_soup = BeautifulSoup(sgm_file,'html.parser')
		list_of_articles = token_soup.find_all("reuters")
		print(list_of_articles[0].text)