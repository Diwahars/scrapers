import urllib2,requests, pprint
from lxml import html
import urlparse, re, csv
import time
f = open("Input.csv")
csv_file = csv.reader(f)
urls = []
for row in csv_file:
	urls.append(row[0])
headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.16 Safari/534.24"}


output = open("PriceCompar.csv","wb")
mywriter = csv.writer(output)
header = ('LYS Product Name','LYS URL','LYS Product Code','LYS MRP','LYS SP','LYS Stock','Category',
		  'Snapdeal Product Name','Snapdeal URL','Snapdeal MRP','Snapdeal SP','Snapdeal Stock','',
		    'Amazon Product Name','Amazon URL','Amazon MRP','Amazon SP','Amazon Stock','',
			  'Flipkart Product Name','Flipkart URL','Flipkart MRP','Flipkart SP','Flipkart Stock')	
mywriter.writerow(header)
def getgoogleurl(search,siteurl=False):
		if siteurl==False:
			return 'http://www.google.com/search?q='+urllib2.quote(search)
		else:
			return 'http://www.google.com/search?q=site:'+urllib2.quote(siteurl)+'%20'+urllib2.quote(search)

def getgooglelinks(search,siteurl=False):
	   #google returns 403 without user agent
	   headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.16 Safari/534.24"}
	   req = urllib2.Request(getgoogleurl(search,siteurl),None,headers)
	   site = urllib2.urlopen(req)
	   data = site.read()
	   site.close()

	   #no beatifulsoup because google html is generated with javascript
	   start = data.find('<div id="res">')
	   end = data.find('<div id="foot">')
	   if data[start:end]=='':
		  #error, no links to find
		  return False
	   else:
		  links =[]
		  data = data[start:end]
		  start = 0
		  end = 0        
		  while start>-1 and end>-1:
			  #get only results of the provided site
			  if siteurl==False:
				start = data.find('<a href="/url?q=')
			  else:
				start = data.find('<a href="/url?q='+str(siteurl))
			  data = data[start+len('<a href="/url?q='):]
			  end = data.find('&amp;sa=U&amp;ei=')
			  if start>-1 and end>-1: 
				  link =  urllib2.unquote(data[0:end])
				  data = data[end:len(data)]
				  if link.find('http')==0:
					  links.append(link)
		  return links[0]

		
def amazonin(url):
	page = requests.get(url)	
	sel = html.fromstring(page.text)
	if sel.xpath('//div[@id="outOfStock"]'):		
		list = ['',url,'','','Out Of Stock','']
		return list
	else:		
		productname = sel.xpath("//h1/span[@id='productTitle']/text()")[0].replace(",","")
		mrp = sel.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()")
		saleprice = sel.xpath("//span[@id='priceblock_saleprice']/text()")
		ourprice = sel.xpath("//span[@id='priceblock_ourprice']")			
		saleshipping = sel.xpath("//span[@class='a-size-base a-color-secondary']/text()")
		url1 = sel.xpath("//span[@class='a-size-medium a-color-success']//a/@href")
		if mrp and saleprice:
			sp = sel.xpath("//span[@id='priceblock_saleprice']/text()")[0].replace(",","")
			mrp = sel.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()")[0].replace(",","")
		elif mrp and ourprice:
			sp = sel.xpath("//span[@id='priceblock_ourprice']/text()")[0].replace(",","")
			mrp = sel.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()")[0].replace(",","")

		elif saleshipping and mrp:
			sp = sel.xpath("//span[@class='a-size-base a-color-secondary']/text()")[0].replace(",","")
			mrp = sel.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()")[0].replace(",","")

		elif saleprice:
			sp = sel.xpath("//span[@id='priceblock_saleprice']/text()")[0].replace(",","")
		elif ourprice:
			mrp = sel.xpath("//span[@id='priceblock_ourprice']/text()")[0].replace(",","").replace(" ","")	

		if url1:
			marketplace_sp = amazonmarket_place(url1)			
			if marketplace_sp>sp:
				sp = marketplace_sp
		list = [productname,url,mrp,sp,'In stock']
		return list	
def amazonmarket_place(url):
	page = requests.get(url)
	sel = html.fromstring(page.text)	
	sp = sel.xpath("//span[@style='text-decoration: inherit; white-space: nowrap;']/text()").replace(",","")
	shippingcost = sel.xpath("//span[@class='olpShippingPrice']/span/text()").extract()
	if shippingcost:
	  sp = str(float(sp) + float(sel.xpath("//span[@class='olpShippingPrice']/span/text()").replace(",","")))
	return sp

def snapdeal_scraper(url):		
		page =  requests.get(url)
		sel = html.fromstring(page.text)    
		if sel.xpath("//div[@class='notifyMe-soldout']") or sel.xpath("//div[@class='noLongerProduct']"):
			ProductName = sel.xpath("//h1[@itemprop='name']/text()")[0].replace(",","")
			list = [ProductName,url,'','','Out Of Stock','']
			return list		
		else:
			mrp = sel.xpath("//span[@id='original-price-id']/text()")
			if mrp:
				sp = sel.xpath("//span[@id='selling-price-id']/text()")[0]
				mrp = sel.xpath("//span[@id='original-price-id']/text()")[0]
			else:
				mrp = sel.xpath("//span[@id='selling-price-id']/text()")[0]
				sp = ''
			ProductName = sel.xpath("//h1[@itemprop='name']/text()")[0].replace(",","")
			stock = sel.xpath("//div[@class='notifyMe-soldout']")
			discntnd = sel.xpath("//div[@class='noLongerProduct']")
			if stock or discntnd:
				stock = "Out Of Stock"
			else:
				stock = "In Stock"
			list = [ProductName,url,mrp,sp,stock,'']
			return list
		
def flipkart_scraper(url):
		page = requests.get(url)
		sel = html.fromstring(page.text)    
		if sel.xpath("//h1[@class='title']/text()"):
			productname = sel.xpath("//h1[@class='title']/text()")[0].replace(",","")      
			mrp = sel.xpath("//span[@class='price']/text()")
		if mrp:
			mrp = sel.xpath("//span[@class='price']/text()")[0].replace(",","").replace("Rs.","")
		sp = sel.xpath("//span[@class='selling-price omniture-field']/text()")
		if sp:
			sp = sel.xpath("//span[@class='selling-price omniture-field']/text()")[0].replace(",","").replace("Rs.","")
		else:
			sp = ''
		stock = sel.xpath("//div[@class='out-of-stock-status']")		
		nosellers = sel.xpath("//div[@class='no-sellers-available omniture-field']")
		if stock or nosellers:
			stock = "Out of Stock"				
		list = [productname,url,mrp,sp,stock]
		return list
	
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
		print lysproductname
		
		row = [lysproductname,sp,mrp,category,url,'']
		row.append(snapdeal_scraper(getgooglelinks(lysproductname,'http://www.snapdeal.com/')))
		# row.append(amazonin(getgooglelinks(lysproductname,'http://www.amazon.in/')))
		# row.append(flipkart_scraper(getgooglelinks(lysproductname,'http://www.flipkart.com/')))
		mywriter.writerow(row)

i = 0
for url in urls:
	liveyoursport_scraper(url.strip())
	i+=1
	
		
	
	
	
	
	
	
	
	
	
			