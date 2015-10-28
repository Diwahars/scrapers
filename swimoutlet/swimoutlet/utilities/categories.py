import csv
def initialize():
	f = open("SwimCat.csv")
	csv_file = csv.reader(f)
	categnamelist = []
	priceidlist = []
	urllist = []
	cat1list, cat2list, cat3list = [], [], []
	
	for row in csv_file:
	  categnamelist.append(row[0])
	  priceidlist.append(row[1])
	  urllist.append(row[2])
	  cat1list.append(row[3])
	  cat2list.append(row[4])
	  cat3list.append(row[5])

	return cat1list, cat2list, cat3list,urllist, categnamelist, priceidlist