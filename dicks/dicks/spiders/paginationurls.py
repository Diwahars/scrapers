# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
# from scrapy.selector import HtmlXPathSelector
# from scrapy.spider import BaseSpider
# from dicks.items import DicksItem
# import urlparse 
# from scrapy.http.request import Request
# from scrapy.selector import Selector
# import re
# import json, csv

# output = open("pagination.csv","wb")
# mywriter = csv.writer(output)
# f = open("categories.csv")
# csv_file = csv.reader(f)
# urllist = []
# lyscat = []
# priceid=[]
# for row in csv_file:
  # urllist.append(row[0])
  # lyscat.append(row[2])
  # priceid.append(row[3])


# class PageSpider(CrawlSpider):
  # name = "pages"
  # allowed_domains = ["dickssportinggoods.com"]
  # start_urls = [
    
    # url.strip() for url in urllist]
    
      

  # def parse(self, response):
  
   # sel = Selector(response)
   # item = DicksItem()
   # category = price =''

   # for i in range(len(urllist)):
     # if response.url.strip() == urllist[i].strip():
       # category = lyscat[i]
       # price = priceid[i]
       # break
    
   # pages = response.xpath('//span[@class="pages"][1]/a[last()]/@href').extract()
   
   # if pages:
     # pages = pages[0]
     # pages = int(pages.split("page=")[-1])

     # for t in range(1,pages+1):
       # url =  response.url+"&page="+str(t)
       # print url
       # row = (url,category,price)
       # mywriter.writerow(row)
   # else:
     # row = (response.url,category,price)
     # mywriter.writerow(row)
      
       
