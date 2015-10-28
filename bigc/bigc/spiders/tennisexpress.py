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

class MySpider(CrawlSpider):
  name = "tennisexpress"
  allowed_domains = ["tennisexpress.com"]
  
  start_urls = [
                "http://www.tennisexpress.com/category.cfm/tennis/asics-mens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/mens-diadora-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/fila-mens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/kswiss-mens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/lacoste-mens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/lotto-mens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/new-balance-mens-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/prince-mens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/mens-tretorn-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/mens-under-armour-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/wilson-mens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/yonex-mens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/yonex-womens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/wilson-womens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/womens-under-armour-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/womens-tretorn-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/prince-womens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/new-balance-womens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/lotto-womens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/lacoste-womens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/kswiss-womens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/womens-hello-kitty-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/fila-womens-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/womens-diadora-tennis-shoes",
                "http://www.tennisexpress.com/category.cfm/tennis/asics-womens-tennis-shoes"
                ]
  
 
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=("//td",)), callback="parse_items" , follow= True),)

  csvfile = None
  printHeader = True
  def to_csv(self, item):
    if self.printHeader:
      self.csvfile = open('TennisExpress.csv','w')
    if self.csvfile:

      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='Item Type,Product ID,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Description,Product Code/SKU,Bin Picking Number,'
        strWrite +='Category,Option Set,Product Availability,Current Stock Level,Free Shipping,Sort Order, Meta Description,Page Title,Product Image Description - 1,Product Image Is Thumbnail - 1,'
        strWrite +='Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,Product Image Sort-8,'
        strWrite +='Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7,Product Image File - 8 \n'
        self.printHeader = False

      
      strWrite += 'Product,,'+item["Product_Name"]+ '*,' + item["Brand_Name"] + ','
      strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item ["Sale_Price"] + ','
      strWrite += ';'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","") + ',' + item["Product_Code"] +  ','  + "TENNISEXPRESS" +  ','      
      strWrite += item["Category"] + ',' + item["Option_Set"] + ',' + "12-17 Working Days,100,N,"
      strWrite += item["Sort_Order"] + ','+ item['MetaDescription'] + ',' + item['TitleTag'] + ','
      strWrite += item["Product_Image_Description_1"] + ',' + "Y,By Option,1,2,3,4,5,6,7,8"
      #for Images
      strWrite += item["Product_Image_File1"] +','
      #loop for seconday images
      for image in item["Product_Image_File2"]:
        strWrite += image.split(").src=")[-1].replace("'","") + ","
        
      strWrite += '\n'

      #print variant
      for sizes in item["variants"]:
        strWrite += 'SKU,,[S]Size= US ' + sizes.replace("\n","").replace("\t","").replace("\r","").split("-")[0] + ',,,,,,' + item ["Product_Code"]+"US"+sizes.replace("\n","").replace("\t","").replace("\r","").split("-")[0] +',TENNISEXPRESS,,,,100,,,,,,,,,,,\n'

      self.csvfile.write(strWrite.encode('utf8'))
    
  def parse_items(self, response):
  #def parse(self, response):
      sel = Selector(response)
      item = BigCItem()     
      item ["Item_Type"] = "Product"
      #Product Name
      item ["Product_Name"] =  sel.xpath("//h1[@id='itemName']/text()").extract()[0].replace(",","-")
      item["MetaDescription"] = "Get your hands on the " + sel.xpath("//h1[@id='itemName']/text()").extract()[0].replace(",","-") + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["TitleTag"] = "Buy the " + sel.xpath("//h1[@id='itemName']/text()").extract()[0].replace(",","-") + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"

      mrp = response.xpath("//span[@id='listPrice']/strong/text()").extract()
      #Pricing
      if mrp:
        x = float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@id='listPrice']/strong/text()").extract()[0])[0])
        y = float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//h2[@class='itemPrice']/text()").extract()[0])[0])
        item ["Retail_Price"] = str((x*65 + 2100)*114.5/100 + x*65*23/100)
        item ["Sale_Price"] = str((y*65 + 2100)*114.5/100 + x*65*23/100)
        item ["Price"] = str((x*65 + 2100)*114.5/100 + x*65*23/100)
      else:
        x= float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//h2[@class='itemPrice'/text()").extract()[0])[0])
        item ["Retail_Price"] = str((x*65 + 2100)*114.5/100 + x*65*23/100)
        item ["Price"] = str((x*65 + 2100)*114.5/100 + x*65*23/100)
        item ["Sale_Price"] = ""
        
        
      if  "ASICS" in item["Product_Name"]:
        item ["Brand_Name"] = "ASICS"
      elif  "DIADORA" in item["Product_Name"]:
        item ["Brand_Name"] = "Diadora"
      elif  "FILA" in item["Product_Name"]:
        item ["Brand_Name"] = "Fila"
      elif  "HELLO KITTY" in item["Product_Name"]:
        item ["Brand_Name"] = "Hello Kitty"
      elif "K-SWISS" in item["Product_Name"]:
        item ["Brand_Name"] = "K-Swiss"
      elif "LACOSTE" in item["Product_Name"]:
        item ["Brand_Name"] = "Lacoste"
      elif "LOTTO" in item["Product_Name"]:
        item ["Brand_Name"] = "Lotto"
      elif "NEW BALANCE" in item["Product_Name"]:
        item ["Brand_Name"] = "New Balance"
      elif "PRINCE" in item["Product_Name"]:
        item ["Brand_Name"] = "Prince"
      elif "TRETORN" in item["Product_Name"]:
        item ["Brand_Name"] = "Tretorn"
      elif "UNDER ARMOUR" in item["Product_Name"]:
        item ["Brand_Name"] = "Under Armour"
      elif "WILSON" in item["Product_Name"]:
        item ["Brand_Name"] = "Wilson"
      elif "YONEX" in item["Product_Name"]:        
        item ["Brand_Name"] = "Yonex"
      else:
        item ["Brand_Name"] = "NULL"
    

      #Product Code Extraction
      code = sel.xpath("//h2[@id='itemNum']/text()").extract()[0].replace("Item #:","")
      item["Product_Code"] = sel.xpath("//h2[@id='itemNum']/text()").extract()[0].replace("Item #:","") + "TNEXP"

      #Product Description 
      item["Product_Description"] = sel.xpath("//div[@class='infoTXT']/p").extract()
      
      #ImageFile
      item["Product_Image_File1"] = sel.xpath("//img[@id='MainImage']/@src").extract()[0].replace("-m.jpg","-l.jpg")
      item["Product_Image_File2"] = sel.xpath("//div[@id='altImageContainer']/a/@onmouseover").extract()
                                            
      #Other Constants
      if "Women" in item ["Product_Name"]:
        item ["Category"] = "Racket Sports/Tennis/Tennis Shoes; Shoes/Women's Shoes/Tennis Shoes"
      else:
        item ["Category"] = "Racket Sports/Tennis/Tennis Shoes; Shoes/Men's Shoes/Tennis Shoes"    
      item["Option_Set"] = sel.xpath("//h1[@id='itemName']/text()").extract()[0].replace(",","-")

      item ["Sort_Order"] = "-250"

      if item["Brand_Name"] =="ASICS" or item["Brand_Name"] =="Wilson" or item["Brand_Name"] =="New Balance"  :
        item ["Sort_Order"] = "-300"
      else:
        item ["Sort_Order"] = "-250"
        
      item["Product_Image_Description_1"] = "Buy " + sel.xpath("//h1[@id='itemName']/text()").extract()[0].replace(",","-").replace("  ","") + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      
      #variant data URL
      url = sel.xpath('//p[@class="infoTXT"]/a/@onclick').extract()[0].split("','")[0].replace("window.open('","").replace("errorform","product2_ext")
      if item["Brand_Name"] not in "Null":
        if "Running" not in item["Product_Name"]:
          request = Request(url,callback=self.parse_items2)
          request.meta["item"] = item
          return request
    
 
#-------VARIANTS EXTRACTION FROM URL-----------
  def parse_items2(self,response):
    sel = Selector(response)
    item = response.meta['item']
    
    item["variants"] = sel.xpath(".//select/option/text()").extract()[1:]
    if item["variants"]:
      #yield item
      self.to_csv(item)
      return item
  
      
        
      
      
      
    
