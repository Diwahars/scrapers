import re
import csv
import pprint

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

from ..helpers import bigcommerce, mycsv



# Globals
# header = ('Item Type','Product Name','Retail Price','Sale Price','Product Code/SKU','Description','Image Url')
# output = open("file.csv", "wb")

# Write base row to CSV
# mywriter = csv.writer(output)
# mywriter.writerow(header)

class Spider(CrawlSpider):
		name = 'adventure18'
		# allowed_domains = ['adventure18.com']
		start_urls = [
        # 'http://www.adventureaxis.in/nrs-men-s-gunnison-shorts.html',
		'http://www.adventure18.com/catalog/camping-hiking-gear/accessories.html',
		# 'http://www.adventureaxis.in/keen-wmns-newport-h2-sandal.html'
		
		]
		
		rules = (
					# Rule (LinkExtractor(allow=(),restrict_xpaths=("//*[contains(@class,'haschild')]",)), follow= True),
			     		# Rule (LinkExtractor(allow=(),restrict_xpaths=("//tbody/tr",)), follow= True),
			     			Rule (LinkExtractor(allow=(),restrict_xpaths=("//ul[@class='pagination']",)), follow= True),
			     	  			Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@id="vmMainPage"]',)), callback="parse_items", follow= True),)
			       

		def parse_items(self,response):
			
		# def parse(self, response):
			sel = Selector(response)			
			# # if stock:
			product_dict = {}
			product_dict['Product Name'] = sel.xpath("///h1/text()").extract()[0]
			product_dict['Description'] = sel.xpath("//div[@class='product_descrp']").extract()[0]
			product_dict['Images'] = sel.xpath("//div[@class='thumb_image']//@href").extract()
			product_dict['Product Code/SKU'] = 'ADVENTURE18' + sel.xpath("//strong[contains(text(),'Product Code')]/following-sibling::text()").extract()[0].strip()
			product_dict['Bin Picking Number'] = 'ADVENTURE18'
			product_dict['Price'] = sel.xpath("//strong[contains(text(),'Price')]/following-sibling::span/text()").extract()[0].split('INR')[-1].strip()
			product_dict['Brand'] = ''
			product_dict['Category'] = '/'.join(x for x in sel.xpath("//span[@class='pathway']/a/text()").extract()[-2:])
			product_dict['Product Availability']  = '7-12 Working Days'
			product_dict['Sort Order'] = '-200'				
			# try:
			sizes = sel.xpath("//select[@id='Size_field']/option/text()").extract()
			name = 'Size'
			variant_dict = {}
			variant_dict[name] = {}
			for size in sizes:
				variant_dict[name][size] = product_dict['Product Code/SKU']+size

			product_dict['Track Inventory'] = 'By Option'
			print 'XXXX'
			bigcommerce.product_row(product_dict)
			bigcommerce.sku_row(variant_dict)

			# except:
			# 	product_dict['Track Inventory'] == 'By Option'
			# 	pass

						 
