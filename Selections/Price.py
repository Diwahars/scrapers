from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from fitindia.priceitems import priceitem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "price"
  allowed_domains = ["scssports.in"]
  start_urls = ["http://scssports.in/index.php?route=product/category&path=60"] 
     

  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//head")
    items = []
    for titles in titles:
      item = priceitem()
      item ["productname"] = titles.select("//div[@class='product-info']/div[@class='left']/div[@class='image']/a/@title").extract()
      item ["MRP"] = titles.select("//div[@class='right']/div[@class='price']/span[@class='price-old']/text()").extract()
      item ["SP"] = titles.select("//div[@class='right']/div[@class='price']/span[@class='price-new']/text()").extract()
      item ["stock"] = titles.select("//div[@class='description']/text()[last()]").extract()
      item ["SKU"] = titles.select("//div[@class='description']/span[contains(text(),'Product Code:')]/following-sibling::text()[1]").extract()     
      items.append(item)
      return(items)


