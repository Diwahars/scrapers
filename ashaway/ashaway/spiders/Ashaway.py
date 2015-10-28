from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider
import urlparse ,re, json, unicodecsv,csv
from scrapy.http.request import Request
output = open("Ashaway.csv","wb")
header = ('Item Type','Product ID','Product Name','Brand Name','Price','Retail Price','Sale Price','Product Description','Product Code/SKU','Bin Picking Number','Category',
                 'Option Set','Product Availability','Current Stock Level','Free Shipping','Sort Order','Meta Description','Page Title',''
             'Product Image Description - 1','Product Image Is Thumbnail - 1',''
             'Track Inventory','Product Image Sort - 1','Product Image Sort - 2','Product Image Sort - 3',
             'Product Image File - 1','Product Image File - 2','Product Image File - 3','Product Image File - 4','Product Image File - 5 ',
    'Product Image File - 6','Product Image File - 7','Product Image File - 8')
mywriter = unicodecsv.writer(output)
mywriter.writerow(header)
class MySpider(CrawlSpider):
  name = "ashaway"
  allowed_domains = ["goode-sport.co.uk"]
  start_urls = [
"http://goode-sport.co.uk/buy/ashaway-seattle-shoe/"    
    ]
  rules = (
   Rule (SgmlLinkExtractor(allow=(),
           restrict_xpaths=("//ul[@class='grid']/li[1]/ul/li/a",))
			, follow= True),       
 Rule (SgmlLinkExtractor(allow=(),
           restrict_xpaths=("//ul[@class='grid page-links']",))
			, follow= True), 			
    Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=('//ul[@class="grid products"]',)),
                 callback="parse_product" , follow= True),
    )

	
	
  def parse_product(self, response):
	sel=Selector(response)
	productname = sel.xpath("//*[@id='article-header']/h1/text()").extract()[0]
	meta = "Buy "+productname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
	description = sel.xpath("//*[@class='article-content']").extract()
	description = ' '.join(w for w in description)
	images  = sel.xpath("//*[@class='gallery grid']//@href").extract()
	price  = sel.xpath("//p[@class='price']/text()").extract()[0].strip()
	category  = sel.xpath("//*[@class='grid history']//li[last()]//text()").extract()[0].strip()
	productid = sel.xpath("//fieldset/input[1]/@value").extract()[0]
	sizes = sel.xpath("//select/option/@value").extract()

	if len(sizes)>2:
		trackinventory  = 'By Option'
	else:
		trackinventory = 'By Product'
	tup = ('Product','',productname,'Ashaway',price,price,price,description,productid,'','',category,productname,'','N','',meta,meta,meta,'Y',
				trackinventory,'1','2','3')
	obj = list(tup)
	for image in images:
		url = "http://goode-sport.co.uk/" + image     
		obj.append(url)
		
	row = tuple(obj)
	mywriter.writerow(row)
	if len(sizes)>2:
		for size in sizes:
			row = ('SKU','','[S]Size= '+size,'','','','','',productid+size)
			mywriter.writerow(row)
			
		
	
	
	
	