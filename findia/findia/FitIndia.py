from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from findia.items import BigCItem
import urlparse
import re
import csv

f = open("categorization.csv")
csv_file = csv.reader(f)
fitindiacat = []
LYScat = []

for row in csv_file:
  fitindiacat.append(row[0])
  LYScat.append(row[1])

class MySpider(CrawlSpider):
  name = "fitindia"
  allowed_domains = ["fitindia.net"]
  
  start_urls = ["http://www.fitindia.net/fitness-equipment/treadmills/sole-f65-treadmill.html"
                ]
  
 
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//ul[@id="nav"]/li/ul/li/ul/li',)), follow= True),
           Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="pages"]',)), follow= True),
  Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="item-inner"]',))
  , callback="parse_items", follow= True),)

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//ul[@id="nav"]/li/ul',)), follow= True),
           Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="pages"]',)), follow= True),
  Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="item-inner"]',))
  , callback="parse_items", follow= True),)

  csvfile = None
  printHeader = True
  def to_csv(self, item):
    if self.printHeader:
      self.csvfile = open('FitIndia.csv','w')
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
      strWrite += ';'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","") + ',' + item["Product_Code"] +  ','  + "FITINDIA" +  ','  

    
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
  #def parse(self, response):
      sel = Selector(response)
      item = BigCItem()     
      item ["Item_Type"] = "Product"
      #Product Name
      pname  = sel.xpath("//div[@class='product-name']/h1/text()").extract()[0].replace(",","-")
      item ["Product_Name"] =  pname
      item["MetaDescription"] = "Get your hands on the " + pname + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["TitleTag"] = "Buy the " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Option_Set"] = pname
      
      mrp = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/p[@class='old-price']/span[@class='price']").extract()
      
      #Pricing
      if mrp:
        item ["Retail_Price"] = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/p[@class='old-price']/span[@class='price']/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
        item ["Sale_Price"] = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/p[@class='special-price']/span[@class='price']/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
        item ["Price"] = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/p[@class='old-price']/span[@class='price']/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
      else:
        item ["Price"] = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/span[@class='regular-price']/span/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
        item ["Retail_Price"] = response.xpath("//div[@class='product-shop span6']//div[@class='price-box'][1]/span[@class='regular-price']/span/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
        item ["Sale_Price"] = ""
        

      item ["Brand_Name"] = "Fit India"
    

      #Product Code Extraction
      
      item["Product_Code"] = "FITINDIA"+sel.xpath("//div[@class='product-sku']/span/text()").extract()[0]

      #Product Description 
      item["Product_Description"] = sel.xpath("//div[@class='std']").extract()
      
      #ImageFile
      img = response.xpath("//div[@class='more-views ma-more-img']/ul/li").extract()
      if img:
        item["Product_Image_File1"] = response.xpath("//div[@class='more-views ma-more-img']/ul/li/a/@href").extract()
      else:
        item["Product_Image_File1"] = sel.xpath("//ul/li[@class='thumbnail-item']/a/@href").extract()

      cat =sel.xpath("//div[@class='breadcrumbs']/ul/li[4]/a/text()").extract()
      if cat:
        item["Category"] = sel.xpath("//div[@class='breadcrumbs']/ul/li[4]/a/text()").extract()[0].replace(",","")
      else:
        item["Category"] = sel.xpath("//div[@class='breadcrumbs']/ul/li[3]/a/text()").extract()[0].replace(",","")
        
      size = len(LYScat)
      for i in range(size):
        if item["Category"] == fitindiacat[i]:          
           item["Category"] = LYScat[i]          
           break
           
      item["Product_Availability"] = "8-13 Working Days"
      item["Current_Stock"] = "100"
      item ["Free_Shipping"] = "N"
      item ["Sort_Order"] = "-250"      

      item["Product_Image_Description_1"] = "Buy " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Product_Image_Is_Thumbnail_1"] = "Y"
      item["Track_Inventory"] = "By Option"      
      item["Product_Image_Sort_1"] = "1"
      item["Product_Image_Sort_2"] = "2"
      item["Product_Image_Sort_3"] = "3"
      item["Product_Image_Sort_4"] = "4"
      item["Product_Image_Sort_5"] = "5"

##      yield item

      self.to_csv(item)
      return item
