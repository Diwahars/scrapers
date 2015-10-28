from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
import urlparse,re,json,unicodecsv
output = open("PresidencyCycles.csv","wb")
header = ('Item Type','Product ID','Product Name','Brand Name','Price','Retail Price','Sale Price','Product Description','Product Code/SKU','Bin Picking Number','Category',
                 'Option Set','Product Availability','Current Stock Level','Free Shipping','Sort Order','Meta Description','Page Title',''
             'Product Image Description - 1','Product Image Is Thumbnail - 1',''
             'Track Inventory','Product Image Sort - 1','Product Image Sort - 2','Product Image Sort - 3','Product Image Sort - 4','Product Image Sort-5','Product Image Sort-6','Product Image Sort-7','Product Image Sort-8',
             'Product Image File - 1','Product Image File - 2','Product Image File - 3','Product Image File - 4','Product Image File - 5 ',
    'Product Image File - 6','Product Image File - 7','Product Image File - 8')
mywriter = unicodecsv.writer(output)
mywriter.writerow(header)

urls = []
for i in range (1,9):
		urls.append("http://www.amazon.in/gp/search/ref=sr_pg_8?me=A10JV993YY4OZ1&rh=i%3Amerchant-items&page="+str(i)+"&ie=UTF8&qid=1432272490")

	
class PresidencyCycles(CrawlSpider):
	name = "presidencycycles"
	allowed_domains = ["amazon.in"]
	start_urls = [
				# "http://www.amazon.in/s/ref=sr_in_P_p_6_76?fst=as%3Aoff&rh=n%3A1984443031%2Cp_6%3AA10JV993YY4OZ1",
				
				url.strip() for url in urls
				]	
				
	rules = (
			# Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//*[@class="pagnNext"]',)), follow= True),
				# Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=("//*[@class='a-link-normal s-access-detail-page  a-text-normal']",)), 
				Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=("//*[@class='a-row a-spacing-none']",)), 
					callback="product_page" , follow= True),
			)
	# def parse(self,response):
	def product_page(self, response):		
		sel = Selector(response)		
		product_name = sel.xpath("//*[@id='productTitle']/text()").extract()[0]
		asin = sel.xpath("//*[@id='ASIN']/@value").extract()[0]
					
		brand_name = sel.xpath("//*[@id='brand']/text()").extract()[0]
		
		
		mrp = sel.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()")
		saleprice = sel.xpath("//span[@id='priceblock_saleprice']/text()")
		ourprice = sel.xpath("//span[@id='priceblock_ourprice']")			
		saleshipping = sel.xpath("//span[@class='a-size-base a-color-secondary']/text()")		
		product_code = sel.xpath("//@data-asin").extract()[0]
		meta = "Get your hands on the " + product_name + ". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"      
		if mrp and saleprice:
			sp = sel.xpath("//span[@id='priceblock_saleprice']/text()").extract()[0].replace(",","")
			mrp = sel.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()").extract()[0].replace(",","")
		elif mrp and ourprice:
			sp = sel.xpath("//span[@id='priceblock_ourprice']/text()").extract()[0].replace(",","")
			mrp = sel.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()").extract()[0].replace(",","")

		elif saleshipping and mrp:
			sp = sel.xpath("//span[@class='a-size-base a-color-secondary']/text()").extract()[0].replace(",","")
			mrp = sel.xpath("//td[@class='a-span12 a-color-secondary a-size-base a-text-strike']/text()").extract()[0].replace(",","")

		elif saleprice:
			sp = sel.xpath("//span[@id='priceblock_saleprice']/text()").extract()[0].replace(",","")
		elif ourprice:
			mrp = sel.xpath("//span[@id='priceblock_ourprice']/text()").extract()[0].replace(",","").replace(" ","")	
			sp = ''  		
		shipping_cost =sel.xpath("//span[@class='a-size-small a-color-secondary shipping3P']/text()").extract()[1].strip()
			
		try:
			shipping_cost =sel.xpath("//span[@class='a-size-small a-color-secondary shipping3P']/text()").extract()[1].strip()
			shipping_cost = float(shipping_cost.split()[0].replace(",","").replace("Rs.",""))
			if sp!='':
				sp = shipping_cost+float(sp.strip())
			
			mrp=shipping_cost + float(mrp.strip())
		except:
			pass
		
			
		description = ''.join(w for w in (sel.xpath("//ul[@class='a-vertical a-spacing-none']").extract()+sel.xpath("//div[@class='pdTab'][1]/table//tr").extract()))
						
		category = '/'.join(w for w in sel.xpath("//span[@class='zg_hrsr_ladder']/a/text()").extract())		
		product_row = ['Product','',product_name,brand_name,
							mrp,mrp,sp,description,product_code,'PresidencyCycles',category,
							product_name,"8-13 Working Days",'100','N',-250,meta,meta,meta,'Y','By Product',1,2,3,4,5,6,7,8]
							

		images = sel.xpath("//script[@type='text/javascript'][contains(text(),'colorImages')]").extract()[0]		
		images = re.findall(r'large":"(.*?)","',images)
		for image in images:
			product_row.append(image)
		mywriter.writerow(product_row)
		