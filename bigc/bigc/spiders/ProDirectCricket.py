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

class MySpider(CrawlSpider):
  name = "prodirectcricket"
  allowed_domains = ["prodirectcricket.com"]
  start_urls = [#"http://www.prodirectcricket.com/Products/GrayNicolls-Omega-XRD-Pro-Spike-Cricket-Shoes-White-Blue-Yellow-56033-92796.aspx",
                "http://www.prodirectcricket.com/lists/asics-cricket-shoes.aspx",
                "http://www.prodirectcricket.com/lists/gray-nicolls-cricket-shoes.aspx",
                "http://www.prodirectcricket.com/lists/kookaburra-cricket-shoes.aspx",
                "http://www.prodirectcricket.com/lists/cricket-shoes.aspx?brand=New%20Balance",
                "http://www.prodirectcricket.com/lists/cricket-shoes.aspx?brand=Gunn%20-and-%20Moore"
                ]
                
  
  #rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="bottom-section"]',))
   # , callback="parse_items", follow= True),)

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="list_productentity"]',)), callback="parse_items" , follow= True),)

  csvfile = None
  printHeader = True
  def to_csv(self, item):
    start = 0
    end=0
    
    if self.printHeader:
      self.csvfile = open('ProDirectCricket.csv','w')
    if self.csvfile:
      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='Item Type,Product ID,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Description,Product Code/SKU,Bin Picking Number,'
        strWrite +='Category,Option Set,Product Availability,Current Stock Level,Free Shipping,Sort Order, Meta Description,Page Title, Product Image Description - 1,Product Image Is Thumbnail - 1,'
        strWrite +='Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,'
        strWrite +='Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,Product Image Sort-8,'
        strWrite +='Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7, Product Image File - 8,\n'
        self.printHeader = False
        
      pfound = 0 #counter to find product from master sheet. If 0 after the loop, product is a NEW product and not uploaded previously
      productid = 0 #Storing the Product ID value for the product row
      
      for i in range(len(namelist)): #Loop to go through all the Item Types in old file.
        if typelist[i] == "Product" and skulist[i] == (item["Product_Code"]): #Comparing Product Names from old sheet and new scrapped 
          start = i # Counter to store index of found Product Name          
          pfound = 1
          productid = idlist[i]
          for r in range(i+1,len(namelist)): #Loop to start at the Counter and Look for next occurance of Item Type = "Product"
            if typelist[r] == "Product" : 
              break   #Loop breaks for next occurance of Item Type = "Product" 
            else:
                end = end+1 #Counting the number of SKUS for each product from the OLD sheet  

      if pfound ==0:
        #printing basic product data for NEW Products
        strWrite += 'Product,'+','+item["Product_Name"]+ ' Cricket Shoes*,' + item["Brand_Name"] + ','
        strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item ["Sale_Price"] + ','
        strWrite += ';'.join(item["Product_Description"]).replace(',',';').replace('<div class="BodyProdDesc">',"").replace("</div>","").replace("<h2>","").replace("</h2>","") + ',' + item["Product_Code"] +  ',' + "PRODIRECTCRICKET" +  ','        
        #for Images      
        strWrite += item["Category"] + ',' + item["Option_Set"] + ',' + item["Product_Availability"] +','
        strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + ',' + item['MetaDescription'] + ',' + item['TitleTag'] + ','
        strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
        strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
        strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ',6,7,'
        for image in item["Product_Image_File1"] :
          strWrite += "http://www.prodirectcricket.com" + image + ","
        strWrite += '\n'
        for sizes in item['variants']:
          strWrite += 'SKU,,[S]Size= UK ' + sizes.replace("ctl00_MainContent_chk","") + ',,,,,,' + item ["Product_Code"]+"UK"+sizes.replace("ctl00_MainContent_chk","") +',PRODIRECTCRICKET,,,,,,,,,,,,,,,\n'

      else:
        strWrite += 'Product,'+productid+','+item["Product_Name"]+ '*,' + item["Brand_Name"] + ','
        strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item ["Sale_Price"] + ','
        strWrite += ';'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","") + ","
        #re.sub("<.*?>","", for replacing HTML tags      
        strWrite += item["Product_Code"] +  ',' + "PRODIRECTCRICKET" +  ','+ item["Category"] + ',' + item["Option_Set"] + ',' + item["Product_Availability"] +','
        strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + "," + item['MetaDescription'] + ',' + item['TitleTag'] + ','
        strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
        strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
        strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ',6,7,' 
        #for Images
        for image in item["Product_Image_File1"] :
          strWrite += "http://www.prodirectcricket.com" + image + ","
        strWrite += '\n'          

        #VARIANT PRINTING SECTION
        old_dict = {} #Dictionary to contain old SKUs and Sizes
        oldlen = 0
        for i in range(start+1,start+1+end): #Storing all list of SKUS in a new list. Will be used for comparing with the new list
          
          old_dict[0,oldlen]= skulist[i] #SKU
          old_dict[1,oldlen]= sizelist[i].replace("[S]Size=UK ","") #Sizes
          old_dict[2,oldlen]= idlist[i] #ProductID
          oldlen = oldlen+1

        
        
        new_dict = {} #Dictionary to contain new SKUs and Sizes
        c=0
        for variant in item["variants"]:
          new_dict[0,c] = item ["Product_Code"]+"UK"+variant.replace("ctl00_MainContent_chk","")
          new_dict[1,c] = (variant.replace("ctl00_MainContent_chk","")) #Sizes into New Dict          
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
            
        for variant in (item["variants"]):
          t=0          
          for i in range(oldlen): # For Printing Product IDs for previously existing products            
            if (item ["Product_Code"]+"UK"+variant.replace("ctl00_MainContent_chk","")) == old_dict[0,i]:              
              strWrite += 'SKU,'+old_dict[2,i]+',[S]Size= UK ' +  variant.replace("ctl00_MainContent_chk","") + ',,,,,,' + item ["Product_Code"]+"UK"+variant.replace("ctl00_MainContent_chk","") +',PRODIRECTCRICKET,,,,100,,,,,,,,,,,\n' 
              t = 1
              break
            
          if t==0:# For products which are new and hence will not have a product ID
            strWrite += 'SKU,,[S]Size= UK ' + variant.replace("ctl00_MainContent_chk","") + ',,,,,,' + item ["Product_Code"]+"UK"+variant.replace("ctl00_MainContent_chk","") +',PRODIRECTCRICKET,,,,100,,,,,,,,,,,\n' 
            
        if diff_dict: #For Printing Out of Stock Data not in Scrapped Data but in the master sheet
          for i in range (r):
            strWrite += 'SKU,'+diff_dict[2,i]+',[S]Size=UK '+diff_dict[1,i] +',,,,,,'+diff_dict[0,i] + ',' +'PRODIRECTCRICKET,,,,0,,,,,,,,,,,\n' 

      self.csvfile.write(strWrite.encode('utf8'))


      
