from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from khelmart.items import KhelmartItem
import urlparse
from scrapy.http.request import Request

class MySpider(CrawlSpider):
  name = "price"
  allowed_domains = ["khelmart.com"]
  start_urls = ["http://www.khelmart.com/Badminton/items/Li-Ning-Flame-N36-Badminton-Racket.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Arcsaber-I-Slash-Badminton-Racket.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-arcsaber-10.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-arcsaber-10.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-arcsaber-10.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-Arcsaber-11.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-Arcsaber-11.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-ArcSaber-3-FL.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-ArcSaber-7.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-ArcSaber-7.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-ArcSaber-8-DX.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-Nanoray-700-fx.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-nanoray-800.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-nanoray-800.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-Nanospeed-9900.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-VOLTRIC-5.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Badminton-Racket-Yonex-ArcSaber-FB.aspx",

                "http://www.khelmart.com/Badminton/items/Yonex-Nanoray-Z-Speed-Badminton-Racket.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Voltric-I-Force-Badminton-Racket.aspx",
                "http://www.khelmart.com/Badminton/items/Yonex-Voltric-Z-Force-Badminton-Racket.aspx",
                "http://www.khelmart.com/Cricket/items/Head-YouTek-Graphene-Pwr-Instinct-Tennis-Racquet.aspx",
                "http://www.khelmart.com/Squash/items/Prince-EXO3-Rebel-Squash-Racket.aspx",
                "http://www.khelmart.com/Squash/items/Prince-O3-Speedport-Silver-Squash-Racket.aspx",
                "http://www.khelmart.com/Table-Tennis/items/Donic-Waldner-Black-Devil-Table-Tennis-Blade.aspx",
                "http://www.khelmart.com/Tennis/items/Head-YouTek-Graphene-Speed-Pro-Tennis-Racquet.aspx",
                "http://www.khelmart.com/Tennis/items/Wilson-Tennis-Rackets-Wilson-BLX-Six-One-Team-95.aspx",
                ]

  
  def parse(self, response):
   hxs = HtmlXPathSelector(response)  
   titles = hxs.select("//head")
   items = []
   
   for titles in titles:
     item = KhelmartItem()
     item ["productname"] = titles.select("//span[@id='Label2']/text()").extract()     
     item ["MRP"] = titles.select("//span[@class='ST_items_details2']/text()").extract()
     item ["SP"] = titles.select("//span[@itemprop='price']/text()").extract()
     item ["SKU"] = titles.select("//span[@class='ST_items_details'][1]/text()").extract()
     item ["stock"] = titles.select("//td[@valign='top']/span[@id='Label29']/text()").extract()
     
     
     items.append(item)
     return(items)
      
            

        
