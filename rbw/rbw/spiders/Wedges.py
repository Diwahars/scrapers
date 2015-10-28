from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from rbw.items import RbwItem
import urlparse 
from scrapy.http.request import Request



class MySpider(CrawlSpider):
  name = "mojo"
  
  start_urls = ["http://members.calbar.ca.gov/fal/Member/Detail/27859"]

  
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="product_thumbnail"]',))
    , callback="parse_items", follow= True),)
  
  def parse(self, response):
    print "Hello"
##    sel = Selector(response)
##    item = RbwItem()
##    hxs = HtmlXPathSelector(response)
##
##    item ["productname"] = sel.xpath("//div[@class='desc_name']/text()").extract()
##    item ["MRP"] = sel.xpath("//span[@class='was_price']/text()").extract()
##    item ["MRP1"] = sel.xpath("//div[@class='desc_price']/text()").extract()
##    item ["SP"] = sel.xpath("//span[@class='now_price']/text()").extract()
##    item ["imgurl"] = sel.xpath("//ul[@id='multiview']/li/a/img/@src").extract()
##    item ["Description"] = sel.xpath("//div[@id='overview']").extract()    
##    variants = sel.xpath(".//select[@name='pcode']/option/text()")
##    skus = sel.xpath(".//select[@name='pcode']/option/@value")
##    
##    
##    for variant,sku in zip(variants,skus):
##      item ["Variant"] = variant.extract()
##      item ["SKU"] = sku.extract()
##      yield item
      




