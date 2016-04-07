import csv
import gensim
from gensim import corpora, models

docDict = {}
docList = []

with open('resultsTok.csv', 'rt') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		docDict[row[0]] = row[1:]
		docList.append(row[1:])
	corpus = [docDict.doc2bow(csvfile) for Tok in resultsTok.csv]

#import genism 

#this turns corpus into a list of vectors equal to the nunmber of docs
#in each doc vector there are tuples corresponding to (term ID, term freq)
#now we can create the lda model
#n is the number of topics that we want
#p is the number of laps the model takes through corpus
ldamodel = genism.models.ldamodel.LdaModel(corpus, num_topics=5, id2word = docDict, passes=1)

#printing will give us the freq of a word in a doc a
corpus_lda = lda[corpus]

for l,t in izip(corpus_lda,corpus):
  print l,"#",t
print 
