import re
import csv
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

from ..helpers import bigcommerce, mycsv


class Spider(CrawlSpider):
		name = 'stepinadventure'
		# allowed_domains = ['adventure18.com']
		start_urls = [
        # 'http://www.adventureaxis.in/nrs-men-s-gunnison-shorts.html',
		'http://www.stepinadventure.com/categories/ACCESSORIES/cid-CU00155578.aspx',
		# 'http://www.adventureaxis.in/keen-wmns-newport-h2-sandal.html'
		
		]
		
		rules = (
					# Rule (LinkExtractor(allow=(),restrict_xpaths=("//*[contains(@class,'haschild')]",)), follow= True),
			     		# Rule (LinkExtractor(allow=(),restrict_xpaths=("//li[@class='current Item_4']",)), follow= True),
			     			# Rule (LinkExtractor(allow=(),restrict_xpaths=("//div[@class='pagercontrol']",)), follow = True),
			     	  			Rule (LinkExtractor(allow=(),restrict_xpaths=("//li[@class='current Item_4']",)), 
			     	  				callback="parse_category", follow= True),)
	

		def parse_category(self, response):			
			sel = Selector(response)			
			
			control_id = sel.xpath("//script[contains(text(),'PgControlId')]").extract()[0].split('PgControlId":')[-1].split(',')[0]
			Client_Id = sel.xpath("//script[contains(text(),'PgControlId')]").extract()[0].split('DivClientId":')[-1].split(',')[0].strip('"')
			
			if sel.xpath("//a[@class='pager']//text()").extract():
				pages = int(sel.xpath("//a[@class='pager']//text()").extract()[-1].strip())
			else:
				pages = 1
				

			for page_num in range(1, pages+1):
				url = 'http://www.stepinadventure.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={"PgControlId":%s,"IsConfigured":true,"PageNo":%s,"DivClientId":"%s","IsRefineExsists":false}' %(control_id, page_num, Client_Id)
				url = url.replace('"','%22')
				# print url
				request = Request(url, self.pagination)
				yield request			

		def pagination(self, response):
			print 'pagination'
			sel = Selector(response)
			product_urls = [url for url in sel.xpath("//div[@class='bucket']//a/@href").extract() if '#' not in url]
			
			for url in product_urls:				
				request = Request(url, self.product_page)
				yield request


		def product_page(self,response):
		# def parse(self, response):
			sel = Selector(response)
					
			product_dict = {}
			product_dict['Product Name'] = sel.xpath("//h1/text()").extract()[0]			
			product_dict['Description'] = sel.xpath("//div[@id='Description']").extract()[0]				
			image_script = sel.xpath("//script[contains(text(),'ZoomPath')]").extract()[0]				
			image_script = re.findall(r'"ZoomPath":"http(.*?)1000"',image_script)
			product_dict['Images'] = [image.replace('width=','width=1000').replace('://','http://') for image in image_script]
			product_dict['Product Code/SKU'] = sel.xpath("//script[contains(text(),'ProductID')]").extract()[0].split('ProductID":')[-1].split(",")[0].strip() + "SINADV"
			product_dict['Bin Picking Number'] = 'STEPINADVENTURE'
			product_dict['Price'] = sel.xpath("//span[@class='sp_amt']/text()").extract()[0]
			try:					
				product_dict['Sale Price'] = sel.xpath("//span[@class='sp_amt']/text()").extract()[1]
			except:					
				product_dict['Sale Price'] = ''

			product_dict['Brand'] = sel.xpath("//div[@class='productbrand']/span/text()").extract()[0]				
			product_dict['Category'] = '/'.join(x for x in sel.xpath("//*[@class='breadcrumbg_l']//a/text()").extract()[-2:])				
			product_dict['Product Availability']  = '7-12 Working Days'
			product_dict['Sort Order'] = '-200'				
			variant_script = sel.xpath("//script[contains(text(),'variantProductId')]").extract()

			if variant_script:
				variant_script = re.findall(r'\[{"VariantValueDesc"(.*?inventory":1,)',variant_script[0])			
				
				variant_dict = {}
				name = 'Size'
				variant_dict[name] = {}

				for variant in variant_script:
					size = variant.split('variantValue":"')[-1].split('"')[0].strip()
					sku = product_dict['Product Code/SKU'] + variant.split('variantProductId":"')[-1].split('"')[0]
					variant_dict[name][size] = sku
				
				product_dict['Track Inventory'] = 'By Option'
				bigcommerce.product_row(product_dict)
				bigcommerce.sku_row(variant_dict)

			else:		
				product_dict['Track Inventory'] = 'By Product'
				bigcommerce.product_row(product_dict)
							 
