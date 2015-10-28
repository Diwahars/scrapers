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

new_dict={}
c=0

class MySpider(CrawlSpider):
  name = "hockeydirect"
  allowed_domains = ["hockeydirect.com"]
  start_urls = [
    
    "http://www.hockeydirect.com/Catalogue/Hockey-Shoes/Hockey-Shoe-Sale/Grays-G-9000-Hockey-Shoe-226020#.VP7bcPzLdM4",
                "http://www.hockeydirect.com/Catalogue/Hockey-Sticks/Grays-Hockey-Sticks/GX-Jumbow-Hockey-Sticks/Grays-GX-8000-Jumbow-Hockey-Stick-221279#.VP_M7fzLdM4",
                "http://www.hockeydirect.com/Catalogue/Hockey-Shoes/Dita-Hockey-Shoes/Dita-Escapist-Hockey-Shoe-356034#.VP_QEfzLdM4",
                "http://www.hockeydirect.com/Catalogue/Hockey-Shoes/Asics-Hockey-Shoes/Asics-Typhoon-2-Women-Hockey-Shoe-826261",
                "http://www.hockeydirect.com/Catalogue/Hockey-Shoes/Hockey-Shoe-Sale/Asics-Gel-Lethal-MP-5-Hockey-Shoe-826246",
                
                "http://www.hockeydirect.com/Catalogue/Hockey-Shoes/Asics-Hockey-Shoes",
                "http://www.hockeydirect.com/catalogue/department.aspx?node_id=0edeee59-4198-41e3-ba49-9c8200b110b9&pagesize=50",
                "http://www.hockeydirect.com/Catalogue/Hockey-Shoes/Kookaburra-Hockey-Shoes",
                "http://www.hockeydirect.com/Catalogue/Hockey-Shoes/Dita-Hockey-Shoes",
                "http://www.hockeydirect.com/Catalogue/Hockey-Shoes/Gryphon-Hockey-Shoes",
                "http://www.hockeydirect.com/Catalogue/Hockey-Stick-For-Sale/Hockey-Shoe-Clearance",
                #sticks
                "http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Mercian-Hockey-Sticks/Pro-Line-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Mercian-Hockey-Sticks/100---Series-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Mercian-Hockey-Sticks/200---Series-Hockey-Stick",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Mercian-Hockey-Sticks/Goalkeeping-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Mercian-Hockey-Sticks/Indoor-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Voodoo-Hockey-Sticks/Regular-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Voodoo-Hockey-Sticks/Yellow-Pack-Hockey-Stick",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Voodoo-Hockey-Sticks/V3-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Voodoo-Hockey-Sticks/Blue-Crisp-Hockey-sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Voodoo-Hockey-Sticks/Attack-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Kookaburra-Hockey-Sticks/Team-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Voodoo-Hockey-Sticks/Junior-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Kookaburra-Hockey-Sticks/L-Bow-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Kookaburra-Hockey-Sticks/M-Bow-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Kookaburra-Hockey-Sticks/I-Bow-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Kookaburra-Hockey-Sticks/Street-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Kookaburra-Hockey-Sticks/Junior-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Grays-Hockey-Sticks/GR-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Kookaburra-Hockey-Sticks/Kookaburra-Indoor-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Kookaburra-Hockey-Sticks/Wooden-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Kookaburra-Hockey-Sticks/Goalkeeping-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Gryphon-Hockey-Sticks/Your-Hockey-Stick",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Grays-Hockey-Sticks/Nano-Hockey-Sticks-2",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Grays-Hockey-Sticks/GX-Jumbow-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Grays-Hockey-Sticks/GX-Dynabow-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Grays-Hockey-Sticks/GX-Scoop-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Grays-Hockey-Sticks/GX-Mid-Bow-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Grays-Hockey-Sticks/GX-Composite-Hockey-Sticks-2",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Grays-Hockey-Sticks/Junior-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Grays-Hockey-Sticks/Wooden-Hockey-Sticks-2",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Grays-Hockey-Sticks/Indoor-Hockey-Sticks-2",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Byte-Hockey-Sticks/X-Series-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Gryphon-Hockey-Sticks/Taboo-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Gryphon-Hockey-Sticks/Chrome-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Gryphon-Hockey-Sticks/Essential-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Grays-Hockey-Sticks/Goalkeeping-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Byte-Hockey-Sticks/M-Series-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/TK-Hockey-Sticks/Platinum-Series-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Gryphon-Hockey-Sticks/Initiation-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Gryphon-Hockey-Sticks/Indoor-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/TK-Hockey-Sticks/Synergy-Series-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/TK-Hockey-Sticks/Trilium-Series-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/TK-Hockey-Sticks/Freedom-Series-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/TK-Hockey-Sticks/Goalkeeping-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/TK-Hockey-Sticks/Indoor-Wood-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/TK-Hockey-Sticks/Junior-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Gryphon-Hockey-Sticks/Gryphon-Goalkeeping-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Dita-Hockey-Sticks/EXA-Range",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Dita-Hockey-Sticks/Dita-Terra-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Dita-Hockey-Sticks/Giga-Composite-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Dita-Hockey-Sticks/Mega-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Dita-Hockey-Sticks/Rebl-Composite-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Dita-Hockey-Sticks/FXR-Range-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Dita-Hockey-Sticks/Junior-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Dita-Hockey-Sticks/Indoor-Hockey-sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Aratac-Hockey-Sticks/NRT-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Aratac-Hockey-Sticks/LBT-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Aratac-Hockey-Sticks/RSS-Hockey-Sticks",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Aratac-Hockey-Sticks/TRX-Hockey-Stick",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Aratac-Hockey-Sticks/FLUO-2-Hockey-stick",
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Aratac-Hockey-Sticks/RAV-Hockey-Stick",
  ]

  rules = (Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=('//div[@class="pagination"]',))
    , follow= True),
    Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=('//div[@class="ballDelils"]',)),
                 callback="parse_items" , follow= True),
    )
  csvfile = None
  printHeader = True

  def to_csv(self, item):
    start =0
    end =0
    if self.printHeader:
      self.csvfile = open('HockeyDirect.csv','w')
    if self.csvfile:
      strWrite = ''      
      if self.printHeader: 
        strWrite +='Item Type,Product ID,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Description,Product Code/SKU,Bin Picking Number,'
        strWrite +='Category,Option Set,Product Availability,Current Stock Level,Free Shipping,Sort Order,Meta Description,Page Title,Product Image Description - 1,Product Image Is Thumbnail - 1,'
        strWrite +='Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,Product Image Sort-8,'
        strWrite +='Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7,Product Image File - 8 \n'
        self.printHeader = False

      pfound = 0 #counter to find product from master sheet. If 0 after the loop, product is a NEW product and not uploaded previously
      productid = 0 #Storing the Product ID value for the product row
      
      for i in range(len(namelist)): #Loop to go through all the Item Types in old file.
        if typelist[i] == "Product" and skulist[i] == (item["Product_Code"]+"HKD"): #Comparing Product Names from old sheet and new scrapped 
          start = i # Counter to store index of found Product Name          
          pfound = 1
          productid = idlist[i]
          for r in range(i+1,len(namelist)): #Loop to start at the Counter and Look for next occurance of Item Type = "Product"
            if typelist[r] == "Product" : 
              break   #Loop breaks for next occurance of Item Type = "Product" 
            else:
                end = end+1 #Counting the number of SKUS for each product from the OLD sheet  

      #print basic product data
      if pfound == 0:
        strWrite += 'Product,,'+item["Product_Name"]+ "*," + item["Brand_Name"] + ','
        strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item["Sale_Price"] + ','
        strWrite += '.'.join(item["Product_Description"]).replace(",","").replace("\n","").replace("\r","") + ',' + item["Product_Code"]  +  'HKD,'+ "HOCKEYDIRECT,"
        strWrite += item["Category"] + ',' + item["Option_Set"] + '6,' + "12-17 Working Days,100,N,"
        strWrite += item["Sort_Order"] + ',' + item["MetaDescription"] + "," + item["TitleTag"] + ","
        strWrite += item["Product_Image_Description_1"] + ',Y,By Option'+','
        strWrite += "1,2,3,4,5,"
        for image in item["Product_Image_File1"] :
          strWrite += "http://www.hockeydirect.com" + image.replace("57x57.jpg","500x500.jpg") + ","
        strWrite += '\n'
      else:
        strWrite += 'Product,'+productid+","+item["Product_Name"]+ "*," + item["Brand_Name"] + ','
        strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item["Sale_Price"] + ','
        strWrite += '.'.join(item["Product_Description"]).replace(",","").replace("\n","").replace("\r","") + ',' + item["Product_Code"]  +  'HKD,'+ "HOCKEYDIRECT,"
        strWrite += item["Category"] + ',' + item["Option_Set"] + '5,' + "12-17 Working Days,100,N," 
        strWrite += item["Sort_Order"] + ',' + item["MetaDescription"] + "," + item["TitleTag"] + ","
        strWrite += item["Product_Image_Description_1"] + ',Y,By Option'+','
        strWrite += "1,2,3,4,5,6,7,8,"
        for image in item["Product_Image_File1"] :
          strWrite += "http://www.hockeydirect.com" + image.replace("57x57.jpg","500x500.jpg") + ","
        strWrite += '\n'
      m=0
      if "Colour" in item["color"]:
        c=0          
        for size in  item["size"]:
          if "Gryphon" not in item["Brand_Name"]:
            new_dict[0,c]= "[S]Size=UK "+size
            new_dict[2,c]= item ["Product_Code"]+"UK"+size + "X"
            c=c+1
          else:
            new_dict[0,c]= "[S]Size=EU "+size
            new_dict[2,c]= item ["Product_Code"]+"UK"+size + "X"
            c=c+1
            
      elif "Weight" in item["color"]:
        c=0
        m=1
        for size in item["size"]:
          for w in item["id1"]:
            new_dict[0,c]= "[S]Size= "+size
            new_dict[1,c]= "[RB]Weight= "+w
            new_dict[2,c]= item ["Product_Code"]+size+w + "X"
            c=c+1
      else: #for third case where product name is in drop down
        c=0        
        for size in item["size"]:            
            new_dict[0,c]= "[S]Size= "+size.split("Hockey")[-1].replace("Shoe Size","UK ").replace("Stick Size","").replace(" ","").replace("UK","UK ")
            new_dict[2,c]= item ["Product_Code"]+size + "X"
            c=c+1
            
      for i in range(c):       
        if m==1:
          strWrite += "SKU,,"+new_dict[0,i]+";"+new_dict[1,i]+",,,,,,"+new_dict[2,i]+",HOCKEYDIRECT,,,,100"
          strWrite += '\n'
        else:          
          strWrite += "SKU,,"+new_dict[0,i]+",,,,,,"+new_dict[2,i]+",HOCKEYDIRECT,,,,100"
          strWrite += '\n'

      self.csvfile.write(strWrite.encode('utf8'))

