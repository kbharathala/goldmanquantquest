import urllib2
import re
import csv
import math
import pandas as pd

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

BASE_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
COMPANY_COUNT = 1008
company_equities = {}
company_industries = {}
company_locations = {}
company_years = {}
companies = []
all_states = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona",
"California", "Colorado", "Connecticut", "District ", "of Columbia",
"Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho",
"Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts",
"Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi",
"Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire",
"New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma",
"Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina",
"South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands",
"Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

def company_industry_multiples(company1, company2):
    if (company1 not in company_industries):
        print("Error: company not in dictionary")
    elif (company2 not in company_industries):
        print("Error: company not in dictionary")
    else:
        company1_info = company_industries[company1]
        company2_info = company_industries[company2]
        toMultiply = 1
        if (company1_info[1] == company2_info[1]):
            toMultiply = math.sqrt(4)
        elif (company1_info[0] == company2_info[0]):
            toMultiply = math.sqrt(2)
        print(toMultiply)
        return toMultiply

def company_location_multiples(company1, company2):
    if (company1 not in company_locations):
        print("Error: company not in dictionary")
    elif (company2 not in company_locations):
        print("Error: company not in dictionary")
    else:
        company1_location = company_locations[company1]
        company2_location = company_locations[company2]
        toMultiply = 1
        if (company1_location == company2_location):
            toMultiply = math.sqrt(4)
        print(toMultiply)
        return toMultiply

def company_equity_multiples(company1, company2):
    if (company1 not in company_equities):
        print("Error: company not in dictionary")
    elif (company2 not in company_equities):
        print("Error: company not in dictionary")
    else:
        company1_equity = company_equities[company1]
        company2_equity = company_equities[company2]
        toMultiply = 1#something to change
        if ((company1_equity == 0) or (company2_equity == 0)):
            toMultiply = 1
        else:
            if (abs(math.log10(company1_equity)-math.log10(company2_equity))<=1):
                toMultiply = math.sqrt(5)
            else:
                if (abs(math.log10(company1_equity)-math.log10(company2_equity))<=2):
                    toMultiply = math.sqrt(4)
                else:
                    if (abs(math.log10(company1_equity)-math.log10(company2_equity))<=3):
                        toMultiply = math.sqrt(3)
                    else:
                        if (abs(math.log10(company1_equity)-math.log10(company2_equity))<=4):
                            toMultiply = math.sqrt(2)
        print(toMultiply)
        return toMultiply

def company_year_multiples(company1, company2):
    if (company1 not in company_years):
        print("Error: company not in dictionary")
        exit()#delete this!
    elif (company2 not in company_years):
        print("Error: company not in dictionary")
        exit()#delete this!
    else:
        company1_year = company_years[company1]
        company2_year = company_years[company2]
        toMultiply = 1#something to change
        if ((company1_year == 0) or (company2_year == 0)):
            toMultiply = 1
        else:   #NEED TO CHANGE THIS
            if (abs(math.log10(company1_year)-math.log10(company2_year))<1):
                toMultiply = math.sqrt(2)
        print(toMultiply)
        return toMultiply        

def create_econ_link_matricies():
    matrix_dict = {}
    im = pd.DataFrame(index = companies, columns = companies)
    lm = pd.DataFrame(index = companies, columns = companies)
    em = pd.DataFrame(index = companies, columns = companies)
    yr = pd.DataFrame(index = companies, columns = companies)
    count = 0
    for company1 in companies:
        for company2 in companies:
            val_i = 1
            val_l = 1
            val_e = 1
            val_y = 1
            if company1 != company2:
                val_i = company_industry_multiples(company1, company2)
                val_l = company_location_multiples(company1, company2)
                val_e = company_equity_multiples(company1, company2)
                val_y = company_year_multiples(company1, company2)
            im.xs(company1)[company2] = val_i
            lm.xs(company1)[company2] = val_l
            em.xs(company1)[company2] = val_e
            yr.xs(company1)[company2] = val_y
            count += 1
            print(count)
    matrix_dict['industry_matrix'] = im
    matrix_dict['location_matrix'] = lm
    matrix_dict['equity_matrix'] = em
    matrix_dict['year_matrix'] = yr
    return matrix_dict

