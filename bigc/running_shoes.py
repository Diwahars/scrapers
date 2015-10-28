from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider

import urlparse,re,json,unicodecsv
import demjson

output = open("Amazon_RunningShoes.csv", 'wb')
mywriter = unicodecsv.writer(output)
header = ('Item Type','ASIN','Brand Name', 'Product Name', 'Size', 'Price', 'Description', 'Specification','Images', 'Item Number')
mywriter.writerow(header)

class Spider(CrawlSpider):
		name = 'amazon'
		# allowed_domains = ['amazon.com']
		start_urls = [
        # 'http://www.amazon.com/ASICS-Gel-Kayano-Running-Lightning-Yellow/dp/B00IEVUIJU/ref=lp_679286011_1_1?s=apparel&ie=UTF8&qid=1442306231&sr=1-1&nodeID=679286011'		
        'http://www.amazon.com/s/ref=sr_pg_7?rh=n%3A7141123011%2Cn%3A7147441011%2Cn%3A679255011%2Cn%3A6127770011%2Cn%3A679286011&page=7&ie=UTF8&qid=1442305626&spIA=B00F2FZD1O,B00AYJ4VWU,B00RW5O3GS,B00N44Y5OQ,B00RW5AG3C,B00DNNX210,B00GH18ETK,B00RQCGA9U,B00F2FZA4O,B00RW59VB0,B00RW5JBJW,B00N44Z5CC,B00WW7M14M,B00RW5AU8S,B00RW5712Q,B008AILY90'
		]	
		
		rules = (
				Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//span[@class="pagnLink"]',)), follow= True),
				Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]',)), 
					callback="parse_category" , follow= True),)

		# def parse(self, response):
		def parse_category(self, response):			
			sel = Selector(response)

			product_name = sel.xpath("//span[@id='productTitle']/text()").extract()[0]						
			specification =  sel.xpath("//ul[@class='a-vertical a-spacing-none']").extract()[0]
			description = sel.xpath("//div[@id='productDescription']/p").extract()[0]						
			variant_dict, price_dict,image_dict = {}, {}, {}			
			price  = float(sel.xpath("//span[@class='a-size-medium a-color-price']/text()").extract()[0].split('-')[1].replace('$',''))
			price = str(price*65 + 2100)*114.5/100 + price*65*23/100

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
			item_number = sel.xpath("//span[contains(text(),'Item model number')]/following-sibling::span").extract()[0]
			parent_asin = sel.xpath("//div[@id='tell-a-friend']/@data-dest").extract()[0].split('parentASIN=')[-1].split('&')[0]
			row = ['Product', parent_asin, brand, product_name,'',price, description, specification, item_number]
			mywriter.writerow(row)

			color_script = sel.xpath("//script[@type='text/javascript'][contains(text(),'customerImages')]").extract()[0].split('data["colorImages"] =')[-1].split('data["heroImage"] = {};')[0]			
			color_script = color_script.rsplit(';',1)[0]
			color_script = demjson.decode(color_script)

			for key,value in variant_dict.iteritems():
				color = value.split('US","')[-1].split('"')[0]			
				image_dict[color] = []
				# image_dict[color] = color_script[color]
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

				

			

		# def pricing(self, response):
		# 	print 'X'
		# 	sel = Selector()
		# 	price = sel.xpath("//span[@class='a-size-medium a-color-price']/text()").extract()[0].strip('$')
		# 	print price









						
	
					
					
					
			
			
						
						
					
					
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
	