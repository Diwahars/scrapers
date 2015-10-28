from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from fitindia.items import CraigslistSampleItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["scssports.in"]
  start_urls = ["http://scssports.in/index.php?route=product/category&path=60"] 
  rules = (Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="box-product-item"]',))
    , callback="parse_items", follow= True),)
    
  def parse_items(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//div[@id='content']")
    items = []
    for titles in titles:
      item = CraigslistSampleItem()
      item ["productname"] = titles.select("//div[@class='product-info']/div[@class='left']/div[@class='image']/a/@title").extract()
      item ["imgurl1"] = titles.select("//div[@class='product-info']/div[@class='left']/div[@class='image']/a/@href").extract()
      item ["imgurl2"] = titles.select("//div[@class='image-additional caruofredsel-additional']/a[1]/@href").extract()
      item ["imgurl3"] = titles.select("//div[@class='image-additional caruofredsel-additional']/a[2]/@href").extract()
      item ["MRP"] = titles.select("//div[@class='right']/div[@class='price']/span[@class='price-old']/text()").extract()
      item ["SP"] = titles.select("//div[@class='right']/div[@class='price']/span[@class='price-new']/text()").extract()
      item ["stock"] = titles.select("//div[@class='description']/text()[last()]").extract()
      item ["Specification"] = titles.select("//div[@class='tab-content']/ul/li/text()").extract()
      item ["Description"] = titles.select("//div[@class='tab-content']/p/text()").extract()
      item ["SubCategory"] = titles.select("//div[@class='breadcrumb']/a[3]/text()").extract()
      item ["Category"] = titles.select("//div[@class='breadcrumb']/a[2]/text()").extract()
      item ["Size"] = titles.select('//option[string-length(@value)!=0]/text()').extract()
      item ["SKU"] = titles.select("//div[@class='description']/span[contains(text(),'Product Code:')]/following-sibling::text()[1]").extract()
           
      items.append(item)
      return(items)


