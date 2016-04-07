#import genism 
from gensim import corpora, models
import csv

#create a dictionary with the texts
dictionary = corpora.Dictionary(excelToDictionary.docDict)

#this turns corpus into a list of vectors equal to the nunmber of docs
#in each doc vector there are tuples corresponding to (term ID, term freq)
corpus = [dictionary.doc2bow(excelToDictionary.docDict) for text in excelToDictionary.docDict]

#now we can create the lda model
#n is the number of topics that we want
#p is the number of laps the model takes through corpus
ldamodel = genism.models.ldamodel.LdaModel(corpus, num_topics=5, id2word = dictionary, passes=1)

#printing will give us the freq of a word in a doc a
corpus_lda = lda[corpus]

for l,t in izip(corpus_lda,corpus):
  print l,"#",t
print 
