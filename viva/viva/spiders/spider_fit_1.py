from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from viva.items import VivaItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["vivafitness.net"]
  start_urls = ["http://vivafitness.net/commercial-equipment/treadmills"]
  
      
                
  def parse(self, response):
   hxs = HtmlXPathSelector(response)  
   titles = hxs.select("//html")
   items = []
   
   for titles in titles.select("//div[class='page-header']"):
     item = VivaItem()
     item ["productname"] = titles.select("//text()").extract()
     items.append(item)

     
     return(items)
      
            

        
