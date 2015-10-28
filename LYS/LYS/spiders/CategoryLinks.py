from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from LYS.itemsPrice import LYSPriceItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "categ"
  allowed_domains = ["liveyoursport.com"]
  start_urls = ["http://www.liveyoursport.com/"]

            
  def parse(self, response):
    sel = Selector(response)
    
    
    item = LYSPriceItem()
    urls = sel.xpath("//ul[@class='navigation-ul-box']/li/a/@href")

    for url in urls:
      item ["productname"] = url.extract()
      yield item
      
    


    

