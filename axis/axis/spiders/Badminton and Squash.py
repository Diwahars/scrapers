from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from axis.items import AxisItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["adventureaxis.in"]
  start_urls = ["http://www.adventureaxis.in/footwear.html",
                "http://www.adventureaxis.in/sale20.html",
                "http://www.adventureaxis.in/camping-outdoor.html",
                "http://www.adventureaxis.in/expeditiongears.html",
                "http://www.adventureaxis.in/outdoorclothing.html",
                "http://www.adventureaxis.in/trekkingequipment.html"
                "http://www.adventureaxis.in/watersportsequipmentinindia.html"]
  
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//dd[@class="last odd"]/ol/li',)), follow= True),
           Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="pages"]',)), follow= True),  
            Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="products-box"]',))
    , callback="parse_items", follow= True),)
    
  def parse_items(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//html")
    items = []
    for titles in titles:
      item = AxisItem()
      item ["productname"] = titles.select("//li[@class='product']/strong/text()").extract()
      item ["MRP"] = titles.select("//span[@class='price'][2]/text()").extract()
      item ["SP"] = titles.select("//span[@class='price'][3]/text()").extract()
      item ["Stock"] = titles.select("//p[@class='availability in-stock']/span/text()").extract()
      item ["sku"] = titles.select("//p[@class='sku']/text()").extract()      
      item ["imgurl"] = titles.select("//p[@class='product-image product-image-zoom']/a/@href").extract()
      item ["imgurl1"] = titles.select("//div[@class='more-views']/ul/li/a/@href").extract()
      item ["Description"] = titles.select("//div[@class='short-description']").extract()
      item ["Specification"] = titles.select("//div[@class='short-description']/div/p/span").extract()
      item ["Color"] = titles.select("//div[@class='input-box'][1]").extract()
      item ["Size"] = titles.select("//div[@class='input-box'][2]").extract()
      
      item ["category"] = titles.select("//div[@class='breadcrumbs']/ul/li/a").extract()
      
      
      items.append(item)
      return(items)





