from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider
from scrapy.http.request import Request
from pricescrapper.items import BigCItem
import urlparse ,re, json, unicodecsv,csv,demjson
from collections import defaultdict
from ..scripts import customsearch_api,extractors,extractors2,mycsv
import urllib2,requests, pprint
import pprint
from lxml import html
output = open("PopularProduct_Output.csv","wb")
mywriter = unicodecsv.writer(output)
mywriter.writerow(mycsv.header)

lys_urls,snapdeal_urls,amazon_urls,flipkart_urls,paytm_urls = mycsv.supplier_urls()
	

class PriceScrapper(CrawlSpider):
	dont_filter=True
	name = "popularproducts1"
	allowed_domains = ["snapdeal.com", "amazon.in", "flipkart.com",'liveyoursport.com', 'paytm.com']  
	
	start_urls = [	
					'http://www.liveyoursport.com/products/sg-test-red-cricket-ball'
					# url.strip() for url in lys_urls
					# "http://www.liveyoursport.com/products/prince-exo3-rebel-squash-racket"
		]

		
	def parse(self,response):
		item = BigCItem()
		sel = Selector(response)
		null_dict = defaultdict(str)
		item = defaultdict(dict)		
		
		item['LYS']['Category']=(sel.xpath("//div[@id='ProductBreadcrumb']/ul/li/a/text()").extract()[1]+
								"/"+sel.xpath("//div[@id='ProductBreadcrumb']/ul/li/a/text()").extract()[2]+
								"/"+sel.xpath("//div[@id='ProductBreadcrumb']/ul/li/a/text()").extract()[3])
		
		item['LYS']['Product_Name'] = sel.xpath("//h1/text()").extract()[0].replace(",","")
		
		sp = sel.xpath("//span[@class='RetailPrice']/strike/text()").extract()
		if sp:
			item['LYS']['SP'] = sel.xpath("//em[@class='ProductPrice VariationProductPrice']/text()").extract()[0].replace(",","").split("Rs ")[-1]
			item['LYS']['MRP'] = sel.xpath("//span[@class='RetailPrice']/strike/text()").extract()[0].replace(",","").split("Rs ")[-1]
		else:
			item['LYS']['SP'] = ""
			item['LYS']['MRP'] = sel.xpath("//em[@class='ProductPrice VariationProductPrice']/text()").extract()[0].replace(",","").split("Rs ")[-1]
    
		stock = sel.xpath("//div[@class='stockIcon Out Of Stock']").extract()
		if stock:
			item['LYS']['Stock'] = "Out of Stock"
		else:
			item['LYS']['Stock'] = "In Stock"
		
		item['LYS']['sku'] = sel.xpath("//span[@class='VariationProductSKU']/text()").extract()[0].strip()
		item['index'] = lys_urls.index(response.url)
		item['LYS']['URL'] = response.url
		
			
		try:
			snapdeal_url = snapdeal_urls[item['index']]
			request = Request(snapdeal_url,callback = self.snapdeal_scraper)
			request.meta['item'] = item			
			yield request
		except:	
			
			try:
				amazon_url = amazon_urls[item['index']]
				request = Request(amazon_url,
									headers={'Referer':'http://amazon.in'},
									callback = self.amazon_scraper)
				request.meta['item'] = item
				request.meta['proxy'] = "http://111.161.126.100:80"
				yield request
			
			except:				
				try:
					flipkart_url = flipkart_urls[item['index']]
					request = Request(flipkart_url,callback = self.flipkart_scraper)
					request.meta['item'] = item
					# request.meta['proxy'] = "http://111.161.126.100:80"
					yield request
			
				except:			
					try:
						paytm_url = paytm_urls[item['index']]
						request = Request(paytm_url,callback = self.paytm_scraper)
						request.meta['item'] = item
						request.meta['proxy'] = "http://111.161.126.100:80"
						yield request
					except:
						pass
		
	def snapdeal_scraper(self,response):
		item = response.meta['item']
		sel = Selector(response)
		
		item['Snapdeal']['URL']= response.url
		try:
			if sel.xpath("//div[@class='notifyMe-soldout']"):
				ProductName = sel.xpath("//h1[@itemprop='name']/text()").extract()[0].replace(",","")
				item['Snapdeal']['ProductName'] =ProductName								
			else:
				mrp = sel.xpath("//span[@id='original-price-id']/text()").extract()
				if mrp:
					item['Snapdeal']['SP'] = sel.xpath("//span[@id='selling-price-id']/text()").extract()[0]
					item['Snapdeal']['MRP'] = sel.xpath("//span[@id='original-price-id']/text()").extract()[0]
				else:
					item['Snapdeal']['MRP'] = sel.xpath("//span[@id='selling-price-id']/text()").extract()[0]
					item['Snapdeal']['SP'] = ''
					
				item['Snapdeal']['_ProductName'] = sel.xpath("//h1[@itemprop='name']/text()").extract()[0].replace(",","")
				stock = sel.xpath("//div[@class='notifyMe-soldout']").extract()
				discntnd = sel.xpath("//div[@class='noLongerProduct']").extract()
				if stock or discntnd:
					item['Snapdeal']['Stock'] = "Out Of Stock"
				else:
					item['Snapdeal']['Stock'] = "In Stock"				
				
		except:						
			item['Snapdeal']['Stock'] = 'Not Found'
		
		
		try:
			amazon_url = amazon_urls[item['index']]
			request = Request(amazon_url,
								headers={'Referer':'http://amazon.in'},
								callback = self.amazon_scraper)
			request.meta['item'] = item
			request.meta['proxy'] = "http://111.161.126.100:80"
			yield request
			
		except:				
			try:
				flipkart_url = flipkart_urls[item['index']]
				request = Request(flipkart_url,callback = self.flipkart_scraper)
				request.meta['item'] = item
				# request.meta['proxy'] = "http://111.161.126.100:80"
				yield request
		
			except:			
				try:
					paytm_url = paytm_urls[item['index']]
					request = Request(paytm_url,callback = self.paytm_scraper)
					request.meta['item'] = item
					request.meta['proxy'] = "http://111.161.126.100:80"
					yield request
				except:
					self.to_csv(item)
		
	def amazon_scraper(self,response):		
		
		sel = Selector(response)
		item = response.meta['item']
		item['Amazon']['URL']= response.url		
		try:				
			item['Amazon']['ProductName'] = sel.xpath("//h1/span[@id='productTitle']/text()").extract()[0].replace(",","")					
			mrp = sel.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()").extract()
			saleprice = sel.xpath("//span[@id='priceblock_saleprice']/text()").extract()
			ourprice = sel.xpath("//span[@id='priceblock_ourprice']/text()").extract()
			saleshipping = sel.xpath("//span[@class='a-size-base a-color-secondary']/text()").extract()
			
			item['Amazon']['Stock'] = 'In Stock' 
			if mrp and saleprice:
				item['Amazon']['SP'] = saleprice[0].replace(",","")
				item['Amazon']['MRP'] = mrp[0].replace(",","")
			elif mrp and ourprice:
				item['Amazon']['SP'] = ourprice[0].replace(",","")
				item['Amazon']['MRP'] = mrp[0].replace(",","")
			elif saleshipping and mrp:
				item['Amazon']['SP'] = sel.xpath("//span[@class='a-size-base a-color-secondary']/text()").extract()[0].replace(",","")
				item['Amazon']['MRP'] = mrp[0].replace(",","")
			elif saleprice:
				item['Amazon']['SP'] = ''
				item['Amazon']['MRP'] = saleprice[0].replace(",","")
			elif ourprice:
				item['Amazon']['MRP'] = ourprice[0].replace(",","")
				item['Amazon']['SP'] =''
			elif mrp:
				item['Amazon']['MRP'] = mrp[0].replace(",","")				
			else:
				item['Amazon']['MRP'] =''			
				item['Amazon']['SP'] =''
				item['Amazon']['Stock'] = 'Out Of Stock' 
				
			marketplace_url = sel.xpath("//span[@class='a-size-medium a-color-success']//a/@href").extract()
			if marketplace_url:
				marketplace_url = 'http://www.amazon.in/'+marketplace_url[0]
				request = Request(marketplace_url,
									headers={'Referer':'http://amazon.in'},
									callback = self.amazon_marketplace)
				request.meta['item'] = item
				request.meta['proxy'] = "http://111.161.126.100:80"				
				yield request		
		except:						
			item['Amazon']['Stock'] = 'Not Found'		
		
		
		try:
			flipkart_url = flipkart_urls[item['index']]
			request = Request(flipkart_url,callback = self.flipkart_scraper)
			request.meta['item'] = item
			# request.meta['proxy'] = "http://111.161.126.100:80"
			yield request
	
		except:				
			try:
				paytm_url = paytm_urls[item['index']]
				request = Request(paytm_url,callback = self.paytm_scraper)
				request.meta['item'] = item
				request.meta['proxy'] = "http://111.161.126.100:80"
				yield request
			except:
				self.to_csv(item)

		
	def amazon_marketplace(self,response):
		
		sel = Selector(response)
		item = response.meta['item']
		try:
			sp = sel.xpath("//span[@style='text-decoration: inherit; white-space: nowrap;']/text()").extract()[0].replace(",","")
			shippingcost = sel.xpath("//span[@class='olpShippingPrice']/span/text()").extract()
			if shippingcost:
				sp = str(float(sp) + float(sel.xpath("//span[@class='olpShippingPrice']/span/text()").extract()[0].replace(",","")))	
			
			if sp>item['Amazon']['SP']: sp = item['Amazon']['SP']
		
		except:			
			try:
				flipkart_url = flipkart_urls[item['index']]
				request = Request(flipkart_url,callback = self.flipkart_scraper)
				request.meta['item'] = item
				# request.meta['proxy'] = "http://111.161.126.100:80"
				yield request
		
			except:				
				try:
					paytm_url = paytm_urls[item['index']]
					request = Request(paytm_url,callback = self.paytm_scraper)
					request.meta['item'] = item
					request.meta['proxy'] = "http://111.161.126.100:80"
					yield request
				except:
					self.to_csv(item)
			
	
	def flipkart_scraper(self,response):
		sel = Selector(response)
		item = response.meta['item']		
		item['Flipkart']['URL'] = response.url	
		
		
		if sel.xpath("//h1[@class='title']/text()").extract():
			item['Flipkart']['ProductName'] = sel.xpath("//h1[@class='title']/text()").extract()[0].replace(",","")      
			
			
			mrp_xpath = sel.xpath("//span[@class='price']/text()").extract()			
			sp_xpath = sel.xpath("//span[@class='selling-price omniture-field']/text()").extract()
			
			if mrp_xpath and sp_xpath:
				item['Flipkart']['MRP'] = mrp_xpath[0].replace(",","").replace("Rs.","")
				item['Flipkart']['SP'] = sp_xpath[0].replace(",","").replace("Rs.","")
			elif sp_xpath:
				item['Flipkart']['MRP'] = sp_xpath[0].replace(",","").replace("Rs.","")
				item['Flipkart']['SP'] = ''
			elif mrp_xpath:
				item['Flipkart']['MRP'] = mrp_xpath[0].replace(",","").replace("Rs.","")
				item['Flipkart']['SP'] = ''
				
			
			stock = sel.xpath("//div[@class='out-of-stock-status'] | //div[@class='no-sellers-available omniture-field']").extract()					
			
			if not stock :
				item['Flipkart']['Stock'] = "In Stock"
			else:
				item['Flipkart']['Stock'] = 'Out Of Stock'			
		
		else:			
			item['Flipkart']['Stock'] = "Not Found"
		
		
		try:			
			paytm_url = paytm_urls[item['index']]
			paytm_url = paytm_url.replace('//paytm.com/shop', '//catalog.paytm.com/v1')
			request = Request(paytm_url,callback = self.paytm_scraper)
			request.meta['item'] = item
			request.meta['proxy'] = "http://111.161.126.100:80"			
			yield request
		
		except:
			self.to_csv(item)
	
	def paytm_scraper(self,response):
	
		sel = Selector(response)
		item = response.meta['item']		
		item['PayTM']['URL'] = response.url
		
		try:		
			raw_json = sel.xpath('//text()').extract()[0]
			product = demjson.decode(raw_json)
			item['PayTM']['ProductName'] = product['name']
			item['PayTM']['MRP'] = product['actual_price']
			item['PayTM']['SP'] = product['offer_price']
			in_stock = product['instock']  # True or False
			
			if in_stock ==True:
				item['PayTM']['Stock'] = 'In Stock'				
			else:
				item['PayTM']['Stock'] = 'Out of Stock'
				
		except:			
			item['PayTM']['Stock'] = 'Not Found'			
			
		self.to_csv(item)
		
	def to_csv(self,item):
		row = []
		pprint.pprint(item)
		# for k in item:
			# print k['ProductName']
			# if k !='LYS':
				# temp_row = [k['ProductName'],k['URL'],k['MRP'],k['SP'],k['Stock'],'|']
				# row.extend(temp_row)
			
			
		# print row
		
		# mywriter.writerow(row)
		
			
			
			
			# row = extractors2.lys_scraper(lys_urls[i])
			# row.append('|')
			# try:
				# row+= extractors2.snapdeal_scraper(snapdeal_urls[i])
				# row.append('|')
			# except:
				# row+= ['','','','','Not Found','|']				
			# try:
				# row+= extractors2.amazon_scraper(amazon_urls[i])
				# row.append('|')
			# except:
				# row+= ['','','','','Not Found','|']				
			# try:
				# row+= extractors2.flipkart_scraper(flipkart_urls[i])
				# row.append('|')
			# except:
				# row+= ['','','','','Not Found','|']	
			# try:
				# row+= extractors2.paytm_scraper(paytm_urls[i])
				# row.append('|')
			# except:
				# row+= ['','','','','Not Found','|']
			
			# mywriter.writerow(row)
			
			
			