from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from BDM.items import BdmItem
import urlparse 
from scrapy.http.request import Request
from scrapy.selector import Selector



class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["bdmcricket.net"]
  start_urls = ["http://www.bdmcricket.net/cricket-ball.html",]

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//p[@class="fl wn6 c4 r7 b"]',))
    , callback="parse_items", follow= True),)
  



  def parse_items(self, response):
    item = BdmItem()
    sel = Selector(response)
    

    productnames = sel.xpath("//td[@class='pd5']/h2/text()")
    descriptions = sel.xpath("//div[@class='c8 lh3 pdc vr tz p63']")
    imgurls = sel.xpath("//td[@align='CENTER']/a/@dataimg")
    
    
    for productname, description, imgurl in zip(productnames, descriptions, imgurls):
      item["Description"] = description.extract()
      item["productname"] = productname.extract()
      
      item["imgurl"] = imgurl.extract()
      

      yield item
      
    

   
