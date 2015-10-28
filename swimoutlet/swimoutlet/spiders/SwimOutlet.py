from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from swimoutlet.items import BigCItem
import string
import urlparse
import re, json, unicodecsv 
from ..utilities import mycsv, categories

mywriter = mycsv.initialize()
cat1list, cat2list, cat3list, urllist, categnamelist, priceidlist = categories.initialize()

class MySpider(CrawlSpider):
  name = "swimoutlet"
  allowed_domains = ["swimoutlet.com"]
  start_urls = [
##    "http://www.swimoutlet.com/womens-tan-thru-swimsuits-c9374/",    
##    "http://www.swimoutlet.com/shoes-accessories-c10211/",
##    "http://www.swimoutlet.com/swim-caps-c9633/#cat=9633&clrc=481&sortby=Popularity"    
##    "http://www.swimoutlet.com/womens-swim-dresses-c9373/",
##    "http://www.swimoutlet.com/shoes-accessories-c10211/",
##    "http://www.swimoutlet.com/swimming-watches-c14082/",
##    "http://www.swimoutlet.com/kickboards-c9661/"
    i.strip() for i in urllist
]

  rules = (
##    Rule (SgmlLinkExtractor(allow=(),
##                            restrict_xpaths=('//ul[@class="pagination"]',))
##    , follow= True),
    Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=('//ul[@class="pagination floatR"] | //nav[@id="blockcontentmnutop"]/span[last()]/a',)),
                 callback="parse_category" , follow= True),
    )

  def parse_category(self,response):
##  def parse(self,response):
    
    sel = Selector(response)    
    hxs = HtmlXPathSelector(response)    
    pageurl = response.url.strip()
    breadcrumb = sel.xpath("//nav[@id='blockcontentmnutop']/span[last()]/a/text()").extract()[0].strip()
##    url = response.url
##    for i in range(len(urllist)):
##      if url == urllist[i]:
##        row =(breadcrumb,priceidlist[i],url,cat1list[i],cat2list[i],cat3list[i])        
##        mywriter.writerow(row)
    
    for i in range(len(urllist)):      
      if breadcrumb==categnamelist[i]:       
        producturls =  sel.xpath("//div[@class='pd-details']/a/@href").extract()
        for x in producturls:          
          item = BigCItem()        
          item ['Category'] = cat1list[i]
          item ['Category2'] = cat2list[i]
          item ['Category3'] = cat3list[i]
          item ['id1'] = priceidlist[i]        
          request = Request(x,callback=self.parse_items)
          request.meta["item"] = item
          yield request      

