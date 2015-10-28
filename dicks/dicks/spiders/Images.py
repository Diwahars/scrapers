from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider
from dicks.items import DicksItem
import urlparse ,re, json, unicodecsv,csv
from scrapy.http.request import Request
rulesfile = open("imageurl.csv","wb")

productcount = 0
pagenamelist = []

header = ('Item Type','Product ID','Product Name','Brand Name','Price','Retail Price','Sale Price','Product Description','Product Code/SKU','Bin Picking Number','Category',
                 'Option Set','Product Availability','Current Stock Level','Free Shipping','Sort Order','Meta Description','Page Title',''
             'Product Image Description - 1','Product Image Is Thumbnail - 1',''
             'Track Inventory','Product Image Sort - 1','Product Image Sort - 2','Product Image Sort - 3','Product Image Sort - 4','Product Image Sort-5','Product Image Sort-6','Product Image Sort-7','Product Image Sort-8',
             'Product Image File - 1','Product Image File - 2','Product Image File - 3','Product Image File - 4','Product Image File - 5 ',
    'Product Image File - 6','Product Image File - 7','Product Image File - 8')
rulewriter = unicodecsv.writer(rulesfile)


class MySpider(CrawlSpider):
	name = "images"
	allowed_domains = ["dickssportinggoods.com"]
	start_urls = [  
	"http://www.dickssportinggoods.com/product/index.jsp?productId=11829197",
# "http://www.dickssportinggoods.com/product/index.jsp?productId=11902520&kw=11902520&sr=1&origkw=11902520",
# "http://www.dickssportinggoods.com/product/index.jsp?productId=11902516&clickid=prod_cs&recid=Product_PageElement_product_rr_1_966",
    # url.strip() for url in urllist
		]
	def parse(self, response): 
		sel = Selector(response)	
		item = DicksItem()
		# item['image_urls']= ["http://www.dickssportinggoods.com/"+image for image in sel.xpath("//@data-enh").extract()]		
		imagescript = sel.xpath('//script[contains(text(), "productJson")]').extract()[0].split('availableColors":')[-1].split("]")[0]+']'
		imageDict = json.loads(imagescript)   
		urls = []
		
		for k in imageDict:
			if 'enhancedImageURL' in k:
				url= "http://www.dickssportinggoods.com" +k['enhancedImageURL']				
				item['image_urls']= [url]
				# item['image_urls']+= [url]
				item['title'] = [k['id']]
				yield item
				
				
		
		# return item			
		# return item
		