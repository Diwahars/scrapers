
# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
# from scrapy.selector import HtmlXPathSelector, Selector
# from scrapy.spider import BaseSpider
# from dicks.items import DicksItem
# from ..library import mycsv,lyslib,helpers,variants
# import urlparse ,re, json, unicodecsv,csv
# from scrapy.http.request import Request
# rulesfile = open("Rules.csv","wb")

# urllist,lyscat,priceid = lyslib.categories('categories_flipkart.csv') #Creating Category List
# brandlist = lyslib.brands() #Creating Brand List for Comparison 
# mycsv.initialize_csv() #Creating output CSVs and writing Headers
# productcount = 0 #Product Count for Splitting Products into multiple files
# global category
# category =''

# print len(urllist)


# class MySpider(CrawlSpider):
# 	name = "dicks_flipkart"
# 	allowed_domains = ["dickssportinggoods.com"]
# 	start_urls = [  
# 	# "http://www.dickssportinggoods.com/product/index.jsp?productId=52152836"
# 	# "http://www.dickssportinggoods.com/family/index.jsp?categoryId=4414164&bc=CatGroup_MensAthleticShirts_R1_C2_ShortSleeves"
# # "http://www.dickssportinggoods.com/product/index.jsp?productId=11829197",
# # "http://www.dickssportinggoods.com/product/index.jsp?productId=11902520&kw=11902520&sr=1&origkw=11902520",
# # "http://www.dickssportinggoods.com/product/index.jsp?productId=11902516&clickid=prod_cs&recid=Product_PageElement_product_rr_1_966",
#     url.strip() for url in urllist	
# 	]	
	
# 	def parse(self, response):
# 		sel = Selector(response)
# 		item = DicksItem()		
# 		if "&page=" in response.url: # Extracting the Page Number and then using that to assign sort.
# 			pagenumber = float(response.url.split("&page=")[-1]) 
# 		else:
# 			pagenumber = 1		
# 		t = 0 + ((pagenumber-1)*48)
# 		item["Sort_Order"] = {}
		
# 		producturls= sel.xpath("//div[@class='prod-details']/h2/a/@href").extract()
# 		productnames = sel.xpath("//div[@class='prod-details']/h2/a/@title").extract()		
		
# 		for url,name in zip(producturls,productnames):
# 			item["Sort_Order"]["http://www.dickssportinggoods.com"+url] = t
# 			t=t+1
			
# 		for i in range(len(urllist)): #comparing the Category URL and assigning LYS Categorization
# 			if urllist[i] == response.url:
# 				item['Category'] = lyscat[i]
# 				item['id1'] = priceid[i]
# 				break
		
# 		for url,name in zip(producturls,productnames):       
# 			if "Fitbit" not in name:         
# 				request=Request("http://www.dickssportinggoods.com"+url, self.product_page)
# 				request.meta["item"] = item
# 				yield request

# 	# def parse(self, response):   
# 	# 	item = DicksItem()
# 	# 	item['Category']= '' 
# 	# 	item['id1']='4'
# 	def product_page(self, response):	
# 		item = response.meta['item']      		
# 		global productcount
# 		productcount += 1
# 		mywriter = mycsv.file_to_write(productcount) #Configuring file to write on based on productcount

		
# 		sel = Selector(response)

# 		pname = sel.xpath("//h1/text()").extract()[0].encode('utf-8')		
# 		item["Brand_Name"] = helpers.brandname(pname,brandlist)			   
		
# 		item ["Product_Name"] =  pname
# 		item["Option_Set"] = pname +'1'
		
# 		item["Product_Image_Description_1"],item["MetaDescription"],item["TitleTag"] = helpers.meta_information(pname)
		
# 		pcode  =sel.xpath("//span[@itemprop='productId sku']/@content").extract()[0].replace("pid:","")
# 		item ["Product_Code"] = pcode + "DSPRTG"
# 		item["Product_Description"] = sel.xpath("//div[@class='prod-sub-content']").extract()[0]
# 		item["Product_Description"] = ''.join(item["Product_Description"]).encode('utf-8')   
	
# 		mrp = sel.xpath("//span[@class='price was']/text()| //span[@class='now']/text()").extract()[0].replace("$","").split("to ")[-1]
		
# 		try:			
# 			sp = sel.xpath("//span[@class='now']/text() | //span[@id='SalePrice']/text()").extract()[0].replace("$","").split("to ")[-1]			
# 		except:
# 			sp = 0
		
# 		item['Retail_Price'],item['Sale_Price']= helpers.pricing_parent(mrp,sp,item['id1'])	
		
# 		sortorder = helpers.sortorder_brand(item["Brand_Name"]) + item["Sort_Order"][response.url]
		
# 		script = {}   
# 		script = sel.xpath('//script[contains(text(), "productJson")]').extract()[0]
# 		c = script.count("'IN_STOCK'")
# 		if c>1:
# 			trackinventory = 'By Option'
# 		else:
# 			trackinventory = 'By Product'

# 		productrow = ["Product","",item["Product_Name"]+"*",item["Brand_Name"],
# 				item['Retail_Price'],item['Retail_Price'],item["Sale_Price"], #price
# 				item["Product_Description"],item ["Product_Code"],"DICKSPORTINGGOODS",item['Category'],item["Product_Name"]+'1',"15-23 Working days","100","N",sortorder,'Y',
# 				item["MetaDescription"],item["TitleTag"],item["Product_Image_Description_1"],"Y",trackinventory,
# 				"1","2","3","4","5","6","7","8"]
	   
# 		images = sel.xpath("//@data-enh").extract()
# 		i =0 
# 		colorid = ''
		
# 	   #IMAGES
# 		imagescript = sel.xpath('//script[contains(text(), "productJson")]').extract()[0].split('availableColors":')[-1].split("]")[0]+']'
# 		imageDict = json.loads(imagescript)   
# 		for index, image in enumerate(images):
# 			url ="http://www.dickssportinggoods.com" + image
# 			productrow.append(url)
# 			if index == 7:
# 				break
	
		 
# 		 # STORING VARIANT IMAGES STARTS HERE-------------------------------
# 		 # item['image_urls']= [url]
		 
# 		 # for k in imageDict:
# 			# try:
# 				# if image == k['enhancedImageURL']:
# 					# colorid = k['id']
# 					# break
# 			# except:
# 				# pass
# 		# if colorid!='':
# 			# filename = item ["Product_Code"]+"_"+k['id']		
# 		# else:		
# 			# filename = item ["Product_Code"]+'main'+str(i)		
# 		# i = i+1
		 
# 		 # item['title'] = [filename]	
# 		 # productrow.append('http://liveyoursport.com/product_images/dicks/'+filename+'.jpg')
# 		 # yield item
		
		 
# 	   # for k in imageDict:	
# 		# if 'enhancedImageURL' in k:
# 			# url= "http://www.dickssportinggoods.com" +k['enhancedImageURL']				
# 			# item['image_urls']= [url]
# 			# filename = item ["Product_Code"]+"_"+k['id']
# 			# item['title'] = [filename]		
# 			# productrow.append('http://liveyoursport.com/product_images/dicks/'+filename+'.jpg')
# 			# yield item
# 	   #VARIANT IMAGES ENDS HERE-------------------------------	
# 		mywriter.writerow(productrow)	   
# 	   #Scraping Variants 
# 		script = {}   
# 		script = sel.xpath('//script[contains(text(), "productJson")]').extract()[0]	   
# 		variants.script_printing(script, mywriter, imageDict)
	   
	   
# 	   