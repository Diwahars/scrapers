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

f = open("input.csv")
csv_file = csv.reader(f)
productname_list = []
for row in csv_file:
  productname_list.append(row[0])

class MySpider(CrawlSpider):
  dont_filter=True
  name = "imagescrapper"
  allowed_domains = ["snapdeal.com", "amazon.in", "amazon.com", "flipkart.com"]

  start_urls = [
    #"http://www.liveyoursport.com/products/tecnifibre-carboflex-125-basaltex-squash-racket"]
    url.strip() for url in productname_list]

  csvfile = None
  printHeader = True
  
  def to_csv(self, item):
    
    if self.printHeader:
      self.csvfile = open('ImageandDesc.csv','w')
    if self.csvfile:

      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='LYS Product Name,LYS URL,LYS Product Code,LYS Stock,,'
        strWrite +='Snapdeal Product Name,Snapdeal URL, SnapdealExactMatch'
        strWrite +='Amazon Product Name,Amazon URL, AmazonExactMatch'
        strWrite +='Product Description'
        strWrite +='Product Image File -1,Product Image File -2,Product Image File -3,Product Image File -4,Product Image File -5'

        strWrite += ' \n'
        self.printHeader = False

      strWrite += item["LYSProduct_Name"] + ',' + item["LYSURL"] + ',' + item["LYSID"] + ',' + item["LYSStock"] + ',,'
      strWrite += item ["SnapdealProductName"] + item ["SnapdealURL"]+ item["SnapdealMatch"]
      strWrite += item ["AmazonProductName"] + item ["AmazonURL"]+ item["AmazonMatch"] 
      strWrite += ';'.join(item["Description"]).replace(',',';').replace("\n","").replace("\r","") + ',' + ';'.join(item["imgurl"]).replace(',',';').replace("\n","").replace("\r","")
      strWrite +=  '\n'  
      

      self.csvfile.write(strWrite.encode('utf8'))


  #def lys(self,response):
  def parse(self,response):
    
    item = BigCItem()
    item["Description"] = "" 
    item["imgurl"] = "" 
    item["LYSID"] = ""
    item["AmazonMatch"] = "" 
    item["SnapdealStock"] = "" 
    item["LYSID"] = ""
    item ["SnapdealURL"] = ""
    item ["SnapdealSP"] = ""
    item ["SnapdealMRP"] = ""
    item ["SnapdealProductName"] = ""
    item ["AmazonURL"] = ""     
    item ["AmazonMRP"] = ""
    item ["AmazonSP"] = ""     
    item ["AmazonProductName"] = ""
    item ["AmazonMatch"] = item ["SnapdealMatch"] = ""
  
    
    sel = Selector(response)   
    item ["LYSProduct_Name"] = sel.xpath("//h1/text()").extract()[0].replace(",","")
    item ["LYSURL"] = response.url   

    stock = response.xpath("//div[@class='stockIcon Out Of Stock']").extract()
    if stock:
      item ["LYSStock"] = "Out of Stock"
    else:
      item ["LYSStock"] = "In Stock"
    
    request=Request("http://www.snapdeal.com/search?noOfResults=20&keyword="+'"'+item ["LYSProduct_Name"]+'"', self.snapdeal)    
    request.meta["item"] = item
    return request
        
  def snapdeal(self,response):
    
    item = response.meta['item']    
    sel = Selector(response)    
    #Checking if the Search Term Exists on Domain
    error  = response.xpath("//span[@id='errorKeyword']").extract()
    x = response.xpath("//div[@class='noSearchMatching-text']")
    soldout = response.xpath("//div[@class='hoverProductImage product-image prodSoldout']").extract()
    if x or error:
      item ["SnapdealProductName"] = "Product Not Found on Snapdeal.com"
      request=Request("http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="+''+item ["LYSProduct_Name"]+'', self.amazonin)
      request.meta["item"] = item
      return request      
    elif soldout:
      pname = response.xpath("//div[@class='hoverProductImage product-image prodSoldout'][1]/a/img/@alt").extract()[0]
      if pname.replace(" ","") == item["LYSProduct_Name"].replace(" ",""):
        item["SnapdealMatch"] = "Exact Match"      
      request = Request(response.xpath("//div[@class='hoverProductImage product-image prodSoldout'][1]/a/@href").extract()[0],callback=self.snapdealitems) #For Parsing Information if search keyword found      
      request.meta["item"]  = item
      return request
      
    else:      
      pname = response.xpath("//div[@class='hoverProductImage product-image '][1]/a/img/@alt").extract()[0]
      if pname.replace(" ","") == item["LYSProduct_Name"].replace(" ",""):
        item["SnapdealMatch"] = "Exact Match"
      request = Request(response.xpath("//div[@class='hoverProductImage product-image '][1]/a/@href").extract()[0],callback=self.snapdealitems) #For Parsing Information if search keyword found 
      request.meta["item"]  = item
      return request

  def snapdealitems(self,response):
    sel = Selector(response)
    item = response.meta['item']      
    item ["Description"] = sel.xpath("//div[@class='detailssubbox']/ul/li").extract()
    item ["SnapdealProductName"] = response.xpath("//h1[@itemprop='name']/text()").extract()[0].replace(",","")
    item ["SnapdealURL"] = response.url   
    item ["imgurl"] = response.xpath("//ul[@id='product-slider']/li/img/@src").extract()
    self.to_csv(item)
    return item   
       

  def amazonin(self,response):
    item = response.meta['item']
    sel = Selector(response)
    noresult =  response.xpath("//h1[@id='noResultsTitle']").extract()
    if noresult:
      
      item ["AmazonProductName"] = "No Product Found at Amazon.in"
      
      self.to_csv(item)
      return item
