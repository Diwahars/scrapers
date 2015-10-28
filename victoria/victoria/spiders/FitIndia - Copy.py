from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from victoria.items import victoriaItem
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
   item = victoriaItem()
   
   for titles in titles:
     item = victoriaItem()
     item ["productname"] = titles.select('//td[@class="product_name"]').extract()
     item ["imgurl"] = titles.select('//tr/td[@class="product_text"]').extract()
     item ["Specification"] = titles.select('//tr/td[@class="product_text"]').extract()
     
     items.append(item)
     return(items)
      
  
