from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from kohinoorcycles.items import KohinoorcyclesItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["kohinoorsalesagency.com"]
  start_urls = ["http://kohinoorsalesagency.com/productac.aspx",
                "http://kohinoorsalesagency.com/product.aspx?proid=6",
                "http://kohinoorsalesagency.com/product.aspx?proid=5",
                "http://kohinoorsalesagency.com/product.aspx?proid=3",
                "http://kohinoorsalesagency.com/product.aspx?proid=4",
                "http://kohinoorsalesagency.com/product.aspx?proid=2",
                "http://kohinoorsalesagency.com/product.aspx?proid=1",
                ]

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="boxwrap"]',))
    , callback="parse_items", follow= True),)
    
  def parse_items(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//html")
    items = []
    for titles in titles:
      item = KohinoorcyclesItem()
      item ["productname"] = titles.select("//span[@id='ContentPlaceHolder3_lblname']/text()").extract()
      item ["category"] = titles.select("//span[@id='ContentPlaceHolder3_lblcat']/text()").extract()
      item ["MRP"] = titles.select("//span[@id='ContentPlaceHolder3_rs1']/text()").extract()      
      item ["specification"] = titles.select("//tbody").extract()
      item ["imgurl"] = titles.select("//div[@class='clearfix']/a/@href").extract()
      items.append(item)
      return(items)


