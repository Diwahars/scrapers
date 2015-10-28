from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from lonsdale.items import LonsdaleItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["lonsdale.com"]
  start_urls = ["http://www.lonsdale.com/"]

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//li[@class="columnGroup clearfix"]',)), follow= True),
           Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//span[@id="divPageNumberBottom"]',)), follow= True),  
            Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="s-productthumbbox"]',))
    , callback="parse_items", follow= True),)



  def parse_items(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//html")
    items = []
    for titles in titles:
      item = LonsdaleItem()
      item ["productname"] = titles.select("//span[@id='ProductName']/text()").extract()
      item ["MRP"] = titles.select("//div[@class='originalprice']/span/text()").extract()
      item ["SP"] = titles.select("//div[@class='saleprice']/span/span/text()").extract()      
      item ["sku"] = titles.select("//p[@class='productCode']/text()").extract()      
      item ["imgurl"] = titles.select("//div[@id='productImages']/div/div/div/a/@href").extract()
      item ["size"] = titles.select("//select[@id='sizeDdl']/option/text()").extract()
      
      item ["Description"] = titles.select("//span[@itemprop='description']").extract()
      
      
      item ["category"] = titles.select("//span[@id='dnn_dnnBreadcrumb_siteMap']/ol/li/a/text()").extract()
      
      
      
      items.append(item)
      return(items)





