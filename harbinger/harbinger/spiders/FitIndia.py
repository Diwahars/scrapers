from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from harbinger.items import HarbingerItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["harbingerfitnessindia.com"]
  start_urls = ["http://harbingerfitnessindia.com/"]

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//li/a[@class="MenuBarItemSubmenu"]',)), follow= True),
    Rule (SgmlLinkExtractor(restrict_xpaths=('//td[@class="redbutton"]',))
    , callback="parse_items", follow= True),)

     
  def parse_items(self, response):
   hxs = HtmlXPathSelector(response)  
   titles = hxs.select("//html")
   items = []
   item = HarbingerItem()
   
   for title in titles:
     item["productname"] = titles.xpath('//title/text()').extract()
     item["Price"] = titles.select('//tr/td[@valign="middle"][2]/text()').extract()
     item["description"] = titles.select('//td[@class="text8"][1]/p/text()').extract()
     item["imgurl"] = titles.select('//img[@id="mainproimg"]/@src').extract()
     item["imgurl1"] = titles.select('//ul[@id="mycarousel"]/li/img/@src').extract()
     item["category"] = titles.select('//font[@color="white"][1]/text()').extract()
     items.append(item)
     
     return(items)