##  def parse(self,response):
##    item = BigCItem()
##    item['Category'] = ''
##    item ['id1'] = 'Apparel'
  def parse_items(self,response):
    item = response.meta['item']    
    sel = Selector(response)
    hxs = HtmlXPathSelector(response)   
    pname = sel.xpath("//h1/text()").extract()[0]
    item ["Product_Name"] =  pname
    item["Option_Set"] = pname
    item["Product_Image_Description_1"] = "Buy "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["MetaDescription"] = "Get your hands on the "+pname +". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["TitleTag"] = "Buy the "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
    item["Brand_Name"]  = sel.xpath("//div[@id='divhoverpopup']/h2/a/@title").extract()[0]
    pcode  =sel.xpath("//div[@class='pro-code']/i/text()").extract()[0].replace("Product Code: ","")
    item ["Product_Code"] = pcode 
    item["Product_Description"] = sel.xpath("//div[@class='pro-description']/p |//div[@class='pro-description']/ul").extract()
    item["Product_Description"] = ''.join(item["Product_Description"]).encode('utf-8')
    mrp = sel.xpath("//span[@id='ListPrice']/text()| //span[@id='ProductPrice']/text()").extract()[0].replace("$","")
    sp = sel.xpath("//span[@id='PriceRange']/text() | //span[@id='SalePrice']/text()").extract()
    item["Sale_Price"] = ""
    if item["Brand_Name"] in ("FINIS","Arena","Speedo","Finis","2XU","Garmin","HYDRO-FIT","Nike","TYR","Yurbuds","Timex"):
      sortorder = "-300"
    elif item["Brand_Name"] == "Sporti":
      sortorder = "-270"
    else:
      sortorder = "-270"      
    item['Retail_Price'], item['Sale_Price'] = mycsv.pricing(mrp, sp, item['id1'])
    
    breadcrumb = sel.xpath("//nav[@class='block-content mnu-top mnu-top-product-detail']/span[last()]/a/text()").extract()[0].strip()
    if breadcrumb == 'Swim.com Compatible':
      breadcrumb = sel.xpath("//nav[@class='block-content mnu-top mnu-top-product-detail']/span[last()-1]/a/text()").extract()[0].strip()
    
    if item ['Category'] and item ['Category2'] and item ['Category3']:
      Category = item ['Category']+'/'+breadcrumb+';'+item ['Category2']+'/'+breadcrumb+';'+item ['Category3']+'/'+breadcrumb
    elif item ['Category'] and item ['Category2']:
      Category = item ['Category']+'/'+breadcrumb+';'+item ['Category2']+'/'+breadcrumb+';'
    else:
      Category = item ['Category']+'/'+breadcrumb
      
    size = response.xpath('//*[@id="divChooseOption2"]/div[2]/script[1][contains(text(),"arraySize")]').extract()
    colorArray = response.xpath('//script[@language="JavaScript"][contains(text(),"arrayColor")]').extract()
    if size or colorArray:
      trackinventory = "By Option"
    else:
      trackinventory = "By Product"
      
    item["Product_Image_File1"] = response.xpath('//*[@id="divChooseOption2"]/img/@name |//div[@class="box-content block-content mnu-content pro-option"]/img/@name').extract()

    tup = ("Product",item["Product_Name"]+"*",item["Brand_Name"],
           item["Retail_Price"],item["Retail_Price"],item["Sale_Price"], #price
           item ["Product_Code"]+"SWMOTLT",Category,"SWIMOUTLET",item["Product_Description"],"100",item["Product_Name"],"15-21 Working days","N",sortorder,
           item["MetaDescription"],item["TitleTag"],item["Product_Image_Description_1"],"Y",trackinventory,
           "1","2","3","4","5","6","7")
    obj = list(tup)
    c = 0
    for i in item["Product_Image_File1"]:
      c=c+1
      imgurl ="http://www.swimoutlet.com/photos/"+i+".jpg"
      if size or colorArray:
        imgurl ="http://www.swimoutlet.com/photos/options/"+i+".jpg"             
      obj.append(imgurl)
      if c==7:
        break      
    row = tuple(obj)
    
    
    if size:
      size = response.xpath('//*[@id="divChooseOption2"]/div[2]/script[1][contains(text(),"arraySize")]').extract()[0].replace("arraySize[0] =","")
      size = re.sub(r'<script(.*)>', '' ,size)
      size = size.replace("arraySize = new Array();","")    
      size = re.sub(r'arraySize(.*)=', ',' ,size)
      size = size.replace("[",'').replace("];","").replace("'",'"').replace('",','":').replace("</script>","")   
      size = "[{" + size + "}]"
      item['size'] = {}
      item['size'] = json.loads(size)[0]
    else:
      item['size'] = ""
      
    if colorArray:      
      colorArray = response.xpath('///script[@language="JavaScript"][contains(text(),"arrayColor")]').extract()[0].replace("arrayColor[0] =","")  
      colorArray = re.sub(r'<script(.*)>', '' ,colorArray)
      colorArray = colorArray.replace("var arrayColor = new Array();","")    
      colorArray = re.sub(r'arrayColor(.*)=', ',' ,colorArray)
      colorArray = colorArray.replace("[",'').replace("];","").replace("'",'"').replace('",','":').replace("</script>","")
      #print colorArray
      colorArray = "[{" + colorArray + "}]"   
      item['color'] = {}
      item['color'] = json.loads(colorArray)[0]
      item['variant'] = {}
      for colorcode, color in item['color'].iteritems():
        if item['size']=="":
          item['variant'][colorcode+"_"+colorcode] = "[S]Color= "+color          
        elif len(item['size']) ==1:        
          for sizecode,size in item['size'].iteritems():
            item['variant'][colorcode+"_"+sizecode] = "[S]Color= "+color+",[RB]Size= "+size
        elif len(item['color']) ==1:
           for sizecode,size in item['size'].iteritems():
            item['variant'][colorcode+"_"+sizecode] = "[RB]Color= "+color+",[S]Size= "+size       
        else:
          for sizecode,size in item['size'].iteritems():
            item['variant'][colorcode+"_"+sizecode] = "[S]Color= "+color+",[S]Size= "+size
          
      combosArray = sel.xpath('//script[@language="JavaScript"][contains(text(),"var separator")]').extract()[0]
      combosArray = re.findall(r'id=.*name',combosArray)
      combosArray = [w.replace("id='size_","").replace("name","").replace('"',"").replace("'","").replace(" ","") for w in combosArray]      
      priceArray = sel.xpath('//script[@language="JavaScript"][contains(text(),"var separator")]').extract()[0]
      priceArray = re.findall(r'value.*/',priceArray)
      priceArray = [w.replace("/","").replace("value=","").replace("'","") for w in priceArray]
      item["Price"] = dict(zip(combosArray,priceArray))
      #print pricedict
      notfound = 0
      
      for key,price in item['Price'].iteritems():        
        if key not in item['variant']:
          notfound = 1
          break
        
      
      if notfound==0:
        mywriter.writerow(row)
        for key,price in item["Price"].iteritems():          
          row=("Rule",item['variant'][key],"","","","",pcode+key,"","SWIMOUTLET","","","","","","","","","","","","","","","","","","",
               "http://www.swimoutlet.com/photos/options/"+pcode+"-"+key.split("_")[0]+"-zoomin.jpg")        
          mywriter.writerow(row)
          row1=("SKU",item['variant'][key],"","","","",pcode+key,"","SWIMOUTLET","","100","","","","","","","","","","","","","","","","",
               "http://www.swimoutlet.com/photos/options/"+pcode+"-"+key.split("_")[0]+"-zoomin.jpg")
          
          mywriter.writerow(row1)
