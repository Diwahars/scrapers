from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from underarmour.items import UnderArmourItem
import urlparse 
from scrapy.http.request import Request

class UnderArmour(CrawlSpider):
  name = "underarmour"
  allowed_domains = ["underarmour.com"]
  start_urls = ["https://www.underarmour.com/en-us/mens/footwear/basketball-shoes"]
  
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="bottom-section"]',))
    , callback="parse_items", follow= True),)
  #rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="tile-inner"]',))
  #    , callback="parse_items", follow= True),)

  csvfile = open('UnderArmour.csv', 'w')
  printHeader = True
  def to_csv(self, item):
    if self.printHeader:
      self.csvfile = open('ProDirectCricketShoes.csv','w')
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
      strWrite += ';'.join(item["Product_Description"]).replace(',',';') + ',' + item["Product_Code"] +  ','  

      #for Images
      strWrite += ';'.join(item["Product_Image_File1"]) + ','
      
      strWrite += item["Category"] + ',' + ';'.join(item["Option_Set"]) + ',' + item["Product_Availability"] +','
      strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + ','
      strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
      strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
      strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"]+',\n'

      #print variant
      for sizes in item['variants']:
        strWrite += 'SKU,[S]Size= US ' + sizes + ',,,,,,' + item["id1"]+ "-" + sizes + item["color"]+',,,,,,,,,,,,,,,,\n'

      self.csvfile.write(strWrite.encode('utf8'))

  def parse_items(self, response):

#--BASIC PRODUCT DATA STARTS HERE---
    sel = Selector(response)
    item = UnderArmourItem()
    hxs = HtmlXPathSelector(response)
    
    item ["Item_Type"] = "Product"
    #Product Name
    color = sel.xpath("//span[@class='current-color-selection']/span[2]/text()")
    pname = sel.xpath("//h1[@itemprop='name']/text()")
    item ["Product_Name"] =  pname.extract()[0] + " " + color.extract()[0]+"*"
    mrp = sel.xpath("//span[@class='buypanel_productprice--orig']/text()").extract()
    item ["Sale_Price"] = ''
    #Pricing
    if mrp:
      item ["Retail_Price"] = mrp[0].replace("$","") 
      item ["Sale_Price"] = sel.xpath("//span[@class='buypanel_productprice-value sale-price']/text()").extract()[0].replace("$","")
      item ["Price"] = mrp[0].replace("$","")
    else:
      item ["Retail_Price"] = sel.xpath("//span[@class='buypanel_productprice-value']/text()").extract()[0].replace("$","")
      item ["Price"] = sel.xpath("//span[@class='buypanel_productprice-value']/text()").extract()[0].replace("$","")
      
          
    item ["Brand_Name"] = "Under Armour"

    #Product Code Extraction
    id = response.xpath("//meta[@property='og:url']/@content").extract()
    for url in id:
      item ["Product_Code"] = url.split('id')[-1] + color.extract()[0]
      item["id1"] = url.split('id')[-1]
      item["color"] = color.extract()[0]

    #Product Description 
    desc1 = sel.xpath("//span[@itemprop='description']/text()")
    desc2 = sel.xpath("//div[@class='buypanel_productdescription is-collapsed']/ul")       
    item["Product_Description"] = desc1.extract() + desc2.extract()
    
    #ImageFile
    item["Product_Image_File1"] = [x.replace("a248.e.akamai.net/f/248/9086/10h/","").split('?')[0] for x in sel.xpath("//div[@class='buypanel_productcaroitem--mobile']/img/@src").extract()]

    #Other Constants
    item["Category"] = "Shoes/Men's Shoes/Basketball Shoes; Team Sports/Basketball/Basketball Shoes"
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
    item["variants"] = sel.xpath(".//li[@class='size-chip']/text()").extract()
    
    self.to_csv(item);

    return item
