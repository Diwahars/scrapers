from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
import urlparse
import re,unicodecsv,csv
output = open("JuriBazar_Images.csv","wb")
mywriter = unicodecsv.writer(output)
header = ('Name','Product Image Url -1','Product Image Url -2','Product Image Url -3'
          'Product Image Url -4','Product Image Url -5')

mywriter.writerow(header)

f = open("input.csv")
csv_file = csv.reader(f)
skulist = [] 
image1 = []
image2 = []
image3 = []
image4 = []
image5 = []

for row in csv_file:
    skulist.append(row[0])
    image1.append(row[1])
    image2.append(row[2])
    image3.append(row[3])
    image4.append(row[4])
    image5.append(row[5])
    
class Juribazar(CrawlSpider):
  name = "juribazar"
  start_urls = ["http://www.liveyoursport.com/products/fuel-elliptical-4-0"]
     

  def parse(self, response):
      print "hello"
      sel = Selector(response)
      for i in range(0,4):
          sku = skulist[i]
          request=Request(image1[i],self.snapdeal)
          
          

  def extractor(self,response):
      sel = Selector(response)
      imgurl = sel.xpath("//div[@class='preview-box']/img/@src").extract()[0]
      
      
          
          
          
    
