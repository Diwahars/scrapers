from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from bigc.items import BigCItem
import urlparse
import re 
import csv
import re

f = open("masterfile.csv")
csv_file = csv.reader(f)
skulist = []
sizelist = []
typelist = []
namelist = []
outofstock = []
idlist = []
binpicklist = []

for row in csv_file:
  skulist.append(row[4])
  sizelist.append(row[2])
  typelist.append(row[0])
  namelist.append(row[2])
  idlist.append(row[1])

class rbw(CrawlSpider):
  name = "racquetballwarehouse"
  allowed_domains = ["racquetballwarehouse.com"]
  start_urls = [
##    "http://www.racquetballwarehouse.com/descpage.html?PCODE=AGS5RB",
##                "http://www.racquetballwarehouse.com/descpage.html?PCODE=ASGUPC3",
                "http://www.racquetballwarehouse.com/RacquetballShoes.html"
                ]
  
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="product_thumbnail"]',))
    , callback="parse_items", follow= True),)
  

  csvfile = None
  printHeader = True
  def to_csv(self, item):
    start = 0
    end=0
    
    if self.printHeader:
      self.csvfile = open('racquetballwarehouse.csv','w')
    if self.csvfile:

      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='Item Type,Product ID,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Description,Product Code/SKU,Bin Picking Number,'
        strWrite +='Category,Option Set,Product Availability,Current Stock Level,Free Shipping,Sort Order, Meta Description,Page Title, Product Image Description - 1,Product Image Is Thumbnail - 1,'
        strWrite +='Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,'
        strWrite +='Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7, \n'
        self.printHeader = False

      pfound = 0 #counter to find product from master sheet. If 0 after the loop, product is a NEW product and not uploaded previously
      productid = 0 #Storing the Product ID value for the product row
      for i in range(len(namelist)): #Loop to go through all the Item Types in old file.
        if typelist[i] == "Product" and namelist[i] == (item["Product_Name"]+ '*'): #Comparing Product Names from old sheet and new scrapped 
          start = i # Counter to store index of found Product Name
          pfound = 1
          productid = idlist[i]
          for r in range(i+1,len(namelist)): #Loop to start at the Counter and Look for next occurance of Item Type = "Product"
            if typelist[r] == "Product" : 
              break   #Loop breaks for next occurance of Item Type = "Product" 
            else:
                end = end+1 #Counting the number of SKUS for each product from the OLD sheet  

      if pfound ==0:
      #print basic product data
        strWrite += 'Product,'+','+item["Product_Name"]+ '*,' + item["Brand_Name"] + ','
        strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item ["Sale_Price"] + ','
        strWrite += ';'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","") + ","
        #re.sub("<.*?>","", for replacing HTML tags

      
        strWrite += item["id1"] +  ',' + "RBW" +  ',' + item["Category"] + ',' + item["Option_Set"] + ',' + item["Product_Availability"] +','
        strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + "," + item['MetaDescription'] + ',' + item['TitleTag'] + ','
        strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
        strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
        strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ',6,7,' 
        #for Images
        strWrite += ','.join(item["Product_Image_File1"]).replace("&nw=55","") +','         
        strWrite += '\n'

        for variant,sku in zip(item["variants"],item["Product_Code"]):
          strWrite += 'SKU,'+',[S]Size= US ' + variant.replace("Size ","").replace("\n","").replace("\t","").replace("\r","").split("-")[0] + ',,,,,,' + sku +',"RBW",,,,100,,,,,,,,,,,\n'

      else:
        strWrite += 'Product,'+productid+','+item["Product_Name"]+ '*,' + item["Brand_Name"] + ','
        strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item ["Sale_Price"] + ','
        strWrite += ';'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","") + ","
        #re.sub("<.*?>","", for replacing HTML tags

      
        strWrite += item["id1"] +  ',' + "RBW" +  ',' + item["Category"] + ',' + item["Option_Set"] + ',' + item["Product_Availability"] +','
        strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + "," + item['MetaDescription'] + ',' + item['TitleTag'] + ','
        strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
        strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
        strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ',6,7,' 
        #for Images
        strWrite += ','.join(item["Product_Image_File1"]).replace("&nw=55","") +','         
        strWrite += '\n'
        
      #VARIANT PRINTING SECTION

        old_dict = {} #Dictionary to contain old SKUs and Sizes
        oldlen = 0
        for i in range(start+1,start+1+end): #Storing all list of SKUS in a new list. Will be used for comparing with the new list
          old_dict[0,oldlen]=skulist[i]
          old_dict[1,oldlen]= sizelist[i]
          old_dict[2,oldlen]= idlist[i]
          oldlen = oldlen+1
          
        new_dict = {} #Dictionary to contain new SKUs and Sizes
        c=0
        for variant,sku in zip(item["variants"],item["Product_Code"]):
          new_dict[0,c] = sku
          new_dict[1,c] = (variant.replace("Size ","").replace("\n","").replace("\t","").replace("\r","").split("-")[0])        
          c= c+1

        diff_dict = {} #Dict which contains older skus
        r=0
        for i in range(oldlen):
          found = 0
          for x in range(c):
            if old_dict[0,i] == new_dict[0,x]:            
              found = 1
              break
          if found ==0:
            diff_dict[0,r] = old_dict[0,i]
            diff_dict[1,r] = old_dict[1,i]
            diff_dict[2,r] = old_dict[2,i]
            r=r+1
            
        for variant,sku in zip(item["variants"],item["Product_Code"]):
          t=0
          for i in range(oldlen): # For Printing Product IDs for previously existing products
            if sku == old_dict[0,i]:
              strWrite += 'SKU,'+old_dict[2,i]+',[S]Size= US ' + variant.replace("Size ","").replace("\n","").replace("\t","").replace("\r","").split("-")[0] + ',,,,,,' + sku +',"RBW",,,,100,,,,,,,,,,,\n'
              t = 1
              break

          if t==0:# For SKUS which are new and hence will not have a product ID
            strWrite += 'SKU,'+',[S]Size= US ' + variant.replace("Size ","").replace("\n","").replace("\t","").replace("\r","").split("-")[0] + ',,,,,,' + sku +',"RBW",,,,100,,,,,,,,,,,\n'
        
        if diff_dict: #For Printing Out of Stock Data not in Scrapped Data but in the master sheet
          for i in range (r):
            strWrite += 'SKU,'+diff_dict[2,i]+','+diff_dict[1,i] +',,,,,,'+diff_dict[0,i] + ',' +'RBW,,,,0,,,,,,,,,,,\n' 
