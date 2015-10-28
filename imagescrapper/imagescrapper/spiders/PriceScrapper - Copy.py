from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from imagescrapper.items import BigCItem
import urlparse
import re
import pandas as pd
import csv

##f = open("input.csv")
##csv_file = csv.reader(f)
##productname_list = []
##for row in csv_file:
##  productname_list.append(row[1])

class MySpider(CrawlSpider):
  dont_filter=True
  name = "test"
  allowed_domains = ["snapdeal.com", "amazon.in", "amazon.com", "flipkart.com"]

  start_urls = [
    "http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=carboflex+140+squash+racket&rh=i%3Aaps%2Ck%3Acarboflex+140+squash+racket"]
    #url.strip() for url in productname_list]

  csvfile = None
  printHeader = True
  
  def to_csv(self, item):
    
    if self.printHeader:
      self.csvfile = open('PriceCompare_Output(Snapdeal,Amazon).csv','w')
    if self.csvfile:
      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='LYS Product Name,LYS URL,LYS Product Code, LYS MRP,LYS SP,LYS Stock,LYS Category,,'
        strWrite +='Snapdeal Product Name,Snapdeal URL, Snapdeal MRP,Snapdeal SP,Snapdeal Stock,Snapdeal Match,,'
        strWrite +='Amazon Product Name,Amazon URL, Amazon MRP,Amazon SP, Amazon Stock,Amazon Match,,'
        strWrite +='Flipkart Product Name,Flipkart URL, Flipkart MRP,Flipkart SP, Flipkart Stock,Flipkart Match,,'
        strWrite += ' \n'
        self.printHeader = False
        
      strWrite += item["LYSProduct_Name"] + ',' + item["LYSURL"] + ',' + item["LYSID"] + ',' + item["LYSMRP"] + ',' + item["LYSSP"] + ',' + item["LYSStock"] + ',' + item["Category"]+ ',,'
      strWrite += item["SnapdealProductName"] + ',' + item ["SnapdealURL"] + ',' + item["SnapdealMRP"] + ',' + item ["SnapdealSP"] + ','+  item["SnapdealStock"] + ',' + item["SnapdealMatch"] + ',' +','
      strWrite += item["AmazonProductName"] + ',' + item ["AmazonURL"] + ',' +item ["AmazonMRP"] + ',' + item ["AmazonSP"] + ',' + item["AmazonStock"] + "," + ';'.join(item["AmazonMatch"]) + ',,'
      strWrite += item["FlipkartProductName"] + ',' + item ["FlipkartURL"] + ',' +item ["FlipkartMRP"] + ',' + item ["FlipkartSP"] + ',' + item["FlipkartStock"] + "," + item["FlipkartMatch"] + ',,'
      strWrite +=  '\n'
      self.csvfile.write(strWrite.encode('utf8'))
      
  #def lys(self,response):
  def parse(self,response):    
    item = BigCItem()
    sel = Selector(response)
    print "Hello"
    item["SnapdealMatch"] = sel.xpath("//li[@id='result_0']").extract()[0]
    return item
    
