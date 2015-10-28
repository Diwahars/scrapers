from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from longshine.items import longshineItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["longshine.in"]
  start_urls = ["http://longshine.in/road-bikes/",
                "http://longshine.in/accessories/",
                "http://longshine.in/components/"]

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="pagination pagination__posts"]',)), follow= True),           
            Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="caption caption__portfolio"]',))
    , callback="parse_items", follow= True),)
  
    
  def parse_items(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//html")
    items = []
    for titles in titles:
      item = longshineItem()
      item ["productname"] = titles.select("//title/text()").extract()
      item ["brand"] = titles.select("//div[@class='portfolio-meta']/span/a[2]/text()").extract()      
      item ["MRP"] = titles.select("//h1/span").extract()
      
      item ["sku"] = titles.select("//p[@class='sku']/text()").extract()      
      item ["imgurl"] = titles.select("//figure[@class='featured-thumbnail thumbnail large']/img/@src").extract()
      
      item ["Description"] = titles.select("//p[1]").extract()
      
      
      item ["category"] = titles.select("//ul[@class='breadcrumb breadcrumb__t']/li/a").extract()
      item ["category1"] = titles.select("//div[@class='portfolio-meta']/span/a[3]/text()").extract()      
      
      
      items.append(item)
      return(items)





