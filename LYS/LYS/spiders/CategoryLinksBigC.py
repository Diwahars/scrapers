from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from LYS.itemsPrice import LYSPriceItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "bigclinks"
  allowed_domains = ["live-you-sport.mybigcommerce.com"]
  start_urls = ["http://live-you-sport.mybigcommerce.com/brands/"]

            
  def parse(self, response):
    sel = Selector(response)
    
    
    item = LYSPriceItem()
    urls = sel.xpath("//div[@class='SubBrandList']/ul/li/a/@href")

    for url in urls:
      item ["productname"] = url.extract()
      yield item
      
    


    

