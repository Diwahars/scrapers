from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider


import urlparse ,re, json, unicodecsv,csv
from scrapy.http.request import Request

output = open("RyderCycles.csv", 'wb')
mywriter = unicodecsv.writer(output)

header = ['Item Type', 'Product Name', 'Brand Name','Product Code', 'Availability', 'Price', ' Description', 'Images']
mywriter.writerow(header)


class MySpider(CrawlSpider):
	name = "rydercycles"
	allowed_domains = ["rydercycles.com"]
	start_urls = [  
	"http://rydercycles.com/our-products/cycles-for-kids"
	]	
	rules = (	
				Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=("//div[@id='menu-inner']",)), follow= True),
				Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="links"]',)), follow= True),
				Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=("//div[@class='box-product product-list list-layout']",)), 
					callback="parse_productpage" , follow= True),)
	
	def parse_productpage(self, response):
		sel = Selector(response)
		product_name = sel.xpath("//h1/text()").extract()[0]
		brand_name = sel.xpath("//div[@class='description']/a/text()").extract()[0]
		product_code = sel.xpath("//div[@class='description']//text()").extract()[6]

		availability = sel.xpath("//div[@class='description']//text()").extract()[9]

		price =  sel.xpath("//div[@class='price']//text()").extract()[1]

		description = sel.xpath("//table[@class='attribute']").extract()[0]
		image = sel.xpath("//div[@class='image']//@href").extract()[0]


		row = ['Product', product_name, brand_name, product_code, availability, price, description, image]
		mywriter.writerow(row)



