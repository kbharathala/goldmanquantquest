import numpy as np
import pandas as pd
import urllib2
import re
import csv
import scipy.spatial.distance as ssd

def cosine_distance(u, v):
    return np.dot(u, v) / (math.sqrt(np.dot(u, u)) * math.sqrt(np.dot(v, v)))

def ngrams_method(sequence, n):
    sequence = list(sequence)
    count = max(0, len(sequence) - n + 1)
    return [tuple(sequence[i:i+n]) for i in range(count)]

#not sure what n is equal to yet
def cosine_similarity_n_grams(dict, n):
    dict_ngrams = {}
    for company in dict:
        ngrams = ngrams_method(dict[company], n)
        dict_ngrams[company] = ngrams
        print(ngrams)
    companies = dict_ngrams.keys()
    df = pd.DataFrame(index = companies, columns= companies)
    for company1 in dict_ngrams:
        for company2 in dict_ngrams:
            val = 0
            if company1 == company2:
                continue
            else:
                val = ssd.cosine(dict_ngrams[company1], np.transpose(dict_ngrams[company2]))
            df.xs(company1)[company2] = val
            print(val)
    return df

docDict = {}
docList = []

with open('resultsTok.csv', 'rt') as csvfile:
  reader = csv.reader(csvfile, delimiter=',', quotechar='|')
  for row in reader:
      docDict[row[0]] = row[1:]
      docList.append(row[1:])

print(docDict) #stuff

cosine_similarity_n_grams(docDict, 1)
