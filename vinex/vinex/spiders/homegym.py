from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from vinex.items import VinexItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "homegym"
  allowed_domains = ["vinexshop.com"]
  start_urls = ["http://www.vinexshop.com/Product_Detail.php?CategoryId=227"]

  rules = (Rule (SgmlLinkExtractor(restrict_xpaths=('//td/a',))
    , callback="parse_items", follow= True),)
  
    
  def parse_items(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//html")
    items = []
    for titles in titles:
      item = VinexItem()
      item ["productname"] = titles.select("//span[@class='title1'][1]/text()").extract()
      item ["imgurl"] = titles.select("//div[@class='popups']/a/@href").extract()
      item ["MRP"] = titles.select("//td[@align='left']/span[@style='text-decoration:none']/text()").extract()
      item ["SP"] = titles.select("//td[@align='left']/b/text()").extract()
      item ["Description"] = titles.select("//span[@class='text1'][1]/text()").extract()
      item ["variant"] = titles.select('//td[@align="justify"]/text()').extract()
      item ["SKU"] = titles.select("//td[@width='15%'][2]/text()").extract()
           
      items.append(item)
      return(items)


