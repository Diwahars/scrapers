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
  name = "flipkart"
  allowed_domains = ["snapdeal.com", "amazon.in", "amazon.com", "flipkart.com"]

  start_urls = [
    #"http://www.liveyoursport.com/products/tecnifibre-carboflex-125-basaltex-squash-racket"]
    url.strip() for url in productname_list]

  csvfile = None
  printHeader = True
  
  def to_csv(self, item):
    
    if self.printHeader:
      self.csvfile = open('PriceCompare_Output(Snapdeal,Amazon,Flipkart).csv','w')
    if self.csvfile:

      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='LYS Product Name,LYS URL,LYS Product Code, LYS MRP,LYS SP,LYS Stock,,'
        strWrite +='Snapdeal Product Name,Snapdeal URL, Snapdeal MRP,Snapdeal SP,Snapdeal Stock,Snapdeal Match,,'
        strWrite +='Amazon Product Name,Amazon URL, Amazon MRP,Amazon SP, Amazon Stock,Amazon Match,,'
        strWrite +='Flipkart Product Name,Flipkart URL, Flipkart MRP,Flipkart SP, Flipkart Stock,Flipkart Match,,'

        strWrite += ' \n'
        self.printHeader = False

      strWrite += item["LYSProduct_Name"] + ',' + item["LYSURL"] + ',' + item["LYSID"] + ',' + item["LYSMRP"] + ',' + item["LYSSP"] + ',' + item["LYSStock"] + ',,'
      strWrite += item["SnapdealProductName"] + ',' + item ["SnapdealURL"] + ',' + item["SnapdealMRP"] + ',' + item ["SnapdealSP"] + ','+  item["SnapdealStock"] + ',' + item["SnapdealMatch"] + ',' +','
      strWrite += item["AmazonProductName"] + ',' + item ["AmazonURL"] + ',' +item ["AmazonMRP"] + ',' + item ["AmazonSP"] + ',' + item["AmazonStock"] + "," + item["AmazonMatch"] + ',,'
      strWrite += item["FlipkartProductName"] + ',' + item ["FlipkartURL"] + ',' +item ["FlipkartMRP"] + ',' + item ["FlipkartSP"] + ',' + item["FlipkartStock"] + "," + item["FlipkartMatch"] + ',,'
      strWrite +=  '\n'  
      

      self.csvfile.write(strWrite.encode('utf8'))


  #def lys(self,response):
  def parse(self,response):
    
    item = BigCItem()
    item["SnapdealMatch"] = "" 
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
    item ["AmazonMatch"] = ""
    item ["AmazonStock"] = item["FlipkartProductName"] = item["FlipkartURL"] = item["FlipkartMRP"] = item["FlipkartSP"] =  item["FlipkartStock"] = item["FlipkartMatch"] = ""     
    
    sel = Selector(response)   
    item ["LYSProduct_Name"] = sel.xpath("//h1/text()").extract()[0].replace(",","")
    item ["LYSURL"] = response.url
    

    sp = response.xpath("//span[@class='RetailPrice']/strike/text()").extract()
    if sp:
      item ["LYSSP"] = response.xpath("//em[@class='ProductPrice VariationProductPrice']/text()").extract()[0].replace(",","").split("Rs ")[-1]
      item ["LYSMRP"] = response.xpath("//span[@class='RetailPrice']/strike/text()").extract()[0].replace(",","").split("Rs ")[-1]
    else:
      item ["LYSSP"] = ""
      item ["LYSMRP"] = response.xpath("//em[@class='ProductPrice VariationProductPrice']/text()").extract()[0].replace(",","").split("Rs ")[-1]
      
  
    stock = response.xpath("//div[@class='stockIcon Out Of Stock']").extract()
    if stock:
      item ["LYSStock"] = "Out of Stock"
    else:
      item ["LYSStock"] = "In Stock"
    
#Calling flipkart
    request=Request('http://www.flipkart.com/search?q="'+item ["LYSProduct_Name"]+'"',callback= self.flipkart)    
    request.meta["item"] = item
    return request
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
        
    item["FlipkartProductName"] = response.xpath("//h1[@class='title']/text()").extract()[0].replace(",","")
    item["FlipkartURL"] = response.url

    mrp = response.xpath("//span[@class='price']/text()").extract()
    if mrp:
      item["FlipkartMRP"] = response.xpath("//span[@class='price']/text()").extract()[0].replace(",","").replace("Rs.","")

    sp = response.xpath("//span[@class='selling-price omniture-field']/text()").extract()
    if sp:
      item["FlipkartSP"] = response.xpath("//span[@class='selling-price omniture-field']/text()").extract()[0].replace(",","").replace("Rs.","")
      
    stock = response.xpath("//div[@class='out-of-stock-status']").extract()
    if stock:
      item["FlipkartStock"] = "Out of Stock"

    self.to_csv(item)
    return item



  
    
