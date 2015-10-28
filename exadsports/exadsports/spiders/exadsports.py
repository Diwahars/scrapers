import re
import csv
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

from ..helpers import bigcommerce, mycsv


class Spider(CrawlSpider):
		name = 'exadsports'
		# allowed_domains = ['adventure18.com']
		start_urls = [
        # 'http://www.adventureaxis.in/nrs-men-s-gunnison-shorts.html',
		'http://www.exadsports.com/Products/All-Products-Merida-Accessories-Shoes/Merida/Merida-Performance-MTB-193A--M--PMI/pid-9910734.aspx',
		# 'http://www.adventureaxis.in/keen-wmns-newport-h2-sandal.html'
		
		]
		
		rules = (
					# Rule (LinkExtractor(allow=(),restrict_xpaths=("//*[contains(@class,'haschild')]",)), follow= True),
			     		# Rule (LinkExtractor(allow=(),restrict_xpaths=("//div[@id='menu']",)), follow= True),
			     			Rule (LinkExtractor(allow=(),restrict_xpaths=("//li[@class='current Item_1']/ul/li/a",)), follow= True),
			     	  			Rule (LinkExtractor(allow=(),restrict_xpaths=("//div[@ref='ctrlshowcase']",)), callback="parse_items", follow= True),)
			       

		def parse_items(self,response):
		# def parse(self, response):
			sel = Selector(response)			
			stock = sel.xpath("//span[@content='out_of_stock']").extract()
			if not stock:
				product_dict = {}
				product_dict['Product Name'] = sel.xpath("//div[@class='rightpane']//h1/text()").extract()[0]
				product_dict['Description'] = ''
				try:
					product_dict['Description'] += sel.xpath("//div[@id='lknFeatures']/div").extract()[0] 
				except:
					pass				
				try:
					product_dict['Description'] += sel.xpath("//*[@id='Description']").extract()[0]
				except:
					pass

				product_dict['Images'] = [image.replace('width=70','width=600') for image in sel.xpath("//div[@class='mutipleimgs_thumbs']//@src").extract()]

				product_dict['Product Code/SKU'] = sel.xpath("//script[contains(text(),'ProductId')]").extract()[0].split('ProductId":')[-1].split(',')[0].strip() + 'EXSPRT'
				product_dict['Bin Picking Number'] = 'EXADSPORTS'
				product_dict['Price'] = sel.xpath("//*[@class='sp_amt']/text()").extract()[0]
				product_dict['Sale Price'] = ''
				product_dict['Brand'] = sel.xpath("//*[@class='brandlname']/text()").extract()[0]
				product_dict['Category'] = sel.xpath("//*[@class='breadcrumbg_l']//a/text()").extract()[-1]
				product_dict['Product Availability']  = '7-12 Working Days'
				product_dict['Sort Order'] = '-200'				
				if 'Shoes' in product_dict['Category']:				
					sizes = sel.xpath("//tr[@class='rowstyle']//*[@class='propertyvalue']/text()").extract()[0].split(',')
					name = 'Size'
					variant_dict = {}
					variant_dict[name] = {}
					for size in sizes:
						variant_dict[name][size.strip()] = product_dict['Product Code/SKU']+size.strip()
					product_dict['Track Inventory'] = 'By Option'
					bigcommerce.product_row(product_dict)
					bigcommerce.sku_row(variant_dict)

				else:		
					product_dict['Track Inventory'] = 'By Product'
					bigcommerce.product_row(product_dict)
							 
