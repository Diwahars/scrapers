from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from nivia.items import NiviaItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["niviasports.com"]
  start_urls = ["http://www.niviasports.com/footwear.html",
                "http://www.niviasports.com/basketball-back-boards3.html"
                ]
  rules = (Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="img-border"]',))
                 , callback="parse_items", follow= True),)
  
    

    
  def parse_items(self, response):
   hxs = HtmlXPathSelector(response)
   titles = hxs.select("//html")
   items = []
   for titles in titles:
     item = NiviaItem()
     item ["productname"] = titles.select("//td[@class='text-gray'][2]").extract()
     item ["description"] = titles.select("//td[@class='text-gray']/text()").extract()
     item ["description1"] = titles.select("//td[@class='text-gray-2-2']/text()").extract()
     item ["imageurl"] = titles.select("//td[@class='prod-bg']/img/@src").extract()     
     item ["productcode"] = titles.select("//td[@class='prod-code']/span/text()").extract()
     
     
     items.append(item)
     return(items)
      
            

        