#--BASIC PRODUCT DATA STARTS HERE--
  def parse_items(self,response):
  #def parse(self,response):
    sel = Selector(response)
    item = BigCItem()
    hxs = HtmlXPathSelector(response)
    
    item ["Item_Type"] = "Product"
    #Product Name
    
    item ["Product_Name"] =  sel.xpath("//div[@class='BodyProdTitle']/h1/text()").extract()[0]
    item["MetaDescription"] = "Get your hands on the " + sel.xpath("//div[@class='BodyProdTitle']/h1/text()").extract()[0] + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["TitleTag"] = "Buy the " + sel.xpath("//div[@class='BodyProdTitle']/h1/text()").extract()[0] + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"

    #Pricing
    mrp = response.xpath("//div[@class='RrpPrice']/br")
    sp = response.xpath("//div[@class='OtherPriceInfo']/br")
    
    if mrp:
      item ["Retail_Price"] =  str((float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@class='OnlinePrice']/text()").extract()[0])[0]) * 95+ 2000)*115/100*110/100)
      item ["Sale_Price"] = ""
      item ["Price"] =  str((float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@class='OnlinePrice']/text()").extract()[0])[0]) * 95+ 2000)*115/100*110/100)
    else:
      item ["Retail_Price"] = str((float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//div[@class='RrpPrice']/text()").extract()[0])[0]) * 95+ 2000)*115/100*110/100)
      item ["Price"] = str((float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//div[@class='RrpPrice']/text()").extract()[0])[0]) * 95+ 2000)*115/100*110/100)
      if sp:
        item ["Sale_Price"] = str((float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@class='OnlinePrice']/text()").extract()[0])[0]) * 95+ 2000)*115/100*110/100)        
      else:
        item ["Sale_Price"] = str((float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//div[@class='OtherPriceInfo']/text()").extract()[0])[0]) * 95+ 2000)*115/100*110/100)
        
    #brandName
    brand = response.xpath("//div[@class='BodyProdTitle']/h1/text()").extract()[0].split(" ")[0]
    if brand == "New":
      item["Brand_Name"] = "New Balance"
    elif brand =="Gunn":
      item["Brand_Name"] = "Gunn and Moore"
    else:
      item["Brand_Name"] = response.xpath("//div[@class='BodyProdTitle']/h1/text()").extract()[0].split(" ")[0]


    #Product Code Extraction
    item ["Product_Code"] = response.xpath("//div[@style='color:#808080;text-align:right;font-size:9px;']/text()").extract()[0].split("Ref : ")[-1]
    
    #Product Description 
    
    
    item["Product_Description"] = sel.xpath("//div[@class='BodyProdDesc']").extract() 
    
    #ImageFile
    item["Product_Image_File1"] = sel.xpath("//div[@id='MainImages']/img/@src").extract()

    item["Category"] = "Team Sports/Cricket/Cricket Shoes and Spikes; Shoes/Men's Shoes/Cricket Shoes"
    item["Option_Set"] = sel.xpath("//div[@class='BodyProdTitle']/h1/text()").extract()[0]
    item["Product_Availability"] = "12-17 Working Days"
    item["Current_Stock"] = "100"
    item["Free_Shipping"] = "N"
    item["Sort_Order"] = "-300" 
    item["Product_Image_Description_1"] = "Buy " + sel.xpath("//div[@class='BodyProdTitle']/h1/text()").extract()[0] + " Cricket Shoes Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["Product_Image_Is_Thumbnail_1"] = "Y"
    item["Track_Inventory"] = "By Option"      
    item["Product_Image_Sort_1"] = "3"
    item["Product_Image_Sort_2"] = "2"
    item["Product_Image_Sort_3"] = "1"
    item["Product_Image_Sort_4"] = "4"
    item["Product_Image_Sort_5"] = "5"
    
    url = "http://www.prodirectcricket.com/Basket" + sel.xpath('//span[@class="But2"]/a/@href').extract()[0].split("Basket")[-1]

    request = Request(url,callback=self.parse_items2)
    request.meta["item"] = item    
    return request
    
 
#-------VARIANTS EXTRACTION-----------
  def parse_items2(self,response):
    sel = Selector(response)
    item = response.meta['item']
    item ["variants"] = sel.xpath("//div[@style='float:left;padding-top:5px;padding-bottom:10px;padding-right:9px;']/label/@for").extract()
    self.to_csv(item)    
    return item
  


            
    
    
