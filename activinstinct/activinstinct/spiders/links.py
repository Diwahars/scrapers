from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from activinstinct.items import ActivinstinctItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "links"
  allowed_domains = ["activinstinct.com"]
  start_urls = ["http://www.activinstinct.com/rugby/",
                "http://www.activinstinct.com/fitness/",
                "http://www.activinstinct.com/cricket/",
                "http://www.activinstinct.com/more-sports/football/", 

                ]             
                      
    
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//html")
    items = []
    for titles in titles:
      item = ActivinstinctItem()
      item ["productname"] = titles.select("//div[@class='menu']/div[@class='c']/ul/li/a/@href").extract()      
            
      
      items.append(item)
      return(items)





