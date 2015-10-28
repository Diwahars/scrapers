from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from findia.items import BigCItem
import urlparse, re, csv
f = open("categorization.csv")
csv_file = csv.reader(f)
fitindiacat = []
LYScat = []
for row in csv_file:
  fitindiacat.append(row[0])
  LYScat.append(row[1])

k = open("brands.csv")
brands_file = csv.reader(k)
brandlist = []
for row in brands_file:
  brandlist.append(row[0])

output = open("FitIndia.csv","wb")
mywriter = csv.writer(output)

header = ('Item Type','Product ID','Product Name','Brand Name',
          'Price','Retail Price','Sale Price',
          'Product Description','Product Code/SKU','Bin Picking Number','Category','Option Set','Product Availability',
          'Current Stock Level','Free Shipping','Sort Order','Meta Description','Page Title',''
          'Product Image Description - 1','Product Image Is Thumbnail - 1',''
          'Track Inventory','Product Image Sort - 1','Product Image Sort - 2','Product Image Sort - 3',
          'Product Image Sort - 4','Product Image Sort-5','Product Image Sort-6','Product Image Sort-7','Product Image Sort-8',
          'Product Image File - 1','Product Image File - 2','Product Image File - 3','Product Image File - 4','Product Image File - 5 ',
          'Product Image File - 6','Product Image File - 7','Product Image File - 8')
mywriter.writerow(header)



class FitIndia(CrawlSpider):
	name = "fitindia"
	allowed_domains = ["fitindia.net"]

	start_urls = [
				# "http://www.fitindia.net/st-550-spirit-treadmill.html"
					"http://www.fitindia.net/rehab.html",
					"http://www.fitindia.net/strength-equipment.html",
					"http://www.fitindia.net/accessories.html",
					"http://www.fitindia.net/fitness-equipment.html"
				]
	rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=("//li[contains(@class,'level1 nav-1')]/a/@href",)), follow= True),
				Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=("//div[@class='pages']",)), follow= True),
					Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="item-inner"]',))
					, callback="parse_items", follow= True),)

	
	def parse_items(self, response):
	# def parse(self, response):
		sel = Selector(response)            
		pname  = sel.xpath("//div[@class='product-name']/h1/text()").extract()[0].replace(",","-")
		for brandname in brandlist:        
			if brandname.lower() in pname.lower():          
				brand = brandname
				break
			else:
				brand = "Fit India"
		if 'IsoSolid' in pname:
			brand = "Iso Solid"         

		if brand == "Fit India":
			pname  = "Fit India "+sel.xpath("//div[@class='product-name']/h1/text()").extract()[0].replace(",","-")              
      
		meta = "Get your hands on the " + pname + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"      
		mrp = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/p[@class='old-price']/span[@class='price']").extract()     
		#Pricing
		try:
			if mrp:
				mrp = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/p[@class='old-price']/span[@class='price']/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
				sp = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/p[@class='special-price']/span[@class='price']/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
				
			else:
				mrp = response.xpath("//div[@class='product-shop span6']/div[@class='price-box'][1]/span[@class='regular-price']/span/text()").extract()[0].replace(",","").replace("\n","").replace("\r","").replace("Rs.","").replace(" ","")
				sp = '' 
		except:
			mrp = sp =  ''
					
			
		productcode = "FITINDIA"+sel.xpath("//div[@class='product-sku']/span/text()").extract()[0]   
		description = sel.xpath("//div[@class='std']").extract()
		description = ''.join(w.encode('utf-8') for w in description)
		description = re.sub(r'<i(.*?)me>','',description)
		description = re.sub(r'style="(.*?)"','',description)		
		
		#ImageFile
		img = response.xpath("//div[@class='more-views ma-more-img']/ul/li").extract()
		if img:
			images = response.xpath("//div[@class='more-views ma-more-img']/ul/li/a/@href").extract()
		else:
			images = sel.xpath("//ul/li[@class='thumbnail-item']/a/@href").extract()
		cat =sel.xpath("//div[@class='breadcrumbs']/ul/li[4]/a/text()").extract()
		cat2 =sel.xpath("//div[@class='breadcrumbs']/ul/li[3]/a/text()").extract()
		if cat:
			category = sel.xpath("//div[@class='breadcrumbs']/ul/li[4]/a/text()").extract()[0].replace(",","")
		elif cat2:
			category = sel.xpath("//div[@class='breadcrumbs']/ul/li[3]/a/text()").extract()[0].replace(",","")
		else:
			category= sel.xpath("//div[@class='breadcrumbs']/ul/li[1]/a/text()").extract()[0].replace(",","")        
		size = len(LYScat)
		for i in range(size):
			if category == fitindiacat[i]:          
				category = LYScat[i]          
				break
		row = ['Product','',pname,brand,
				mrp,mrp,sp,
				description,productcode,'FITINDIA',category,pname,"8-13 Working Days",'100','N',-250,meta,meta,meta,'Y','By Product',1,2,3,4,5,6,7,8]
		for image in images:
			row.append(image)
		mywriter.writerow(row)