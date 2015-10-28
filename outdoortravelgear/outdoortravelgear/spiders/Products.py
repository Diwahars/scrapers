from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from outdoortravelgear.items import BigCItem
import urlparse ,re, json, unicodecsv,csv
from scrapy.http.request import Request
output = open("Product_urls.csv","wb")
mywriter = unicodecsv.writer(output)
header = ('Product','Category')
mywriter.writerow(header)

class OutdoorGear(CrawlSpider):
    
    name = "products"
    allowed_domains = ["outdoortravelgear.com"]
    start_urls = [
        "http://www.outdoortravelgear.com/product-list/clothing/bottoms/"
    ]
    rules = (
    Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=("//div[@id='divMainCategory']//ul/li/a",)),
                 callback="parse_category" , follow= True),
    )
##    def parse(self, response):
    def parse_category(self, response):
        sel = Selector(response)
        item = BigCItem()
        item['Category'] = sel.xpath("//h1/strong/text()").extract()[0].strip()
        urls  = sel.xpath("//div[@id='productList']//ul/li/a/@href").extract()
        for url in urls:
            yield Request("http://www.outdoortravelgear.com"+url,
                              self.products,
                                  meta={'item':item})

    def products(self,response):
        print "Hello"
        sel = Selector(response)
        item = response.meta['item']
        producturls = sel.xpath("//div[@class='color_list']/a/@href").extract()
        for product in producturls:
            row = ("http://www.outdoortravelgear.com"+product,item['Category'])
            print row
            mywriter.writerow(row)
            
        yield 
        
         
            
            
        
        
        
       
    
           
       
            
                 
     

     
    
  
    



  
    
