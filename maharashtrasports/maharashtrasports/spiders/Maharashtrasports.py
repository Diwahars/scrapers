from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider

import urlparse ,re, json, unicodecsv,csv
from scrapy.http.request import Request
output = open("MaharashtraSports.csv","wb")
mywriter = unicodecsv.writer(output)
header = ('Item Type','Product ID','Product Name','Brand Name','Price','Retail Price','Sale Price','Product Description','Product Code/SKU','Bin Picking Number','Category',
                 'Option Set','Product Availability','Current Stock Level','Free Shipping','Sort Order','Meta Description','Page Title',''
             'Product Image Description - 1','Product Image Is Thumbnail - 1',''
             'Track Inventory','Product Image Sort - 1','Product Image Sort - 2','Product Image Sort - 3','Product Image Sort - 4',
             'Product Image File - 1','Product Image File - 2','Product Image File - 3','Product Image File - 4')
mywriter.writerow(header)

class MySpider(CrawlSpider):
	name = 'maharashtrasports'
	allowed_domains = ['maharashtrasports.in']
	start_urls = ['http://www.maharashtrasports.in/']
	rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//li[@class="expandable"]/ul/li',))
    , callback="parse_items", follow= True),)
	
	def parse_items(self,response):
		sel = Selector(response)
		name =  sel.xpath("//div[@class='headPad']/text()").extract()[0].split()
		name = ' '.join(name[w] for w in range(1,len(name)))
		meta  = "Get your hands on the "+name +". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
		sku = response.url.split("pid=")[-1].split('&')[0] + 'MHSPORTS'	
		
		images  = sel.xpath("//ul/li/img/@src").extract()
		description =  sel.xpath("//div[@style='padding:10px 0px 0px 10px;']").extract()
		row  = ['Product','',name,'Maharashtra Sports','','','',
				description,sku,'MaharashtraSports','',name,'','100','N','-150',
				meta,meta,meta,'Y','By Product',1,2,3,4]
		for image in images:
			row.append('http://www.maharashtrasports.in/'+image)
		mywriter.writerow(row)
			
		
		
		
	