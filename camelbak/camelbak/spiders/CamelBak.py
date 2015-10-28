from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from camelbak.items import CamelbakItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["camelbakindia.com"]
  start_urls = ["http://www.camelbakindia.com/cbi/catalog/8",
                "http://www.camelbakindia.com/cbi/catalog/8?sort_by=title&sort_order=ASC&page=1"]

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="s_item grid_3"]',))
                 , callback="parse_items", follow= True),)


  def parse_items(self, response):
   hxs = HtmlXPathSelector(response)  
   titles = hxs.select("//html")
   items = []
   
   for titles in titles:
     item = CamelbakItem()
     item ["productname"] = titles.select("//h1/text()").extract()
     item ["imgurl"] = titles.select("//div[@id='product_images']/a/img/@src").extract()
     item ["imgurl2"] = titles.select("//div[@id='product_gallery']/ul/li/a/@href").extract()
     item ["stock"] = titles.select("//div[@class='field-item even']/text()").extract()
     item ["description"] = titles.select("//div[@class='field field-name-body field-type-text-with-summary field-label-hidden']").extract()
     item ["SP"] = titles.select("//p[@class='s_price'][1]/text()").extract()
     item ["Video"] = titles.select("//div[@class='s_box']/div/iframe/@src").extract()
      
     
     items.append(item)
     return(items)
      
            

        
