from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from findia.items import BigCItem
import urlparse, re, csv
f = open("categorization.csv")
csv_file = csv.reader(f)
fitindiacat = []
LYScat = []
urls = []
for row in csv_file:
  fitindiacat.append(row[0])
  LYScat.append(row[1])

k = open("brands.csv")
brands_file = csv.reader(k)
brandlist = []
for row in brands_file:
  brandlist.append(row[0])
  
k = open("missingproducts.csv")
missing_urls = csv.reader(k)

for row in missing_urls:
  urls.append(row[0])

output = open("FitIndiaMissing.csv","wb")
mywriter = csv.writer(output)

header = ('Item Type','Product ID','Product Name','Brand Name',
          'Price','Retail Price','Sale Price',
          'Product Description','Product Code/SKU','Bin Picking Number','Category','Option Set','Product Availability',
          'Current Stock Level','Free Shipping','Sort Order','Meta Description','Page Title',''
          'Product Image Description - 1','Product Image Is Thumbnail - 1',''
          'Track Inventory','Product Image Sort - 1','Product Image Sort - 2','Product Image Sort - 3',
          'Product Image Sort - 4','Product Image Sort-5','Product Image Sort-6','Product Image Sort-7','Product Image Sort-8',
          'Product Image File - 1','Product Image File - 2','Product Image File - 3','Product Image File - 4','Product Image File - 5 ',
          'Product Image File - 6','Product Image File - 7','Product Image File - 8')
mywriter.writerow(header)



class FitIndiaMissing(CrawlSpider):
  name = "fitindia2"
  allowed_domains = ["fitindia.net"]
  
  start_urls = [ url.strip() for url in urls
                 ]
  csvfile = None
  printHeader = True
  def to_csv(self, item):
      tup = ('Product','',item["Product_Name"],item['Brand_Name'],
             item['Price'],item['Retail_Price'],item['Sale_Price'],
             item['Product_Description'],item["Product_Code"],'FITINDIA',item['Category'],item['Option_Set'],
             item['Product_Availability'],item['Current_Stock'],item['Free_Shipping'],item['Sort_Order'],item['MetaDescription'],
             item['TitleTag'],item['Product_Image_Description_1'],item["Product_Image_Is_Thumbnail_1"],item["Track_Inventory"],
             item["Product_Image_Sort_1"], item["Product_Image_Sort_2"], item["Product_Image_Sort_3"],
             item["Product_Image_Sort_4"], item["Product_Image_Sort_5"],'6','7','8'
             )

      obj = list(tup)
      for image in item["Product_Image_File1"]:
          obj.append(image)

      row = tuple(obj)
      mywriter.writerow(row)

  def parse(self, response):
      sel = Selector(response)
      item = BigCItem()
      item['Category'] = ''
      pname  = sel.xpath("//div[@class='product-name']/h1/text()").extract()[0].replace(",","-")
      for brandname in brandlist:        
        if brandname.lower() in pname.lower():          
          item ["Brand_Name"] = brandname
          break
        else:
          item ["Brand_Name"] = "Fit India"
      if 'IsoSolid' in pname:
        item ["Brand_Name"] = "Iso Solid"
         
          
      item ["Item_Type"] = "Product"
      #Product Name
      if item ["Brand_Name"] == "Fit India":
          pname  = "Fit India "+sel.xpath("//div[@class='product-name']/h1/text()").extract()[0].replace(",","-")     
          
      item ["Product_Name"] =  pname
      item["MetaDescription"] = "Get your hands on the " + pname + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["TitleTag"] = "Buy the " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Option_Set"] = pname      
      mrp = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/p[@class='old-price']/span[@class='price']").extract()     
      #Pricing
      if mrp:
        item ["Retail_Price"] = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/p[@class='old-price']/span[@class='price']/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
        item ["Sale_Price"] = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/p[@class='special-price']/span[@class='price']/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
        item ["Price"] = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/p[@class='old-price']/span[@class='price']/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
      else:
        item ["Price"] = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/span[@class='regular-price']/span/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
        item ["Retail_Price"] = response.xpath("//div[@class='product-shop span6']//div[@class='price-box'][1]/span[@class='regular-price']/span/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
        item ["Sale_Price"] = ""    
      item["Product_Code"] = "FITINDIA"+sel.xpath("//div[@class='product-sku']/span/text()").extract()[0]   
      item["Product_Description"] = sel.xpath("//div[@class='std']").extract()      
      #ImageFile
      img = response.xpath("//div[@class='more-views ma-more-img']/ul/li").extract()
      if img:
        item["Product_Image_File1"] = response.xpath("//div[@class='more-views ma-more-img']/ul/li/a/@href").extract()
      else:
        item["Product_Image_File1"] = sel.xpath("//ul/li[@class='thumbnail-item']/a/@href").extract()
##
      cat =sel.xpath("//div[@class='breadcrumbs']/ul/li[4]/a/text()").extract()
      cat2 =sel.xpath("//div[@class='breadcrumbs']/ul/li[3]/a/text()").extract()
      if cat:
        item["Category"] = sel.xpath("//div[@class='breadcrumbs']/ul/li[4]/a/text()").extract()[0].replace(",","")
      elif cat2:
        item["Category"] = sel.xpath("//div[@class='breadcrumbs']/ul/li[3]/a/text()").extract()[0].replace(",","")
      else:
        item["Category"] = sel.xpath("//div[@class='breadcrumbs']/ul/li[1]/a/text()").extract()[0].replace(",","")
        
        
      size = len(LYScat)
      for i in range(size):
        if item["Category"] == fitindiacat[i]:          
           item["Category"] = LYScat[i]          
           break
           
      item["Product_Availability"] = "8-13 Working Days"
      item["Current_Stock"] = "100"
      item ["Free_Shipping"] = "N"
      item ["Sort_Order"] = "-250"      
      item["Product_Image_Description_1"] = "Buy " + pname + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
      item["Product_Image_Is_Thumbnail_1"] = "Y"
      item["Track_Inventory"] = "By Option"      
      item["Product_Image_Sort_1"] = "1"
      item["Product_Image_Sort_2"] = "2"
      item["Product_Image_Sort_3"] = "3"
      item["Product_Image_Sort_4"] = "4"
      item["Product_Image_Sort_5"] = "5"

##      yield item

      self.to_csv(item)
      return item
