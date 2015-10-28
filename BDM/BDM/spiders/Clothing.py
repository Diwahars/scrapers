from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from BDM.items import BdmItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "clothing"
  allowed_domains = ["bdmcricket.net"]
  start_urls = ["http://www.bdmcricket.net/cricket-ball.html"]
           
  def parse(self, response):
   hxs = HtmlXPathSelector(response)  
   titles = hxs.select("//html")
   items = []
     
   for titles in titles:
     item = BdmItem()
     item ["productname"] = titles.select('//html').extract()
     
     
     
     items.append(item)
     return(items)
      
  

