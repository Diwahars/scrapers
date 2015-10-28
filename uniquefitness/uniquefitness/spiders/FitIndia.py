from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from uniquefitness.items import UniquefitnessItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["uniquegym.com"]
  start_urls = ["http://uniquegym.com/unique_power.html",
                "http://uniquegym.com/unique_strength.html",
                "http://uniquegym.com/unique_fit.html",
                "http://uniquegym.com/unique_acce.html",
                "http://uniquegym.com/unique_upl.html"]
     
  def parse(self, response):
   hxs = HtmlXPathSelector(response)  
   titles = hxs.select("//html")
   items = []
   
   
   for titles in titles:
    item = UniquefitnessItem()
    item["productname"] = titles.select('//a[@class="zoom"]/@title').extract()
    item["imgurl"] = titles.select('//a[@class="zoom"]/@href').extract()
    items.append(item)
     
    return(items)
