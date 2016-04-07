import csv

docDict = {}
docList = []

with open('resultsTok.csv', 'rt') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		docDict[row[0]] = row[1:]
		docList.append(row[1:])

print(docDict)
