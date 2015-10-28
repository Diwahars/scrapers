from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider
from junglee.items import JungleeItem
import urlparse
from scrapy.http.request import Request
import unicodecsv, csv

header =  ('Product Name','ASIN','Junglee URL', 'Image URL')
f = open("Junglee_Images.csv" ,"wb")
mywriter = unicodecsv.writer(f)
mywriter.writerow(header)

input_file = open("Input.csv")
csv_dict = csv.DictReader(input_file)
input_dict = {}

for row in csv_dict:
  input_dict[row['ASIN']] = row['seller-sku']




class MySpider(CrawlSpider):
  name = "images"
  allowed_domains = ["junglee.com"]
  start_urls = ["http://www.junglee.com/s/ref=sr_nr_p_wa_0?rh=i%3Aaps%2Ck%3Alive%20your%20sport&keywords=live%20your%20sport&amp;ie=UTF8&amp"]

  rules = (
           Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//div[@id="pagn"]',)), follow= True),
    Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="results-row"]',))
    , callback="parse_items", follow= True),)  

  def parse_items(self, response):
  # def parse(self, response):
    sel = Selector(response)
    asin = sel.xpath("//@asin").extract()[0]
    if asin in input_dict:
      
      product_name = sel.xpath("//h1[@class='productTitle']/text()").extract()[0]    
      row = [product_name, asin, response.url]

      try:
        alt_images = sel.xpath("//script[contains(text(),'imageJSON')]").extract()[0].split('[')[-1].split(']')[0].split(",")
        for image in alt_images:
          row.append(image.strip('"'))
      except:
        image = sel.xpath("//div[@id='mainImage']//img/@src").extract()[0]
        row.append(image)

      mywriter.writerow(row)

