from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from bhaseen.items import BhaseenItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["fitnessnleisure.com"]
  start_urls = ["http://www.fitnessnleisure.com/golf-irons.html"]

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="fr w35"]',))
                 , callback="parse_items", follow= True),)

  def parse_items(self, response):
   hxs = HtmlXPathSelector(response)  
   titles = hxs.select("//html")
   items = []
   
   for titles in titles:
     item = BhaseenItem()
     item ["productname"] = titles.select("//div/div/h2/b").extract()
     item ["imgurl"] = titles.select("//span[@class='p1_250']/a/@rel").extract()
     
     
     
     items.append(item)
     return(items)
      
            

        
