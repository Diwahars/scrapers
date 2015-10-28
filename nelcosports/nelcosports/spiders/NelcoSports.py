from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider
from nelcosports.items import DicksItem
import urlparse ,re, json, csv
from scrapy.http.request import Request
output = open("NelcoSports.csv","wb")
mywriter = csv.writer(output)
productcount = 0
pagenamelist = []

header = ('Item Type','Product ID','Product Name','Brand Name','Price','Retail Price','Sale Price','Product Description','Product Code/SKU','Bin Picking Number','Category',
                 'Option Set','Product Availability','Current Stock Level','Free Shipping','Sort Order','Meta Description','Page Title',''
             'Product Image Description - 1','Product Image Is Thumbnail - 1',''
             'Track Inventory','Product Image Sort - 1',
             'Product Image File - 1')

mywriter.writerow(header)
##f = open("categories.csv")
##csv_file = csv.reader(f)

##for row in csv_file:

class NelcoSpider(CrawlSpider):
  name = "nelcosports"
  allowed_domains = ["nelcosport.com"]
  start_urls = [
"http://www.nelcosport.com/More_Product_Detail.php?CateId=2&FinalCateId=178"
    ]
  rules = (
    Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=("//table//td[@class='left_menu']/a",))
    , follow= True),
    Rule (SgmlLinkExtractor(allow=(),
                            restrict_xpaths=('//div/div[@class="product_name"]',)),
                 callback="parse_category" , follow= True),
    )

##  def parse(self, response):
  def parse_category(self, response):
     sel = Selector(response)
     item = DicksItem()
     pname = sel.xpath("//div[@class='product_name']/text()").extract()[0]  
     pname = pname.encode('utf-8')
     item['Brand_Name'] = "Nelco Sports"          
     item["Product_Image_Description_1"] = "Buy "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
     item["MetaDescription"] = "Get your hands on the "+pname +". Buy it Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"
     item["TitleTag"] = "Buy the "+pname+" Online in India at LiveYourSport.com| Free Shipping and Massive Discounts"   
     pcode  =sel.xpath("//input[@type='checkbox']/@value").extract()[0] +"NELPRD"
     item["Product_Description"] = sel.xpath("//td[@class='form_text_normal']/text()").extract()
     item["Product_Description"] = ''.join(item["Product_Description"]).encode('utf-8')
     
     mrp = []
     sp = sel.xpath("//td[@class='guest']/text()").extract()
     sp  = min(float(x) for x in sp)     
     mrp = sel.xpath("//tr/td[@class='form_text'][last()-1]/text()").extract()
     mrp = min(float(x) for x in mrp)     
     sortorder = -150     
     trackinventory = 'By Option'
     image = ("http://www.nelcosport.com/"+
              sel.xpath('//div[@class="enlarge"]/a/@href').extract()[0])
     category =  sel.xpath("//h1[@class='heading1']/a/text()").extract()[0]
     row  = ("Product","",pname,item["Brand_Name"],
             mrp,mrp,sp, #price
             item["Product_Description"],pcode,"NELCOSPORTS",category,
             pname,"15-23 Working days","100","N",sortorder,
             item["MetaDescription"],item["TitleTag"],item["Product_Image_Description_1"],"Y",trackinventory,
             "1",image)

     mywriter.writerow(row)

     variants = {}
     variants['sku'] = sel.xpath("//input[@type='checkbox']/@value").extract()
     x = sel.xpath("//tr/td[2]/text()").extract()
     variants['weight']  = ''
     for w in x:      
       if 'Weight' in w:
         variants['weight'] = sel.xpath("//tr/td[@class='form_text'][2]/text()").extract()
         break
       
     variants['size'] =sel.xpath('//tr/td[@bgcolor="#FFFFFF"][last()]/text()').extract()     
     variants['price'] = sel.xpath('//td[@class="guest"]/text()').extract()
     count = 0
     for i in range(len(variants['size'])):
       variants['size'][i]= ''.join(variants['size'][i]).encode('utf-8')      
       if variants['size'][0] == variants['size'][i]:
         count = count +1

     if len(variants['price'])>1:
       for i in range(len(variants['price'])):       
         if variants['weight']:           
           if variants['size'][i].strip() == '' or count ==len(variants['price']):             
             row = ("Rule",'',"[S]Weight ="+variants['weight'][i]+"KG",
                    '','[FIXED]'+variants['price'][i],'[FIXED]'+variants['price'][i],'[FIXED]'+variants['price'][i]
                    ,'',variants['sku'][i],'NELCOSPORTS',
                    '','','','100')
             rules = ("Rule",'',"[S]Weight ="+variants['weight'][i]+"KG",
                    '','[FIXED]'+variants['price'][i],'[FIXED]'+variants['price'][i],'[FIXED]'+variants['price'][i]
                      ,'',variants['sku'][i],'NELCOSPORTS',
                    '','','','100')         
           else:             
             row = ("Rule",'',"[S]Weight ="+variants['weight'][i]+"KG"+",[S]Size="+variants['size'][i].strip('Size'),
                    '','[FIXED]'+variants['price'][i],'[FIXED]'+variants['price'][i],'[FIXED]'+variants['price'][i]
                    ,'',variants['sku'][i],'NELCOSPORTS',
                    '','','','100')             
         else:
           row = ("Rule",'',"[S]Size="+variants['size'][i].strip('Size'),
                   '','[FIXED]'+variants['price'][i],'[FIXED]'+variants['price'][i],'[FIXED]'+variants['price'][i]
                  ,'',variants['sku'][i],'NELCOSPORTS',
                    '','','','100')  
         mywriter.writerow(row)
      
