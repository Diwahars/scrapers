from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from myntra.items import MyntraItem
import urlparse 
from scrapy.http.request import Request



class MySpider(CrawlSpider):
  name = "mojo1"
  allowed_domains = ["myntra.com"]
  start_urls = ["http://www.myntra.com/sports-shoes?f=brands%3AASICS%2CAdidas%2CLi%2520Ning%2CSalomon"]
  
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//li',))
    , callback="parse_items", follow= True),)
  
  def parse_items(self, response):
  #def parse(self, response):

    sel = Selector(response)
    item = MyntraItem()
    hxs = HtmlXPathSelector(response)
    
    item ["Item_Type"] = "Product"
    item ["Product_Name"] = sel.xpath("//h1[@class='title']/text()").extract()

    mrp = response.xpath("//div[@class='price']/span[@class='strike']/text()").extract()

    if mrp:
      item ["Retail_Price"] = mrp[0].replace("Rs.","")
      item ["Sale_Price"] = sel.xpath("//div[@class='price']/text()").extract()[0].replace("Rs.","")
      item ["Price"] = mrp[0].replace("Rs.","")
    else:
      item ["Retail_Price"] = sel.xpath("//div[@class='price']/text()").extract()[0].replace("Rs.","")
      item ["Price"] = sel.xpath("//div[@class='price']/text()").extract()[0].replace("Rs.","")
      
          
    item ["Brand_Name"] = sel.xpath("//ul[@class='breadcrumb']/li[5]/a/text()").extract()[0].replace("Sports Shoes","")
    item ["Product_Code"] ="IND"+sel.xpath("//h4[@class='id pdt-code']/text()").extract()[0].replace("Product Code:","")
    item["Option_Set"] = sel.xpath("//h1[@class='title']/text()").extract()
    item["Product_Image_File"] = sel.xpath("//div[@class='thumbs']/img/@data-blowup").extract()
    
    item['Category'] = "Shoes/" + sel.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").extract()[0].replace("en Footwear","en's Running Shoes") + "/Cross Training"
    
    
    
    item["Free_Shipping"] = "N"
    item["Track_Inventory"] = "By Product"
    item["Product_Availability"] = "2-7 Business  Days"
    item["Product_Image_File"] = sel.xpath("//div[@class='thumbs']/img/@data-blowup").extract()
    item["Product_Image_Description_1"] = "Buy" + sel.xpath("//h1[@class='title']/text()").extract()[0] + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["Product_Image_Is_Thumbnail_1"] = "Y"

    item["Product_Image_Sort_1"] = "1"
    item["Product_Image_Sort_2"] = "2"
    item["Product_Image_Sort_3"] = "3"
    item["Product_Image_Sort_4"] = "4"
    item["Product_Image_Sort_5"] = "5"
    
    
    yield item
  
    variants = sel.xpath(".//div[@class='sizes']/button/text()")
    skus = sel.xpath(".//div[@class='sizes']/button/@data-sku")
    stocks = sel.xpath(".//div[@class='sizes']/button/@data-count")
    
    
    
    for variant,sku,stock in zip(variants,skus,stocks):
      item ["Item_Type"] = "SKU"
      item ["Free_Shipping"] = ""
      item ["Product_Availability"] = ""
      item ["Product_Name"] = "[S]Size=UK "+variant.extract()
      item ["Product_Code"] = "IND"+sku.extract()
      item ["Current_Stock"] = stock.extract()
      item ["Sale_Price"] = ""
      item ["Retail_Price"] = ""
      item ["Price"] = ""
      item ["Brand_Name"] = ""
      item["Category"] = ""
      item["Free_Shipping"] = ""
      item["Product_Availability"] = ""
      item["Option_Set"] = ""
      item["Product_Image_File"] = ""
      item["Track_Inventory"] = ""
      
      item["Product_Image_Is_Thumbnail_1"] = "Y"
      item["Product_Image_Sort_1"] = ""
      item["Product_Image_Sort_2"] = ""
      item["Product_Image_Sort_3"] = ""
      item["Product_Image_Sort_4"] = ""
      item["Product_Image_Sort_5"] = ""
      item["Product_Image_Description_1"] = ""
      

      yield item

    
      




