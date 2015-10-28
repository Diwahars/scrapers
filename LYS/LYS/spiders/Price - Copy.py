from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from LYS.items import BigCItem
import urlparse 
from scrapy.http.request import Request
from scrapy.selector import Selector
import re
import json, csv

output1 = open("BlogImageUrls.csv","wb")
mywriter = csv.writer(output1)


class MySpider(CrawlSpider):
  name = "tesla"
  allowed_domains = ["blog.liveyoursport.com"]
  start_urls = ["http://blog.liveyoursport.com/2014/03/03/football-nutrition-eat/",
                ]
  
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="menu-menu1-container"]/ul/li',)), follow= True),
           Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="wp-pagenavi"]',)), follow= True),
            Rule (SgmlLinkExtractor(restrict_xpaths=('//h2[@class="entry-title"]',)), callback="parse_items", follow= True),)
           
  def parse_items(self, response):
##  def parse(self, response):
  
     
   sel = Selector(response)
   item = BigCItem()   
   pname = sel.xpath("//img/@src").extract()
   
   for i in pname:
     urllist =[]
     urllist.append(i)
     mywriter.writerow(urllist)

   
     
     

   
