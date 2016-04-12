import csv
import gensim
from bow import BagOfWords
from gensim import corpora, models
import pandas as pd

docDict = {}
docList = []

with open('resultsTok.csv', 'rt') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		docDict[row[0]] = row[1:]
		docList.append(row[1:])

#import genism 

#this turns corpus into a list of vectors equal to the nunmber of docs
#in each doc vector there are tuples corresponding to (term ID, term freq)
print('here1')
texts = pd.read_csv('resultsTok.csv', header=0, delimiter="/t", quoting=3 )
texts_data_features = vectorizer.transform(texts)
print texts.shape

#Create am empty list and append the clean reviews one by one 
print('here2')
#now we can create the lda model
#n is the number of topics that we want
#p is the number of laps the model takes through corpus
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word = docDict, passes=1)

#printing will give us the freq of a word in a doc a
corpus_lda = lda[corpus]

for l,t in izip(corpus_lda,corpus):
  print l,"#",t
print 
