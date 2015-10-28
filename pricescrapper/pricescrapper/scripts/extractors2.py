import urllib2,requests, pprint
from lxml import html
import urlparse, re, csv
import demjson


		
def amazon_scraper(url):
	# try:
		page = requests.get(url)	
		sel = html.fromstring(page.text)			
		try:	
			
			productname = sel.xpath("//h1/span[@id='productTitle']/text()")[0].replace(",","")
			if sel.xpath("//span[@class='a-size-medium a-color-price']"):
				return [productname,'','','','Out Of Stock']
			else:
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
				else:
					mrp =''
				
					
				if url1:
					url1 = 'http://www.amazon.in/'+url1[0]
					marketplace_sp = amazonmarket_place(url1)			
					try:
						if marketplace_sp>sp:
							sp = marketplace_sp
							list = [productname,url,mrp,sp,'In stock']
							return list
						else:
							list = [productname,url,mrp,sp,'In stock']
							return list
							
					except:
						sp = marketplace_sp
						list = [productname,url,mrp,sp,'In stock']
						return list 
				
		except:
			return ['','','','','Not Found']
	# except:
		# return ['','','','','Not Found']
		
		
def amazonmarket_place(url):
	headers = {'user-agent':'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13'}
	page = requests.get(url,headers=headers)	
	sel = html.fromstring(page.text)	
	sp = sel.xpath("//span[@style='text-decoration: inherit; white-space: nowrap;']/text()")[0].replace(",","")
	shippingcost = sel.xpath("//span[@class='olpShippingPrice']/span/text()")
	if shippingcost:
	  sp = str(float(sp) + float(sel.xpath("//span[@class='olpShippingPrice']/span/text()")[0].replace(",","")))	
	return sp

def snapdeal_scraper(url):		
	try:
		page =  requests.get(url)
		sel = html.fromstring(page.text)    
		try:
			if sel.xpath("//div[@class='notifyMe-soldout']"):
				ProductName = sel.xpath("//h1[@itemprop='name']/text()")[0].replace(",","")
				list = [ProductName,url,'','','Out Of Stock']
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
				list = [ProductName,url,mrp,sp,stock]
				return list
		except:
			return ['','','','','Not Found']
	except:
			return ['','','','','Not Found']
		
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
			list = [productname,url,mrp,sp,'In Stock']
			return list
		else:
			list = ['','','','','Not Found']
			return list

def paytm_scraper(url):		
		url1 = url.replace('https://paytm.com/shop', 'https://catalog.paytm.com/v1')
		page = requests.get(url1)		
		try:			
			sel = html.fromstring(page.text)    		
			raw_json = sel.xpath('//text()')[0]
			item = demjson.decode(raw_json)
			name = item['name']
			MRP = item['actual_price']
			SP = item['offer_price']
			in_stock = item['instock']  # True or False
			
			if in_stock ==True:
				list = [name,url,MRP,SP,'In Stock']
				return list
			else:
				list = [name,url,MRP,SP,'Out Of Stock']
				return list				
		except:
			list = ['','','','','Not Found']
			return list

def lys_scraper(url):
		
		page = requests.get(url)
		sel = html.fromstring(page.text)    
		category=(sel.xpath("//div[@id='ProductBreadcrumb']/ul/li/a/text()")[1]+
						"/"+sel.xpath("//div[@id='ProductBreadcrumb']/ul/li/a/text()")[2]+
								"/"+sel.xpath("//div[@id='ProductBreadcrumb']/ul/li/a/text()")[3])
		LYS_ProductName = sel.xpath("//h1/text()")[0].replace(",","")
		
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
		sku = sel.xpath("//span[@class='VariationProductSKU']/text()")[0].strip()
		
		LYS_row = [LYS_ProductName,url,sku,mrp,sp,stock,category]
		
		return LYS_row
		
if __name__ == '__main__':
	print paytm_scraper("https://paytm.com/shop/p/tecnifibre-carboflex-125-squash-racquet-CMPLXSPOTECNIFIBRE-CDUMM315676D6CA112")
	

	
	
	
	
	
			