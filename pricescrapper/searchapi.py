import pprint,json,unicodecsv,csv
import urllib2,requests, pprint
from lxml import html
import urlparse, re, csv

from googleapiclient.discovery import build
output = open("OutputUrls.csv","wb")
mywriter = unicodecsv.writer(output)
header = ('Product Name','LYS URL','Amazon URL','Snapdeal URL','Flipkart URL','PayTM URL')
mywriter.writerow(header)
f = open("input.csv")
csv_file = csv.reader(f)
urllist =[]
for row in csv_file:
  urllist.append(row[0])


def main():
	# for i in range(15):
		url = ''
		# url = urllist[i].strip()
		# query= liveyoursport_scraper(url)
		query = 'Butterfly Addoy 2000 Table Tennis Bat'		
		amazon_url = amazon_in(query)
		flipkart_url = flipkart(query)
		snapdeal_url = snapdeal(query)
		paytm_url = paytm(query)
		row =[query,url,amazon_url,snapdeal_url,flipkart_url,paytm_url]
		print row
		mywriter.writerow(row)
		

def amazon_in(query):
	# try:
		service = build("customsearch", "v1",developerKey="AIzaSyAQmRE0WVS8Dcbjgdd2_Bua9ZBq5U1Svok")	
		res = service.cse().list(q=query,cx='003190724308582426242:nxe2zjdf8kg',).execute()
		name = res['items'][0]['title']		
		print res
		return res['items'][0]['link']
	# except:
		# return ''

	
def flipkart(query):
	try:
		service = build("customsearch", "v1",	
						developerKey="AIzaSyAQmRE0WVS8Dcbjgdd2_Bua9ZBq5U1Svok")
	
		res = service.cse().list(q=query,cx='003190724308582426242:qktujgcevvq',).execute()
		return res['items'][0]['link']
	except:
		return ''
def snapdeal(query):
	try:
		service = build("customsearch", "v1",	
						developerKey="AIzaSyAQmRE0WVS8Dcbjgdd2_Bua9ZBq5U1Svok")
	
		res = service.cse().list(q=query,	cx='003190724308582426242:ibh8b0rhzf0',).execute()
		return res['items'][0]['link']
	except:
		return ''

def paytm(query):
	try:
		service = build("customsearch", "v1",	
						developerKey="AIzaSyAQmRE0WVS8Dcbjgdd2_Bua9ZBq5U1Svok")
	
		res = service.cse().list(q=query,	cx='003190724308582426242:oojgya2rem4',).execute()
		return res['items'][0]['link']
	except:
		return ''
	
if __name__ == '__main__':
	main()
	# amazon_in()
	# flipkart()
	# snapdeal()
	# paytm()
def liveyoursport_scraper(url):	
		page = requests.get(url)
		sel = html.fromstring(page.text)
		category=(sel.xpath("//div[@id='ProductBreadcrumb']/ul/li/a/text()")[1]+
								"/"+sel.xpath("//div[@id='ProductBreadcrumb']/ul/li/a/text()")[2]+
									"/"+sel.xpath("//div[@id='ProductBreadcrumb']/ul/li/a/text()")[3])
		lysproductname = sel.xpath("//h1/text()")[0].replace(",","")				
		sp = sel.xpath("//span[@class='RetailPrice']/strike/text()")
		if sp:
			sp = sel.xpath("//em[@class='ProductPrice VariationProductPrice']/text()")[0].replace(",","").split("Rs ")[-1]
			mrp = sel.xpath("//span[@class='RetailPrice']/strike/text()")[0].replace(",","").split("Rs ")[-1]
		else:
			sp = ""
			mrp = sel.xpath("//em[@class='ProductPrice VariationProductPrice']/text()")[0].replace(",","").split("Rs ")[-1]
		stock = sel.xpath("//div[@class='stockIcon Out Of Stock']")
		if stock:
			stock = "Out of Stock"
		else:
			stock = "In Stock"
				
		row = [lysproductname,sp,mrp,category,url,'']
		return lysproductname

	
	
	