##    item["SnapdealStock"] = "" 
##    item["LYSID"] = ""
##    item ["SnapdealURL"] = ""
##    item ["SnapdealSP"] = ""
##    item ["SnapdealMRP"] = ""
##    item ["SnapdealProductName"] = ""
##    item ["AmazonURL"] = ""     
##    item ["AmazonMRP"] = ""
##    item ["AmazonSP"] = ""     
##    item ["AmazonProductName"] = ""
##    item ["AmazonMatch"] = ""
##    item ["AmazonStock"] = item["FlipkartProductName"] = item["FlipkartURL"] = item["FlipkartMRP"] = item["FlipkartSP"] =  item["FlipkartStock"] = item["FlipkartMatch"] = ""     
##    
##    sel = Selector(response)   
##    item ["LYSProduct_Name"] = sel.xpath("//h1/text()").extract()[0].replace(",","")
##    item ["LYSURL"] = response.url
##    sp = response.xpath("//span[@class='RetailPrice']/strike/text()").extract()
##    if sp:
##      item ["LYSSP"] = response.xpath("//em[@class='ProductPrice VariationProductPrice']/text()").extract()[0].replace(",","").split("Rs ")[-1]
##      item ["LYSMRP"] = response.xpath("//span[@class='RetailPrice']/strike/text()").extract()[0].replace(",","").split("Rs ")[-1]
##    else:
##      item ["LYSSP"] = ""
##      item ["LYSMRP"] = response.xpath("//em[@class='ProductPrice VariationProductPrice']/text()").extract()[0].replace(",","").split("Rs ")[-1]        
##    stock = response.xpath("//div[@class='stockIcon Out Of Stock']").extract()
##    if stock:
##      item ["LYSStock"] = "Out of Stock"
##    else:
##      item ["LYSStock"] = "In Stock"
##      
##    request=Request("http://www.snapdeal.com/search?noOfResults=20&keyword="+'"'+item ["LYSProduct_Name"]+'"', self.snapdeal)    
##    request.meta["item"] = item
##    return request
##        
##  def snapdeal(self,response):
##    
##    item = response.meta['item']    
##    sel = Selector(response)    
##    #Checking if the Search Term Exists on Domain
##    error  = response.xpath("//span[@id='errorKeyword']").extract()
##    x = response.xpath("//div[@class='noSearchMatching-text']")
##    soldout = response.xpath("//div[@class='hoverProductImage product-image prodSoldout']").extract()
##    if x or error:
##      item ["SnapdealProductName"] = "Product Not Found on Snapdeal.com"
##      request=Request("http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="+''+item ["LYSProduct_Name"]+'', self.amazonin)
##      request.meta["item"] = item
##      return request      
##    elif soldout:
##      pname = response.xpath("//div[@class='hoverProductImage product-image prodSoldout'][1]/a/img/@alt").extract()[0]
##      if pname.replace(" ","") == item["LYSProduct_Name"].replace(" ",""):
##        item["SnapdealMatch"] = "Exact Match"      
##      request = Request(response.xpath("//div[@class='hoverProductImage product-image prodSoldout'][1]/a/@href").extract()[0],callback=self.snapdealitems) #For Parsing Information if search keyword found      
##      request.meta["item"]  = item
##      return request      
##    else:      
##      pname = response.xpath("//div[@class='hoverProductImage product-image '][1]/a/img/@alt").extract()[0]
##      if pname.replace(" ","") == item["LYSProduct_Name"].replace(" ",""):
##        item["SnapdealMatch"] = "Exact Match"
##      request = Request(response.xpath("//div[@class='hoverProductImage product-image '][1]/a/@href").extract()[0],callback=self.snapdealitems) #For Parsing Information if search keyword found 
##      request.meta["item"]  = item
##      return request
##
##  def snapdealitems(self,response):
##    sel = Selector(response)
##    item = response.meta['item']
##    name = response.url
##    mrp = response.xpath("//span[@id='original-price-id']/text()").extract()
##    if mrp:
##      item ["SnapdealSP"] = response.xpath("//span[@id='selling-price-id']/text()").extract()[0]
##      item ["SnapdealMRP"] = response.xpath("//span[@id='original-price-id']/text()").extract()[0]
##    else:
##      item ["SnapdealMRP"] = response.xpath("//span[@id='selling-price-id']/text()").extract()[0]
##      
##    item ["SnapdealURL"] = response.url   
##    item ["SnapdealProductName"] = response.xpath("//h1[@itemprop='name']/text()").extract()[0].replace(",","")
##    stock = response.xpath("//div[@class='notifyMe-soldout']").extract()
##    if stock:
##      item["SnapdealStock"] = "Out Of Stock"
##    else:
##      item["SnapdealStock"] = "In Stock"
##
##    request=Request('http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords='+item ["LYSProduct_Name"]+'', self.amazonin)    
##    request.meta["item"] = item
##    return request
##  def amazonin(self,response):
##    
##    item = response.meta['item']
##    sel = Selector(response)
##    result =  response.xpath("//html").extract()
##    item["AmazonMatch"] = result
##    return item
####    if result:
####      url = response.xpath("//a[@class='a-link-normal s-access-detail-page  a-text-normal']/@href").extract()[0]
####      pname = response.xpath("//a[@class='a-link-normal s-access-detail-page  a-text-normal']/@title").extract()[0]
####      if pname.replace("Racquet","Racket").replace(" ","") == item["LYSProduct_Name"].replace(" ","") :
####        item["AmazonMatch"] = "ExactMatch"            
####      request = Request(url,callback=self.amazoninitems)
####      request.meta["item"] = item
####      return request
####     
######      request=Request("http://www.flipkart.com/search?q="+item ["LYSProduct_Name"], self.flipkart)
######      request.meta["item"] = item
######      return request
####    else:
####      item ["AmazonProductName"] = "No Product Found at Amazon.in"
####      self.to_csv(item)
####      return item
##      
##    
##  def amazoninitems(self,response):
##    sel = Selector(response)
##    item = response.meta['item']
##    item ["AmazonURL"] = response.url
##    item ["AmazonProductName"] = response.xpath("//h1/span[@id='productTitle']/text()").extract()[0].replace(",","")   
##    mrp = response.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()").extract()
##    saleprice = response.xpath("//span[@id='priceblock_saleprice']/text()").extract()
##    ourprice = response.xpath("//span[@id='priceblock_ourprice']").extract()
##    item ["AmazonMRP"] = ""
##    saleshipping = response.xpath("//span[@class='a-size-base a-color-secondary']/text()").extract()
##    url1 = response.xpath("//span[@class='a-size-medium a-color-success']/a/@href").extract()
##    
##    if mrp and saleprice:      
##      item ["AmazonSP"] = response.xpath("//span[@id='priceblock_saleprice']/text()").extract()[0].replace(",","")
##      item ["AmazonMRP"] = response.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()").extract()[0].replace(",","")
##    elif mrp and ourprice:
##      item ["AmazonSP"] = response.xpath("//span[@id='priceblock_ourprice']/text()").extract()[0].replace(",","")
##      item ["AmazonMRP"] = response.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()").extract()[0].replace(",","")
##    elif saleshipping and mrp:
##      item ["AmazonSP"] = response.xpath("//span[@class='a-size-base a-color-secondary']/text()").extract()[0].replace(",","")
##      item ["AmazonMRP"] = response.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()").extract()[0].replace(",","")
##    elif saleprice:
##      item ["AmazonSP"] = response.xpath("//span[@id='priceblock_saleprice']/text()").extract()[0].replace(",","")
##    elif ourprice:
##      item ["AmazonSP"] = response.xpath("//span[@id='priceblock_ourprice']/text()").extract()[0].replace(",","").replace(" ","")
##    elif url:#Fetching from MarketPlace Listings
##      url = response.xpath("//span[@class='a-size-medium a-color-success']/a/@href").extract()[0]
##      request = Request("http://www.amazon.in/"+url,callback=self.amazonmarketplace)
##      request.meta["item"] = item
##      return request    
##      
##    self.to_csv(item)
##    return item
###Calling flipkart
####    request=Request("http://www.flipkart.com/search?q="+item ["LYSProduct_Name"],callback= self.flipkart)    
####    request.meta["item"] = item
####    return request
##
##  def amazonmarketplace(self,response):
##    
##    sel = Selector(response)
##    item = response.meta['item']
##    sp = response.xpath("//span[@style='text-decoration: inherit; white-space: nowrap;']/text()").extract()[0].replace(",","")
##    shippingcost = response.xpath("//span[@class='olpShippingPrice']/span/text()").extract()
##    if shippingcost:
##      item ["AmazonSP"] = str(float(sp) + float(response.xpath("//span[@class='olpShippingPrice']/span/text()").extract()[0].replace(",","")))
##    self.to_csv(item)
##    return item
###Calling flipkart
####    request=Request("http://www.flipkart.com/search?q="+item ["LYSProduct_Name"],callback= self.flipkart)    
####    request.meta["item"] = item
####    return request
####      
##    
####  
####  def flipkart(self,response):   
####    sel = Selector(response)
####    item = response.meta['item']
####    noresult = response.xpath("//div[@class='noResults']").extract()
####    if noresult:
####      item["FlipkartProductName"] = "No Product Found"
####      self.to_csv(item)   
####      return item
####    else:
####      pname = response.xpath("//div[@class='pu-title fk-font-13']/a/@title").extract()[0]
####      if pname.replace("Racquet","Racket") == item["LYSProduct_Name"]:
####        item["FlipkartMatch"] = "Exact Match"
####              
####      url = "http://www.flipkart.com"+ response.xpath("//div[@class='pu-title fk-font-13']/a/@href").extract()[0]
####      request=Request(url, callback = self.flipkartitems)
####      request.meta["item"] = item
####      return request
####
####    
####           
####  def flipkartitems(self,response):    
####    sel = Selector(response)
####    item = response.meta['item']
####        
####    item["FlipkartProductName"] = response.xpath("//h1[@class='title']/text()").extract()[0].replace(",","")
####    item["FlipkartURL"] = response.url
####
####    mrp = response.xpath("//span[@class='price']/text()").extract()
####    if mrp:
####      item["FlipkartMRP"] = response.xpath("//span[@class='price']/text()").extract()[0].replace(",","").replace("Rs.","")
####
####    sp = response.xpath("//span[@class='selling-price omniture-field']/text()").extract()
####    if sp:
####      item["FlipkartSP"] = response.xpath("//span[@class='selling-price omniture-field']/text()").extract()[0].replace(",","").replace("Rs.","")
####      
####    stock = response.xpath("//div[@class='out-of-stock-status']").extract()
####    if stock:
####      item["FlipkartStock"] = "Out of Stock"
##
##
##
  
    