def matrix_compilation(full_matrix_dict):
    count = 0
    industry_matrix = matrix_dict['industry_matrix']
    location_matrix = matrix_dict['location_matrix']
    equity_matrix = matrix_dict['equity_matrix']
    year_matrix = matrix_dict['year_matrix']
    final_matrix = pd.DataFrame(index = companies, columns = companies)
    sum_dict = {}
    for company1 in companies:
        sum_row = 0
        for company2 in companies:
            val = industry_matrix.get_value(company1, company2) * location_matrix.get_value(company1, company2) * equity_matrix.get_value(company1, company2) * year_matrix.get_value(company1, company2)#will need to be modified once we have lda
            final_matrix.xs(company1)[company2] = val
            sum_row += val
        sum_dict[company1] = sum_row
    for company1 in companies:
        divisor = sum_dict[company1]
        sum_row = 0
        for company2 in companies:
            val = (final_matrix.get_value(company1, company2) / divisor)
            final_matrix.xs(company1)[company2] = val
            sum_row += val
    return final_matrix

def file_cleaner(link, company_name):

    print(company_name)

    tokenizer = RegexpTokenizer(r'\w+')
    p_stemmer = PorterStemmer()

    f = urllib2.urlopen(link)
    text = f.read()

    temp = text

    # Removes everything after See Also
    first = temp.find("See also")
    second = temp[first+1:].find("See also")
    temp = temp[:first+second]

    # Removes everything before the start of the article
    first = temp.find("navigation, search")
    temp = temp[first+18:]

    temp = temp[temp.find("Website"):]
    tokens = []

    # box_text = temp[temp.find('AbbVie'):]
    # print(box_text)
    # year_start = box_text.find("Founded")
    # year_stop = box_text.find(";")
    # year_text = box_text[year_start:year_stop]
    # print(year_text)

    common_words = ["Wikipedia", "CEO", "amp", "view", "edits", "View of the content page", "Discussion about the content page"
                    "A list of recent changes in the wiki", " what you can do", "Discussion about edits from this IP address", 
                    "Find background information on current events", "Load a random article", "Recent changes in pages linked from this page"
                    , "A list of edits made from this IP address", "Upload files", "Enlarge", "Portal", "Template", "Wikipedia:Citation need",
                    "Visit the main page", "Reuters", "Forbes", "Wikipedia:About", "Help:Category", "Help:CS1 errors"]

    while(temp.find("<a href=\"/wiki/") != -1):
        checker = True
        first = temp.find("<a href=\"/wiki/")
        second = temp[first:].find("title=")
        end = temp[second+first+7:].find("\"")
        term = temp[second+first+7:end+second+first+7]
        temp = temp[end:]
        #if term not in tokens and term.strip() not in all_states and "Wikipedia" not in term and "CEO" not in term and "amp" not in term and "Category" not in term:
        if term not in common_words and term.strip() not in all_states:
            tokens.append(term)
            # for word in common_words:
            #     if word in term:
            #         checker = False
            # if checker:
            #     tokens.append(term)

    # Tokenizing and removing common stop words

    # tokens = tokenizer.tokenize(text.lower())
    # tokens = [unicode(i, 'ascii', 'ignore') for i in tokens]
    # tokens = [str(i) for i in tokens if not i in get_stop_words('en')]
    # tokens = [i for i in tokens if not i.isdigit()]

    # Removes all the html and extra white space
    text = re.sub('<[^>]*>', '', text)
    #print(text)
    text = " ".join(text.split())

    # Removes everything after See Also
    first = text.find("See also")
    second = text[first+1:].find("See also")
    text = text[:first+second]

    # Removes everything before the start of the article
    first = text.find("navigation, search")
    text = text[first+18:]

    temp = text[text.find("Website"):]

    # Removes everything between brackets.
    text = re.sub(r'\[[^)]*\]', '', text)
    year_start = text.find("Founded ")
    equity_start = text.find("Total assets US$")

    year_text = text[year_start:]
    year_stop = year_text.find(";")
    year_info = year_text[:year_stop]
    year_info = year_info.split(" ")
    if (len(year_info) >=2):
        year_info = year_info[1]
    else:
        year_info = year_info[0]
        print(year_info)
    if (year_info is None):
        company_years[company_name] = 0
    else:
        company_years[company_name] = year_info

    if (equity_start < 0):
        company_equities[company_name] = 0
    else:
        equity_text = text[equity_start + 16:]
        equity_end = equity_text.find("il")
        if ((equity_end  > 25) or (equity_end < 0)):
            equity_end = equity_text.find("B (")
            if (equity_end  > 25 or equity_end < 0):
                equity_end = equity_text.find("M (")
                if (equity_end > 25 or equity_end < 0):
                    equity_end = equity_text.find("(FY ")
                    if (equity_end > 35 or equity_end < 0):
                        equity_end = equity_text.find("bn")
        equity_amt = equity_text[:equity_end]
        equity_amt = equity_amt.strip().lower().replace(',', '').replace('$', '')
        print(company_name)
        #print(equity_amt)
        val = 0
        if 'b' in equity_amt:
            val = 1000000000
        else:
            if 'm' in equity_amt:
                val = 1000000
            else:
                if 't' in equity_amt:
                    val = 1000000000000
                else:
                    val = 1
        equity_amt = equity_amt.split("&")[0].split(" ")[0]
        equity_amt = float(equity_amt) * val
        if equity_amt < 1000000:
            print"SOMETHING WENT WRONG"
            equity_amt = 0
        company_equities[company_name] = equity_amt
        #print(equity_amt)

    # Tokenizing and removing common stop words
    # tokens = tokenizer.tokenize(text.lower())
    # tokens = [unicode(i, 'ascii', 'ignore') for i in tokens]
    # tokens = [str(i) for i in tokens if not i in get_stop_words('en')]
    # tokens = [i for i in tokens if not i.isdigit()]
    # tokens = [i for i in tokens if len(i) > 2]

    return tokens

