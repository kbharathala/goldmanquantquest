import urllib2
import re
import csv

BASE_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
COMPANY_COUNT = 1008

def file_cleaner(link):
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
    return text

f = urllib2.urlopen(BASE_URL)
text = f.read()

with open('results.csv', 'wb') as f:
    writer = csv.writer(f)
    count = 0
    company_links = []
    #company_text = {}
    while((text.find("<td><a href=\"/wiki/") != -1 or text.find("<td><a href=\"/w/index.php?title=") != -1) and count < COMPANY_COUNT*2 + 8):
        if(text.find("<td><a href=\"/wiki/") > text.find("<td><a href=\"/w/index.php?title=")):
            text = text[text.find("(page does not exist)")+10:]
            count += 1
        else:
            start = text.find("<td><a href=\"/wiki/")
            text = text[start+1:]
            end = text.find("title")
            if(count %2 == 0):
                company_name = text[18:end-2]
                print(company_name)
                link = "https://en.wikipedia.org/wiki/" + company_name
                #company_text[company_name] = file_cleaner(link)
                writer.writerow([company_name, file_cleaner(link)])
            count += 1
            text = text[end:]