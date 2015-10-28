from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from uniquefitness.items import UniquefitnessItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "mojo2"
  allowed_domains = ["uniquegym.com"]
  start_urls = ["http://uniquegym.com/"]
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//ul[@class="menu"]/li',))
                 , callback="parse_items", follow= True),)
  
     
  def parse_items(self, response):
   hxs = HtmlXPathSelector(response)  
   titles = hxs.select("//html")
   items = []
   
   
   for titles in titles:
    item = UniquefitnessItem()
    item["productname"] = titles.select('//td[@class="product_name"]/strong/text()').extract()
    item["imgurl"] = titles.select('//a[@class="zoom"]/@href').extract()
    item["description"] = titles.select('//td[@class="main_text"]/ul').extract()
    items.append(item)
     
    return(items)
