from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from tynor.items import TynorItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["tynorindia.com"]
  start_urls = ["http://www.tynorindia.com/catalog/body-belts-braces/",
                "http://www.tynorindia.com/catalog/cervical-aids/",
                "http://www.tynorindia.com/catalog/fracture-aids/",
                "http://www.tynorindia.com/catalog/finger-splints/",
                "http://www.tynorindia.com/catalog/silicon-foot-products/",
                "http://www.tynorindia.com/catalog/walking-aids/",
                "http://www.tynorindia.com/catalog/physiotherapy-aids/",
                "http://www.tynorindia.com/catalog/allied-products/",
                "http://www.tynorindia.com/catalog/traction-kits/",
                "http://www.tynorindia.com/catalog/neoprene-products/",
                "http://www.tynorindia.com/catalog/wrist-fore-arm-products/",
                "http://www.tynorindia.com/catalog/knees-ankle-supports/"      
                          ]
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="box"]',)),callback="parse_items", follow= True),)
  
  def parse_items(self, response):
   hxs = HtmlXPathSelector(response)
   titles = hxs.select("//html")
   items = []
   for titles in titles:
     item = TynorItem()
     item ["productname"] = titles.select("//div[@class='Pro-right-con']/h1/text()").extract()
     item ["Size"] = titles.select("//div[@style='width:400px; clear:both; font-size:13px; margin:0 0 10px 1px;']/text()").extract()
     item ["SKU"] = titles.select("//div[@style='width:400px; font-size:13px; margin:0 0 4px 1px;']/text()").extract()     
     item ["Description"] = titles.select("//div[@class='Pro-right-con']").extract()
     item ["imgurl1"] = titles.select("//div[@id='carousel']/div/img/@src").extract()
     item ["imgurl2"] = titles.select("//table[@class='tableData']/tr/td/input/@src").extract()
           
         
     items.append(item)
     return(items)
      
            

        
