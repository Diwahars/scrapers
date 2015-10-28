import re
import csv
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from pprint import pprint
from ..helpers import bigcommerce, mycsv


class Spider(CrawlSpider):
		name = 'adventureaxis'
		allowed_domains = ['adventureaxis.in']
		start_urls = [
        'http://www.adventureaxis.in/nrs-men-s-gunnison-shorts.html',
		'http://www.adventureaxis.in/millet-climb-addict-tee-shirt-ss-995.html',
		'http://www.adventureaxis.in/keen-wmns-newport-h2-sandal.html'
		
		]
		
		rules = (
					# Rule (LinkExtractor(allow=(),restrict_xpaths=("//div[@class='nav container clearer show-bg']",)), follow= True),
			     		Rule (LinkExtractor(allow=(),restrict_xpaths=("//div[@class='nav container clearer show-bg']",)), follow= True),
			     	  		Rule (LinkExtractor(restrict_xpaths=('//div[@class="product-image-wrapper"]',)), callback="parse_items", follow= True),)
			       

		def parse_items(self,response):
		# def parse(self, response):
			sel = Selector(response)			
			product_dict = {}
			product_dict['Product Name'] = sel.xpath("//div[@class='product-name']/h1/text()").extract()[0]
			product_dict['Description'] = sel.xpath("//div[@class='short-description']").extract()[0]				
			product_dict['Images'] = sel.xpath("//p[@class='product-image zoom-inside']//@href").extract()
			product_dict['Product Code/SKU'] = sel.xpath("//div[@class='no-display']/input/@value").extract()[0] + 'ADVAXS'
			product_dict['Bin Picking Number'] = 'ADVENTUREAXIS'
			product_dict['Price'] = sel.xpath("//div[@class='price-box']//span[@class='price']/text()").extract()[0].replace("Rs",'').strip()
			if sel.xpath("//div[@class='price-box']//span[@class='price']/text()").extract():
				product_dict['Sale Price'] = sel.xpath("//div[@class='price-box']//span[@class='price']/text()").extract()[1].replace("Rs",'').strip()
			else:
				product_dict['Sale Price'] = ''

			product_dict['Brand'] = ''
			product_dict['Category'] = '/'.join(categ for categ in sel.xpath("//div[@class='breadcrumbs']//a/text()").extract()[-2:])
			product_dict['Product Availability']  = '7-12 Working Days'
			product_dict['Sort Order'] = '-200'			
			size_script = sel.xpath("//script[contains(text(),'spConfig')]").extract()

			if size_script:
				product_dict['Track Inventory'] = 'By Option'
				bigcommerce.product_row(product_dict)
				variant_dict = {}
				
				size_script = sel.xpath("//script[contains(text(),'spConfig')]").extract()[0].split("Size")[-1].split('Color')[0]
				sizes = re.findall('label(.*?),',size_script)
				if sizes:
					variant_dict['Size'] = {}
					for size in sizes:
						size  = size.strip('"').strip(":").strip('"')
						if 'Select' not in size:
							variant_dict['Size'][size] = product_dict['Product Code/SKU']+size.replace(' ','')
				

				color_script = sel.xpath("//script[contains(text(),'spConfig')]").extract()[0].split("Color")[-1].split('ShoeSize')[0]
				if colors:
					colors = re.findall('label(.*?),',color_script)
					variant_dict['Color'] = {}								
					for color in colors:
						color = color.strip('"').strip(":").strip('"').replace('\\','').replace('/',' ')
						if 'Select' not in color:
							variant_dict['Color'][color] = product_dict['Product Code/SKU']+color.replace(' ','')
					
				bigcommerce.sku_row(variant_dict)

			else:
				product_dict['Track Inventory'] = 'By Product'
				bigcommerce.product_row(product_dict)

						 
