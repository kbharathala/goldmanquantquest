import csv
from bow import BagOfWords
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

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word = dictionary, passes=20)

# #printing will give us the freq of a word in a doc a
corpus_lda = ldamodel[corpus]

for l,t in izip(corpus_lda,corpus):
  print l,"#",t
print 