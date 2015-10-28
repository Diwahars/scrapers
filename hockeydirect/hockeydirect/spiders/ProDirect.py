from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from hockeydirect.items import HockeyDirectItem
import urlparse 


class MySpider(CrawlSpider):
  name = "hockeydirect"
  allowed_domains = ["hockeydirect.com"]
  start_urls = ["http://www.hockeydirect.com/Catalogue/Hockey-Shoes/Asics-Hockey-Shoes",
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
"http://www.hockeydirect.com//Catalogue/Hockey-Sticks/Aratac-Hockey-Sticks/RAV-Hockey-Stick",]

  rules = (Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=('//div[@class="pagination"]',))
    , follow= True),
    Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=('//div[@class="ballDelils"]',)),
                 callback="parse_items" , follow= True),
    )

  csvfile = open('test.csv', 'w')
  printHeader = True
  def to_csv(self, item):
    if self.csvfile:
      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='Item Type,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Description,Product Code/SKU,'
        strWrite +='Category,Option Set,Product Availability,Current Stock Level,Free Shipping,Sort Order,Product Image Description - 1,Product Image Is Thumbnail - 1,'
        strWrite +='Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,'
        strWrite +='Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 , \n'
        self.printHeader = False
#-------CSV Printing-------------------------------------
      #print basic product data
      strWrite += 'Product,'+item["Product_Name"]+ "*," + item["Brand_Name"] + ','
      strWrite += item["Price"] + ','+ '.'.join(item["Retail_Price"]).replace("\n","").replace("\r","").replace("  ","") +  ',' + '.'.join(item["Sale_Price"]).replace("\n","").replace("\r","").replace("  ","") + ','
      strWrite += '.'.join(item["Product_Description"]).replace(",","").replace("\n","").replace("\r","") + ',' + item["Product_Code"] +  ','  

      #for Images
      strWrite += item["Category"] + ',' + item["Option_Set"] + ',' + item["Product_Availability"] +','
      strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + ','
      strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
      strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
      strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ','
      #strWrite += ','.join(item["Product_Image_File1"]) +  +'\n'

      for image in item["Product_Image_File1"] :
        strWrite += "http://www.hockeydirect.com" + image.replace("57x57.jpg","500x500.jpg") + ","

      strWrite += '\n'
#---------------------------------------VARIANTS------------------------------------------
      for sizes in item['size']:        
          if item['id1'] !="":
            for colors in item["color"]:
              strWrite += 'SKU,[S]Size= ' + sizes.split("Shoe")[-1].replace("Size","UK") + '; [S]' + item['id1'].extract()[0].replace("\n","").replace("\r","").replace("  ","") + "=" + colors + ',,,,,,' + item ["Product_Code"]+ "UK" + sizes.split("Size")[-1].replace('"',"") + colors + ',,,,,,,,,,,,,,,,\n'
          else:           
            strWrite += 'SKU,[S]Size= ' + sizes.split("Shoe")[-1].split("Hockey Stick Size ")[-1].replace("Size","UK") + ',,,,,,' + item ["Product_Code"]+"UK"+ sizes.split("Hockey Stick Size ")[-1].split("Size")[-1].replace(" ","") +',,,,,,,,,,,,,,,,\n'
     
      self.csvfile.write(strWrite.encode('utf8'))

#--BASIC PRODUCT DATA STARTS HERE--
  def parse_items(self,response):
  #def parse(self,response):

    sel = Selector(response)
    item = HockeyDirectItem()
    hxs = HtmlXPathSelector(response)
    
    item ["Item_Type"] = "Product"
    #Product Name   
    item ["Product_Name"] =  sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","")
    item["Option_Set"] = sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","")
    item["Product_Image_Description_1"] = "Buy " + sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","") + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    #Pricing
    item ["Retail_Price"] =  sel.xpath("//p[@class='fLeft']/span/text()").re(r'\d+')
    sp = response.xpath("//div[@class='price']/p/strong/text()").re(r'\d+')
    if sp:
      item ["Sale_Price"] = sel.xpath("//div[@class='price']/p/strong/text()").re(r'\d+')
    else:
      item ["Sale_Price"] = sel.xpath("//span[@class='NowPriceValue']/text()").re(r'\d+')
      
    item ["Price"] = ""               
    #brandName
    item["Brand_Name"]  = response.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","").split(" ")[0]
    #Product Code Extraction
    item ["Product_Code"] = response.xpath("//div[@class='proDetailsLeft']/h3/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","").split("Product code:")[-1]
    #Product Description
    item["Product_Description"] = sel.xpath("//div[@id='productDescription']/ul/li/text()").extract()
    #ImageFile
    item["Product_Image_File1"] = sel.xpath("//ul[@class='glyProduct']/li/span/img/@src").extract()
    #category
    sex = sel.xpath("//div[@class='proTop']/h2/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","").split(" Hockey")[0].split(" ")[-1]
    if sex =="Women":
      item["Category"] = "Team Sports/Hockey/" + sel.xpath("//ul[@class='braedcamp']/li[1]/a/text()").extract()[0].replace("Hockey Sticks","Sticks").replace("\n","").replace("\r","").replace("  ","") + ";Shoes/Women's Shoes/Hockey Shoes and Spikes"
    elif sex =="Ladies":
      item["Category"] = "Team Sports/Hockey/" +  sel.xpath("//ul[@class='braedcamp']/li[1]/a/text()").extract()[0].replace("Hockey Sticks","Sticks").replace("\n","").replace("\r","").replace("  ","") + ";Shoes/Women's Shoes/Hockey Shoes and Spikes"
    else:
      item["Category"] = "Team Sports/Hockey/" + sel.xpath("//ul[@class='braedcamp']/li[1]/a/text()").extract()[0].replace("Hockey Sticks","Sticks").replace("\n","").replace("\r","").replace("  ","") + ";Shoes/Men's Shoes/Hockey Shoes and Spikes"
      
    item["Product_Availability"] = "15-20 Working Days"
    item["Current_Stock"] = "100"
    item["Free_Shipping"] = "N"
    item["Sort_Order"] = "-250"
    item["Product_Image_Is_Thumbnail_1"] = "Y"
    item["Track_Inventory"] = "By Product"      
    item["Product_Image_Sort_1"] = "1"
    item["Product_Image_Sort_2"] = "2"
    item["Product_Image_Sort_3"] = "3"
    item["Product_Image_Sort_4"] = "4"
    item["Product_Image_Sort_5"] = "5"
    #Sizing info   
    item ["size"] = sel.xpath("//div[@class='proSlt'][1]/select/option/text()").extract()
    #Weight
    item ["color"] = sel.xpath("//div[@class='proSlt'][2]/select/option/text()").extract()
#--------Generating Variable for Second variant for creating conditions for variant printing----------
    id1 = sel.xpath("//div[@class='labeling'][2]/h4/text()")
    
    if id1:
      item['id1'] = id1
      self.to_csv(item)
      return item
    else:
      item['id1'] = ""
      self.to_csv(item)
      return item
      
    
  


            
    
    
