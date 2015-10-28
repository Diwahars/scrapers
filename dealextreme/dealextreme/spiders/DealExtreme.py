from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider
import urlparse ,re, json, unicodecsv,csv
from scrapy.http.request import Request
f = open("DealExtreme.csv")
csv_file = csv.reader(f)
urllist =[]
for row in csv_file:
  urllist.append(row[0])  
output = open("DealExtreme_output.csv","wb")
mywriter = unicodecsv.writer(output)
header = ('Item Type','Product ID','Product Name','Brand Name','Price','Retail Price','Sale Price','Product Description','Product Code/SKU','Bin Picking Number','Category',
                 'Option Set','Product Availability','Current Stock Level','Free Shipping','Sort Order','Meta Description','Page Title',''
             'Product Image Description - 1','Product Image Is Thumbnail - 1',''
             'Track Inventory','Product Image Sort - 1','Product Image Sort - 2','Product Image Sort - 3','Product Image Sort - 4','Product Image Sort-5',
             'Product Image File - 1','Product Image File - 2','Product Image File - 3','Product Image File - 4','Product Image File - 5 ' )
mywriter = unicodecsv.writer(output)
mywriter.writerow(header)

class DealExtreme(CrawlSpider):
  name = "dealextreme"
  allowed_domains = ["dx.com"]
  start_urls = [
  
  url.strip() for url in urllist
    ]
  rules = (
   Rule (SgmlLinkExtractor(allow=(),
           restrict_xpaths=("//div[@class='pagenumber']",))
			, follow= True),        
    Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=("//p[@class='title']",)),
                 callback="parse_product" , follow= True),
    )
   
  def parse(self, response):
	
	sel = Selector(response)
	# LinkExtraction
	# script = sel.xpath("//script[contains(text(),'productAttrs: [')]").extract()[0]
	# script = re.findall(r'productAttrs(.*)',script)
	# links = re.findall(r'Url":(.*?)",',script[0])
	# for link in links:
		# link = "http://www.dx.com/p/"+link.replace('"',"")
		# row = [link]
		# mywriter.writerow(row)
	
	#ProductExtraction		
	pname = 'Impertus '+sel.xpath("//h1/span/text()").extract()[0]
	metainfo = "Buy "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
	images  = sel.xpath("//ul[@class='product-small-images']//img/@src").extract()
	price  = sel.xpath("//span[@id='price']/text()").extract()[0] 
	price =  float(price)*115/100*4
	prince = str(price)
	category = (sel.xpath('//div[@class="position"]/a[last()-1]/text()').extract()[0]+'/'+
					sel.xpath('//div[@class="position"]/a[last()]/text()').extract()[0])
	description = ["DISCLAIMER: LiveYourSport.com does not take responsibility for any support claims and technical troubleshooting."
						+"This product is not valid for any technical support, warranty after purchase or protected by our after sales services."
							+"We only offer protection against delivery damages and manufacturing defects claimed within 10 days of delivery of the product."]
	description = description.append(sel.xpath("//div[@id='overview']").extract() +sel.xpath("//div[id='specification']").extract())
											
	sku = sel.xpath("//span[@id='sku']/text()").extract()[0] + 'DXMDCHN'				
	row  = ["Product","",pname + '*',"Impertus",price*140/100,price*140/100,price,
				description,sku,'DEALEXTREME',category,pname,'12-19 Working Days',100,'N',-270,metainfo,metainfo,metainfo,
				'Y','By Product',1,2,3,4,5]
	for image in images:
		image = image.replace("//img","img")
		row.append(image)			
	mywriter.writerow(row)
	