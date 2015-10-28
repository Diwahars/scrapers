from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from activinstinct.items import ActivinstinctItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "triathlon"
  allowed_domains = ["activinstinct.com"]
  start_urls = ["http://www.activinstinct.com/triathlon/accessories/",
                "http://www.activinstinct.com/triathlon/base-layer/",
                "http://www.activinstinct.com/triathlon/bikes-and-accessories/",
                "http://www.activinstinct.com/triathlon/clothing/",
                "http://www.activinstinct.com/triathlon/goggles-and-masks/",
                "http://www.activinstinct.com/triathlon/mobile-app-accessories/",
                "http://www.activinstinct.com/triathlon/shoes/",
                "http://www.activinstinct.com/triathlon/swimwear/",
                "http://www.activinstinct.com/triathlon/watches-and-heart-rate-monitors/",
                "http://www.activinstinct.com/triathlon/wetsuits/"]
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





