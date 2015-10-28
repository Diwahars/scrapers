from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from smcricket.items import BigCItem
import urlparse
import re

class MySpider(CrawlSpider):
  name = "smcricket"
  allowed_domains = ["smcricket.com"]
  
  start_urls = ["http://www.smcricket.com/product-gallery.php?gid=10&cid=13"]
  
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="accordion-content"]',)), follow= True),
  Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="prodThumb"]',))
  , callback="parse_items", follow= True),)

  csvfile = None
  printHeader = True
  def to_csv(self, item):
    if self.printHeader:
      self.csvfile = open('SmCricket.csv','w')
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
      strWrite += 'Product,'+item["Product_Name"] + "," + "SM Cricket" + ','
      strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item ["Sale_Price"] + ','
      strWrite += ';'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","").replace("div","p") + ',' + item["Product_Code"] +  ','  + "SMCRICKET" +  ','  

    
      strWrite += item["Category"] + ',' + item["Option_Set"] + ',' + item["Product_Availability"] +','
      strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + ','+ item['MetaDescription'] + ',' + item['TitleTag'] + ','
      strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
      strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
      strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ',6,7,' 
      #for Images'
      strWrite += item["Product_Image_File1"] + ',' ';'.join(item["Product_Image_File2"]).replace(',',';').replace("\n","").replace("\r","") + ','
      #loop for seconday images
      strWrite += "\n"
      self.csvfile.write(strWrite.encode('utf8'))

      
    
  def parse_items(self, response):
      sel = Selector(response)
      item = BigCItem()
      item ["Item_Type"] = "Product"
      #Product Name
      pname  = sel.xpath("//div[@class='insideRightContent']/h2/text()").extract()[0].replace(",","-")
      item ["Product_Name"] =  pname
      item["MetaDescription"] = "Get your hands on the " + pname + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["TitleTag"] = "Buy the " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Option_Set"] = pname
      cat= sel.xpath("//div[@class='wrap']/p/text()").extract()[0].split(">")[-2].replace(" ","")

      if cat =="EnglishWillow" or cat=="KashmirWillow" or cat=="KashmirWillow" or cat =="KashmirWillowJunior" or cat=="EnglishWillowJunior":
        item ["Category"] = "Team Sports/Cricket/Bats"
      elif cat =="LeatherBalls(AlumTanned)" or cat=="EnglishWillow" or cat=="LeatherBalls(VegetableTanned)":
        item ["Category"] = "Team Sports/Cricket/Balls"
      elif cat=="BattingLeg-Guards" or cat =="ThighGuards" or cat=="BattingLeg-Guards" or cat=="AbdominalGuards" or cat=="ElbowGuards" or cat=="ChestGuards" or cat=="WicketKeepingLeg-Guards":
        item ["Category"] = "Team Sports/Cricket/Pads and Guards"
      elif cat =="WicketKeepingGloves" or cat =="WicketKeepingInnerGloves" or cat =="BattingGloves" or cat=="IndoorBattingGloves" or cat=="IndoorWicketKeepingGloves":
        item ["Category"] = "Team Sports/Cricket/Gloves"
      elif cat == "Helmets":
        item ["Category"] = "Team Sports/Cricket/Helmets"
      elif cat== "KitBags" or cat=="CricketSet":
        item ["Category"] = "Team Sports/Cricket/Cricket Kits"
      else:
        item ["Category"] = "Team Sports/Cricket/Accessories"
        

      item ["Price"] = ""
      item ["Retail_Price"] = ""
      item ["Sale_Price"] = ""
      item ["Brand_Name"] = "SM Cricket"
      #Product Code Extraction
      code = response.xpath("//span[@style='color: rgb(249, 157, 28);']/strong/text()").extract()
      code1 = response.xpath("//strong[@style='color: rgb(249, 157, 28);']/text()").extract()
      if code:
        item["Product_Code"] = "SMCRICKET"+ response.xpath("//span[@style='color: rgb(249, 157, 28);']/strong/text()").extract()[0].split("Product Code:")[-1].replace("\n","").replace(',',';').replace("\n","").replace("\r","").replace(" ","")
      elif code1:
        item["Product_Code"] ="SMCRICKET"+ response.xpath("//strong[@style='color: rgb(249, 157, 28);']/text()").extract()[0].split("Product Code:")[-1].replace("\n","").replace(',',';').replace("\n","").replace("\r","").replace(" ","")
      else:
        item["Product_Code"] ="SMCRICKET"+ response.xpath("//div[@class='prodInsideImgs']/text()").extract()[0].split("Product Code:")[-1].replace("\n","").replace(',',';').replace("\n","").replace("\r","").replace(" ","")
        
        

      #Product Description 
      item["Product_Description"] = sel.xpath("//div[@class='insideRightContent']/div[2]").extract()
      
      #ImageFile
      item["Product_Image_File1"] = response.xpath("//div[@class='prodInsideImgs']/img/@src").extract()[0]
      item["Product_Image_File2"] = response.xpath("//div[@class='prodInsideImgs']/p/button/img/@src").extract()
      
      item["Product_Availability"] = "3-8 Working Days"
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
      self.to_csv(item)
      return item

