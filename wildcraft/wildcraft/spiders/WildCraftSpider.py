from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from wildcraft.items import BigCItem
from scrapy.selector import Selector
import urlparse 
from scrapy.http.request import Request
import json
import csv,re

output = open("Wildcraft.csv","wb")
mywriter = csv.writer(output)
output.write('Item Type,Product Name,Product Code/SKU,Brand Name,Price,Retail Price,Sale Price,Category,Bin Picking Number,Product Description,'
             'Current Stock Level,Option Set,Product Availability,Free Shipping,Sort Order,Meta Description,Page Title,'
             'Product Image Description - 1,Product Image Is Thumbnail - 1,'
             'Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,'
             'Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7,\n')

class MySpider(CrawlSpider):
  name = "wildcraft"
  allowed_domains = ["wildcraft.in"]
  start_urls = [
##    "http://wildcraft.in/men/jackets-pullovers-warmers/men-s-husky-jacket-pro-dark-chocolate",
##    "http://wildcraft.in/packs-and-gear/backpacks/pack-y-blue"
                "http://wildcraft.in/packs-and-gear/accessories/passport-pouch-black"
    "http://wildcraft.in/packs-and-gear/rucksacks/?p=1",
                "http://wildcraft.in/packs-and-gear/rucksacks/?p=2",
                "http://wildcraft.in/packs-and-gear/rucksacks/?p=3",
                "http://wildcraft.in/packs-and-gear/rucksacks/?p=4",
                "http://wildcraft.in/packs-and-gear/rucksacks/?p=5",
                "http://wildcraft.in/packs-and-gear/rucksacks/?p=6",
                "http://wildcraft.in/packs-and-gear/backpacks/?p=1",
                "http://wildcraft.in/packs-and-gear/backpacks/?p=2",
                "http://wildcraft.in/packs-and-gear/backpacks/?p=3",
                "http://wildcraft.in/packs-and-gear/backpacks/?p=4",
                "http://wildcraft.in/packs-and-gear/backpacks/?p=5",
                "http://wildcraft.in/packs-and-gear/backpacks/?p=6",
                "http://wildcraft.in/packs-and-gear/backpacks/?p=7",
                "http://wildcraft.in/packs-and-gear/duffle-bags/?p=1",
                "http://wildcraft.in/packs-and-gear/duffle-bags/?p=2",
                "http://wildcraft.in/packs-and-gear/sleeping-bags",
                "http://wildcraft.in/packs-and-gear/pac-n-go/?p=1",
                "http://wildcraft.in/packs-and-gear/pac-n-go/?p=2",
                "http://wildcraft.in/packs-and-gear/pac-n-go/?p=3",
                "http://wildcraft.in/packs-and-gear/accessories/?p=4",
                "http://wildcraft.in/packs-and-gear/accessories/?p=3",
                "http://wildcraft.in/packs-and-gear/accessories/?p=2",
                "http://wildcraft.in/packs-and-gear/accessories/?p=1",
                "http://wildcraft.in/men/wind-rain-cheaters/?p=1",
                "http://wildcraft.in/men/wind-rain-cheaters/?p=2",
                "http://wildcraft.in/men/sandals-flipflops-footwear/p=1",
                "http://wildcraft.in/men/sandals-flipflops-footwear/p=2",
                "http://wildcraft.in/men/sandals-flipflops-footwear/p=3",
                "http://wildcraft.in/women/womens-footwear",
                "http://wildcraft.in/men/jackets-pullovers-warmers/p=1",
                "http://wildcraft.in/men/jackets-pullovers-warmers/p=2",
                "http://wildcraft.in/men/jackets-pullovers-warmers/p=3",
                
                ] 
  rules = (
##    Rule (SgmlLinkExtractor(allow=(),
##                            restrict_xpaths=('//ul[@class="shop-menu sub-menu"]',))
##    , follow= True),
    Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=('//div[@class="prod_holder"]',)),
                 callback="parse_items" , follow= True),
    )

    
  def parse_items(self, response):
