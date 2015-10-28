from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from MBS.items import MbsItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "moj1o"
  allowed_domains = ["mybadmintonstore.com"]
  start_urls = ["http://www.mybadmintonstore.com/shop/index.php?cPath=25_26_180"]
  rules = Rule (SgmlLinkExtractor(restrict_xpaths=('//a/href',))
    , callback="parse_items", follow= True)
    
   
  def parse_items(self, response):
   hxs = HtmlXPathSelector(response)
   titles = hxs.select("//html")
   items = []
   for titles in titles:
     item = MbsItem()
     item ["productname"] = titles.select("//div[@class='content']/div[@class='inner']/table/tr/td/a/b/text()").extract()
     item ["imgurl1"] = titles.select("//p[@style='text-align: center; background: white']/img/@src").extract()
     item ["imgurl2"] = titles.select("//p[@align='center']/img/@src").extract()
     item ["imgurl3"] = titles.select("//div[@align='center']/a/img/@src").extract()
     item ["MRP"] = titles.select("//td[@class='pageHeading']/text()").extract()
     item ["Description"] = titles.select("//div[@align='center']").extract()
     item ["SKU"] = titles.select("//td[@class='pageHeading']/span/text()").extract()
     item ["Category"] = titles.select("//td[@class='headerNavigation']/a[4]/text()").extract()
     
     items.append(item)
     return(items)
      
            

        
