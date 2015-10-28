from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider

import urlparse,re,json,unicodecsv
import demjson


class Spider(CrawlSpider):

		name = 'mens_fashion_shoes'
		# allowed_domains = ['amazon.com']
		start_urls = [        
        'http://www.amazon.com/s/ref=lp_679255011_ex_n_7?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A679255011%2Cn%3A679312011',
        'http://www.amazon.com/Mens-Boots/b?ie=UTF8&node=679307011',
        'http://www.amazon.com/s/ref=lp_679255011_ex_n_8?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A679255011%2Cn%3A679313011&bbn=10445813011&ie=UTF8&qid=1445406717',
        'http://www.amazon.com/s/ref=lp_679255011_ex_n_9?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A679255011%2Cn%3A3420996011&bbn=10445813011&ie=UTF8&qid=1445406717',
        'http://www.amazon.com/s/ref=lp_679255011_ex_n_10?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A679255011%2Cn%3A6127766011&bbn=10445813011&ie=UTF8&qid=1445406717',
        'http://www.amazon.com/s/ref=lp_679255011_ex_n_11?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A679255011%2Cn%3A679319011&bbn=10445813011&ie=UTF8&qid=1445406717',
        'http://www.amazon.com/s/ref=lp_679255011_ex_n_12?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A679255011%2Cn%3A679320011&bbn=10445813011&ie=UTF8&qid=1445406717',
        'http://www.amazon.com/s/ref=lp_679255011_ex_n_13?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A679255011%2Cn%3A679324011&bbn=10445813011&ie=UTF8&qid=1445406717',
        'http://www.amazon.com/s/ref=lp_679255011_ex_n_14?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A679255011%2Cn%3A679334011&bbn=10445813011&ie=UTF8&qid=1445406717'
		]	
		
		rules = (
				Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@id="pagn"]',)), follow= True),
				Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//li[contains(@id,"result")]',)), 
					callback="parse_product" , follow= True),)

		# def parse(self, response):
		def parse_product(self, response):			
			sel = Selector(response)
			product_name = sel.xpath("//span[@id='productTitle']/text()").extract()[0]						
			specification =  sel.xpath("//ul[@class='a-vertical a-spacing-none']").extract()[0]
			description = sel.xpath("//div[@id='productDescription']/p").extract()[0]						
			variant_dict, price_dict,image_dict = {}, {}, {}			
			price  = sel.xpath("//span[@class='a-size-medium a-color-price']/text()").extract()[0].replace('$','')
			if '-' in price:
				price = price.split('-')[1]			
			price = float(price)
			price = str((price*65 + 2100)*114.5/100 + price*65*23/100)

			try:
				brand = sel.xpath("//a[@id='brand']/text()").extract()[0]
			except:
				brand =  sel.xpath("//a[@id='brand']/@href").extract()[0].split("/")[-2]

			size_script = sel.xpath("//script[@language='JavaScript'][contains(text(),'window.isTwisterAUI = 1')]").extract()[0].split('dimensionValuesDisplayData')[-1].split('"deviceType')[0]
			new_script = re.findall('"(.*?)]',size_script.split("hidePopover")[0])
			for i in new_script:
				asin = i.split('[')[0].replace(':{"','').replace('":','')				
				variants = i.split('["')[-1]
				variant_dict[asin] = variants		
				# price_script = sel.xpath("//script[contains(text(),'immutableURLPrefix')]").extract()[0].split('immutableURLPrefix')[-1]
				# price_url = 'http://www.amazon.com'
				# price_url += price_script.split('"immutableParams"')[0].split('":"')[-1].split('",')[0]
				# price_url += '&psc=1'
				# price_url += '&asinList='+asin
				# price_url += '&isFlushing=2'			
				# dpEnvironment = sel.xpath("//script[contains(text(),'dpEnvironment')]").extract()[0].split('"dpEnvironment" : ')[-1].split('"')[1].replace('"',"")
				# price_url += '&dpEnvironment='+dpEnvironment
				# price_url += '&id='+asin
				# price_url += '&mType=full'				
				# request = Request(price_url, callback = self.pricing)
				# yield request
			
			parent_asin = sel.xpath("//div[@id='tell-a-friend']/@data-dest").extract()[0].split('parentASIN=')[-1].split('&')[0]
			row = ['Product', parent_asin, brand, product_name,'',price, description, specification]
			mywriter.writerow(row)

			color_script = sel.xpath("//script[@type='text/javascript'][contains(text(),'customerImages')]").extract()[0].split('data["colorImages"] =')[-1].split('data["heroImage"] = {};')[0]			
			color_script = color_script.rsplit(';',1)[0]
			color_script = demjson.decode(color_script)

			for key,value in variant_dict.iteritems():
				color = value.split('"')[-2].split('"')[0]			
				image_dict[color] = []
				
				for images in color_script[color]:					
					image_dict[color].append(images['large'])
									

			for asin, variants in variant_dict.iteritems():
				color =  variants.split('"')[-2]
				row = []
				size  = variants.split('"')[0]
				row = ['SKU', asin, '', color, size, price, '', '']

				for image in image_dict[color]:
					row.append(image)

				mywriter.writerow(row)
