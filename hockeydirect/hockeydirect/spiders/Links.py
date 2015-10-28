from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from hockeydirect.items import HockeyDirectItem
import urlparse 
from scrapy.http.request import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider

class MySpider(CrawlSpider):
  name = "links"
  allowed_domains = ["hockeydirect.com"]
  start_urls = ["http://www.hockeydirect.com/Catalogue/Hockey-Shoes/Adidas-Hockey-Shoes/adidas-Flex-Women-Hockey-Shoe-Mint-296059#.VLpdpSuUf60",
                "http://www.hockeydirect.com/Catalogue/Hockey-Shoes/Grays-Hockey-Shoes/Grays-G8000-Ladies-Hockey-Shoe-226040"]
                
     
#--BASIC PRODUCT DATA STARTS HERE--
  def parse(self,response):
  #def parse(self,response):
    sel = Selector(response)
    item = HockeyDirectItem()

    item ["Item_Type"] = sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","").split(" Hockey")[0].split(" ")[-1]

    yield item


            
    
    
