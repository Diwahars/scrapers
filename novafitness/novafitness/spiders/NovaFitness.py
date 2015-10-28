from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from novafitness.items import BigCItem
import urlparse
import re
import csv

f = open("categories.csv")
csv_file = csv.reader(f)
novafitcat = []
LYScat = []

for row in csv_file:
  novafitcat.append(row[0])
  LYScat.append(row[1])

class MySpider(CrawlSpider):
  name = "novafitness"
  allowed_domains = ["novafitness.net"]
  
  start_urls = ["http://www.novafitness.net/motorized-treadmills.html"
                ]
  
 
  rules = (Rule (SgmlLinkExtractor(restrict_xpaths=('//ul/li[@class="actv1"]',))
  , callback="parse_items", follow= True),)


  csvfile = None
  printHeader = True
  def to_csv(self, item):
    if self.printHeader:
      self.csvfile = open('NovaFitness.csv','w')
    if self.csvfile:
      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='Item Type,Product Name,Brand Name,Product Description,Product Code/SKU,Bin Picking Number,'
        strWrite +='Category,Product Availability,Current Stock Level,Free Shipping,Sort Order, Meta Description,Page Title,Product Image Description - 1,Product Image Is Thumbnail - 1,'
        strWrite +='Track Inventory,Product Image Sort - 1,'
        strWrite +='Product Image File - 1,\n'
        self.printHeader = False
      #print basic product data
        
      for pname,sku,desc,image in zip(item ["Product_Name"],item["Product_Code"],item["Product_Description"],item["Product_Image_File1"]):          
        item["MetaDescription"] = "Get your hands on the " + pname+ ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
        item["TitleTag"] = "Buy the " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
        item["Product_Image_Description_1"] = "Buy " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
        #Product Code Extraction      
        item["Product_Code"] = "NOVAFIT"+sku
      
        strWrite += 'Product,'+pname.replace(",","") + ',' + item["Brand_Name"] + ','      
        strWrite += re.sub('<a.*?">',"",desc.replace(',',';').replace("\n","").replace("\r","")) + ',' + sku +  ','  + "NOVAFIT" +  ','    
        strWrite += item["Category"] + ',' + item["Product_Availability"] +','
        strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + ','+ item['MetaDescription'] + ',' + item['TitleTag'] + ','
        strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + "By Product" + ','
        strWrite += item["Product_Image_Sort_1"] + ','  
        #for Images'
        strWrite += image
        #loop for seconday images
        strWrite += "\n"
      self.csvfile.write(strWrite.encode('utf8'))
    
  #def parse(self, response):
  def parse_items(self, response):
      
      sel = Selector(response)
      item = BigCItem()     
      item ["Item_Type"] = "Product"
      item ["Brand_Name"] = "Novafit"
      item["Product_Availability"] = "8-13 Working Days"
      item["Current_Stock"] = "100"
      item ["Free_Shipping"] = "N"
      item ["Sort_Order"] = "-100"      
      item["Product_Image_Is_Thumbnail_1"] = "Y"      
      item["Product_Image_Sort_1"] = "1"
      item["Product_Image_Sort_2"] = "2"
      item["Product_Image_Sort_3"] = "3"
      item["Product_Image_Sort_4"] = "4"
      item["Product_Image_Sort_5"] = "5"
      #Product Name
      item["Product_Name"]  = sel.xpath("//h2[@class='h2_clr fl']/b/text()").extract()
      item["Product_Code"] = sel.xpath("//p[@class='pd7']/text()").extract()
      item["Product_Description"] = sel.xpath("//div[@class='fl w33']/div").extract()
      item["Product_Image_File1"] = sel.xpath("//div[@class='bo2 bc3 p_250']/span/a/@dataimg").extract()
      cat = sel.xpath("//div[@class='p7 j c1 ul1']/h1/text()").extract()[0]
      for i in range(len(novafitcat)):
        if novafitcat[i] == cat:
          item["Category"] = LYScat[i]
          break
      
      self.to_csv(item)
      return item

      
