import csv
from bow import BagOfWords
import gensim
from gensim import corpora, models

docDict = {}
docList = []

with open('resultsTok.csv', 'rt') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		docDict[row[0]] = row[1:]
		docList.append(row[1:])

dictionary = corpora.Dictionary(docList)
corpus = [dictionary.doc2bow(text) for text in docList]
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word = dictionary, passes=3)
print(ldamodel.show_topics(num_topics=10, num_words=10, log=False, formatted=True))
# corpus_lda = ldamodel[corpus]

# for i in range(min(len(corpus_lda), len(corpus))):
# 	print(corpus_lda[i], corpus[i])