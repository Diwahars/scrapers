from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from LYS.items import BigCItem
import urlparse 
from scrapy.http.request import Request
from scrapy.http import FormRequest
from scrapy import log
import json
import re


class mensrunning(CrawlSpider):
  name = "categorization1"
  allowed_domains = ["liveyoursport.com"
                     ]
  start_urls = ["http://www.liveyoursport.com/cricket-bats/"]

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//ul[@class="PagingList"]',)), follow= True),
           Rule (SgmlLinkExtractor(restrict_xpaths=('//ul[@class="ProductList "]',)), callback="parse_item", follow= True),)

  csvfile = None
  printHeader = True
  def to_csv(self, item):
    if self.printHeader:
      self.csvfile = open('LYSCategorization.csv','w')
    if self.csvfile:

      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='Item Type,Product Name,Product Description,Product Code/SKU,'
        strWrite +='Category'
        self.printHeader = False

      
        # generate product row
      strWrite += 'Product,'+item['Product_Name']+" "+','
      strWrite += '.'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","")+ ","
      strWrite += item["Product_Code"] + ','
      strWrite += item['Category']  + ',\n'

      self.csvfile.write(strWrite.encode('utf8'))

  def parse_item(self, response):
  #def parse(self, response):
    sel = Selector(response)
    
    item = BigCItem()
    pname =  response.xpath("//div[@class='ProductMain']/h1/text()").extract()
    
    item ["Product_Name"]  = response.xpath("//div[@class='ProductMain']/h1/text()").extract()[0].replace(',',';').replace("\n","").replace("\r","")
    item ["Product_Code"]  = sel.xpath("//span[@class='VariationProductSKU']/text()").extract()[0].replace(',',';').replace("\n","").replace("\r","")
    item ["Product_Description"] = sel.xpath("//span[@class='prod-descr']").extract()
    desc = sel.xpath("//span[@class='prod-descr']").extract()

    if any("English Willow" in s for s in desc) or any("English Willow" in s for s in pname) :
      item["Category"] = "Team Sports/Cricket/Cricket Bats;Team Sports/Cricket/Cricket Bats/English Willow Bats"
    elif any("Kashmir" in s for s in desc) or any("Kashnmir" in s for s in pname) :
      item["Category"] = "Team Sports/Cricket/Cricket Bats;Team Sports/Cricket/Cricket Bats/Kashmir Willow Bats"
    elif any("Junior" in s for s in desc) or any("Junior" in s for s in pname) and any("Bat" in s for s in pname) :
      item["Category"] = "Team Sports/Cricket/Cricket Bats;Team Sports/Cricket/Cricket Bats/Junior Cricket Bats"
    elif any("indoor" in s for s in desc) or any("futsal" in s for s in desc)or any("rubber sole" in s for s in desc)  and any("Shoes" in s for s in pname) :
      item["Category"] = "Team Sports/Football/Football Shoes;Team Sports/Football/Football Shoes/Indoor Football Shoes"
    else :
      item["Category"] = "NULL"
    
    self.to_csv(item)
    return item
