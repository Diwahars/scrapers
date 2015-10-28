
import csv, unicodecsv
header = ('LYS Product Name','LYS URL','LYS Product Code','LYS MRP','LYS SP','LYS Stock','Category','|',
		'Snapdeal Product Name','Snapdeal URL','Snapdeal MRP','Snapdeal SP','Snapdeal Stock','|',
		'Amazon Product Name','Amazon URL','Amazon MRP','Amazon SP','Amazon Stock','|',
		  'Flipkart Product Name','Flipkart URL','Flipkart MRP','Flipkart SP','Flipkart Stock','|',
		  'PayTM Product Name','PayTM URL','PayTM MRP','PayTM SP','PayTM Stock','|',)	

def supplier_urls():
		f = open("popularproducts.csv")
		csv_file = csv.reader(f)
		lys_urls, snapdeal_urls , amazon_urls , paytm_urls , flipkart_urls = [], [] , [] , [] , []
		
		for row in csv_file:
			lys_urls.append(row[0])
			snapdeal_urls.append(row[1])
			amazon_urls.append(row[2])
			flipkart_urls.append(row[3])
			paytm_urls.append(row[4])
			
			
		return lys_urls,snapdeal_urls,amazon_urls,flipkart_urls,paytm_urls  