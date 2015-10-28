from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider
from scrapy.http.request import Request
from pricescrapper.items import BigCItem
import urlparse ,re, json, unicodecsv,csv
from ..scripts import customsearch_api,extractors,extractors2,mycsv
import urllib2,requests, pprint
from lxml import html
output = open("API_Output.csv","wb")
mywriter = unicodecsv.writer(output)

mywriter.writerow(mycsv.header)


f = open("input.csv")
csv_file = csv.reader(f)
productname_list = []
i = 0
for row in csv_file:
  productname_list.append(row[0])

	

class PriceScrapper(CrawlSpider):
	dont_filter=True
	name = "pricescrapper"
	allowed_domains = ["snapdeal.com", "amazon.in", "amazon.com", "flipkart.com",'google.co.in','google.com']  
	start_urls = [				
					url.strip() for url in productname_list
		]
		
	def parse(self,response):
		item = BigCItem()
		sel = Selector(response)
		category=(sel.xpath("//div[@id='ProductBreadcrumb']/ul/li/a/text()").extract()[1]+
						"/"+sel.xpath("//div[@id='ProductBreadcrumb']/ul/li/a/text()").extract()[2]+
								"/"+sel.xpath("//div[@id='ProductBreadcrumb']/ul/li/a/text()").extract()[3])
		LYS_ProductName = sel.xpath("//h1/text()").extract()[0].replace(",","")
		LYS_url = response.url
		sp = response.xpath("//span[@class='RetailPrice']/strike/text()").extract()
		if sp:
			sp = response.xpath("//em[@class='ProductPrice VariationProductPrice']/text()").extract()[0].replace(",","").split("Rs ")[-1]
			mrp = response.xpath("//span[@class='RetailPrice']/strike/text()").extract()[0].replace(",","").split("Rs ")[-1]
		else:
			sp = ""
			mrp = response.xpath("//em[@class='ProductPrice VariationProductPrice']/text()").extract()[0].replace(",","").split("Rs ")[-1]
    
		stock = response.xpath("//div[@class='stockIcon Out Of Stock']").extract()
		if stock:
			stock = "Out of Stock"
		else:
			stock = "In Stock"
		sku = sel.xpath("//span[@class='VariationProductSKU']/text()").extract()[0].strip()
		
		LYS_row = [LYS_ProductName,LYS_url,sku,mrp,sp,stock,category,'|']
		
		row = LYS_row + snapdeal_extractor(LYS_ProductName) + amazon_extractor(LYS_ProductName)+ flipkart_extractor(LYS_ProductName) + paytm_extractor(LYS_ProductName)
		
		mywriter.writerow(row)

		
def snapdeal_extractor(productname):
	url = customsearch_api.snapdeal(productname)
	if url!='':
			row = extractors2.snapdeal_scraper(url)
	else:
		row = ['','','','','Not Found']

	row.append('|')	
	return row
	
	
def amazon_extractor(productname):
	url = customsearch_api.amazon(productname)
	if url!='':
		row = extractors2.amazon_scraper(url)
	else:
		row= ['','','','','Not Found']
	row.append('|')
	return row
	
def flipkart_extractor(productname):
	url = customsearch_api.flipkart(productname)
	if url!='':
		row = extractors2.flipkart_scraper(url)
	else:
		row = ['','','','','Not Found']

	row.append('|')
	return row
	
def paytm_extractor(productname):
	url = customsearch_api.paytm(productname)
	if url!='':
		row = extractors2.paytm_scraper(url)
	else:
		row = ['','','','','Not Found']

	row.append('|')
	return row
	
	
	
