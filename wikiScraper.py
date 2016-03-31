# import urllib2

# f = urllib2.urlopen("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
# text = f.read()

# count = 0
# company_links = []
# company_text = []
# while((text.find("<td><a href=\"/wiki/") != -1 or text.find("<td><a href=\"/w/index.php?title=") != -1) and count < 1008):
# 	if(text.find("<td><a href=\"/wiki/") > text.find("<td><a href=\"/w/index.php?title=")):
# 		text = text[text.find("(page does not exist)")+10:]
# 		count += 1
# 	else:
# 		start = text.find("<td><a href=\"/wiki/")
# 		text = text[start+1:]
# 		end = text.find("title")
# 		if(count %2 == 0):
# 			company_name = text[18:end-2]
# 			company_links.append("https://en.wikipedia.org/wiki/" + company_name)
# 		count += 1
# 		text = text[end:]

# count = 0
# for link in company_links:
# 	count += 1
# 	f = urllib2.urlopen(link)
# 	company_text.append(f)
# 	if(count %10 == 0):
# 		print(count)

print('hello')
