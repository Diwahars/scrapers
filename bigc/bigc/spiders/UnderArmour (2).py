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
import json

class UnderArmour(CrawlSpider):
  name = "underarmour1"
  allowed_domains = ["underarmour.com"]
  start_urls = [#"https://www.underarmour.com/en-us/mens/footwear/basketball-shoes",]
                #"https://www.underarmour.com/en-us/mens/apparel/tops/hoodies"]
                "https://www.underarmour.com/en-us/outlet/mens/tops"]
  
    
  
 # rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="grid-content"]',))
  #  , callback="parse_items", follow= True),)
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="next"]',)), follow= True),
   Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="bottom-section"]',))
    , callback="parse_items", follow= True),)
  
  csvfile = None
  printHeader = True
  def to_csv(self, item):
    if self.printHeader: 
      self.csvfile = open('UnderArmour.csv','w')
    if self.csvfile:
      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='Item Type,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Description,Product Code/SKU,'
        strWrite +='Category,Option Set,Product Availability,Current Stock Level,Free Shipping,Sort Order, Meta Description,Page Title, Product Image Description - 1,Product Image Is Thumbnail - 1,'
        strWrite +='Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,'
        strWrite +='Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 , \n'
        self.printHeader = False

      #print basic product data
      strWrite += 'Product,'+item["Product_Name"]+ ',' + item["Brand_Name"] + ','
      strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item ["Sale_Price"] + ','
      strWrite += ';'.join(item["Product_Description"]).replace(',',';').replace('\n',"").replace("</div>","").replace("<h2>","").replace("</h2>","") + ',' + item["Product_Code"] +  ','  

      #for Images
      
      
      strWrite += item["Category"] + ',' + ';'.join(item["Option_Set"]) + ',' + item["Product_Availability"] +','
      strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + ',' + item['MetaDescription'] + ',' + item['TitleTag'] + ','
      strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
      strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
      strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ','
      #strWrite += ','.join(item["Product_Image_File1"]) +  +'\n'

      strWrite += ';'.join(item["Product_Image_File1"]) + ','

      strWrite += '\n'

      #print variant
      for sizes in item['variants']:
        strWrite += 'SKU,[S]Size= US ' + sizes + ',,,,,,' + item["id1"]+ "-" + sizes + item["color"]+',,,,,,,,,,,,,,,,\n'

      self.csvfile.write(strWrite.encode('utf8'))

      
#--BASIC PRODUCT DATA STARTS HERE--
  def parse_items(self,response):
  #def parse(self,response):
    sel = Selector(response)
    item = BigCItem()
    
    
    item ["Item_Type"] = "Product"
    #Product Name    
    color = sel.xpath("//span[@class='current-color-selection']/span[2]/text()")
    pname = sel.xpath("//h1[@itemprop='name']/text()")
    item ["Product_Name"] =  pname.extract()[0] + " " + color.extract()[0]+"*"    
    item["MetaDescription"] = "Get your hands on the " + pname.extract()[0] + " " + color.extract()[0] + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["TitleTag"] = "Buy the " +  pname.extract()[0] + " " + color.extract()[0] + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"

    #Pricing
    mrp = response.xpath("//span[@class='buypanel_productprice--orig']/text()")    
    if mrp:
      item ["Retail_Price"] =  str(float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@class='buypanel_productprice--orig']/text()").extract()[0])[0]) * 65*131/100+700)
      item ["Sale_Price"] = str(float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@class='buypanel_productprice-value sale-price']/text()").extract()[0])[0]) * 65*131/100+700)
      item ["Price"] =  str(float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@class='buypanel_productprice--orig']/text()").extract()[0])[0]) * 65*131/100+700)
    else:
      item ["Retail_Price"] = str(float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@class='buypanel_productprice-value']/text()").extract()[0])[0]) * 65*131/100+700)
      item ["Price"] = str(float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@class='buypanel_productprice-value']/text()").extract()[0])[0]) * 65*131/100+700)
      item ["Sale_Price"] = ""
        
    #brandName
    item ["Brand_Name"] = "Under Armour"
    #Product Code Extraction
    id = response.xpath("//meta[@property='og:url']/@content").extract()
    for url in id:
      item ["Product_Code"] = url.split('id')[-1] + color.extract()[0]
      item["id1"] = url.split('id')[-1]
      item["color"] = color.extract()[0]
    
    #Product Description 
    #Product Description 
    desc1 = sel.xpath("//span[@itemprop='description']/text()")
    desc2 = sel.xpath("//div[@class='buypanel_productdescription is-collapsed']/ul")       
    item["Product_Description"] = desc1.extract() + desc2.extract()
    
    #ImageFile
    item["Product_Image_File1"] = [x.replace("a248.e.akamai.net/f/248/9086/10h/","").split('?')[0] for x in sel.xpath("//div[@class='buypanel_productcaroitem--mobile']/img/@src").extract()]

    #CATEGORY
    #cat= sel.xpath("//h1[@itemprop='name']/text()")
    #if  

    
    item["Category"] = "Shoes/Men's Shoes/Basketball Shoes; Team Sports/Basketball/Basketball Shoes"
#Other Constants
    item["Option_Set"] = sel.xpath("//h1[@itemprop='name']/text()").extract()    
    item["Product_Availability"] = "12-17 Working Days"
    item["Current_Stock"] = "100"
    item["Free_Shipping"] = "N"
    item["Sort_Order"] = "-300" 
    item["Product_Image_Description_1"] = "Buy " + sel.xpath("//h1[@itemprop='name']/text()").extract()[0] + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["Product_Image_Is_Thumbnail_1"] = "Y"
    item["Track_Inventory"] = "By Product"      
    item["Product_Image_Sort_1"] = "1"
    item["Product_Image_Sort_2"] = "2"
    item["Product_Image_Sort_3"] = "3"
    item["Product_Image_Sort_4"] = "4"
    item["Product_Image_Sort_5"] = "5"
    

    #---Sizes/Variants Start Here----
    item["variants"] = {}
    script                    = response.xpath("//script[contains(.,'JSON.parse')]").extract()[0]
    scriptJson                = script.split('JSON.parse(')[3].split('),')[0]
    scriptJsonDict            = json.loads(scriptJson)
    for x in scriptJsonDict['MATERIALS']:
      item["variants"][x['CODE']]                                     = {}
      item["variants"][x['CODE']]["sizes"]                            = {}
      item["variants"][x['CODE']]["colorCode"]                        = x['COLOR']['PRIMARY']['CODE']
      item["variants"][x['CODE']]["color"]                            = x['COLOR']['PRIMARY']['NAME']
      item["variants"][x['CODE']]["colorRGB"]                         = x['COLOR']['PRIMARY']['RGB']
      item["variants"][x['CODE']]["Retail_Price"]                     = x['PRICE']['ORIG']['MAX']
      item["variants"][x['CODE']]["Sale_Price"]                       = x['PRICE']['CURRENT']['MAX']
      item["variants"][x['CODE']]["image"]                            = []
      for c in x['ASSETS']:
        item["variants"][x['CODE']]["image"].append('https://origin-d4.scene7.com/is/image/Underarmour/'+c['NAME']+'?scl=2')
      
      for c in x['SIZES']:
        item["variants"][x['CODE']]["sizes"][c['CODE']]               = {}
        item["variants"][x['CODE']]["sizes"][c['CODE']]['inventory']  = c['INVENTORY']
        item["variants"][x['CODE']]["sizes"][c['CODE']]['name']       = c['NAME']
      
    self.to_csv(item);

    return item
