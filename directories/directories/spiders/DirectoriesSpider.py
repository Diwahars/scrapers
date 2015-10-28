from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from starkenn.items import StarkennItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["starkennbikes.com"]
  start_urls = ["http://www.starkennbikes.com/BikeDetails.aspx?id=594"]
  
  def parse(self, response):
   hxs = HtmlXPathSelector(response)
   titles = hxs.select("//head")
   items = []
   for titles in titles:
     item = StarkennItem()
     item ["productname"] = titles.select("//span[@class='PageHeaderText']/text()").extract()
     item ["MRP"] = titles.select("//span[@id='ctl00_ContentPlaceHolder1_lblPrice'][1]/text()").extract()
     item ["Stock"] = titles.select("//span[@id='ctl00_ContentPlaceHolder1_lblInStock']/text()").extract()
     item ["Size"] = titles.select("//span[@id='ctl00_ContentPlaceHolder1_lblSelectSize']/option/text()").extract()
     item ["SKU"] = titles.select("//span[@id='ctl00_ContentPlaceHolder1_lblCodeValue']/text()").extract()
     item ["Description1"] = titles.select("//span[@id='ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_lblOverView']/text()" and "//ul[id='ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_blFeatures]/li/text()").extract()
     item ["Description2"] = titles.select("//span[@itemprop='email']/text()").extract()
     item ["Description3"] = titles.select("//span[@itemprop='email']/text()").extract()
     item ["Specification"] = titles.select("//tr[@class='SpecContent']/tr/td/text()" and "//tr[@class='SpecContent']/td/span/text()").extract()
     
         
     items.append(item)
     return(items)
      
            

        
