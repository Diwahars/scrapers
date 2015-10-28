from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from activinstinct.items import ActivinstinctItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "outdoor"
  allowed_domains = ["activinstinct.com"]
  start_urls = ["http://www.activinstinct.com/more-sports/outdoor/accessories/",
                "http://www.activinstinct.com/more-sports/outdoor/base-layer/",
                "http://www.activinstinct.com/more-sports/outdoor/clothing/",
                "http://www.activinstinct.com/more-sports/outdoor/cooking-equipment-utensils/",
                "http://www.activinstinct.com/more-sports/outdoor/food-drink-storage/",
                "http://www.activinstinct.com/more-sports/outdoor/gps-and-watches/",
                "http://www.activinstinct.com/more-sports/outdoor/rucksacks/",
                "http://www.activinstinct.com/more-sports/outdoor/walking-and-hiking/"
                "http://www.activinstinct.com/more-sports/outdoor/sleeping-bags/",
                "http://www.activinstinct.com/more-sports/outdoor/socks/",
                "http://www.activinstinct.com/more-sports/outdoor/tents/",
                "http://www.activinstinct.com/more-sports/outdoor/walking-poles/",
                ]             
                      
                
                
                
                
                
                
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//ul[@id="pagination-digg"]',)), follow= True),
    Rule (SgmlLinkExtractor(restrict_xpaths=('//ul[@class="clearfix"]',))
    , callback="parse_items", follow= True),)
    
  def parse_items(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//html")
    items = []
    for titles in titles:
      item = ActivinstinctItem()
      item ["productname"] = titles.select("//h1[@class='black']/text()").extract()
      item ["MRP"] = titles.select("//p[@class='blue']/text()").extract()
      item ["SP"] = titles.select("//p[@id='product-price']/text()").extract()
      item ["Stock"] = titles.select("//div[@class='notifyMe-soldout']/text()").extract()
      item ["SKU"] = titles.select("//div/p[@class='gray']/text()").extract()      
      item ["imgurl"] = titles.select("//div[@id='product-image-view']/div/a/img/@src").extract()
      item ["Description"] = titles.select("//div[@id='hp_fix_desc']").extract()
      item ["Size"] = titles.select("//li/a[@class='button3']/span/text()").extract()
      
      
      items.append(item)
      return(items)





