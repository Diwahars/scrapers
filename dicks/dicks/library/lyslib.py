import csv
def categories(filename):
		f = open(filename)
		csv_file = csv.reader(f)
		urllist =[]
		lyscat =[]
		priceid=[]
		for row in csv_file:
			urllist.append(row[0])
			lyscat.append(row[1])
			priceid.append(row[2])
			
		return urllist,lyscat,priceid
		
def brands():	
	k = open("Brandslist1.csv")
	brand_file = csv.reader(k)
	brandlist = []
	for row in brand_file:
		brandlist.append(row[0])
	return brandlist
