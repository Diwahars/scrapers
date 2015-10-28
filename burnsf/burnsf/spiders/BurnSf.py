from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from burnsf.items import BigCItem
import urlparse
import re
import csv
class MySpider(CrawlSpider):
  name = "burnsf"
  allowed_domains = ["burnsf.in"]
  
  start_urls = [#"http://www.burnsf.in/fitness-accessories/burn-12kg-dumbbell-set.html"]
    "http://www.burnsf.in/gym-equipments.html"]
  
## 
  rules = (
    Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="parentMenu"]',)), follow= True),
    Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="pages"]',)), follow= True),
  Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="product-block-inner"]',))
  , callback="parse_items", follow= True),)


  csvfile = None
  printHeader = True
  def to_csv(self, item):
    if self.printHeader:
      self.csvfile = open('Burnsf.csv','w')
    if self.csvfile:

      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='Item Type,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Description,Product Code/SKU,Bin Picking Number,'
        strWrite +='Category,Option Set,Product Availability,Current Stock Level,Free Shipping,Sort Order, Meta Description,Page Title,Product Image Description - 1,Product Image Is Thumbnail - 1,'
        strWrite +='Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,'
        strWrite +='Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7, \n'
        self.printHeader = False

      #print basic product data   
      strWrite += 'Product,'+item["Product_Name"]+ ',' + item["Brand_Name"] + ','
      strWrite +=  ''.join([i for i in item["Price"] if ord(i) < 128]).replace(',','') + ','+ ''.join([i for i in item["Price"] if ord(i) < 128]).replace(',','') +  ',' + item ["Sale_Price"] + ','
      strWrite += ';'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","") + ',' + item["Product_Code"] +  ','  + "BURNSF" +  ','  

    
      strWrite += item["Category"] + ',' + item["Option_Set"] + ',' + item["Product_Availability"] +','
      strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + ','+ item['MetaDescription'] + ',' + item['TitleTag'] + ','
      strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
      strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
      strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ',6,7,' 
      #for Images'
      strWrite += ';'.join(item["Product_Image_File1"]).replace(',',';').replace("\n","").replace("\r","") + ','
      #loop for seconday images
      strWrite += "\n"
      self.csvfile.write(strWrite.encode('utf8'))
    
  def parse_items(self, response):
##  def parse(self, response):
      sel = Selector(response)
      item = BigCItem()     
      item ["Item_Type"] = "Product"
      #Product Name
      pname  = sel.xpath("//div[@class='product-name']/h1/text()").extract()[0].replace(",","-")
      item ["Product_Name"] =  pname
      item["MetaDescription"] = "Get your hands on the " + pname + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["TitleTag"] = "Buy the " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Option_Set"] = pname
      
      item ["Retail_Price"] = ""
      item ["Price"] = response.xpath("//span/span[@class='price']/text()").extract()[0].replace("\x7F","")
      item ["Sale_Price"] = ""
      item ["Brand_Name"] = "Burn Fitness"
      #Product Code Extraction
      item["Product_Code"] = "BURNSF"+sel.xpath("//div[@class='sku']/text()").extract()[0]
      #Product Description 
      item["Product_Description"] = sel.xpath("//div[@class='std']").extract()      
      #ImageFile
      item["Product_Image_File1"] = response.xpath("//div[@class='product-block']/a/@href").extract()

      item["Category"] =response.url.split("/")[3]
        
      item["Product_Availability"] = "8-13 Working Days"
      stock = response.xpath("//p[@class='availability in-stock']/span/text()").extract()[0]
      if stock =="In stock":
        item["Current_Stock"] = "100"
      else:
        item["Current_Stock"] = "0"
      
      item ["Free_Shipping"] = "N"
      item ["Sort_Order"] = "-190"      

      item["Product_Image_Description_1"] = "Buy " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Product_Image_Is_Thumbnail_1"] = "Y"
      item["Track_Inventory"] = "By Product"      
      item["Product_Image_Sort_1"] = "1"
      item["Product_Image_Sort_2"] = "2"
      item["Product_Image_Sort_3"] = "3"
      item["Product_Image_Sort_4"] = "4"
      item["Product_Image_Sort_5"] = "5"

##      yield item

      self.to_csv(item)
      return item
