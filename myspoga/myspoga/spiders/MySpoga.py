import re
import csv
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from ..helpers import bigcommerce, mycsv



class MySpider(CrawlSpider):
  name = "myspoga"
  allowed_domains = ["myspoga.com"]
  start_urls = ["http://myspoga.com/index.php/sports-products/swimming-world/swimming-goggles/snorkel-for-scuba-diving.html",
                "http://myspoga.com/index.php/sports-products/cricket-world/cricket-store-best-bat/jjjonex-power-zone-kashmir-willow-bat.html"
##                "http://myspoga.com/index.php/sports-products.html"
                ]

  rules = (Rule (LinkExtractor(allow=(),restrict_xpaths=('//li[@class="submenu first"]',)), follow= True),
           Rule (LinkExtractor(allow=(),restrict_xpaths=('//div[@class="pages"]',)), follow= True),
           Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="category-products"]',)),callback="parse_items" , follow= True),
    )
 
  def parse_items(self, response):
    print 'XXXX'
  # def parse(self,response):
    
    sel = Selector(response)    
    product_dict = {}
    product_dict['Product Name'] = sel.xpath("//div[@class='product-name']/h1/text()").extract()[0].replace(",","")
    product_dict['Description'] = sel.xpath("//div[@class='product-collateral']/div/div/div[@class='std']").extract()    
    product_dict['Product Code/SKU'] = sel.xpath("//div[@class='no-display']/input/@value").extract()[0] + 'MSPG'
    product_dict['Bin Picking Number'] = 'MYSPOGA'    
    product_dict['Brand'] = ''    
    product_dict['Product Availability']  = '7-12 Working Days'
    product_dict['Sort Order'] = '-200'  
    product_dict["Images"] = sel.xpath("//div[@class='slideshow-box']/ul/li/a/@href").extract()   
    product_dict["Product_Description"] = sel.xpath("//div[@class='product-collateral']/div/div/div[@class='std']").extract()
    product_dict["Category"] = '/'.join(x for x in sel.xpath("//div[@class='breadcrumbs']/ul/li/a/text()").extract()[2:4])     
    product_dict['Track Inventory'] = 'By Product'

    try:      
      price_id = sel.xpath("//div[@class='no-display']/input/@value").extract()[0].strip()
      product_dict ["Price"] = sel.xpath("//span[@id='old-price-"+price_id+"']/text()").extract()[0].strip()
      product_dict ["Sale_Price"] = sel.xpath("//span[@id='product-price-"+price_id+"']/text()").extract()[0].strip()
    except:    
      product_dict ["Price"] = sel.xpath("//span[@id='product-price-"+price_id+"']/span/text()").extract()[0].strip()
      product_dict ["Sale_Price"] = ''

    stock = sel.xpath("//p[@class='availability in-stock']/span/text()").extract()
    if stock:
      product_dict["Current_Stock"] = "100"
    else:
      product_dict["Current_Stock"] = "0"     

    bigcommerce.product_row(product_dict)
    
    
