from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from bigc.items import BigCItem
import urlparse 
from scrapy.http.request import Request
from scrapy.http import FormRequest
from scrapy import log
import json
import re
import csv
import imp
converter = imp.load_source('converter.py', '/Users/alfonsjose/Documents/Work/LYS/Web Scrapping/helpers/converter.py')
f = open("masterfile.csv")
csv_file = csv.reader(f)
skulist = []
sizelist = []
typelist = []
namelist = []
outofstock = []
idlist = []
binpicklist = []
for row in csv_file:
  skulist.append(row[4])
  sizelist.append(row[2])
  typelist.append(row[0])
  namelist.append(row[2])
  idlist.append(row[1])


class mensrunning(CrawlSpider):
  name = "roadrunner"
  allowed_domains = ["roadrunnersports.com",
                     "roadrunnersports.scene7.com"]
  start_urls = ["http://www.roadrunnersports.com/rrs/products/BRK1078/mens-brooks-beast-12/"
    #"http://www.roadrunnersports.com/rrs/products/ASC1724/mens-asics-gelkayano-21/",
                #"http://www.roadrunnersports.com/rrs/products/ASC1726/"
##    "http://www.roadrunnersports.com/rrs/mensshoes/?SearchHandle=QT1tZW5zc2hvZXMgbWVudXJyc35CPW1lbnNzaG9lcyBtZW51cnJzfkQ9MjR_RT0wXjFeMl5Qcmlvcml0eTJ_ST1Tb3J0VklQUHJpY2V_Sz00fkw9MX5NPTQ0fg&Action=2&AnswerID=2094&searchQuery=mensshoes%20menurrs",
##                "http://www.roadrunnersports.com/rrs/mensshoes/?SearchHandle=QT1tZW5zc2hvZXMgbWVudXJyc35CPW1lbnNzaG9lcyBtZW51cnJzfkQ9MjR_RT0wXjFeMl5Qcmlvcml0eTJ_ST1Tb3J0VklQUHJpY2V_Sz00fkw9MX5NPTQ0fg&Action=2&AnswerID=1482&searchQuery=mensshoes%20menurrs",
##                "http://www.roadrunnersports.com/rrs/mensshoes/?SearchHandle=QT1tZW5zc2hvZXMgbWVudXJyc35CPW1lbnNzaG9lcyBtZW51cnJzfkQ9MjR_RT0wXjFeMl5Qcmlvcml0eTJ_ST1Tb3J0VklQUHJpY2V_Sz00fkw9MX5NPTQ0fg&Action=2&AnswerID=2715&searchQuery=mensshoes%20menurrs",
##                "http://www.roadrunnersports.com/rrs/c/track-spikes/",
##                "http://www.roadrunnersports.com/rrs/mensshoes/?SearchHandle=QT1tZW5zc2hvZXMgbWVudXJyc35CPW1lbnNzaG9lcyBtZW51cnJzfkQ9MjR_RT0wXjFeMl5Qcmlvcml0eTJ_ST1Tb3J0VklQUHJpY2V_Sz00fkw9MX5NPTQ0fg&Action=2&AnswerID=128&searchQuery=mensshoes%20menurrs",
##                "http://www.roadrunnersports.com/rrs/mensshoes/?SearchHandle=QT1tZW5zc2hvZXMgbWVudXJyc35CPW1lbnNzaG9lcyBtZW51cnJzfkQ9MjR_RT0wXjFeMl5Qcmlvcml0eTJ_ST1Tb3J0VklQUHJpY2V_Sz00fkw9MX5NPTQ0fg&Action=2&AnswerID=3555&searchQuery=mensshoes%20menurrs",
##                "http://www.roadrunnersports.com/rrs/mensshoes/?SearchHandle=QT1tZW5zc2hvZXMgbWVudXJyc35CPW1lbnNzaG9lcyBtZW51cnJzfkQ9MjR_RT0wXjFeMl5Qcmlvcml0eTJ_ST1Tb3J0VklQUHJpY2V_Sz00fkw9MX5NPTQ0fg&Action=2&AnswerID=2547&searchQuery=mensshoes%20menurrs",
##                "http://www.roadrunnersports.com/rrs/womensshoes/?SearchHandle=QT13b21lbnNzaG9lcyBtZW51cnJzfkI9d29tZW5zc2hvZXMgbWVudXJyc35EPTI0fkU9MF4xXjJeUHJpb3JpdHkyfkk9U29ydFZJUFByaWNlfks9NH5MPTF_TT00Nn4&Action=2&AnswerID=2094&searchQuery=womensshoes%20menurrs",
##                "http://www.roadrunnersports.com/rrs/womensshoes/?SearchHandle=QT13b21lbnNzaG9lcyBtZW51cnJzfkI9d29tZW5zc2hvZXMgbWVudXJyc35EPTI0fkU9MF4xXjJeUHJpb3JpdHkyfkk9U29ydFZJUFByaWNlfks9NH5MPTF_TT00Nn4&Action=2&AnswerID=128&searchQuery=womensshoes%20menurrs",
##                "http://www.roadrunnersports.com/rrs/womensshoes/?SearchHandle=QT13b21lbnNzaG9lcyBtZW51cnJzfkI9d29tZW5zc2hvZXMgbWVudXJyc35EPTI0fkU9MF4xXjJeUHJpb3JpdHkyfkk9U29ydFZJUFByaWNlfks9NH5MPTF_TT00Nn4&Action=2&AnswerID=1482&searchQuery=womensshoes%20menurrs",
##                "http://www.roadrunnersports.com/rrs/womensshoes/?SearchHandle=QT13b21lbnNzaG9lcyBtZW51cnJzfkI9d29tZW5zc2hvZXMgbWVudXJyc35EPTI0fkU9MF4xXjJeUHJpb3JpdHkyfkk9U29ydFZJUFByaWNlfks9NH5MPTF_TT00Nn4&Action=2&AnswerID=2715&searchQuery=womensshoes%20menurrs",
##                "http://www.roadrunnersports.com/rrs/womensshoes/?SearchHandle=QT13b21lbnNzaG9lcyBtZW51cnJzfkI9d29tZW5zc2hvZXMgbWVudXJyc35EPTI0fkU9MF4xXjJeUHJpb3JpdHkyfkk9U29ydFZJUFByaWNlfks9NH5MPTF_TT00Nn4&Action=2&AnswerID=2905&searchQuery=womensshoes%20menurrs",
##                "http://www.roadrunnersports.com/rrs/womensshoes/?SearchHandle=QT13b21lbnNzaG9lcyBtZW51cnJzfkI9d29tZW5zc2hvZXMgbWVudXJyc35EPTI0fkU9MF4xXjJeUHJpb3JpdHkyfkk9U29ydFZJUFByaWNlfks9NH5MPTF_TT00Nn4&Action=2&AnswerID=2547&searchQuery=womensshoes%20menurrs"
  ]

  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//td[@id="paging_count"]',)), follow= True),
           Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="product_colorways_image"]',)), callback="parse_item", follow= True),)

  csvfile = None
  printHeader = True
  def to_csv(self, item):
    start = 0
    end=0
    
    if self.printHeader:
      self.csvfile = open('RoadRunnerSportsRunningShoes.csv','w')
    if self.csvfile:

      strWrite = ''
      #headers
      if self.printHeader: 
        strWrite +='Item Type,Product ID,Product Name,Brand Name,Price,Retail Price,Sale Price,Product Description,Product Code/SKU,Bin Picking Number,'
        strWrite +='Category,Option Set,Product Availability,Current Stock Level,Free Shipping,Sort Order, Meta Description,Page Title, Product Image Description - 1,Product Image Is Thumbnail - 1,'
        strWrite +='Track Inventory,Product Image Sort - 1,Product Image Sort - 2,Product Image Sort - 3,Product Image Sort - 4,Product Image Sort-5,Product Image Sort-6,Product Image Sort-7,'
        strWrite +='Product Image File - 1,Product Image File - 2,Product Image File - 3,Product Image File - 4,Product Image File - 5 ,Product Image File - 6,Product Image File - 7, \n'
        self.printHeader = False

      pfound = 0 #counter to find product from master sheet. If 0 after the loop, product is a NEW product and not uploaded previously
      productid = 0 #Storing the Product ID value for the product row
      for color,sizes in item['variant'][item['sku']].iteritems():
        for i in range(len(namelist)): #Loop to go through all the Item Types in old file.          
          if typelist[i] == "Product" and skulist[i] == (item['sku']+item['color'][color]):           
          #if typelist[i] == "Product" and namelist[i] == (item['Product_Name']+" " + item['color'][color]+"*"): #Comparing Product Names from old sheet and new scrapped
            
            start = i # Counter to store index of found Product Name
            pfound = 1
            productid = idlist[i]
            for r in range(i+1,len(namelist)): #Loop to start at the Counter and Look for next occurance of Item Type = "Product"
              if typelist[r] == "Product" : 
                break   #Loop breaks for next occurance of Item Type = "Product" 
              else:
                  end = end+1 #Counting the number of SKUS for each product from the OLD sheet  
      print "#",pfound
      #not Found Products
      if pfound ==0:
        if item["Brand_Name"] not in("Nike","adidas","Reebok","Puma"):
          for color,sizes in item['variant'][item['sku']].iteritems():
            # generate product row
            strWrite += 'Product,,'+item['Product_Name']+" " + item['color'][color]+"*"+','+item['Brand_Name']+','+item['Retail_Price']+','+item['Retail_Price']+','+item['Sale_Price']+','
            strWrite += '.'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","").replace('<.*?>)',"").replace("When choosing running shoes, find your perfect fit using this chart. Category types are based on factors like arch height, running habits and body frame.","").replace("This web exclusive item ships separately within the continental U.S. only. You can count on this item to ship in 3-5 business days!","") + ","
            strWrite += item['sku']+item['color'][color]+ ',' + "ROADRUNNER" +','
            strWrite += item['Category']  + ',' + item['Product_Name']+item['color'][color] + ',' + item["Product_Availability"] +','
            strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"]  + "," + "Buy the " + item['Product_Name']+" " + item['color'][color] + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
            strWrite += ',' + "Buy the " + item['Product_Name']+" " + item['color'][color]+ " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts" + ','
            strWrite += "Buy the " + item['Product_Name']+" " + item['color'][color]+ " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts" + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
            strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
            strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ',6,7,'
            strWrite += ','.join(item['Product_Image_File1'][color])+',\n'
            #strWrite += 'Product,'+item['productname']+','+item['sku']+','+item['color'][color]+',,,,'+','.join(item[''][color])+',\n'
            #only write availabe products to csv
            for width,sizeList in sizes.iteritems():
              for size,sku in sizeList.iteritems():
                strWrite += 'SKU,,[S]Size= US '+size+'.Width ='+width+',,,,,,'+sku+','+"ROADRUNNER,,,,100"+',\n'
      else:
        if item["Brand_Name"] not in("Nike","adidas","Reebok","Puma"):
          for color,sizes in item['variant'][item['sku']].iteritems():
            print pfound
            # generate product row
            strWrite += 'Product,'+productid+","+item['Product_Name']+" " + item['color'][color]+"*"+','+item['Brand_Name']+','+item['Retail_Price']+','+item['Retail_Price']+','+item['Sale_Price']+','
            strWrite += '.'.join(item["Product_Description"]).replace(',',';').replace("\n","").replace("\r","").replace('<.*?>)',"").replace("When choosing running shoes, find your perfect fit using this chart. Category types are based on factors like arch height, running habits and body frame.","").replace("This web exclusive item ships separately within the continental U.S. only. You can count on this item to ship in 3-5 business days!","") + ","
            strWrite += item['sku']+item['color'][color]+ ',' + "ROADRUNNER" +','
            strWrite += item['Category']  + ',' + item['Product_Name']+item['color'][color] + ',' + item["Product_Availability"] +','
            strWrite += item["Current_Stock"] + ',' + item["Free_Shipping"] + ',' + item["Sort_Order"]  + "," + "Buy the " + item['Product_Name']+" " + item['color'][color] + " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
            strWrite += ',' + "Buy the " + item['Product_Name']+" " + item['color'][color]+ " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts" + ','
            strWrite += "Buy the " + item['Product_Name']+" " + item['color'][color]+ " Online in India at LiveYourSport.com| Free Shipping and Massive Discounts" + ',' + item["Product_Image_Is_Thumbnail_1"] + ',' + item["Track_Inventory"] + ','
            strWrite += item["Product_Image_Sort_1"] + ',' + item["Product_Image_Sort_2"] + ',' + item["Product_Image_Sort_3"] + ','
            strWrite += item["Product_Image_Sort_4"] + ',' + item["Product_Image_Sort_5"] + ',6,7,'
            strWrite += ','.join(item['Product_Image_File1'][color])+',\n'
        #VARIANT PRINTING SECTION

          old_dict = {} #Dictionary to contain old SKUs and Sizes
          oldlen = 0
          for i in range(start+1,start+1+end): #Storing all list of SKUS in a new list. Will be used for comparing with the new list
            old_dict[0,oldlen]=skulist[i]
            old_dict[1,oldlen]= sizelist[i]
            old_dict[2,oldlen]= idlist[i]
            oldlen = oldlen+1
            
          new_dict = {} #Dictionary to contain new SKUs and Sizes
          c=0
          for width,sizeList in sizes.iteritems():
              for size,sku in sizeList.iteritems():
                new_dict[0,c] = sku
                new_dict[1,c] = 'SKU,,[S]Size= US '+size+'.Width ='+width
                c= c+1
                
          diff_dict = {} #Dict which contains older skus
          r=0
          for i in range(oldlen):
            found = 0
            for x in range(c):
              if old_dict[0,i] == new_dict[0,x]:            
                found = 1
                break
            if found ==0:
              diff_dict[0,r] = old_dict[0,i]
              diff_dict[1,r] = old_dict[1,i]
              diff_dict[2,r] = old_dict[2,i]
              r=r+1

          for width,sizeList in sizes.iteritems():
            t=0
            for size,sku in sizeList.iteritems():
              if sku == old_dict[0,i]:
                strWrite += 'SKU,'+old_dict[2,i]+',[S]Size= US '+size+'.Width ='+width+',,,,,,'+sku+','+"ROADRUNNER,,,,100"+',\n'
                t = 1
              if t==0:# For SKUS which are new and hence will not have a product ID
                strWrite += 'SKU,,[S]Size= US '+size+'.Width ='+width+',,,,,,'+sku+','+"ROADRUNNER,,,,100"+',\n'

          if diff_dict:
            for i in range (r):
              strWrite += 'SKU,'+diff_dict[2,i]+','+diff_dict[1,i] +',,,,,,'+diff_dict[0,i] + ',' +'ROADRUNNER,,,,0,,,,,,,,,,,\n' 
        self.csvfile.write(strWrite.encode('utf8'))

  #def parse_item(self, response):
  def parse(self, response):
    sel = Selector(response)
    url = 'http://www.roadrunnersports.com/rrs/product-detail/build-selections.jsp'
    item = BigCItem()
    pname =  response.xpath("//meta[@property='og:title']/@content").extract()[0]
    item ["Product_Name"]  = response.xpath("//meta[@property='og:title']/@content").extract()[0]

    if "Trail" in pname :
      item ["Product_Name"]  = response.xpath("//meta[@property='og:title']/@content").extract()[0] + " Running Shoe"
    
    
    mrp = float(sel.xpath("//span[@class='prod_detail_reg_price']/span/text()").extract()[0])
    
    item ["Retail_Price"]  = str((mrp*65 + mrp*30/100*70/100*65)*112.5/100 + mrp*65*15/100)
    item_sp               = response.xpath("//span[@class='prod_detail_sale_price']/span/text()").extract()
    
    if item_sp:
      sp = float(sel.xpath("//span[@class='prod_detail_sale_price']/span/text()").extract()[0].split("-")[-1].replace("$",""))
      item ["Sale_Price"]         = str((sp*65 + 30/100*70*65)*112.5/100 + sp*65*15/100)
    else:
      item ["Sale_Price"]         = ''
    #categorization
    cat     =  response.xpath("//div[@id='grp_1']/p/span[1]/text()")
    sex =  response.xpath("//meta[@property='og:title']/@content").extract()[0]
    if sex in("Women's"):
      sex= "Women's"
    else:
      sex= "Men's"

    item["Product_Description"] = response.xpath("//div[@id='grp_1']/p").extract() + response.xpath("//div[@id='grp_1']/ul/li").extract()
       
    if cat:
