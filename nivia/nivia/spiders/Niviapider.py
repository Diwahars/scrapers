from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from nivia.items import NiviaItem
import urlparse 
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["niviasports.com"]
  start_urls = ["http://www.niviasports.com/basketball2.html",
                "http://www.niviasports.com/basketball3.html",
                "http://www.niviasports.com/football2.html",
                "http://www.niviasports.com/football3.html",
                "http://www.niviasports.com/football4.html",
                "http://www.niviasports.com/basketball-shoes.html",
                "http://www.niviasports.com/volleyball3.html",
                "http://www.niviasports.com/volleyball2.html",
                "http://www.niviasports.com/cricket-shoes-main.html",
                "http://www.niviasports.com/athletics.html",
                "http://www.niviasports.com/otherballs.html",
                "http://www.niviasports.com/otherballs2.html",
                "http://www.niviasports.com/sports_gloves_1.html",
                "http://www.niviasports.com/sports_gloves_2.html",
                "http://www.niviasports.com/training_aids_1.html",
                "http://www.niviasports.com/training_aids_2.html",
                "http://www.niviasports.com/training_aids_3.html",
                "http://www.niviasports.com/training_aids_4.html",
                "http://www.niviasports.com/training_aids_5.html",
                "http://www.niviasports.com/professional-shoes.html",
                "http://www.niviasports.com/f-accessories.html",
                "http://www.niviasports.com/accessories_1.html",
                "http://www.niviasports.com/accessories_2.html",
                "http://www.niviasports.com/accessories_3.html",
                "http://www.niviasports.com/accessories_4.html",
                "http://www.niviasports.com/supports_1.html",
                "http://www.niviasports.com/supports_2.html",                
                "http://www.niviasports.com/football_nets.html",
                "http://www.niviasports.com/soccer_stockings_main.html",
                "http://www.niviasports.com/football-shoes-main1.html",
                "http://www.niviasports.com/football-shoes-main2.html",
                "http://www.niviasports.com/football-shoes-main3.html",
                "http://www.niviasports.com/shin-guards.html",
                "http://www.niviasports.com/shin-guards2.html",
                "http://www.niviasports.com/shin-guards3.html",
                "http://www.niviasports.com/dumbbell_sports_1.html",
                "http://www.niviasports.com/supports_1.html",
                "http://www.niviasports.com/supports_2.html",
                "http://www.niviasports.com/yoga_mats_1.html",
                "http://www.niviasports.com/basketball-net.html",
                "http://www.niviasports.com/volleyball-net.html",
                "http://www.niviasports.com/athletics.html",
                "http://www.niviasports.com/court-shoes.html",
                "http://www.niviasports.com/tennis-shoes.html",
                "http://www.niviasports.com/jogging-shoes.html",
                "http://www.niviasports.com/basketball-shoes.html",
                "http://www.niviasports.com/cricket-shoes.html",
                "http://www.niviasports.com/kids-shoes.html",
                "http://www.niviasports.com/professional-shoes.html",
                "http://www.niviasports.com/inline_skates.html",
                "http://www.niviasports.com/inline_skates_2.html",
                ]
  rules = (Rule (SgmlLinkExtractor(restrict_xpaths=('//div[@class="img-border"]',))
                 , callback="parse_items", follow= True),)
  
    

    
  def parse_items(self, response):
   hxs = HtmlXPathSelector(response)
   titles = hxs.select("//html")
   items = []
   for titles in titles:
     item = NiviaItem()
     item ["productname"] = titles.select("//td[@class='prod-name']").extract()
     item ["description"] = titles.select("//td[@class='text-gray-2']/text()").extract()
     item ["description1"] = titles.select("//td[@class='text-gray-2-2']/text()").extract()
     item ["imageurl"] = titles.select("//td[@class='prod-bg']/img/@src").extract()     
     item ["productcode"] = titles.select("//td[@class='prod-code']/span/text()").extract()
     
     
     items.append(item)
     return(items)
      
            

        
