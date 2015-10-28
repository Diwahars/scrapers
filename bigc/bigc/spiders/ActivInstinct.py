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
  name = "activinstinct"
  allowed_domains = ["activinstinct.com"]
  start_urls = [
##                "http://www.activinstinct.com/hockey/goalie-equipment/sticks/grays-gx-5000-goalkeeping-hockey-stick-2013/",
##                "http://www.activinstinct.com/hockey/goalie-equipment/upper-body-protection/mercian-xtreme-chest-arm-shoulder-protector/",
##                "http://www.activinstinct.com/hockey/sticks/adult/composite-sticks/kookaburra-vortex-hockey-stick-2013/",
##                "http://www.activinstinct.com/hockey/sticks/junior/grays-revo-junior-hockey-stick/",]
##    "http://www.activinstinct.com/footwear/squash/mens/adidas-adipower-stabil-11-mens-court-shoes-white-silver-blue/"
                
                "http://www.activinstinct.com/hockey/protection/",
                "http://www.activinstinct.com/hockey/goalie-equipment/",
                "http://www.activinstinct.com/hockey/shoes/",
                "http://www.activinstinct.com/hockey/sticks/adult/",
                "http://www.activinstinct.com/hockey/sticks/junior/",                
                "http://www.activinstinct.com/footwear/squash/"
                
                ]

  rules = (Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=('//div[@id="pagination"]',))
    , follow= True),
    Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=('//ul[@class="clearfix"]',)),
                 callback="parse_items" , follow= True),
    )
  csvfile = None
  printHeader = True

  def to_csv(self, item):
    if self.printHeader:
      self.csvfile = open('ActivInstinct.csv','w')
    if self.csvfile:
      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='Item Type,Product ID,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Description,Product Code/SKU,Bin Picking Number,'
        strWrite +='Category,Option Set,Product Availability,Current Stock Level,Free Shipping,Sort Order,Meta Description,Page Title,Product Image Description - 1,Product Image Is Thumbnail - 1,'
        strWrite +='Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,'
        strWrite +='Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 , Product Image File - 6 ,\n'
        self.printHeader = False

      #print basic product data
      strWrite += 'Product,,'+item["Product_Name"]+ "*," + item["Brand_Name"] + ','
      strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item["Sale_Price"] + ','
      strWrite += '.'.join(item["Product_Description"]).replace(",","").replace("\n","").replace("\r","") + ',' + item["Product_Code"]+  'ACVIN,'+ 'ACTIVINSTINCT,'
      strWrite += item["Category"] + ',' + item["Option_Set"] + ','
      strWrite += "12-17 Working Days,100,N," + item["Sort_Order"] + ',' + item["MetaDescription"] + "," + item["TitleTag"] + ","
      strWrite += item["Product_Image_Description_1"] + ',' + "Y,By Option,1,2,3,4,5,6,"      
      for image in item["Product_Image_File1"] :
        strWrite += image +","
      strWrite += '\n'
      for size in item["variants"]:
        strWrite += "SKU,,[S]Size="+size.replace("UK","UK ")
        strWrite += ",,,,,,"+item["Product_Code"]+size+",ACTIVINSTINCT,,,,100"
        strWrite += '\n'
      
      self.csvfile.write(strWrite.encode('utf8'))

  def parse_items(self,response):
  #def parse(self,response):
    sel = Selector(response)
    item = BigCItem()
    hxs = HtmlXPathSelector(response)
    
    item ["Item_Type"] = "Product"
    #Product Name
    pname = sel.xpath("//h1[@class='black']/text()").extract()[0].replace(",","") 
    item ["Product_Name"] =  pname
    item["Option_Set"] = pname
    item["Product_Image_Description_1"] = "Buy "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["MetaDescription"] = "Get your hands on the "+pname +". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["TitleTag"] = "Buy the "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    cat3 = response.xpath("//div[@id='breadcrumbs']/a[5]/text()").extract()[0]
    cat2 = response.xpath("//div[@id='breadcrumbs']/a[4]/text()").extract()[0]
    cat = response.xpath("//div[@id='breadcrumbs']/a[3]/text()").extract()[0]
    cat0 = response.xpath("//div[@id='breadcrumbs']/a[2]/text()").extract()[0] 
    if cat0 =="Hockey":
      if cat =="Shoes":
        if cat2 =="Women's" or cat2=="Ladies":
          item["Category"] = "Team Sports/Hockey/Shoes; Shoes/Women's Shoes/Hockey Shoes and Spikes"
        elif cat2 =="Men's":
          item["Category"] = "Team Sports/Hockey/Shoes; Shoes/Women's Shoes/Hockey Shoes and Spikes"
        elif cat2=="Junior":
          item["Category"] = "Team Sports/Hockey/Shoes; Shoes/Junior Shoes/Hockey Shoes and Spikes"
      elif cat =="Protection":
        item["Category"] = "Team Sports/Hockey/Protective Gear/"+cat2
      elif cat =="Sticks":
        item["Category"] = "Team Sports/Hockey/Sticks/"+cat2
        if cat3:
          item["Category"] = "Team Sports/Hockey/Sticks/"+cat2+"/"+cat3
          
      elif cat == "Goalie equipment":
        item["Category"] = "Team Sports/Hockey/Goalie Equipment/"+cat2
      else:
        item["Category"] = cat
    else:      
      if response.xpath("//div[@id='breadcrumbs']/a[2]/text()").extract()[0]=="Footwear":
        print "Hello"
        if cat2 =="Women's" or cat2=="Ladies":
          item["Category"] = "Racket Sports/Squash/Squash Shoes/Women's;Shoes/Women's Shoes/Indoor Court Shoes"
        elif cat2 =="Men's":
          item["Category"] = "Racket Sports/Squash/Squash Shoes/Men's;Shoes/Men's Shoes/Indoor Court Shoes"
        elif cat2=="Junior":
          item["Category"] = "Racket Sports/Squash/Squash Shoes/Junior;Shoes/Junior Shoes/Indoor Court Shoes"
      else:
        item["Category"] = "Racket Sports/Squash/Rackets"

    #Pricing
    mrp = (re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@id='product-price-rrp-display-sub']/text()").extract()[0])[0])
    if cat =="Shoes":      
      if mrp:
        mrp = (float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@id='product-price-rrp-display-sub']/text()").extract()[0])[0])*97+2500)*114.5/100*130/100
        sp = (float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//p[@id='product-price']/text()").extract()[0])[0])*97+2500)*114.5/100*130/100
      else:
        mrp=sp = (float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//p[@id='product-price']/text()").extract()[0])[0])*97+2500)*114.5/100*130/100
        
      item ["Retail_Price"] = str(mrp) 
      item ["Price"] =  str(mrp)
      item ["Sale_Price"] = str(sp)
    else:
      if mrp:
        mrp = (float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//span[@id='product-price-rrp-display-sub']/text()").extract()[0])[0])*97+2500)*114.5/100*130/100
        sp = (float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//p[@id='product-price']/text()").extract()[0])[0])*97+2500)*114.5/100*130/100
      else:
        mrp=sp = (float(re.findall(r'\d+\.?\d+|\d+',sel.xpath("//p[@id='product-price']/text()").extract()[0])[0])*97+2500)*114.5/100*130/100
      item ["Retail_Price"] = str(mrp) 
      item ["Price"] =  str(mrp)
      item ["Sale_Price"] = str(sp)
    item["Brand_Name"]  = sel.xpath("//script[@type='text/javascript'][18]").extract()[0].split("brand")[-1].split("price")[0].split(",")[0].split("'")[-2]
    if "Adidas" in item["Brand_Name"] or "Asics" in item["Brand_Name"]:
      item["Sort_Order"] = "-300"
    else:
      item["Sort_Order"] = "-240"
      
    item ["Product_Code"] = sel.xpath("//script[@type='text/javascript'][18]").extract()[0].split("id")[-1].split("price")[0].split(",")[0].split("'")[-2]
    #Product Description
    item["Product_Description"] = sel.xpath("//div[@id='product_description_text']").extract()
       
    
    variant = response.xpath("//ul[@class='attribute-list'][2]/li/a/span/text()").extract()
    if variant:
      item["variants"]= sel.xpath("//ul[@class='attribute-list'][2]/li/a/span/text()").extract()
    else:
      item["variants"]= sel.xpath("//ul[@class='attribute-list'][1]/li/a/span/text()").extract()      
    url = sel.xpath("//a[@class='colorboxSlider openBoxButton']/@href").extract()[0]
    request = Request(url,self.parse_items2)
    request.meta["item"] = item    
    return request  
 
#-------IMAGE EXTRACTION-----------
  def parse_items2(self,response):
    
    sel = Selector(response)
    item = response.meta['item']
    item["Product_Image_File1"] =  sel.xpath("//div[@id='simple-slider']/a/@href").extract()
    self.to_csv(item)    
    return item
    

  
  


            
    
    
