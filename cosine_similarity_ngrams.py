import numpy as np
import pandas as pd

#not sure what n is equal to yet
def cosine_similarity_n_grams(dict, n):
	dict_ngrams = {}
	for company in dict:
		dict_ngrams[company] = ngrams(dict[company], n)
	companies = dict_ngrams.keys()
	df = pd.DataFrame(index = companies, columns= companies)
	for company1 in dict_ngrams:
		for company2 in dict_ngrams:
			val = 0
			if company1 == company2:
			else: 
				val = consine_distance(dict_ngrams[company1], dict_ngrams[company2]) # don't know what to do about reverse part
			df.xs(company1)[company2] = val
	return df

	
def get_array_words(html):
# write!

def cosine_distance(u, v):
    return np.dot(u, v) / (math.sqrt(np.dot(u, u)) * math.sqrt(np.dot(v, v)

def ngrams(sequence, n, pad_left=False, pad_right=False, pad_symbol=None):
	if pad_left:
        sequence = chain((pad_symbol,) * (n-1), sequence)
    if pad_right:
        sequence = chain(sequence, (pad_symbol,) * (n-1))
    sequence = list(sequence)

    count = max(0, len(sequence) - n + 1)
    return [tuple(sequence[i:i+n]) for i in range(count)] 
