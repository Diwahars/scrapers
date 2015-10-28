from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
import urlparse 
from scrapy.http.request import Request
import unicodecsv

output = open("Output.csv",'w')
mywriter = unicodecsv.writer(output)


class MySpider(CrawlSpider):
  name = "test"
  
  start_urls = [
  				"http://mobspare.com/",
  				# 'http://mobspare.com/13-battery',
  				]
  
  rules = (
  		Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=("//a[@class='menu-item-title']",)), follow= True),
  		Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=("//div[@id='pagination']",)), follow= True),
  		Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=("//div[@class='product-image-container']",)),
    callback="parse_items", follow= True),)
  
  def parse_items(self, response):
	sel = Selector(response)
  	product_name = sel.xpath("//h1/text()").extract()[0]
  	row = [product_name]
  	mywriter.writerow(row)


    