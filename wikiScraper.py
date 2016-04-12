import urllib2
import re
import csv

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

BASE_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
COMPANY_COUNT = 1008

def file_cleaner(link):
    tokenizer = RegexpTokenizer(r'\w+')
    p_stemmer = PorterStemmer()

    f = urllib2.urlopen(link)
    text = f.read()

    # Removes all the html and extra white space
    text = re.sub('<[^>]*>', '', text)
    text = " ".join(text.split())
    
    # Removes everything after See Also
    first = text.find("See also")
    second = text[first+1:].find("See also")
    text = text[:first+second]

    # Removes everything before the start of the article
    first = text.find("navigation, search")
    text = text[first+18:]

    # Removes everything between brackets.
    text = re.sub(r'\[[^)]*\]', '', text)

    # Tokenizing and removing common stop words
    tokens = tokenizer.tokenize(text.lower())
    tokens = [unicode(i, 'ascii', 'ignore') for i in tokens]
    tokens = [str(i) for i in tokens if not i in get_stop_words('en')]
    tokens = [i for i in tokens if len(i) > 2]

    return tokens

#print(file_cleaner("https://en.wikipedia.org/wiki/3M"))

f = urllib2.urlopen(BASE_URL)
text = f.read()

with open('resultsTok.csv', 'wb') as f:
    writer = csv.writer(f)
    count = 0
    company_links = []
    company_industries = {}
    #company_text = {}
    while((text.find("<td><a href=\"/wiki/") != -1 or text.find("<td><a href=\"/w/index.php?title=") != -1) and count < COMPANY_COUNT*2 + 8):
        if(text.find("<td><a href=\"/wiki/") > text.find("<td><a href=\"/w/index.php?title=")):
            text = text[text.find("(page does not exist)")+10:]
            count += 1
        else:
            start = text.find("<td><a href=\"/wiki/")
            text = text[start+1:]
            end = text.find("title")
            start_industrial = text.find("reports</a></td>") + 20
            industrial_text = text[start_industrial+1:]
            end_industrial = industrial_text.find("<td><a href=") - 7
            end_general_industrial = industrial_text.find("</td>");
            if(count %2 == 0):
                general_industry_text = industrial_text[:end_general_industrial]
                specific_industry_text = industrial_text[end_general_industrial + 10 : end_industrial +1]
                company_name = text[18:end-2]
                print(company_name)
                company_industries[company_name] = (general_industry_text, specific_industry_text)
                link = "https://en.wikipedia.org/wiki/" + company_name
                clean_file = file_cleaner(link)
                #company_text[company_name] = file_cleaner(link)
                writer.writerow([company_name] + clean_file)
                if(company_name == "Zoetis"):
                    break
            count += 1
            text = text[end:]
    print(company_industries)