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
import re


class runningwarehouse(CrawlSpider):
  name = "runningwarehouse_flipkart"
  allowed_domains = ["runningwarehouse.com"]
  start_urls = ["http://www.runningwarehouse.com/fpm.html",
                "http://www.runningwarehouse.com/fpw.html",
                #"http://www.runningwarehouse.com/ASICS_Gel_Kayano_21_Lite_Show/descpage-AK21LM1.html"
                ]
  
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//ul[@class="lnav_subsection"][2]/li[position()>2]',))
    , callback="parse_categories", follow= True),)
  

  csvfile = None
  printHeader = True
  def to_csv(self, item):
    start = 0
    end=0
    if self.printHeader:
      self.csvfile = open('RunningWarehouse_flipkart.csv','w')
    if self.csvfile:
      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='Item Type,Product ID,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Description,Product Code/SKU,Bin Picking Number,'
        strWrite +='Category,Option Set,Product Availability,Current Stock Level,Free Shipping,Sort Order, Meta Description,Page Title, Product Image Description - 1,Product Image Is Thumbnail - 1,'
        strWrite +='Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,Product Image Sort-8,'
        strWrite +='Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7, Product Image File - 8,\n'
        self.printHeader = False

      #print basic product data
      if ("Null") not in item["Brand_Name"]:
        strWrite += 'Product,'+','+item["Product_Name"]+ '*,' + item["Brand_Name"] + ','
        strWrite += item["Price"] + ','+ item["Retail_Price"] +  ',' + item ["Sale_Price"] + ','
        #Product Description and Video
        strWrite += (item["video"]+
                     re.sub('<img.*?>',"",
                            re.sub('</div.*?>',"",
                                   re.sub('<div.*?>',"",
                                          re.sub('<a.*?">',"",
                                                 re.sub('<a.*?blank">',"",';'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r",""))))))
                                          + ",")
        #re.sub("<.*?>","", for replacing HTML tags        
        strWrite += item["Product_Code"]+"RNWH" +  ',' + "RUNNINGWAREHOUSE" +  ',' + item["Category"] + ',' + item["Option_Set"] + '2,' + item["Product_Availability"] +','
        #strWrite += item["Product_Code"] +  ',' + "RUNNINGWAREHOUSE" +  ',' + "Category" + ',' + item["Option_Set"] + ',' + item["Product_Availability"] +','
        strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"] + "," + item['MetaDescription'] + ',' + item['TitleTag'] + ','
        strWrite += item["Product_Image_Description_1"] + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
        strWrite += "1,2,3,4,5,6,7,8,"
        #for Images
        strWrite += item["Product_Image_File1"]+","+item["Product_Image_File2"]+","+','.join(item["Product_Image_File3"]) +','         
        strWrite += '\n'

        for size,sku in zip(item["variants"],item["id1"]):
          strWrite += 'SKU,,'+ size.split("Width")[0].replace("Size ","[S]Size=US ").replace(u'\xa0',"")
          
          if "B" in size.split("Width")[1].split("In")[0].replace(u'\xa0',""):
            strWrite += ";[RB]Width= Narrow Width (" +size.split("Width")[1].split("In")[0].replace(u'\xa0',"").replace(" ","") +")"
          elif "D" in size.split("Width")[1].split("In")[0].replace(u'\xa0',""):
            strWrite += ";[RB]Width= Medium Width (" +size.split("Width")[1].split("In")[0].replace(u'\xa0',"").replace(" ","") +")"
          elif "2E" in size.split("Width")[1].split("In")[0].replace(u'\xa0',""):
            strWrite += ";[RB]Width= Wide Width (" +size.split("Width")[1].split("In")[0].replace(u'\xa0',"").replace(" ","") +")"
          elif "4E" in size.split("Width")[1].split("In")[0].replace(u'\xa0',""):
            strWrite += ";[RB]Width= Extra Wide Width (" +size.split("Width")[1].split("In")[0].replace(u'\xa0',"").replace(" ","") +")"
            
          strWrite += ',,,,,,' + item["Product_Code"]+sku +',"RUNNINGWAREHOUSE",,,,100,,,,,,,,,,,\n'

  
      self.csvfile.write(strWrite.encode('utf8')) 

  def parse_categories(self,response):
  #def parse(self,response):
      
      sel = Selector(response)      
      plist = sel.xpath("//div[@class='name']/a/@href").extract()
      brandlist = sel.xpath("//div[@class='name']/a/text()").extract()
      
      for i,brand in zip(plist,brandlist):
        
        
        if brand.split(" ")[0] !="adidas" and brand.split(" ")[0]!="Nike":
          item = BigCItem()
          
          cat = sel.xpath("//div[@id='content_wrap']/h1/text()").extract()[0]
          if "Women's Maximal" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Women's Running Shoes/Maximal Cushioned Running Shoes"
          elif "Women's Minimal " in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Women's Running Shoes/Minimalist Running Shoes"
          elif "Women's Road Racing" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Women's Running Shoes/Road Racing Running Shoes"
          elif "Women's Trail" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Women's Running Shoes/Trail Running Shoes"
          elif "Women's Minimum Neutral" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Women's Running Shoes/Neutral Running Shoes;Shoes/Men's Shoes/Cross Training Shoes"
          elif "Women's Minimum Support" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Women's Running Shoes/Support Running Shoes"
          elif "Women's Moderate Motion Control " in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Women's Running Shoes/Motion Control Running Shoes"
          elif "Women's Track and Field" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Spikes" + ";Shoes/Women's Running Shoes/Track and Field Running Spikes"
          elif "Women's Cross Country" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Spikes" + ";Shoes/Women's Running Shoes/Cross Country Running Shoes"
          elif "Kids" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Junior Shoes/Running Shoes"
          elif "Maximal" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Men's Running Shoes/Maximal Cushioned Running Shoes"
          elif "Minimal" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Men's Running Shoes/Minimalist Running Shoes"
          elif "Road Racing" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Men's Running Shoes/Road Racing Running Shoes"
          elif "Trail" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Men's Running Shoes/Trail Running Shoes"
          elif "Men's Minimum Neutral" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Men's Running Shoes/Neutral Running Shoes;Shoes/Men's Shoes/Cross Training Shoes"
          elif "Support" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Men's Running Shoes/Support Running Shoes"
          elif "Motion Control" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Men's Running Shoes/Motion Control Running Shoes"
          elif "Track and Field" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Spikes" + ";Shoes/Men's Running Shoes/Track and Field Running Spikes"
          elif "Cross Country" in cat:
            item["Category"]  = "Run & Cycle/Running/Running Spikes" + ";Shoes/Men's Running Shoes/Cross Country Running Shoes"
          else:
            item["Category"]  = "Run & Cycle/Running/Running Shoes" + ";Shoes/Men's Running Shoes/Neutral Running Shoes"
            
          request = Request(i,callback=self.parse_items) #For Parsing ProductURLS
          request.meta["item"]  = item
          yield request
        
  def parse_items(self, response):
  #def parse(self, response):
      sel = Selector(response)
      
      item = response.meta['item']
      item ["Item_Type"] = "Product"
      #Product Name
      pname = sel.xpath("//h1[@class='name']/text()")
      item ["Product_Name"] = sel.xpath("//h1[@class='name']/text()").extract()[0]
      item["MetaDescription"] = "Get your hands on the " + pname.extract()[0] + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["TitleTag"] = "Buy the " + pname.extract()[0] + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Product_Image_Description_1"] = "Buy " + pname.extract()[0] + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Option_Set"] = pname.extract()[0]      
      sp = response.xpath("//span[@class='sale']/text()")
      list1 = response.xpath("//div[@class='product_pricing fl']/span[@class='list']/text()")
      
      #Pricing
      if list1:
		cost_in_dollars = float(response.xpath("//span[@class='list']/text()").extract()[0].replace("$","").replace("MSRP: ","").replace("msrp: ",""))
		cost_shipping = cost_in_dollars*65 + 3250
		landed_cost = cost_shipping*130/100
		comission_shipping = landed_cost*110/100+200
		sales_tax = comission_shipping * 114.5/100
		final_price = sales_tax * 115/100
		item ["Price"] = item ["Retail_Price"] = str(final_price)
		item ["Sale_Price"] = ""                
        
		if sp:
			cost_in_dollars = float(response.xpath("//span[@class='sale']/text()").extract()[0].replace("$","").replace("Sale: ","").replace("Price: ","").replace("To View Add to Cart","0"))
			cost_shipping = cost_in_dollars*65 + 3250
			landed_cost = cost_shipping*130/100
			comission_shipping = landed_cost*110/100+200
			sales_tax = comission_shipping * 114.5/100
			final_price = sales_tax * 115/100 
			item ["Sale_Price"] = str(final_price)
		  
		 

      else:
		cost_in_dollars = float(response.xpath("//span[@class='price']/text()").extract()[0].replace("$","").replace("Price: ","").replace("MSRP: ","").replace("To View Add to Cart","0"))
		cost_shipping = cost_in_dollars*65 + 3250
		landed_cost = cost_shipping*130/100
		comission_shipping = landed_cost*110/100+200
		sales_tax = comission_shipping * 114.5/100
		final_price = sales_tax * 115/100
		item ["Retail_Price"] = item ["Price"] = str(final_price)
		item ["Sale_Price"] = ""
  
      #Product Code Extraction
      item["Product_Code"] = sel.xpath("//meta[@itemprop='sku']/@content").extract()[0]
      #Product Description
      desc = sel.xpath("//div[@class='left_column fl']").extract()
      desc1 = sel.xpath("//div[@class='right_column fr']").extract()
      tech =  sel.xpath("//div[@id='tech_tab']").extract()
      item["Product_Description"] = desc
      #ImageFile
      item["Product_Image_File1"] = "http://img.runningwarehouse.com/360/"+item["Product_Code"]+"/zoom_side.jpg"
      item["Product_Image_File2"] = "http://img.runningwarehouse.com/360/"+item["Product_Code"]+"/zoom_sole.jpg"
      imglist = ["1","3","4","6","9","13"]
      list3 = []
      for i in imglist:
        list3.append("http://img.runningwarehouse.com/360/"+item["Product_Code"]+"/"+i+".jpg")
        
      item["Product_Image_File3"] = list3

      #Other Constants
           
      item["Product_Availability"] = "12-17 Working Days"
      item["Current_Stock"] = "100"
      item ["Free_Shipping"] = "N"
      item["Product_Image_Is_Thumbnail_1"] = "Y"
      item["Track_Inventory"] = "By Option"                 
      #variant data        
      item ["variants"] = sel.xpath("//span[@class='styleitem']/text()").extract()
      item ["id1"] = sel.xpath("//span[@class='styleitem']/@data-scode").extract()

      
      if  "Brooks"in item["Product_Name"]:
        item ["Brand_Name"] = "Brooks"
      elif "HOKA ONE ONE" in item["Product_Name"]:
        item ["Brand_Name"] = "HOKA ONE ONE"
      elif "New Balance" in item["Product_Name"]:
        item ["Brand_Name"] = "New Balance"
      elif "Mizuno" in item["Product_Name"]:
        item ["Brand_Name"] = "Mizuno"
      elif "Saucony" in item["Product_Name"]:
        item ["Brand_Name"] = "Saucony"
      elif "Altra" in item["Product_Name"]:
        item ["Brand_Name"] = "Altra"
      elif "Inov-8" in item["Product_Name"]:
        item ["Brand_Name"] = "Inov-8"
      elif "Karhu" in item["Product_Name"]:
        item ["Brand_Name"] = "Karhu"
      elif "Under Armour" in item["Product_Name"]:
        item ["Brand_Name"] = "Under Armour"
      elif "La Sportiva" in item["Product_Name"]:
        item ["Brand_Name"] = "La Sportiva"
      elif "Merrel" in item["Product_Name"]:        
        item ["Brand_Name"] = "Merrel"
      elif "Montrail" in item["Product_Name"]:        
        item ["Brand_Name"] = "Montrail"
      elif "Newton" in item["Product_Name"]:        
        item ["Brand_Name"] = "Newton"
      elif "The North Face" in item["Product_Name"]:        
        item ["Brand_Name"] = "The North Face"
      elif "On " in item["Product_Name"] or "ON " in item["Product_Name"]:        
        item ["Brand_Name"] = "On"
      elif "Pearl Izumi" in item["Product_Name"]:        
        item ["Brand_Name"] = "Pearl Izumi"      
      elif "Scott" in item["Product_Name"]:        
        item ["Brand_Name"] = "Scott"      
      elif "Zoot" in item["Product_Name"]:        
        item ["Brand_Name"] = "Zoot"
      else:
        item ["Brand_Name"] = "Null"
        
      if item["Brand_Name"] in ("Asics","Saucony","Mizuno","Brooks","New Balance","ASICS"):
        item ["Sort_Order"] = str(float(-400-(cost_in_dollars*20/100)))
      elif item["Brand_Name"] in ("Hoka One One","Salomon","Altra","Under Armour"):
        item ["Sort_Order"] = str(float(-350-(cost_in_dollars*20/100)))
      else:
        item ["Sort_Order"] = str(float(-300-(cost_in_dollars*20/100)))
      

      item["video"] = ""
      self.to_csv(item)
      return item

##      vurl = response.xpath("//a[@class='industry_vidlink icon_index_1']/@href").extract()
##      if vurl:
##        request = Request(vurl[0],callback=self.parse_video) #For Video Page
##        request.meta["item"]  = item
##        return request
##      else:
##        item["video"] = ""
##        self.to_csv(item)
##        return item

##  def parse_video(self,response):
##      sel = Selector(response)
##      item = response.meta['item']
##      #item ["video"] = sel.xpath("//html").extract()[0]
##      item ["video"] = ('<iframe width="560" height="315" src="'
##                         +"https://www.youtube.com/watch?v=j6cT0XSLPWw"
##                             +'" frameborder="0" allowfullscreen></iframe>')
##      self.to_csv(item)
##      return item
        
        





    
    
