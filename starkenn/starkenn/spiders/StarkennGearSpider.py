from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from starkenn.items import BigCItem
import urlparse
from scrapy import log
import re
import csv

f = open("categories.csv")
csv_file = csv.reader(f)
starkenncat = []
LYScat = []

for row in csv_file:
  starkenncat.append(row[0])
  LYScat.append(row[1])

 
class MySpider(CrawlSpider):
  name = "starkenngear"
  allowed_domains = ["starkennbikes.com"]  
  start_urls = ["http://www.starkennbikes.com/GearsCategory.aspx"]
  
  csvfile = None
  printHeader = True
  def to_csv(self, item):
    if self.printHeader:
      self.csvfile = open('starkenngear.csv','w')
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
      strWrite += ';'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","") + ',' + item["Product_Code"] +  ','  + "STARKENN" +  ','      
      strWrite += item["Category"] + ',' + item["Option_Set"] + ',' + item["Product_Availability"] +','
      strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + ','+ item['MetaDescription'] + ',' + item['TitleTag'] + ','
      strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
      strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
      strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ',6,7,'
      #for Images'
      strWrite += "http://www.starkennbikes.com/"+ ';'.join(item["Product_Image_File1"]).replace(',',';').replace("\n","").replace("\r","") + ','
      #loop for seconday images
      strWrite += "\n"
      for size in item["variant"]:
        strWrite += "SKU,[S]Size= "+size +",,,,,,"+item["Product_Code"]+size.replace(" ","")+ ",STARKENN,,,,"+item["Current_Stock"] + "\n"        
      self.csvfile.write(strWrite.encode('utf8'))

  def parse(self,response):
    item = BigCItem()
    sel = Selector(response)
    url = sel.xpath("//td[@colspan='1']/a/@href").extract()
    for x in url:
      request = Request("http://www.starkennbikes.com/"+x,callback=self.parse_categories) #For Parsing Information if search keyword found
      request.meta["item"]  = item
      yield request
      
  def parse_categories(self,response):
    #item = response.meta['item']
    sel = Selector(response)
    #item["Category"] = ""
    url = sel.xpath("//table[@class='PageNormalTextSmall']/tr/td[@align='center']/a/@href").extract()        
    brand = sel.xpath("//td[@colspan='3']/span/text()").extract()    
    category = []
    size = len(brand)
    for i in range(size):
      category.append(sel.xpath("//span[@class='PageHeaderText']/text()").extract()[0])
    
    for x,name,cat in zip(url,brand,category):
      item = BigCItem()
      item["Category"] = cat
      
      for i in range(len(starkenncat)):
        if cat == starkenncat[i]:
          item["Category"] = LYScat[i]
          break
        else:
          item["Category"] = "NA-"+cat
      item["Brand_Name"] = name
      request = Request("http://www.starkennbikes.com/"+x,callback=self.parse_items) #For Parsing Information if search keyword found
      request.meta["item"]  = item
      yield request    
    
  #def parse_items(self, response):
  def parse_items(self, response):
      sel = Selector(response)
      item = response.meta['item']
      
      item ["Item_Type"] = "Product"
      #Product Name
      pname  = sel.xpath("//span[@id='ctl00_ContentPlaceHolder1_lblProductName']/font/text()").extract()
      if pname:
        pname = sel.xpath("//span[@id='ctl00_ContentPlaceHolder1_lblProductName']/font/text()").extract()[0].replace(",","-")
      else:
        pname = sel.xpath("//span[@id='ctl00_ContentPlaceHolder1_lblGearName']/font/text()").extract()[0].replace(",","-")
      item ["Product_Name"] =  pname
      item["MetaDescription"] = "Get your hands on the " + pname + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["TitleTag"] = "Buy the " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Option_Set"] = pname
      
      
      item ["Retail_Price"] = response.xpath("//span[@id='ctl00_ContentPlaceHolder1_lblPrice']/b/font/text()").extract()[0].replace(",","").replace("Rs.","").replace(" /-","")
      item ["Price"] = response.xpath("//span[@id='ctl00_ContentPlaceHolder1_lblPrice']/b/font/text()").extract()[0].replace(",","").replace("Rs.","").replace(" /-","")
      item ["Sale_Price"] = ""

      #Product Code Extraction
     
      item["Product_Code"] = "STARKENN"+sel.xpath("//span[@id='ctl00_ContentPlaceHolder1_lblCodeValue']/text()").extract()[0]

      #Product Description
      overview = sel.xpath("//span[@id='ctl00_ContentPlaceHolder1_TabContainer1_TabPanel1_lblOverView']").extract()
      features = sel.xpath("//ul[@id='ctl00_ContentPlaceHolder1_TabContainer1_TabPanel2_blFeatures']").extract() 
      spec1 = sel.xpath("//table[@class='PageNormalTextSmall'][2]").extract()
      spec2 = sel.xpath("//tr[@class='SpecificationAlternate']").extract()
      frame = sel.xpath("//table[@id='ctl00_ContentPlaceHolder1_TabContainer1_TabPanel4_dgGeometry']").extract()
      
      
      item["Product_Description"] = overview+ features+ spec1 + frame
      
      #ImageFile
      item["Product_Image_File1"] = response.xpath("//td[@align='center']/a/img/@src").extract()
      
      item["Product_Availability"] = "8-13 Working Days"
      
      item["Current_Stock"] = "100"
      
      stock = sel.xpath("//span[@id='ctl00_ContentPlaceHolder1_lblInStock']/font/text()").extract()[0]
      
      if stock =="In Stock":
        item["Current_Stock"] = "100"
      else:
        item["Current_Stock"] = "0"
      item ["Free_Shipping"] = "N"
      item ["Sort_Order"] = "-250"      

      item["Product_Image_Description_1"] = "Buy " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Product_Image_Is_Thumbnail_1"] = "Y"
      
      item["Product_Image_Sort_1"] = "1"
      item["Product_Image_Sort_2"] = "2"
      item["Product_Image_Sort_3"] = "3"
      item["Product_Image_Sort_4"] = "4"
      item["Product_Image_Sort_5"] = "5"
      item["variant"]= ""
      
      item["variant"]= response.xpath("//select/option/text()").extract()[1:]
      if item["variant"]:
        item["Track_Inventory"] = "By Option"
      else:
        item["Track_Inventory"] = "By Product"      

      self.to_csv(item)
      return item