##  def parse(self,response):
    item = BigCItem()
    sel = Selector(response)
    cat2 = sel.xpath("//ul[@class='breadcrumb']/li/a/span/text()").extract()[2] 
    pname = "Wildcraft "+sel.xpath("//h1[@class='p_name']/text()").extract()[0]+" "+cat2[:-1]
    item ["Product_Name"] =  item["Option_Set"] = pname
    item["Product_Image_Description_1"] = item["TitleTag"] = "Buy "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["MetaDescription"] = "Get your hands on the "+pname +". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["Brand_Name"] = "Wildcraft"
    pcode  =sel.xpath("//div[@class='p_sku']/text()").extract()[0]
    item ["Product_Code"] = pcode + "WILDCRAFT"
    item["Product_Description"] = sel.xpath("//div[@class='p_description']").extract()
    desc2= sel.xpath("//div[@class='std product-features']").extract()
    item["Product_Description"] = ''.join(item["Product_Description"]).encode('utf-8')
    mrp = sel.xpath("//span[@itemprop='price']/text()").extract()[0]
    sortorder = "-200"
    script = sel.xpath("//script[contains(text(),'var spConfig')]").extract()
    cat1 = sel.xpath("//ul[@class='breadcrumb']/li/a/span/text()").extract()[1]
    
    stock = sel.xpath("//span[@content='out_of_stock']/text()").extract()
    if stock:
      stock = "0"
    else:
      stock = "100"
    
                    
    if script:
      trackinventory = "By Option"
    else:
      trackinventory = "By Product"
      
    images = sel.xpath("//img[@class='gallery-image']").extract()
    tup = ("Product",item["Product_Name"],item ["Product_Code"],item["Brand_Name"],
             mrp,mrp,"", #price
             cat1+"/"+cat2,"WILDCRAFT",item["Product_Description"],stock,item["Product_Name"],"3-10 Working Days","N",sortorder,
             item["MetaDescription"],item["TitleTag"],item["Product_Image_Description_1"],"Y",trackinventory,
             "1","2","3","4","5","6","7")
    obj = list(tup)
    
    if images:
      images = sel.xpath("//img[@class='gallery-image']/@src").extract()
      for image in images:
        url =image.replace("70x70/","")
        obj.append(url)
      
      
    else:
      images = sel.xpath("//script[contains(text(),'comment by ba')]").extract()[0]
      images = re.findall(r'http.*?.jpg',images)
      for image in images:
        url =image.replace("70x70/","")
        obj.append(url)
        
    row = tuple(obj)
    mywriter.writerow(row)

    if script:
      variantscript = sel.xpath("//script[contains(text(),'var spConfig')]").extract()[0].split("var productMap = {")[-1].split('};')[0]
      variantscript = "{"+variantscript.split("{")[-1].replace("[","<").replace("]","}").replace("<<","<")+"}"   
      varvalues = re.findall(r':<"\d.*?,',variantscript)
      varvalues  = [w.replace('<"',"").replace('"',"").replace(",","").replace(":","") for w in varvalues]      
      varkeys = re.findall(r'"\d*.?:',variantscript)
      varkeys = [w.replace(":","").replace('"',"") for w in varkeys]    

      varDict = dict(zip(varkeys,varvalues))     

      sizescript = sel.xpath("//script[contains(text(),'var spConfig')]").extract()[0].split("//console.log")[0].split('"options":')[-1]
      sizekey = re.findall(r'"id":".*?,',sizescript)
      sizekey = [w.replace('"id"',"").replace('"',"").replace(":","").replace(",","") for w in sizekey]
      sizevalue = re.findall(r'"label":".*?,',sizescript)
      sizevalue = [w.replace('"label"',"").replace('"',"").replace(":","").replace(",","") for w in sizevalue]
      
      sizeDict = dict(zip(sizekey,sizevalue))
      size = sel.xpath("//label[@class='required']/text()").extract()

      
      for key,value in varDict.iteritems():
        if key in sizeDict:
          if "size" in size:          
            row = ('SKU','[S]Size= '+sizeDict[key],value+"WILDCRAFT","","","","","",'WILDCRAFT',
                  "",stock,"","","","","","","","","","","","","","","","")
          else:
            row = ('SKU','[S]Color= '+sizeDict[key],value+"WILDCRAFT","","","","","",'WILDCRAFT',
                  "",stock,"","","","","","","","","","","","","","","","")
            
          mywriter.writerow(row)
