from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from activinstinct.items import ActivinstinctItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["activinstinct.com"]
  start_urls = ["http://www.activinstinct.com/more-sports/outdoor/accessories/",
                "http://www.activinstinct.com/more-sports/outdoor/base-layer/",
                "http://www.activinstinct.com/more-sports/outdoor/clothing/",
                "http://www.activinstinct.com/more-sports/outdoor/cooking-equipment-utensils/",
                "http://www.activinstinct.com/more-sports/outdoor/food-drink-storage/",
                "http://www.activinstinct.com/more-sports/outdoor/gps-and-watches/",
                "http://www.activinstinct.com/more-sports/outdoor/rucksacks/",
                "http://www.activinstinct.com/more-sports/outdoor/walking-and-hiking/"
                "http://www.activinstinct.com/more-sports/outdoor/sleeping-bags/",
                "http://www.activinstinct.com/more-sports/outdoor/socks/",
                "http://www.activinstinct.com/more-sports/outdoor/tents/",
                "http://www.activinstinct.com/more-sports/outdoor/walking-poles/",
                "http://www.activinstinct.com/racket-sports/tennis/shoes/",
                "http://www.activinstinct.com/racket-sports/tennis/ball-machines/",
                "http://www.activinstinct.com/racket-sports/tennis/accessories-and-nets/",
                "http://www.activinstinct.com/running/accessories/",
                "http://www.activinstinct.com/running/athletic-supports/",
                "http://www.activinstinct.com/running/bags/",
                "http://www.activinstinct.com/running/base-layer/",
                "http://www.activinstinct.com/running/clothing/"
                "http://www.activinstinct.com/running/mobile-app-accessories/",
                "http://www.activinstinct.com/running/shoes/",
                "http://www.activinstinct.com/running/socks/"
                "http://www.activinstinct.com/running/sports-nutrition/",
                "http://www.activinstinct.com/running/watches-and-heart-rate-monitors/",
                "http://www.activinstinct.com/racket-sports/squash/bags/",
                "http://www.activinstinct.com/racket-sports/squash/accessories/",                
                "http://www.activinstinct.com/racket-sports/squash/shoes/",
                "http://www.activinstinct.com/racket-sports/squash/clothing/",
                "http://www.activinstinct.com/racket-sports/squash/mini-squash/",
                "http://www.activinstinct.com/racket-sports/badminton/rackets/talbot-torro/",
                "http://www.activinstinct.com/racket-sports/badminton/rackets/ashaway/",
                "http://www.activinstinct.com/triathlon/accessories/",
                "http://www.activinstinct.com/triathlon/base-layer/",
                "http://www.activinstinct.com/triathlon/bikes-and-accessories/",
                "http://www.activinstinct.com/triathlon/clothing/",
                "http://www.activinstinct.com/triathlon/goggles-and-masks/",
                "http://www.activinstinct.com/triathlon/mobile-app-accessories/",
                "http://www.activinstinct.com/triathlon/shoes/",
                "http://www.activinstinct.com/triathlon/swimwear/",
                "http://www.activinstinct.com/triathlon/watches-and-heart-rate-monitors/",
                "http://www.activinstinct.com/triathlon/wetsuits/",
                "http://www.activinstinct.com/more-sports/football/accessories/",
                "http://www.activinstinct.com/more-sports/football/athletic-supports/",
                "http://www.activinstinct.com/more-sports/football/bags/",
                "http://www.activinstinct.com/more-sports/football/balls/",
                "http://www.activinstinct.com/more-sports/football/base-layer/",
                "http://www.activinstinct.com/more-sports/football/boots/",
                "http://www.activinstinct.com/more-sports/football/clothing/",
                "http://www.activinstinct.com/more-sports/football/gloves/",
                "http://www.activinstinct.com/more-sports/football/goals-and-nets/",
                "http://www.activinstinct.com/more-sports/football/replica-kits/",
                "http://www.activinstinct.com/more-sports/football/sports-nutrition/",
                "http://www.activinstinct.com/more-sports/football/training-equipment/",
                "http://www.activinstinct.com/cricket/accessories/",
                "http://www.activinstinct.com/cricket/bags/",
                "http://www.activinstinct.com/cricket/balls/",
                "http://www.activinstinct.com/cricket/base-layer/",
                "http://www.activinstinct.com/cricket/bats/","http://www.activinstinct.com/cricket/clothing/","http://www.activinstinct.com/cricket/cricket-sets/","http://www.activinstinct.com/cricket/international-shirts/","http://www.activinstinct.com/cricket/kwik-cricket/","http://www.activinstinct.com/cricket/protection/","http://www.activinstinct.com/cricket/shoes/","http://www.activinstinct.com/cricket/training/","http://www.activinstinct.com/cricket/wicket-keeping/",
                "http://www.activinstinct.com/rugby/accessories/","http://www.activinstinct.com/rugby/athletic-supports/","http://www.activinstinct.com/rugby/bags/","http://www.activinstinct.com/rugby/balls/","http://www.activinstinct.com/rugby/base-layer/","http://www.activinstinct.com/rugby/boots/","http://www.activinstinct.com/rugby/clothing/","http://www.activinstinct.com/rugby/kicking-tees/","http://www.activinstinct.com/rugby/mouthguards/","http://www.activinstinct.com/rugby/posts/","http://www.activinstinct.com/rugby/protection/","http://www.activinstinct.com/rugby/replica-shirts/","http://www.activinstinct.com/rugby/sports-nutrition/","http://www.activinstinct.com/rugby/training-equipment/",
                "http://www.activinstinct.com/fitness/accessories/","http://www.activinstinct.com/fitness/athletic-supports/","http://www.activinstinct.com/fitness/boxing/","http://www.activinstinct.com/fitness/clothing/","http://www.activinstinct.com/fitness/cross-trainers/","http://www.activinstinct.com/fitness/exercise-bikes/","http://www.activinstinct.com/fitness/fitness-equipment/","http://www.activinstinct.com/fitness/mobile-app-accessories/","http://www.activinstinct.com/fitness/multi-gyms-and-benches/","http://www.activinstinct.com/fitness/rowing-machines/","http://www.activinstinct.com/fitness/shoes/","http://www.activinstinct.com/fitness/sports-nutrition/","http://www.activinstinct.com/fitness/treadmills-running-machines/","http://www.activinstinct.com/fitness/watches-and-heart-rate-monitors/",
                "http://www.activinstinct.com/fitness/weight-lifting/","http://www.activinstinct.com/fitness/yoga/"             
                ]             
                      
                
                
                
                
                
                
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//ul[@id="pagination-digg"]',)), follow= True),
    Rule (SgmlLinkExtractor(restrict_xpaths=('//ul[@class="clearfix"]',))
    , callback="parse_items", follow= True),)
    
  def parse_items(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//html")
    items = []
    for titles in titles:
      item = ActivinstinctItem()
      item ["productname"] = titles.select("//h1[@class='black']/text()").extract()      
      item ["MRP"] = titles.select("//p[@class='blue']/text()").extract()
      item ["SP"] = titles.select("//p[@id='product-price']/text()").extract()
      item ["Stock"] = titles.select("//div[@class='notifyMe-soldout']/text()").extract()
      item ["SKU"] = titles.select("//div/p[@class='gray']/text()").extract()      
      item ["imgurl"] = titles.select("//div[@id='product-image-view']/div/a/img/@src").extract()
      item ["Description"] = titles.select("//div[@id='hp_fix_desc']").extract()
      item ["Size"] = titles.select("//li/a[@class='button3']/span/text()").extract()
      item ["category"] = titles.select("//div[@id='breadcrumbs']/a/text()").extract()
      
      
      items.append(item)
      return(items)





