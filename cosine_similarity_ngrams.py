import numpy as np
import pandas as pd
import urllib2
import re

def file_cleaner(page_text):
    # Removes all the html and extra white space
    text = re.sub('<[^>]*>', '', page_text)
    text = " ".join(text.split())
    
    # Removes all the 
    first = text.find("See also")
    second = text[first+1:].find("See also")
    text = text[:first+second].split()
    return text 

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
        ngrams = ngrams_method(file_cleaner(dict[company]), n)
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
                val = cosine_distance(dict_ngrams[company1][:200], dict_ngrams[company2][:200]) # don't know what to do about reverse part
            df.xs(company1)[company2] = val
            print(val)
    return df

f = urllib2.urlopen("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
text = f.read()
count = 0
company_links = []
company_text = {}
print('here!')
while((text.find("<td><a href=\"/wiki/") != -1 or text.find("<td><a href=\"/w/index.php?title=") != -1) and count < 1008):
    if(text.find("<td><a href=\"/wiki/") > text.find("<td><a href=\"/w/index.php?title=")):
        print('I died')
        text = text[text.find("(page does not exist)")+10:]
        count += 1
    else:
        start = text.find("<td><a href=\"/wiki/")
        text = text[start+1:]
        end = text.find("title")
        if(count %2 == 0):
            company_name = text[18:end-2]
            link = "https://en.wikipedia.org/wiki/" + company_name
            company_text[company_name] = urllib2.urlopen(link).read()
            company_links.append(link)
        count += 1
        print(count)
        text = text[end:]

print(company_text)
print('hello')

cosine_similarity_n_grams(company_text, 1)
