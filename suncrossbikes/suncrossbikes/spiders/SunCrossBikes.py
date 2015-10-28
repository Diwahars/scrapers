from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from suncrossbikes.items import BigCItem
import urlparse
import re

class MySpider(CrawlSpider):
  name = "suncross"
  allowed_domains = ["suncrossbikes.com"]
  
  start_urls = ["http://suncrossbikes.com/bike_detail.php?bikeId=154&BikeCatId=2&Brands=12",]
                #"suncrossbikes.com"]
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//ul[@class="brand"]',)), follow= True),
  Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="bikes_list"]',))
  , callback="parse_items", follow= True),)

  csvfile = None
  printHeader = True
  def to_csv(self, item):
    if self.printHeader:
      self.csvfile = open('SunCrossBikes.csv','w')
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
    
      strWrite += 'Product,'+item["Product_Name"]+ '*,' + item["Brand_Name"] + ','
      strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item ["Sale_Price"] + ','
      strWrite += ';'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","") + ',' + item["Product_Code"] +  ','  + "SUNCROSSBIKES" +  ','  

    
      strWrite += item["Category"] + ',' + item["Option_Set"] + ',' + item["Product_Availability"] +','
      strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + ','+ item['MetaDescription'] + ',' + item['TitleTag'] + ','
      strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
      strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
      strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ',6,7,' 
      #for Images 
      strWrite += item["Product_Image_File1"] +','
      #loop for seconday images
      
      strWrite += '\n'

     

      self.csvfile.write(strWrite.encode('utf8'))
    
  def parse_items(self, response):
  #def parse(self, response):
      sel = Selector(response)
      item = BigCItem()     
      item ["Item_Type"] = "Product"
      #Product Name
      pname = sel.xpath("//div[@class='bike_name_code']/h2/text()").extract()[0].replace(",","")
      item ["Product_Name"] =  pname
      item["MetaDescription"] = "Get your hands on the " + pname + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["TitleTag"] = "Buy the " + pname+ " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"

      mrp = response.xpath("//span[@id='listPrice']/strong/text()").extract()
      #Pricing
      item ["Retail_Price"] = sel.xpath("//div[@class='rate']/h3/text()").extract()[0].replace(",","")
      item ["Sale_Price"] = ""
      item ["Price"] = sel.xpath("//div[@class='rate']/h3/text()").extract()[0].replace(",","")
      
      item ["Brand_Name"] = sel.xpath("//div[@class='middle_container']/a/text()").extract()[1]
    

      #Product Code Extraction
      
      item["Product_Code"] = item ["Brand_Name"]+response.url.replace("http://suncrossbikes.com/bike_detail.php?bikeId=","").split("&")[0]

      #Product Description 
      item["Product_Description"] = sel.xpath("//div[@class='specification']/ul").extract()
      
      #ImageFile
      item["Product_Image_File1"] = "http://suncrossbikes.com/"+ sel.xpath("//div[@class='middle_container']/img/@src").extract()[0]

      item ["Category"] = sel.xpath("//div[@class='middle_container']/a/text()").extract()[2]

      item["Option_Set"] = pname
      item["Product_Availability"] = "8-13 Working Days"
      item["Current_Stock"] = "100"
      item ["Free_Shipping"] = "N"
      item ["Sort_Order"] = "-200"
      item["Product_Image_Description_1"] = "Buy " +pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Product_Image_Is_Thumbnail_1"] = "Y"
      item["Track_Inventory"] = "By Product"      
      item["Product_Image_Sort_1"] = "1"
      item["Product_Image_Sort_2"] = "2"
      item["Product_Image_Sort_3"] = "3"
      item["Product_Image_Sort_4"] = "4"
      item["Product_Image_Sort_5"] = "5"
      #variant data URL
##      url = sel.xpath('//p[@class="infoTXT"]/a/@onclick').extract()[0].split("','")[0].replace("window.open('","").replace("errorform","product2_ext")   
##
##      request = Request(url,callback=self.parse_items2)
##      request.meta["item"] = item    
##      return request
      self.to_csv(item)
      return item
    
  
      
        
      
      
      
    
