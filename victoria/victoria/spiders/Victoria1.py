from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from victoria.items import VItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "victoria"
  allowed_domains = ["victoriasportsco.com"]
  start_urls = ["http://www.victoriasportsco.com/snooker_biliard_table.php#vs20"]
  
 
     
  def parse(self, response):
    hxs = HtmlXPathSelector(response)  
    titles = hxs.select("//html")
    items = []
    item = VItem()
    
    names = hxs.xpath('//td[@class="product_name"]/strong/text()')
    imageurls = hxs.xpath('//tr/td[@align="center"]/a/img/@src')
    for name, url in zip(names, imageurls):
        item["productname"] = name
        item["imgurl"] = url
        yield item

    