#      item ["Category"] = "Run & Cycle/Running/Running Shoes;Shoes/"+ sex + " Running Shoes/" + sel.xpath("//div[@id='grp_1']/p/span[1]/text()").extract()[0].replace("+","")
      cat= ";Shoes/"+sex+" Running Shoes/"+response.xpath("//div[@id='grp_1']/p/span[1]/text()").extract()[0].replace("+","") +" Running Shoes"
      
      item ["Product_Name"]  = response.xpath("//meta[@property='og:title']/@content").extract()[0] + " " + response.xpath("//div[@id='grp_1']/p/span[1]/text()").extract()[0] + " Running Shoe"
    else:
      cat= ""

    if any("hiking" in s for s in item["Product_Description"]) or any("Hiking" in s for s in item["Product_Description"]):
      item ["Category"] = "Run & Cycle/Running/Running Shoes;Shoes/"+ sex + " Shoes/Hiking Shoes" + cat
    elif any("trail" in s for s in item["Product_Description"]) or any("Trail" in s for s in item["Product_Description"]):
      item ["Category"] = "Run & Cycle/Running/Running Shoes;Shoes/"+ sex + " Running Shoes/Trail Running Shoes" + cat
    elif any("minimalist" in s for s in item["Product_Description"]) or any("barefoot" in s for s in item["Product_Description"]) or any("Barefoot" in s for s in item["Product_Description"]):
      item ["Category"] = "Run & Cycle/Running/Running Shoes;Shoes/"+ sex + " Running Shoes/Barefoot Running Shoes" + cat
    elif any("spike" in s for s in item["Product_Description"]):
      item ["Category"] = "Run & Cycle/Running/Running Shoes;Shoes/"+ sex + " Running Shoes/Racing Spikes" + cat
    elif any("cross-train" in s for s in item["Product_Description"])or any("trainer" in s for s in item["Product_Description"])or any("training shoe" in s for s in item["Product_Description"]) or any("gym" in s for s in item["Product_Description"]) or any("workout" in s for s in item["Product_Description"]):
      item ["Category"] = "Run & Cycle/Running/Running Shoes;Shoes/"+ sex + " Shoes/Cross Training Shoes" + cat   
    else:
      if cat:
        item ["Category"] = "Run & Cycle/Running/Running Shoes"+ cat
      else:
        item ["Category"] = "NULL"
        
    item ["Brand_Name"]          = response.xpath("//span[@itemprop='brand']/text()").extract()[0]
    if item["Brand_Name"] in ("Asics","Mizuno","Brooks","Saucony","New Balance"):
       item ["Sort_Order"] = str(-300-(20/100*mrp))
    elif item["Brand_Name"] in ("Under Armour","Altra","Hoka One One","Inov8","Salomon","Vibram FiveFingers"):
        item ["Sort_Order"] = str(-270-(20/100*mrp))
    else :
      item ["Sort_Order"] = str(-250-(20/100*mrp))
      
    item["Product_Availability"] = "12-17 Working Days"
    item["Current_Stock"] = "100"
    item ["Free_Shipping"] = "N"
    item["Product_Image_Is_Thumbnail_1"] = "Y"
    item["Track_Inventory"] = "By Option"
    item["Product_Image_Sort_1"] = "1"
    item["Product_Image_Sort_2"] = "2"
    item["Product_Image_Sort_3"] = "3"
    item["Product_Image_Sort_4"] = "4"
    item["Product_Image_Sort_5"] = "5"
    
    item ["imageSetUrls"] = {}
    item ["imageSetUrls2"] = {}
    colors                = response.xpath("//a[@class='ref2QIColor']/@name").extract()
    item ["Product_Image_File1"]      = {}
    hrefs                 = response.xpath("//a[@class='ref2QIColor']/@href").extract()
    item ["color"]     = {}
    for idx,href in enumerate(hrefs):
      #create links to image sets
      if colors[idx] not in item ["imageSetUrls"]:
        item ["imageSetUrls"][colors[idx]] = []
      item ["imageSetUrls"][colors[idx]].append("http://roadrunnersports.scene7.com/is/image/roadrunnersports/"+href.split('/')[-1].split('_')[0]+"-IS?req=set,json&scl=1")
      if colors[idx] not in item ["imageSetUrls2"]:
        item ["imageSetUrls2"][colors[idx]] = []
      item ["imageSetUrls2"][colors[idx]].append("http://roadrunnersports.scene7.com/is/image/roadrunnersports/"+href.split('/')[-1].split('_')[0]+"-IS?req=set,json&scl=1")
      item ["color"][href.split('/')[-1].split('_')[0].split('-')[1]] = colors[idx]
      
    #request product info as json
    item ["sku"]          = response.url.strip('/').split('/')[-2]
    payload               = {'id':item ["sku"]}
    request               = FormRequest(url,formdata=payload,callback=self.parseJsonProduct)
    request.meta['item']  = item

    return request

  #parse product info from json file 
  def parseJsonProduct(self,response):
    item                  = response.meta['item']
    #make a valid json file out of it and remove unneeded data
    prodResponse          = response.body.split('$+$')[0].strip().replace("'",'"')
    prodDict              = {}
    sizeWidthDict         = {}
    jsonresponse          = json.loads(prodResponse)
    for product,value in jsonresponse.iteritems():
      if item["sku"] not in prodDict:
        prodDict[item["sku"]]={}
      if value['c'] not in prodDict[item["sku"]]:
        prodDict[item["sku"]][value['c']] ={}
      if value['w'] not in prodDict[item["sku"]][value['c']]:
        prodDict[item["sku"]][value['c']][value['w']]={}
      if value['s'] not in sizeWidthDict:
        sizeWidthDict[value['s']] = []
      if value['w'] not in sizeWidthDict[value['s']]:
        sizeWidthDict[value['s']].append(value['w'])
      prodDict[item["sku"]][value['c']][value['w']][value['s']]=value['sku']
    item['variant']       = prodDict
    item['size_width_list'] = sizeWidthDict
    #request first imageset
    if item["imageSetUrls"]:
      color,href            = item["imageSetUrls"].popitem()
      if len(href)>1:
        item["imageSetUrls"][color] = href[1:]
      request               = Request(href[0],callback=self.parseJsonImageSet)
      request.meta['item']  = item
      return request
      
    self.to_csv(item)
    return item

  def parseJsonImageSet(self,response):
    item                  = response.meta['item']
    imageSetResponse      = response.body
    #make a valid json file out of it, if only one image available it was a list => make a dict 
    imageSetResponse      = imageSetResponse.replace('/*jsonp*/s7jsonResponse(','')
    imageSetResponse      = ','.join(imageSetResponse.split(',')[:-1])
    imageSetResponse      = imageSetResponse.replace('"item":[','"item":')
    imageSetResponse      = imageSetResponse.replace('"item":','"item":[')
    imageSetResponse      = imageSetResponse.replace('}]}}','}}}')
    imageSetResponse      = imageSetResponse[::-1].replace('}}}','}}]}')[::-1]

    color                 = response.url.split('-')[1].split('?')[0]
    isImageSet            = False
    if len(response.url.split('-'))>2:
      isImageSet          = True
    item['Product_Image_File1'][color] = []
    
    jsonresponse          = json.loads(imageSetResponse)
    for index,imageItem in enumerate(jsonresponse['set']['item']):
      #check if there is a image set or only one image
      if 'isDefault' not in imageItem['i']:
        imageUrl = 'http://roadrunnersports.scene7.com/is/image/'+imageItem['i']['n']+'?iv='+imageItem['iv']
        #response url is image set => image can be scaled
        if isImageSet:
          imageUrl += '&scl=1'
        item['Product_Image_File1'][color].append(imageUrl)
      else:
        # there is no image set append request for default image
        if item['color'][color] not in item["imageSetUrls"]:
          item ["imageSetUrls"][item['color'][color]] = []
        if item['color'][color] not in item["imageSetUrls2"]:
          item ["imageSetUrls2"][item['color'][color]] = []
        item["imageSetUrls"][item['color'][color]].append('http://roadrunnersports.scene7.com/is/image/roadrunnersports/'+item['sku']+'-'+color+'?req=set,json&scl=1')
        item["imageSetUrls2"][item['color'][color]].append('http://roadrunnersports.scene7.com/is/image/roadrunnersports/'+item['sku']+'-'+color+'?req=set,json&scl=1')

    if item["imageSetUrls"]:
      color,href            = item["imageSetUrls"].popitem()
      if len(href)>1:
        item["imageSetUrls"][color] = href[1:]
      request               = Request(href[0],callback=self.parseJsonImageSet)
      request.meta['item']  = item
      return request

    self.to_csv(item)
    return item
