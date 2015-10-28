from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from acmefitness.items import BigCItem
import urlparse
import re


class MySpider(CrawlSpider):
  name = "acmefitness"
  allowed_domains = ["acmefitness.in"]  
  start_urls = [
                "http://www.acmefitness.in"
                # 'http://www.acmefitness.in/accessories/kettle-balls'
                ]

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@class="nav1"]/ul',)), follow= True),
    Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="product"]',))
    , callback="parse_items", follow= True),)

  csvfile = None
  printHeader = True

  def to_csv(self, item):
    if self.printHeader:
      self.csvfile = open('AcmeFitness.csv','w')
    if self.csvfile:
      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='Item Type,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Description,Product Code/SKU,Bin Picking Number,'
        strWrite +='Category,Option Set,Product Availability,Current Stock Level,Free Shipping,Sort Order,Meta Description,Page Title,Product Image Description - 1,Product Image Is Thumbnail - 1,'
        strWrite +='Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,'
        strWrite +='Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 , \n'
        self.printHeader = False
#-------CSV Printing-------------------------------------
      #print basic product data
      strWrite += 'Product,'+item["Product_Name"]+ "*," + item["Brand_Name"] + ','
      strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item["Sale_Price"] + ','
      strWrite += '.'.join(item["Product_Description"]).replace(",","").replace("\n","").replace("\r","") + ',' + item["Product_Code"]  +  'HKD,'+ 'ACMEFITNESS,'

      #for Images
      strWrite += item["Category"] + ',' + item["Option_Set"] + '2,' + item["Product_Availability"] +','
      strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + ',' + item["MetaDescription"] + "," + item["TitleTag"] + ","
      strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
      strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
      strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ','
      #strWrite += ','.join(item["Product_Image_File1"]) +  +'\n'

      for image in item["Product_Image_File1"] :
        strWrite += image.split("'")[0].split("'")[-1]

      strWrite += '\n'
