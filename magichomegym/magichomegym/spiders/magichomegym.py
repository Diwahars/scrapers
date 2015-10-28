import re
import csv
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

from ..helpers import bigcommerce, mycsv


class Spider(CrawlSpider):
		name = 'magichomegym'
		# allowed_domains = ['adventure18.com']
		start_urls = [
        # 'http://www.adventureaxis.in/nrs-men-s-gunnison-shorts.html',
		'http://magichomegym.com/home-gyms',
		# 'http://www.adventureaxis.in/keen-wmns-newport-h2-sandal.html'
		
		]
		
		rules = (
					# Rule (LinkExtractor(allow=(),restrict_xpaths=("//*[contains(@class,'haschild')]",)), follow= True),
			     		# Rule (LinkExtractor(allow=(),restrict_xpaths=("//div[@id='menu']",)), follow= True),
			     			# Rule (LinkExtractor(allow=(),restrict_xpaths=("//ul[@class='navi']/li",)), follow= True),
			     	  			Rule (LinkExtractor(allow=(),restrict_xpaths=("//ul[@class='navi']/li",)), callback="parse_items", follow= True),)
			       

		def parse_items(self,response):

		# def parse(self, response):
			sel = Selector(response)			
			
			# # if stock:
			product_dict = {}
			product_dict['Product Name'] = sel.xpath("//h1/span/text()").extract()[0]
			product_dict['Description'] = sel.xpath("//div[@id='tab-description']").extract()[0]
			try: 
				product_dict['Description']+= sel.xpath("//div[@id='tab-attribute']").extract()[0]
			except:
				pass
			product_dict['Images'] = sel.xpath("//div[@class='product-info']//div[contains(@class,'image')]//@href").extract()
			product_dict['Product Code/SKU'] = sel.xpath("//div[@class='description']/span[contains(text(),'Product Code')]/following-sibling::text()").extract()[0].strip() + 'MGCHGYM'
			product_dict['Bin Picking Number'] = 'MAGICHOMEGYM'
			product_dict['Price'] = sel.xpath("//div[@class='product-info']//span[@class='price-old']/text()").extract()[0]
			product_dict['Sale Price'] = sel.xpath("//div[@class='product-info']//span[@class='price-new']/text()").extract()[0]
			product_dict['Brand'] = 'Magic Home Gym'
			product_dict['Category'] = sel.xpath("//*[@class='breadcrumb']/a/text()").extract()[1]
			product_dict['Product Availability']  = '7-12 Working Days'
			product_dict['Sort Order'] = '-200'				
			# try:
			# sizes = sel.xpath("//select[@id='Size_field']/option/text()").extract()
			# name = 'Size'
			# variant_dict = {}
			# variant_dict[name] = {}
			# for size in sizes:
			# 	variant_dict[name][size] = product_dict['Product Code/SKU']+size

			product_dict['Track Inventory'] = 'By Product'
			
			bigcommerce.product_row(product_dict)
			# bigcommerce.sku_row(variant_dict)

			# except:
			# 	product_dict['Track Inventory'] == 'By Option'
			# 	pass

						 
