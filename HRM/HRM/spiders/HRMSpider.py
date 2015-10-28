from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from HRM.items import HrmItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["axtrosports.com"]
  start_urls = ["http://www.axtrosports.com/catalog/seo_sitemap/product/"]
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//ol',)), follow= True),
    Rule (SgmlLinkExtractor(restrict_xpaths=('//ul[@class="sitemap"]',))
    , callback="parse_items", follow= True),)
    
   
  def parse_items(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//head")
    items = []
    for titles in titles:
      item = HrmItem()
      item ["productname"] = titles.select("//h3[@class='product-name']/text()").extract()      
      item ["MRP"] = titles.select("//span[@class='price'][1]/text()").extract()
      item ["stock"] = titles.select("//p[@class='availability in-stock']/span/text()").extract()
      item ["imgurl"] = titles.select("//div[@class='more-views']/ul/li/a/img/@src").extract()      
      item ["Description"] = titles.select("//div[@class='box-collateral box-description']").extract()
      item ["Size"] = titles.select("//div[@class='input-box']/select/option/text()").extract()
      
      items.append(item)
      return(items)
      
            

        