#---------------------------------------VARIANTS------------------------------------------

      for size,price in item["size"].iteritems():
        strWrite +='SKU,[S]Size= ' + size + ',,,'+ price + ',,,' + item ["Product_Code"]+ ",ACMEFITNESS,,,,100,,,,,,,,,,,\n"
      self.csvfile.write(strWrite.encode('utf8'))
    
  def parse_items(self, response):
  # def parse(self, response):  
    
    sel = Selector(response)
    item = BigCItem()
    pname = (sel.xpath("//div[@class='desc-headings']/span/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","") + " "
             + sel.xpath("//span[@id='itemTitle']/text()").extract()[0].replace("\n","").replace("\r","").replace("  ",""))
    brand = response.xpath("//div[@class='product-subheadings']/a[4]/text()").extract()
    if brand:
      item["Brand_Name"]  = response.xpath("//div[@class='product-subheadings']/a/text()").extract()[2]
    else:
      if "Power Block" in pname:
        item["Brand_Name"]="Power Block"
      elif "Co Fit" in pname:
        item["Brand_Name"]="Co Fit"
      elif "Life Fitness" in pname:
        item["Brand_Name"]="Life Fitness"
      elif "AbCoster" in pname:
        item["Brand_Name"]="Ab Coaster"
      elif "LifeSpan" in pname:
        item["Brand_Name"]="LifeSpan Fitness"
      elif "BH FitnesS" in pname:
        item["Brand_Name"]="BH Fitness"
      elif "Bowflex" in pname:
        item["Brand_Name"]="Bowflex"
      elif "Octane" in pname:
        item["Brand_Name"]="Octane"
      elif "Schwinn" in pname:
        item["Brand_Name"]="Schwinn"
      else:
        item["Brand_Name"]="Acme Fitness"
      
    if item["Brand_Name"].strip() not in pname:
      pname = item["Brand_Name"]+" "+(sel.xpath("//div[@class='desc-headings']/span/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","") + " "
             + sel.xpath("//span[@id='itemTitle']/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","")) 
    else:
      pname = (sel.xpath("//div[@class='desc-headings']/span/text()").extract()[0].replace("\n","").replace("\r","").replace("  ","") + " "
             + sel.xpath("//span[@id='itemTitle']/text()").extract()[0].replace("\n","").replace("\r","").replace("  ",""))
      
    pname1 = sel.xpath("//div[@class='product-subheadings']/a/text()").extract()[1].replace("\n","").replace("\r","").replace("  ","")
    
    item ["Product_Name"] = pname 
    item["Option_Set"] = pname 
    item["Product_Image_Description_1"] = "Buy " + pname+ " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["MetaDescription"] = "Get your hands on the " +pname + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["TitleTag"] = "Buy the " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    #Pricing
    mrp = sel.xpath("//span[@class='price-strike']/text()").extract()[0].replace("Rs.","").replace(",","")    
    sp = response.xpath("//span[@itemprop='price']/text()").extract()
    sp1 = response.xpath("//span[@id='offprice']/text()").extract()
    mrp1 = response.xpath("//span[@id='listprice']/text()").extract()  


    if sp and mrp:
      item ["Sale_Price"] = sp[0].replace("Rs.","").replace(",","").replace("\n","").replace("\r","").replace("  ","")
      item ["Retail_Price"] = mrp
      item ["Price"] =  mrp
    elif sp1 and mrp1:
      item ["Sale_Price"] = sp1[0].replace("Rs.","").replace(",","").replace("\n","").replace("\r","").replace("  ","")
      item ["Retail_Price"] = mrp1[0].replace("Rs.","").replace(",","").replace("\n","").replace("\r","").replace("  ","")
      item ["Price"] =  mrp1[0].replace("Rs.","").replace(",","").replace("\n","").replace("\r","").replace("  ","")
    elif sp:
      item ["Retail_Price"] = item ["Price"] =  sp      
    elif sp1:
      item ["Retail_Price"]= item ["Price"] = sp1[0].replace("Rs.","").replace(",","").replace("\n","").replace("\r","").replace("  ","")
      
    
    #Product Code Extraction
    item ["Product_Code"] = "ACMEFIT"+response.url.split("/")[-1]
    #Product Description
    item["Product_Description"] = sel.xpath("//div[@id='java']").extract()
    #ImageFile
    img1 = response.xpath("//div[@id='wrap']/a/@href").extract()
    if img1:
      item["Product_Image_File1"] = response.xpath("//div[@id='wrap']/a/img/@src").extract()[0]
    else:
      item["Product_Image_File1"] = sel.xpath("//div[@class='zoom-desc']/a/@href").extract()[0]
    #category

    cat = response.xpath("//div[@class='product-subheadings']/a/text()").extract()[1].replace(" ","")
    
    if cat in "Treadmills":
      item["Category"] = "Fitness/Fitness Machines/Treadmills"
    elif cat  in "Ellipticals":
      item["Category"] = "Fitness/Fitness Machines/Elliptical Trainers"
    elif cat in "Cycles":
      item["Category"] = "Fitness/Fitness Machines/Exercise Bikes"
    elif cat in "Home Gyms":
      item["Category"] = "Fitness/Strength Training/Multi Gym"
    elif cat in "Benches":
      item["Category"] = "Fitness/Strength Training/Benches"
    elif cat in "AB Coasters":
      item["Category"] = "Fitness/Strength Training/Abs & Core"
    elif cat in "Accessories":
      item["Category"] = " Fitness/Fitness Machines/Accessories"
    elif cat in "Combos":
      item["Category"] = "Fitness/Strength Training/Combos"
      
    item["Product_Availability"] = "15-20 Working Days"
    item["Current_Stock"] = "100"
    item["Free_Shipping"] = "N"
    item["Sort_Order"] = "-250"
    item["Product_Image_Is_Thumbnail_1"] = "Y"
    item["Track_Inventory"] = "By Option"      
    item["Product_Image_Sort_1"] = "1"
    item["Product_Image_Sort_2"] = "2"
    item["Product_Image_Sort_3"] = "3"
    item["Product_Image_Sort_4"] = "4"
    item["Product_Image_Sort_5"] = "5"
    #Sizing info   
    item ["size"] = {}
    sizes = sel.xpath("//select/option/text()").extract()
    prices = sel.xpath("//select[@name='frm_attr1']/option/@value").extract()
    
    
    for size,price in zip(sizes,prices):
      item['size'][size] = price.split('^')[0]

    
##    yield item
    self.to_csv(item)
    return item
    
