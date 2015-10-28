from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider
from dicks.items import DicksItem
import urlparse ,re, json, unicodecsv,csv
from scrapy.http.request import Request
ouput = open("FitIndia.csv","wb")
mywriter = unicodecsv.writer(output)
header = ('Item Type','Product ID','Product Name','Brand Name','Price','Retail Price','Sale Price','Product Description','Product Code/SKU','Bin Picking Number','Category',
                 'Option Set','Product Availability','Current Stock Level','Free Shipping','Sort Order','Meta Description','Page Title',''
             'Product Image Description - 1','Product Image Is Thumbnail - 1',''
             'Track Inventory','Product Image Sort - 1','Product Image Sort - 2','Product Image Sort - 3','Product Image Sort - 4','Product Image Sort-5','Product Image Sort-6','Product Image Sort-7','Product Image Sort-8',
             'Product Image File - 1','Product Image File - 2','Product Image File - 3','Product Image File - 4','Product Image File - 5 ',
    'Product Image File - 6','Product Image File - 7','Product Image File - 8')
	

class HolabirdSpider(CrawlSpider):
	name = "fitindia"
	allowed_domains = ["fitkart.in"]
	start_urls = [ "http://www.fitkart.in"
					
    
	rules = (
			Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//ul[@class="nav navbar-nav"]',)), follow= True),			    
			      Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@ng-repeat="product in products"]',))
  					, callback="parse_items", follow= True),)

	def parse_item(self, response):
		sel = Selector(response)

		product_name = sel.xpath("//")
