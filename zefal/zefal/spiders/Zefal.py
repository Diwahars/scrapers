from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from zefal.items import BigCItem
import urlparse
from scrapy import log
import re
import csv

f = open("categories.csv")
csv_file = csv.reader(f)
zefalcat = []
LYScat = []

for row in csv_file:
  zefalcat.append(row[0])
  LYScat.append(row[1])

 
class MySpider(CrawlSpider):
  name = "zefal"
  allowed_domains = ["zefal.com"]
  start_urls = ["http://www.zefal.com/en/19-toe-clips-and-toe-straps"]

  rules = (
    Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//ul[@class="tree "]/li',)), follow= True),
    Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="cat_list_img"]',)), follow= True),
  Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="prod_list_img"]',))
  , callback="parse_items", follow= True),)
  
  csvfile = None
  printHeader = True
  def to_csv(self, item):
    if self.printHeader:
      self.csvfile = open('Zefal.csv','w')
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
      strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item ["Sale_Price"] + ','
      strWrite += ';'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","") + ',' + item["Product_Code"] +  ','  + "ZEFAL" +  ','      
      strWrite += item["Category"] + ',' + item["Option_Set"] + ',' + item["Product_Availability"] +','
      strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + ','+ item['MetaDescription'] + ',' + item['TitleTag'] + ','
      strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
      strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
      strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ',6,7,'
      #for Images'
      strWrite += ','.join(item["Product_Image_File1"]) + ','
      #loop for seconday images
      strWrite += "\n"
      self.csvfile.write(strWrite.encode('utf8'))

  def parse_items(self,response):
  #def parse(self,response):
      item = BigCItem()    
      sel = Selector(response)
            
      item ["Item_Type"] = "Product"
      #Product Name
      pname  = sel.xpath("//h3/text()").extract()[0]
      item ["Product_Name"] =  pname
      item["MetaDescription"] = "Get your hands on the " + pname + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["TitleTag"] = "Buy the " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Option_Set"] = pname
      
      
      item ["Retail_Price"] = ""
      item ["Price"] = ""
      item ["Sale_Price"] = ""
      #Product Code Extraction
      cat2 = response.xpath("//div[@class='breadcrumb']/a[2]/text()")
      if cat2:
        item ["Category"] = sel.xpath("//div[@class='breadcrumb']/a/text()").extract()[0] + "/" + sel.xpath("//div[@class='breadcrumb']/a/text()").extract()[1]
      else:
        item ["Category"] = sel.xpath("//div[@class='breadcrumb']/a/text()").extract()[0]

      for i in range(len(zefalcat)):
        if zefalcat[i] == item ["Category"]:
          item ["Category"] = LYScat[i]
        
      item["Product_Code"] = "ZEFAL"+sel.xpath("//span[@class='prod_ref']/text()").extract()[0].replace(" ","")
      item ["Brand_Name"] = "Zefal"

      #Product Description
      overview = sel.xpath("//div[@id='produc']").extract()
      features = sel.xpath("//div[@id='more_info_sheets']").extract() 
      item["Product_Description"] = overview+ features
      
      #ImageFile
      item["Product_Image_File1"] = response.xpath("//ul[@id='thumbs_list_frame']/li/a/@href").extract()      
      item["Product_Availability"] = "8-13 Working Days"      
      item["Current_Stock"] = "100"
      item ["Free_Shipping"] = "N"
      item ["Sort_Order"] = "-180"      
      item["Product_Image_Description_1"] = "Buy " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Product_Image_Is_Thumbnail_1"] = "Y"
      item["Track_Inventory"] = "By Product"
      item["Product_Image_Sort_1"] = "1"
      item["Product_Image_Sort_2"] = "2"
      item["Product_Image_Sort_3"] = "3"
      item["Product_Image_Sort_4"] = "4"
      item["Product_Image_Sort_5"] = "5"
      item["variant"]= ""
     

      self.to_csv(item)
      return item
