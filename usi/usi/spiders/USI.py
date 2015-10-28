import re
import csv
import pprint

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

from ..helpers import bigcommerce, mycsv


class Spider(CrawlSpider):
    name = 'usi'
    
    start_urls = [
        'http://universalsportsinds.com/uni/index.php?action=9997&id=557&cid=217'
    # 'http://universalsportsinds.com/uni/index.php?action=9999',
            ]
    
    rules = (
          # Rule (LinkExtractor(allow=(),restrict_xpaths=("//*[contains(@class,'haschild')]",)), follow= True),
            Rule (LinkExtractor(allow=(),restrict_xpaths=("//div[@id='cssmenu']/ul/li",)), follow= True),
                # Rule (LinkExtractor(allow=(),restrict_xpaths=('//div[@class="row featuredProducts r2"]',)), follow= True),                
                    Rule (LinkExtractor(allow=(),restrict_xpaths=('//div[@class="row featuredProducts r2"]',)), callback="parse_items", follow= True),)
             

    def parse_items(self,response):      
    # def parse(self, response):
      print 'XXXXX'
      sel = Selector(response)      
      # # if stock:
      product_dict = {}
      product_dict['Product Name'] = sel.xpath("//span[@class='title4']/text()").extract()[0]      
      product_dict['Description'] = sel.xpath("//div[@style='float:right; width:450px;color: #fff;']//p").extract()
      product_dict['Images'] = ['http://universalsportsinds.com/uni/'+src for src in sel.xpath("//div[@id='proimgs']//img/@src").extract()]
      product_dict['Product Code/SKU'] = 'USI' + sel.xpath("//*[contains(text(),'Code:')]/following-sibling::text()").extract()[0].strip()      
      product_dict['Bin Picking Number'] = 'USI'
      product_dict['Price'] = sel.xpath("//span[@id='scr_tot']/text()").extract()[0]
      product_dict['Brand'] = 'USI'
      product_dict['Category'] = '/'.join(x for x in sel.xpath("//div[@class='pageLinks']/a/text()").extract()[-2:])
      product_dict['Product Availability']  = '7-12 Working Days'
      product_dict['Sort Order'] = '-200'
      
      try:
        sizes = sel.xpath("//select[@name='_size']/option/text()").extract()
        name = 'Size'
        variant_dict = {}
        variant_dict[name] = {}
        
        for size in sizes:
          if 'Select' not in size:
              variant_dict[name][size] = product_dict['Product Code/SKU']+size

        name = 'Color'
        variant_dict[name] = {}
        colors = sel.xpath("//select[@name='_color']/option/text()").extract()

        for color in colors:
          if 'Select' not in color:
            variant_dict[name][color] = product_dict['Product Code/SKU']+color
       
        product_dict['Track Inventory'] = 'By Option'
        
        bigcommerce.product_row(product_dict)
        bigcommerce.sku_row(variant_dict)
      except:
        product_dict['Track Inventory'] = 'By Product'
        bigcommerce.product_row(product_dict)

             