#print(file_cleaner("https://en.wikipedia.org/wiki/Abbott_Laboratories", "Abbott_Laboratories"))

f = urllib2.urlopen(BASE_URL)
text = f.read()

with open('keywordTok.csv', 'wb') as f:
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
            start_industrial = text.find("reports</a></td>") + 20
            industrial_text = text[start_industrial+1:]
            end_industrial = industrial_text.find("<td><a href=") - 7
            end_general_industrial = industrial_text.find("</td>");
            start_location = text.find("<td><a href=")
            location_text = text[start_location:]
            place_start_location = location_text.find('title="') + 7
            place_end_location = location_text.find('">')
            end_location = text.find("</a></td>");


            if(count % 2 == 0):
                company_name = text[18:end-2]
                general_industry_text = industrial_text[:end_general_industrial]
                specific_industry_text = industrial_text[end_general_industrial + 10 : end_industrial +1]
                place_text = location_text[place_start_location:place_end_location]
                place_contains_class = place_text.find(" class=")
                if (place_contains_class > 0):
                    place_text = place_text[:place_contains_class - 1]
                if (place_text.find(",") > 0):
                    place_text = place_text.split(",")
                    if (place_text[1].strip() in all_states):
                        company_locations[company_name] = "United States"
                    else:
                        company_locations[company_name] = place_text[1]
                else:
                    company_locations[company_name] = place_text

                company_industries[company_name] = (general_industry_text, specific_industry_text)
                link = "https://en.wikipedia.org/wiki/" + company_name
                clean_file = file_cleaner(link, company_name)
                writer.writerow([company_name] + clean_file)
                companies.append(company_name)
                if(company_name == "Zoetis"):
                    break
            count += 1
            text = text[end:]
            print(count)

    print('company_industries')
    print(company_industries)
    print('company_locations')
    print(company_locations)
    print('company_equities')
    print(company_equities)
    print(company_years)
    print(companies)

    matrix_dict = create_econ_link_matricies()
    for matrix in matrix_dict:
        print(matrix_dict[matrix])
    print(matrix_compilation(matrix_dict))


    #Testing both functions
    #company_industry_multiples("3M", "AbbVie")
    #company_industry_multiples("AFLAC_Inc", "Affiliated_Managers_Group_Inc")
    #company_industry_multiples("Interpublic_Group", "Omnicom_Group")
    #company_location_multiples("3M", "AbbVie")
    #company_location_multiples("AFLAC_Inc", "Affiliated_Managers_Group_Inc")
    #company_location_multiples("Interpublic_Group", "Omnicom_Group")
    #company_location_multiples("Extra_Space_Storage", "Transocean")
    #company_location_multiples("3M", "Transocean")
