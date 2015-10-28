from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from LYS.itemsPrice import LYSPriceItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "price"
  allowed_domains = ["liveyoursport.com"]
  start_urls = ["http://www.liveyoursport.com/products/adidas-r-6-table-tennis-rubber"]

           
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//head")
    items = []
    for titles in titles:
      item = LYSPriceItem()
      item ["productname"] = titles.select("//h1[@style='text-transform: none;']/text()").extract()
      item ["MRP"] = titles.select("//span[@class='strikethrough-price'][1]/text()").extract()
      item ["SP"] = titles.select("//span[@class='selling-price']/text()").extract()      
      item ["SKU"] = titles.select("//div[@class='small-sub']/text()").extract()
      item ["URL"] = titles.select("//div[@class='fb-like']/@data-href").extract()
           
      items.append(item)
      return(items)