##      request=Request("http://www.flipkart.com/search?q="+item ["LYSProduct_Name"], self.flipkart)
##      request.meta["item"] = item
##      return request
    
    else:
      url = response.xpath("//a[@class='a-link-normal s-access-detail-page  a-text-normal']/@href").extract()[0]
      pname = response.xpath("//a[@class='a-link-normal s-access-detail-page  a-text-normal']/@title").extract()[0]
      if pname.replace("Racquet","Racket").replace(" ","") == item["LYSProduct_Name"].replace(" ","") :
        item["AmazonMatch"] = "ExactMatch"      
      
      request = Request(url,callback=self.amazoninitems)
      request.meta["item"] = item
      return request
    
  def amazoninitems(self,response):
    sel = Selector(response)
    item = response.meta['item']
    desc2 =  response.xpath("//ul[@class='a-vertical a-spacing-none']/li").extract()
    desc1 = response.xpath("//div[@class='productDescriptionWrapper']/text()").extract()
    desc3= response.xpath("//div[@class='aplus']/div/h5").extract()
    item ["AmazonURL"] = response.url
    item ["AmazonProductName"] = response.xpath("//h1/span[@id='productTitle']/text()").extract()[0].replace(",","")   
    if desc1:
      item ["Description"] = desc1
    elif desc1 and desc2:
      item ["Description"] = desc1 + desc2
    elif desc1 and desc2 and desc3:
      item ["Description"] = desc1 + desc2 + desc3

    item['imgurl'] = response.xpath("//span[@class='a-button-tex']/img/@src").extract()    
    self.to_csv(item)
    return item
   
  
  def flipkart(self,response):   
    sel = Selector(response)
    item = response.meta['item']
    noresult = response.xpath("//div[@class='noResults']").extract()
    if noresult:
      item["FlipkartProductName"] = "No Product Found"
      self.to_csv(item)   
      return item
    else:
      pname = response.xpath("//div[@class='pu-title fk-font-13']/a/@title").extract()[0]
      if pname.replace("Racquet","Racket") == item["LYSProduct_Name"]:
        item["FlipkartMatch"] = "Exact Match"
              
      url = "http://www.flipkart.com"+ response.xpath("//div[@class='pu-title fk-font-13']/a/@href").extract()[0]
      request=Request(url, callback = self.flipkartitems)
      request.meta["item"] = item
      return request

    
           
  def flipkartitems(self,response):    
    sel = Selector(response)
    item = response.meta['item']
        
    item["imgurl"] = response.xpath("//div[@class='imgWrapper']/img/@src").extract()
    desc = response.xpath("//ul[@class='keyFeaturesList']").extract()
    desc1 = response.xpath("//div[@class='description-text']").extract()
    if desc and desc1:
      item["Description"] = desc+desc1
    elif desc:
      item["Description"] = desc
    elif desc1:
      item["Description"] = desc1
      
    self.to_csv(item)
    return item


  
    
