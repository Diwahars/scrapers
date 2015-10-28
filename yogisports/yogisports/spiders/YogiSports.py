from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from yogisports.items import BigCItem
import urlparse
import re
import csv

output = open("YogiSports.csv","wb")
mywriter = csv.writer(output)
output.write('Item Type,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Description,Product Code/SKU,Bin Picking Number,Current Stock Level,'
             'Category,Option Set,Product Availability,Free Shipping,Sort Order,Meta Description,Page Title,'
             'Product Image Description - 1,Product Image Is Thumbnail - 1,'
             'Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,Product Image Sort-8,Product Image Sort-9,'
             'Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7,Product Image File - 8,Product Image File - 9 \n')

class MySpider(CrawlSpider):
  name = "yogisports"
  allowed_domains = ["yogisports.com"]
  start_urls = ["http://www.yogisports.com/sports-wear--mens/men-shoes/"
                ]
  rules = (
         Rule (SgmlLinkExtractor(allow=(),
                          restrict_xpaths=('//div[@class="col-xs-3 col-sm-3"] | //div[@class="col-lg-6 mm-col"]/div/ul',))
  , follow= True),
  Rule (SgmlLinkExtractor(allow=(),
                          restrict_xpaths=('//div[@class="product-info clearfix"]',)),
               callback="parse_items" , follow= True),
  )
  
##  rules = (Rule (SgmlLinkExtractor(allow=(),
##                          restrict_xpaths=('//div[@class="col-lg-6 mm-col"]/div/ul',)),
##               callback="parse_items" , follow= True),  )
    
  def to_csv(self, item):
    
    tup = ("Product",item["Product_Name"],"",
           #item["Retail_Price"][0],item["Retail_Price"],item["Sale_Price"],
           item["Retail_Price"][0].replace("Rs",""),item["Retail_Price"][0].replace("Rs",""),item["Sale_Price"][0].replace("Rs",""),
           item["Product_Description"],"","YOGISPORTS",item["Current_Stock"],item["Category"],item["Product_Name"],"2-7 Working days","N","",
           item["MetaDescription"],item["TitleTag"],item["Product_Image_Description_1"],"Y","By Product",
           "1","2","3","4","5","6","7")
    obj = list(tup)
    
    for i in item["Product_Image_File1"]:
      obj.append(i)
    row = tuple(obj)
    mywriter.writerow(row)    

    for size in item["variants"]:
      varrow = ("SKU","[S]Size= "+size.replace("IND UK","UK").split("/")[0].split("-")[-1].replace("IND","UK"),"","","","","","","YOGISPORTS","100")
      mywriter.writerow(varrow)    

    
  def parse_items(self,response):
    
  #def parse(self,response):
    sel = Selector(response)
    hxs = HtmlXPathSelector(response)

    
    
    for product in response.xpath("//div[@class='product']"):
      item = BigCItem()
      p1 = product.xpath("div/div/span[@class='price-old']/text()").extract()
      if p1:
        item ["Retail_Price"] = product.xpath("div/div/span[@class='price-old']/text()").extract()
        item ["Sale_Price"] = product.xpath("div/div/span[@class='price-new']/text()").extract()
      else:
        item ["Retail_Price"] = product.xpath("div/div/span[@class='price-new']/text()").extract()
        item ["Sale_Price"] = ["",""]

      url = product.xpath("a/@href").extract()[0]
##      print url
      
      request = Request(url,callback=self.parse_productinfo) 
      request.meta["item"]  = item
      yield request
      
  def parse_productinfo(self,response):
    sel = Selector(response)
    item = response.meta['item']    
    pname = sel.xpath("//div[@class='display-mode']/ul/text()").extract()[0]
    item ["Product_Name"] =  pname 
    item["Option_Set"] = pname
    item["Product_Image_Description_1"] = "Buy "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["MetaDescription"] = "Get your hands on the "+pname +". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["TitleTag"] = "Buy the "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"    
    item["Current_Stock"] = "100"    
    item["Product_Image_File1"] = sel.xpath("//div[@class='zoomContainer']/div/div/img/@src").extract()   
    item["Product_Description"] = sel.xpath("//div[@id='prdtDescription']").extract()[0]
    
    item["Category"] = (sel.xpath("//div[@class='breadcrumbs']/ul/li[3]/a/text()").extract()[0]
                          + "/"
                               +sel.xpath("//div[@class='breadcrumbs']/ul/li[4]/a/text()").extract()[0])
  
    item["variants"] = sel.xpath("//select[@name='ctl00$PlaceHolderMain$ddlSize']/option/text()").extract()[1:]
    
    self.to_csv(item)
    return item
  
  


            
    
    
