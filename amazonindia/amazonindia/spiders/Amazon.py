from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from amazonindia.items import AmazonindiaItem
import urlparse 
from scrapy.http.request import Request
from scrapy.selector import Selector


class MySpider(CrawlSpider):
  name = "price"
  allowed_domains = ["amazon.in"]
  
  start_urls = ["http://www.amazon.in/WD-Elements-Portable-External-Drive/dp/B008GS8LT0/ref=pd_rhf_dp_s_cp_3_G9P7?ie=UTF8&refRID=1TWXME8SQQDP6JGTQ8J3",
                "http://www.amazon.in/BAS-Vampire-Blaster-English-Cricket/dp/B00NTI4OOS"]
                

    
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//html")
    
    items = []
    for titles in titles:
      item = AmazonindiaItem()
      item ["productname"] = titles.select("//span[@id='productTitle']/text()").extract()
      item ["MRP"] = titles.select("//div[@id='price']/table/tr[1]/td[2]/text()").extract()
      item ["SP"] = titles.select("//div[@id='price']/table/tr[2]/td[2]/span[1]/text()").extract()
      item ["MarketplaceSP"] = titles.select("//div[@id='unqualifiedBuyBox']/div/div/span/text()").extract()
      item ["Stock"] = titles.select("//div[@id='availability']/span/text()").extract()
      item ["SKU"] = titles.select("//input[@id='tagActionCode']/@value").extract()      
      
      
      items.append(item)
      return(items)





