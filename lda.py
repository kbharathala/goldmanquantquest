#import genism and the dictionary docDict
from gensim import corpora, models
from excelToDictionary import docDict 

#now we can create the lda model
#n is the number of topics that we want
#p is the number of laps the model takes through corpus
ldamodel = genism.models.ldamodel.LdaModel(docDict, num_topics=5, id2word = dictionary, passes=1)

#printing will give us the freq of a word in a doc a
docDict_lda = lda[docDict]

for l,t in izip(corpus_lda,corpus):
  print l,"#",t
print 
