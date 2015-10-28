from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from botsaddle.items import BotsaddleItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["store.bumsonthesaddle.com"]
  start_urls = ["http://store.bumsonthesaddle.com/products/"]
  rules = (Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="container"]',))
    , callback="parse_items", follow= True),)
  

     
  def parse_items(self, response):
   hxs = HtmlXPathSelector(response)  
   titles = hxs.select("//body")
   items = []
   
   for titles in titles:
     item = BotsaddleItem()
     item ["productname"] = titles.select("//div[@class='span4']/header/h1/text()").extract()
     item ["imgurl"] = titles.select("//ul[@id='product-thumbnails']/li[@class='tmb-all']/a/@href").extract()
     item ["MRP"] = titles.select("//span[@class='price']/text()").extract()
     item ["Description"] = titles.select("//div[@class='productdetails_content ']").extract()
     item ["Category"] = titles.select("//div[@class='span9']/nav").extract()     
     item ["SKU"] = titles.select("//script[@id='analytics']").extract()
     item ["Variant"] = titles.select("//span[@class='variant-description']/text()").extract()
     item ["stock"] = titles.select("//p[@class='delivery']/text()").extract()
     
     items.append(item)
     return(items)
      
            

        
