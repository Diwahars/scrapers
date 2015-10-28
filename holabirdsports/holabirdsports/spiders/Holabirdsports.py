from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from holabirdsports.items import BigCItem
import urlparse,re,json,csv
from ..utilities import converter
output = open("HolabirdSports.csv","wb")
header = ('Item Type','Product ID','Product Name','Brand Name','Price','Retail Price','Sale Price','Product Description','Product Code/SKU','Bin Picking Number','Category',
                 'Option Set','Product Availability','Current Stock Level','Free Shipping','Sort Order','Meta Description','Page Title',''
             'Product Image Description - 1','Product Image Is Thumbnail - 1',''
             'Track Inventory','Product Image Sort - 1','Product Image Sort - 2','Product Image Sort - 3','Product Image Sort - 4','Product Image Sort-5','Product Image Sort-6','Product Image Sort-7','Product Image Sort-8',
             'Product Image File - 1','Product Image File - 2','Product Image File - 3','Product Image File - 4','Product Image File - 5 ',
    'Product Image File - 6','Product Image File - 7','Product Image File - 8')
mywriter = csv.writer(output)
mywriter.writerow(header)

class HolabirdSpider(CrawlSpider):
	name = "holabirdsports"
	allowed_domains = ["holabirdsports.com"]
	start_urls = [   
					"http://www.holabirdsports.com/shoes/women-s/indoor-squash-racquetball.html",
					"http://www.holabirdsports.com/shoes/men-s/indoor-squash-racquetball.html",
					"http://www.holabirdsports.com/shoes/women-s/tennis.html",
					"http://www.holabirdsports.com/shoes/junior-s/tennis.html",
					"http://www.holabirdsports.com/shoes/men-s/tennis.html",
					"http://www.holabirdsports.com/tennis/accessories/overgrips.html",
					"http://www.holabirdsports.com/tennis/accessories/replacement-grips.html",
					"http://www.holabirdsports.com/tennis/accessories/tape.html",
					"http://www.holabirdsports.com/tennis/accessories/grip-enhancement.html",
					"http://www.holabirdsports.com/tennis/clothing/socks.html",
					"http://www.holabirdsports.com/tennis/clothing/sweatbands.html",
					"http://www.holabirdsports.com/tennis/strings-stringing/string.html",
					"http://www.holabirdsports.com/tennis/strings-stringing/stencils-ink.html",
					"http://www.holabirdsports.com/tennis/strings-stringing/grommets-bumper-guards-2.html",
					"http://www.holabirdsports.com/tennis/strings-stringing/string-savers.html",
					# 'http://www.holabirdsports.com/tennis/accessories/replacement-grips/full-size-build-up-sleeve.html',

    ]
	rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=("//div[@class='pages']",)), callback="parse_category" , follow= True),)

	def parse_category(self, response):
		item = BigCItem()
		sel = Selector(response)
		if "&p=" in response.url:
			pagenumber = float(response.url.split("&p=")[-1])
		else:
			pagenumber = 1
		t = 0 + ((pagenumber-1)*16)       
		productpages = sel.xpath("//h2[@class='product-name']/a/@href").extract()
		productnames = sel.xpath("//h2[@class='product-name']/a/text()").extract()
		item["Sort_Order"] = {}
		for url in productpages:
		  item["Sort_Order"][url] = t
		  t=t+1
		
		for url,name in zip(productpages,productnames):
		  if "Nike" not in name:
			 request=Request(url, self.product_page)
			 request.meta["item"] = item
			 yield request
			 
	def product_page(self, response):
		item = response.meta['item']   
	# def parse(self, response):	
		# item = BigCItem()   
		sel = Selector(response)
		pname = sel.xpath("//meta[@property='og:title']/@content").extract()[0]
		pname = ''.join(pname).encode('utf-8')

		optionset = pname
		item["Product_Image_Description_1"] = "Buy "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
		item["MetaDescription"] = "Get your hands on the "+pname +". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
		item["TitleTag"] = "Buy the "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
		item["Brand_Name"]  = sel.xpath("//script[@type='text/javascript'][contains(text(),'Brand :')]").extract()[0].split("Brand : \'")[-1].split("\'")[0].encode('utf-8')
		script  =sel.xpath("//script[@type='text/javascript'][contains(text(),'Brand :')]").extract()[0]
		category  = sel.xpath("//div[@class='breadcrumbs']/ul/li[2]/a/text()").extract()[0]
		# category = ''
		#Pricing
		if response.xpath("//span[@class='msrp_price']/text()").extract():
			mrp = response.xpath("//span[@class='msrp_price']/text()").extract()[0].split("$")[-1]
			sp = script.split("Value : ")[-1].split(",")[0]
						
			if category =='Shoes':
			  mrp = converter.cleanup_price(mrp)
			  sp = converter.cleanup_price(sp)
			else:           
			   mrp = converter.cleanup_price(mrp,'Accessories')
			   sp = converter.cleanup_price(sp,'Accessories')
		else:
			mrp = response.xpath("//div[@class='add-to-cart-price']").extract()[0].split("$")[-1].split("<b")[0]			
			if category =='Shoes':
			  mrp = converter.cleanup_price(mrp,'Accessories')
			  sp = ''
			else:
			  mrp = converter.cleanup_price(mrp,'Accessories')
			  sp = ''

		print mrp			
  	  #categorization
		if category =="Shoes":
			x = sel.xpath("//div[@class='breadcrumbs']/ul/li[4]/a/text()").extract()[0]         
			if 'Squash' in x:         
				if "ASICS" in item["Brand_Name"]:
					sortorder = -350            
				elif "Salming" in item["Brand_Name"] or "adidas" in item["Brand_Name"]:
					sortorder = -330
				else:
					sortorder = -290
					
				if "Women" in pname:
					category = "Racket Sports/Squash/Squash Shoes/Women's Shoes; Racket Sports/Badminton/Badminton Shoes/Women's Shoes; Racket Sports/Table Tennis/Table Tennis Shoes; Team Sports/Volleyball/Volleyball Shoes/Women's Shoes; Shoes/Women's Shoes/Indoor Court Shoes"
				elif "Junior" in pname:
					category = "Racket Sports/Squash/Squash Shoes/Junior Shoes; Racket Sports/Badminton/Badminton Shoes; Racket Sports/Table Tennis/Table Tennis Shoes; Team Sports/Volleyball/Volleyball Shoes/Junior Shoes; Shoes/Junior Shoes/Indoor Court Shoes"
				else:
					category = "Racket Sports/Squash/Squash Shoes/Men's Shoes; Racket Sports/Badminton/Badminton Shoes/Men's Shoes; Racket Sports/Table Tennis/Table Tennis Shoes; Team Sports/Volleyball/Volleyball Shoes/Men's Shoes; Shoes/Men's Shoes/Indoor Court Shoes"
			  
			else:
				sortorder = -350
				if "Women" in pname:
					category = "Shoes/Women's Shoes/Tennis Shoes;Racket Sports/Tennis/Tennis Shoes/Women's Shoes"
				elif "Junior" in pname:
					category = "Shoes/Junior Shoes/Tennis Shoes;Racket Sports/Tennis/Tennis Shoes"
				else:
					category = "Shoes/Men's Shoes/Tennis Shoes;Racket Sports/Tennis/Tennis Shoes/Men's Shoes"
		else:
			sortorder = -250
			cat2 = sel.xpath("//div[@class='breadcrumbs']/ul/li[4]/a/text()").extract()[0]
			if cat2 == 'Overgrips':
				category = "Racket Sports/Tennis/Grips/Overgrips;Racket Sports/Squash/Racket Grips/Overgrips"
			elif cat2 == 'Replacement Grips':
				category = "Racket Sports/Tennis/Grips/Replacement Grips;Racket Sports/Squash/Racket Grips/Replacement Grips"
			elif cat2 == 'Tape':
				category = "Racket Sports/Tennis/Accessories/Tapes"
			elif cat2 == 'Grip Enhancement':
				category = "Racket Sports/Tennis/Grips/Grip Enhancements;Racket Sports/Tennis/Accessories/Grip Enhancements;Racket Sports/Squash/Racket Grips/Grip Enhancements"
				category = category + ";Racket Sports/Squash/Racket Grips/Grip Enhancements"
			elif cat2 == 'String':
				category = 'Racket Sports/Tennis/Strings'
			elif cat2 == 'Grommets, Bumper Guards':
				category = 'Racket Sports/Tennis/Accessories/Grommets, Bumper Guards;'
			elif cat2 == 'String Savers':
				category = 'Racket Sports/Tennis/Accessories/String Savers'
			elif cat2 == 'Stencils & Ink':
				category = 'Racket Sports/Tennis/Accessories/Stencils & Ink'
			elif cat2 == 'Socks':
				category = 'Racket Sports/Tennis/Apparel/Socks;Racket Sports/Tennis/Accessories/Socks;Shoes/Accessories/Socks/Tennis Socks'
				category = category +';Apparel/Accessories/Socks/Tennis Socks'
			elif cat2 == 'Sweatbands':
				category = "Apparel/Accessories/Headbands; Racket Sports/Squash/Accessories;Racket Sports/Tennis/Accessories;Run & Cycle/Running/Accessories"

		sortorder = sortorder + item["Sort_Order"][response.url]
		
		sku = sel.xpath("//script[@type='text/javascript'][contains(text(),'Brand :')]").extract()[0].split("prodid: \'")[-1].split("\'")[0].strip()+"HLABRD"
		description = sel.xpath("//div[@id='panel_description']/p").extract()
		if description:
			description = re.sub(r'<a(.*)>','',sel.xpath("//div[@id='panel_description']/p").extract()[0]).encode('utf-8')
		else:
			description = ''
			description = ''.join(description).encode('utf-8')
		imagefiles = sel.xpath("//li/a[contains(@onclick,'return hb_thumbnail_click')]/@onmouseover").extract()
		if not imagefiles:
			imagefiles = sel.xpath("//img[@id='image']/@src").extract()			
		sizescript = response.xpath("//script[@type='text/javascript'][contains(text(),'var spConfig')]")
		if sizescript:
			trackinventory = 'By Option'
		else:
			trackinventory = 'By Product'

		row = ["Product",'',pname+"*"
				,item["Brand_Name"],  mrp,mrp,sp,          #price
			   description,sku,"HOLABIRDSPORTS",category,optionset,"15-21 Working days","100",'N',sortorder,
			   item["MetaDescription"],item["TitleTag"],item["Product_Image_Description_1"],"Y",trackinventory,
			   "1","2","3","4","5","6","7","8"]	
		for files in imagefiles:
			image = files.replace("hb_image_swap('","").strip(')').strip("'").replace("260x260","500x500")
			row.append(image)		
		mywriter.writerow(row)			
		
		if sizescript:
			sizescript = sel.xpath("//script[@type='text/javascript'][contains(text(),'var spConfig')]").extract()[0].split('"template')[0]
			sizescript = sizescript.replace('<script type="text/javascript">','')
			sizescript = re.sub(r'var(.*?)options":','',sizescript)
			sizescript = re.sub(r'"oldPrice(.*?)}','',sizescript)
			sizescript = tempscript = re.sub(r'"id":','',re.sub(r',"label":',':',sizescript))
			sizescript = re.sub(r'code"(.*)}','',re.sub(r'](.*),','',sizescript))
			sizescript = sizescript.replace(",,{",',') + '}'
			sizescript = sizescript.split("[")[-1].replace(",}","}")
			sizedict = json.loads(sizescript.replace(",}","}"))       
		widthscript = response.xpath("//script[@type='text/javascript'][contains(text(),'hb_shoe_width')]").extract()
		if widthscript:
			widthscript= tempscript
			widthscript= re.sub('(.*?)options":\[','',widthscript)
			widthscript= '['+re.sub(']}','',re.sub(',,{',',',widthscript))+']'
			widthscript= widthscript.replace(",},","}")
			widthdict =json.loads(widthscript)[0]
		if sizescript:
			trackinventory = 'By Option'
			stockscript = sel.xpath("//script[@type='text/javascript'][contains(text(),'var stStatus')]/text()").extract()[0]
			stockscript = re.sub("/",",",
								  re.sub(",",":",re.sub(r':{,','/',
									   re.sub(r'var(.*?)us','',
											  (re.sub(r'"is_in(.*?)}','',stockscript))))))

			stockscript = stockscript.split(":{}")[0].split("s(")[-1]
			stockscript = stockscript.replace("{","").replace('"',"")
			stockscript = [w for w in stockscript.split(',')]
			c=0
			stocklist ={}
			for i in range(len(stockscript)):
				for key in sizedict:          
					if key == (stockscript[i].split(':')[0]):
						stocklist['size',c] = '[S]Size= US '+sizedict[key].strip()
						stocklist['SKU',c] = key
						break
				if widthscript:
					for key in widthdict:
						if key == (stockscript[i].split(':')[1]):
							stocklist['width',c] = ',[S]Width= '+widthdict[key]
							stocklist['SKU',c] = stocklist['SKU',c]+ key
							break
				else:
					stocklist['width',c] = ''
				stocklist['SKU',c] = stocklist['SKU',c]
				row = ('SKU','',stocklist['size',c]+stocklist['width',c],'','','','','',sku+stocklist['SKU',c],
				'HOLABIRDSPORTS','','','','100')
				mywriter.writerow(row)

				c=c+1