#--BASIC PRODUCT DATA STARTS HERE--
  def parse_items(self,response):
  #def parse(self,response):

    sel = Selector(response)
    item = BigCItem()
    hxs = HtmlXPathSelector(response)
    
    item ["Item_Type"] = "Product"
    #Product Name
    
    colour = response.xpath("//div[@class='labeling'][2]/h4/text()").extract()
    if colour:
      if "Colour" in colour[0]:
        item["Product_Name"] = (sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","")
                                + " "+sel.xpath("//div[@class='proSltWrap'][2]/div/select/option/text()").extract()[0])
      else:
        item["Product_Name"] = sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","")
    else:
      item["Product_Name"] = sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","")
      
    item["Option_Set"] = sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","")
    item["Product_Image_Description_1"] = "Buy " + sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","") + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["MetaDescription"] = "Get your hands on the " + sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","") + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["TitleTag"] = "Buy the " + sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","") + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    #Pricing
    item ["Retail_Price"] =  str(105.5/100*(float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//p[@class='fLeft']/span/text()").extract()[0])[0]) * 97*123/100 + 2300))
    item ["Price"] =  str(105.5/100*(float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//p[@class='fLeft']/span/text()").extract()[0])[0]) * 97*123/100 + 2300))
    sp = response.xpath("//div[@class='price']/p/strong/text()").re(r'\d+')
    if sp:
      item ["Sale_Price"] = str(105.5/100*(float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//div[@class='price']/p/strong/text()").extract()[0])[0]) *  97*123/100 + 2300))
    else:
      item ["Sale_Price"] = str(105.5/100*(float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@class='NowPriceValue']/text()").extract()[0])[0]) * 97*123/100 + 2300))
    sex = sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","").split(" Hockey")[0].split(" ")[-1]    
   
    if "Women" in item["Product_Name"] or "Ladies" in item["Product_Name"] :
      item["Category"] = "Team Sports/Hockey/Hockey Shoes;Shoes/Women's Shoes/Hockey Shoes and Spikes"
    elif "Junior" in item["Product_Name"] :
      item["Category"] = "Team Sports/Hockey/Hockey Shoes;Shoes/Women's Shoes/Hockey Shoes and Spikes"      
    else:
      item["Category"] = "Team Sports/Hockey/Hockey Shoes;Shoes/Men's Shoes/Hockey Shoes and Spikes"

    x = sel.xpath("//ul[@class='braedcamp']/li[1]/a/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","")
    if x =="Hockey Sticks":
      item["Category"] = "Team Sports/Hockey/Sticks"    
    item["Brand_Name"]  = response.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","").split(" ")[0]
    item ["Product_Code"] = response.xpath("//div[@class='proDetailsLeft']/h3/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","").split("Product code:")[-1]    
    item["Product_Description"] = sel.xpath("//div[@id='productDescription']/ul/li").extract()
    item["Product_Image_File1"] = sel.xpath("//ul[@class='glyProduct']/li/span/img/@src").extract()
    
    if "Adidas" or "Asics" or "Grays" in item["Brand_Name"]:
      item["Sort_Order"] = "-300"
    else:
      item["Sort_Order"] = "-270"
    #Sizing info
    color = response.xpath("//div[@class='labeling'][2]/h4/text()").extract()
    if color:
      item["color"] = response.xpath("//div[@class='labeling'][2]/h4/text()").extract()[0]
    else:
      item["color"] = ""
      
    item["size"] = sel.xpath("//div[@class='proSlt'][1]/select/option/text()").extract()
    item["id1"] = sel.xpath("//div[@class='proSlt'][2]/select/option/text()").extract()      
    
    if "Running" not in item["Product_Name"]:
      self.to_csv(item)
      return item
      
    
  


            
    
    