##        
      self.csvfile.write(strWrite.encode('utf8')) 
    
  def parse_items(self, response):
##  def parse(self, response):
      sel = Selector(response)
      item = BigCItem()     
      item ["Item_Type"] = "Product"
      #Product Name
      pname = sel.xpath("//div[@class='descname_price clearfix']/div/span/text()")
      item ["Product_Name"] = pname.extract()[0].split("Size")[0]
      item["MetaDescription"] = "Get your hands on the " + pname.extract()[0].split("Size")[0] + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["TitleTag"] = "Buy the " + pname.extract()[0].split("Size")[0] + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Product_Image_Description_1"] = "Buy " + pname.extract()[0].split("Size")[0] + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Option_Set"] = pname.extract()[0].split("Size")[0]

      
      mrp = response.xpath("//span[@class='was_price']/text()").extract()
      #Pricing
      if mrp:
        mrp =  float(response.xpath("//span[@class='was_price']/text()").extract()[0].split("$")[-1])
        sp= float(sel.xpath("//span[@class='now_price']/text()").extract()[0].split("$")[-1])
        print sp
        item ["Retail_Price"] = str((((63.5*mrp*103/100)*130/100*70/100)+2100)*114.5/100 + (63.5*mrp*103/100)*20/100)
        item ["Sale_Price"] = str((((63.5*sp*103/100)*130/100*70/100)+2100)*114.5/100 + (63.5*sp*103/100)*20/100)
        item ["Price"] = item ["Retail_Price"]
        
      else:
        mrp= float(sel.xpath("//span[@class='desc_price']/text()").extract()[0].split("$")[-1])
        item ["Retail_Price"] = str((((63.5*mrp*103/100)*130/100*70/100)+2100)*114.5/100 + (63.5*mrp*103/100)*20/100)
        item ["Price"] = item ["Retail_Price"]
        item ["Sale_Price"] = ""

      item ["Brand_Name"] = pname.extract()[0].replace("adidas","Adidas").split(" ")[0]
      #Product Code Extraction
      item["id1"] = sel.xpath("//div[@class='comment_button_wrap']/a/@href").extract()[0].split("?PCODE=")[-1]
      #Product Description
      item["Product_Description"] = sel.xpath("//div[@id='overview']/p").extract() +sel.xpath("//div[@id='overview']/ul").extract()
      
      #ImageFile
      item["Product_Image_File1"] = sel.xpath("//ul[@id='multiview']/li/a/img/@src").extract()

      #Other Constants
      cat = pname.extract()[0]
      if "Womens'" in cat or "Women's" in cat :      
        item ["Category"] = "Racket Sports/Squash/Squash Shoes; Racket Sports/Badminton/Badminton Shoes; Racket Sports/Table Tennis/Table Tennis Shoes; Team Sports/Volleyball/Volleyball Shoes; Shoes/Women's Shoes/Indoor Court Shoes"
      elif "Junior" in cat:
        item ["Category"] = "Racket Sports/Squash/Squash Shoes; Racket Sports/Badminton/Badminton Shoes; Racket Sports/Table Tennis/Table Tennis Shoes; Team Sports/Volleyball/Volleyball Shoes; Shoes/Women's Shoes/Indoor Court Shoes;Shoes/Women's Shoes/Indoor Court Shoes; Shoes/Junior Shoes/Indoor Court Shoes"
      else:
        item ["Category"] = "Racket Sports/Squash/Squash Shoes; Racket Sports/Badminton/Badminton Shoes; Racket Sports/Table Tennis/Table Tennis Shoes; Team Sports/Volleyball/Volleyball Shoes; Shoes/Men's Shoes/Indoor Court Shoes"
      
      item["Product_Availability"] = "12-17 Working Days"
      item["Current_Stock"] = "100"
      item ["Free_Shipping"] = "N"
      if item["Brand_Name"] in ("Asics","ASICS","Mizuno","Adidas"):
        item ["Sort_Order"] = "-300"
      else:
        item ["Sort_Order"] = "-250" 
      
      item["Product_Image_Is_Thumbnail_1"] = "Y"
      item["Track_Inventory"] = "By Option"      
      item["Product_Image_Sort_1"] = "1"
      item["Product_Image_Sort_2"] = "2"
      item["Product_Image_Sort_3"] = "3"
      item["Product_Image_Sort_4"] = "4"
      item["Product_Image_Sort_5"] = "5"
      #variant data        
      item ["variants"] = sel.xpath(".//select[@name='pcode']/option/text()").extract()[1:]
      item ["Product_Code"] = sel.xpath(".//select[@name='pcode']/option/@value").extract()[1:]
      self.to_csv(item)
      return item





    
    
