from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from golfessentials.items import GolfessentialsItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "drivers"
  allowed_domains = ["golfessentials.in"]
  start_urls = ["http://golfessentials.in/products.php?type=Drivers&page=0"]

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="pagination"]',)), follow= True),
    Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="boxes"]',))
    , callback="parse_items", follow= True),)  
  
    
  def parse_items(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//html")
    items = []
    for titles in titles:
      item = GolfessentialsItem()
      item ["productname"] = titles.select("//h2[8]/text()").extract()
      item ["MRP"] = titles.select("//h3[@class='left mrp']/text()").extract()
      item ["SP"] = titles.select("//h3[@class='left sp']/text()").extract()
      item ["imgurl"] = titles.select("//ul[@id='thumblist']/li/a/img/@src").extract()
      item ["Description"] = titles.select("//div[@class='grid_18 description left alpha omega']").extract()
      item ["Variant"] = titles.select("//table[@id='product_table']/tr/td").extract()
      
      
      items.append(item)
      return(items)





