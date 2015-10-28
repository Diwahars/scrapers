from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from LYS.itemsPrice import LYSPriceItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "review"
  allowed_domains = ["liveyoursport.com"]
  start_urls = ["http://www.liveyoursport.com//products?category=tennis-equipment",
"http://www.liveyoursport.com//products?category=Tennis+Rackets",
"http://www.liveyoursport.com//products?category=Tennis_balls",
"http://www.liveyoursport.com//products?category=Tennis_grips",
"http://www.liveyoursport.com//products?category=Tennis_Strings",
"http://www.liveyoursport.com//products?category=tennis_apparel-and-shoes",
"http://www.liveyoursport.com//products?category=Tennis_bags",
"http://www.liveyoursport.com//products?category=string-machine",
"http://www.liveyoursport.com//products?category=tennis-electronics",
"http://www.liveyoursport.com//products?category=Tennis_Ball_Machines",
"http://www.liveyoursport.com//products?category=more-tennis-equipment",
"http://www.liveyoursport.com//products?category=badminton",
"http://www.liveyoursport.com//products?category=replacement-grip--4",
"http://www.liveyoursport.com//products?category=Badminton+Rackets",
"http://www.liveyoursport.com//products?category=badminton_grips",
"http://www.liveyoursport.com//products?category=badminton_shuttlecocks",
"http://www.liveyoursport.com//products?category=Badminton-Strings",
"http://www.liveyoursport.com//products?category=badminton_footwear",
"http://www.liveyoursport.com//products?category=Badminton-bags",
"http://www.liveyoursport.com//products?category=more-badminton-equipment",
"http://www.liveyoursport.com//products?category=table-tennis",
"http://www.liveyoursport.com//products?category=apparel-and-shoes",
"http://www.liveyoursport.com//products?category=table_tennis_blades",
"http://www.liveyoursport.com//products?category=table_tennis_rubbers",
"http://www.liveyoursport.com//products?category=Table_Tennis_balls",
"http://www.liveyoursport.com//products?category=Table-Tennis-tables",
"http://www.liveyoursport.com//products?category=table-tennis-bats",
"http://www.liveyoursport.com//products?category=more-table-tennis-equipment",
"http://www.liveyoursport.com//products?category=cricket",
"http://www.liveyoursport.com//products?category=apparel--15",
"http://www.liveyoursport.com//products?category=cricket-bats",
"http://www.liveyoursport.com//products?category=cricket-sets",
"http://www.liveyoursport.com//products?category=Cricket-gloves",
"http://www.liveyoursport.com//products?category=Cricket-helmets",
"http://www.liveyoursport.com//products?category=Cricket-pads-and-guards",
"http://www.liveyoursport.com//products?category=Cricket-balls",
"http://www.liveyoursport.com//products?category=more-cricket-equipment",
"http://www.liveyoursport.com//products?category=football",
"http://www.liveyoursport.com//products?category=footballs",
"http://www.liveyoursport.com//products?category=gloves--10",
"http://www.liveyoursport.com//products?category=shin-guards",
"http://www.liveyoursport.com//products?category=Football-training-equipment",
"http://www.liveyoursport.com//products?category=footwear--3",
"http://www.liveyoursport.com//products?category=Football-apparel",
"http://www.liveyoursport.com//products?category=more-football-equipment",
"http://www.liveyoursport.com//products?category=basketball",
"http://www.liveyoursport.com//products?category=basketballs",
"http://www.liveyoursport.com//products?category=Basketball-back-boards",
"http://www.liveyoursport.com//products?category=Basketball-rings",
"http://www.liveyoursport.com//products?category=Basketball-footwear",
"http://www.liveyoursport.com//products?category=Basketball-apparel",
"http://www.liveyoursport.com//products?category=more-basketball-equipment",
"http://www.liveyoursport.com//products?category=hockey",
"http://www.liveyoursport.com//products?category=Hockey-balls",
"http://www.liveyoursport.com//products?category=ice-hockey",
"http://www.liveyoursport.com//products?category=Hockey-protective-gear",
"http://www.liveyoursport.com//products?category=Hockey-sticks",
"http://www.liveyoursport.com//products?category=more-hockey-equipment",
"http://www.liveyoursport.com//products?category=running",
"http://www.liveyoursport.com//products?category=Running-electronics",
"http://www.liveyoursport.com//products?category=more-cycling-equipment",
"http://www.liveyoursport.com//products?category=running-bottles",
"http://www.liveyoursport.com//products?category=running-spikes",
"http://www.liveyoursport.com//products?category=running-shoes",
"http://www.liveyoursport.com//products?category=Running-apparel",
"http://www.liveyoursport.com//products?category=running-rehab",
"http://www.liveyoursport.com//products?category=more-running-equipment",
"http://www.liveyoursport.com//products?category=cycling",
"http://www.liveyoursport.com//products?category=accessories--4",
"http://www.liveyoursport.com//products?category=city-bikes",
"http://www.liveyoursport.com//products?category=cycling-helmets",
"http://www.liveyoursport.com//products?category=electronics--6",
"http://www.liveyoursport.com//products?category=folding-bikes",
"http://www.liveyoursport.com//products?category=hybrid-bikes",
"http://www.liveyoursport.com//products?category=junior-bikes",
"http://www.liveyoursport.com//products?category=maintenance-tools",
"http://www.liveyoursport.com//products?category=more-running-equipment",
"http://www.liveyoursport.com//products?category=mountain-bikes",
"http://www.liveyoursport.com//products?category=road-bikes",
"http://www.liveyoursport.com//products?category=cycling-spares",
"http://www.liveyoursport.com//products?category=trekking-bikes",
"http://www.liveyoursport.com//products?category=cycling-apparel",
"http://www.liveyoursport.com//products?category=more-cycling-equipment",
"http://www.liveyoursport.com//products?category=swimming",
"http://www.liveyoursport.com//products?category=electronics--10",
"http://www.liveyoursport.com//products?category=fins",
"http://www.liveyoursport.com//products?category=goggles",
"http://www.liveyoursport.com//products?category=Swimming-goggles-and-masks",
"http://www.liveyoursport.com//products?category=Swimming-headgear",
"http://www.liveyoursport.com//products?category=swimming-accessories",
"http://www.liveyoursport.com//products?category=swimsuits",
"http://www.liveyoursport.com//products?category=more-swimming-equipment",
"http://www.liveyoursport.com//products?category=golf",
"http://www.liveyoursport.com//products?category=Golf-carts-bags-and-trolleys",
"http://www.liveyoursport.com//products?category=complete-golf-sets",
"http://www.liveyoursport.com//products?category=golf-drivers",
"http://www.liveyoursport.com//products?category=electronics--8",
"http://www.liveyoursport.com//products?category=golf-fairway-woods",
"http://www.liveyoursport.com//products?category=footwear--5",
"http://www.liveyoursport.com//products?category=golf-irons",
"http://www.liveyoursport.com//products?category=golf-putters",
"http://www.liveyoursport.com//products?category=swing-analyzers",
"http://www.liveyoursport.com//products?category=golf-wedges",
"http://www.liveyoursport.com//products?category=Golf-balls",
"http://www.liveyoursport.com//products?category=men-s-golf-clubs",
"http://www.liveyoursport.com//products?category=mens-Golf-apparel",
"http://www.liveyoursport.com//products?category=golf-gloves",
"http://www.liveyoursport.com//products?category=more-golf-equipment",
"http://www.liveyoursport.com//products?category=boxing",
"http://www.liveyoursport.com//products?category=boxing-accessories",
"http://www.liveyoursport.com//products?category=boxing-equipment",
"http://www.liveyoursport.com//products?category=Boxing-gloves",
"http://www.liveyoursport.com//products?category=more-sports",
"http://www.liveyoursport.com//products?category=athletics",
"http://www.liveyoursport.com//products?category=bags--8",
"http://www.liveyoursport.com//products?category=balls--7",
"http://www.liveyoursport.com//products?category=baseball--2",
"http://www.liveyoursport.com//products?category=chess-sets+and+equipment",
"http://www.liveyoursport.com//products?category=fencing",
"http://www.liveyoursport.com//products?category=Indoor-Board-games",
"http://www.liveyoursport.com//products?category=handballs-equipment",
"http://www.liveyoursport.com//products?category=lacrosse",
"http://www.liveyoursport.com//products?category=martial-arts-equipment",
"http://www.liveyoursport.com//products?category=multi-sports-equipment",
"http://www.liveyoursport.com//products?category=pool",
"http://www.liveyoursport.com//products?category=roller-skating-equipment",
"http://www.liveyoursport.com//products?category=rugby--2",
"http://www.liveyoursport.com//products?category=scooter",
"http://www.liveyoursport.com//products?category=shooting-balls-equipment",
"http://www.liveyoursport.com//products?category=skate-boarding-equipment",
"http://www.liveyoursport.com//products?category=softball-bat",
"http://www.liveyoursport.com//products?category=throw-balls",
"http://www.liveyoursport.com//products?category=tug-of-war",
"http://www.liveyoursport.com//products?category=volleyball-equipment",
"http://www.liveyoursport.com//products?category=racewalking-equipment",
"http://www.liveyoursport.com//products?category=water-sports",
"http://www.liveyoursport.com//products?category=adventure-and-outdoor",
"http://www.liveyoursport.com//products?category=climbing",
"http://www.liveyoursport.com//products?category=diving",
"http://www.liveyoursport.com//products?category=fishing",
"http://www.liveyoursport.com//products?category=hiking-and-mountaineering",
"http://www.liveyoursport.com//products?category=horse-riding",
"http://www.liveyoursport.com//products?category=kayaking",
"http://www.liveyoursport.com//products?category=sailing",
"http://www.liveyoursport.com//products?category=surfing",
"http://www.liveyoursport.com//products?category=target-sports",
"http://www.liveyoursport.com//products?category=triathlon",
"http://www.liveyoursport.com//products?category=fitness-machines",
"http://www.liveyoursport.com//products?category=elliptical-trainers",
"http://www.liveyoursport.com//products?category=exercise-bikes",
"http://www.liveyoursport.com//products?category=rowers",
"http://www.liveyoursport.com//products?category=stepper",
"http://www.liveyoursport.com//products?category=treadmills--3",
"http://www.liveyoursport.com//products?category=more-fitness-machines",
"http://www.liveyoursport.com//products?category=strength-training",
"http://www.liveyoursport.com//products?category=abs-and-core",
"http://www.liveyoursport.com//products?category=back",
"http://www.liveyoursport.com//products?category=functional-equipment",
"http://www.liveyoursport.com//products?category=medicine-balls",
"http://www.liveyoursport.com//products?category=more-strength-training-equipment",
"http://www.liveyoursport.com//products?category=lower-body-training",
"http://www.liveyoursport.com//products?category=upper-body-training",
"http://www.liveyoursport.com//products?category=Multi+Gym",
"http://www.liveyoursport.com//products?category=weights",
"http://www.liveyoursport.com//products?category=barbells",
"http://www.liveyoursport.com//products?category=benches",
"http://www.liveyoursport.com//products?category=combo",
"http://www.liveyoursport.com//products?category=dumbbells",
"http://www.liveyoursport.com//products?category=power-block",
"http://www.liveyoursport.com//products?category=vipr",
"http://www.liveyoursport.com//products?category=weight-benches",
"http://www.liveyoursport.com//products?category=weight-discs",
"http://www.liveyoursport.com//products?category=weight-lifting-jackets",
"http://www.liveyoursport.com//products?category=weight-racks",
"http://www.liveyoursport.com//products?category=fitness-accessories",
"http://www.liveyoursport.com//products?category=bags--3",
"http://www.liveyoursport.com//products?category=balance-and-flexibility",
"http://www.liveyoursport.com//products?category=cardio",
"http://www.liveyoursport.com//products?category=electronics--9",
"http://www.liveyoursport.com//products?category=icebath",
"http://www.liveyoursport.com//products?category=pull-up-and-push-up-bars",
"http://www.liveyoursport.com//products?category=rehab",
"http://www.liveyoursport.com//products?category=resistance-bands--4",
"http://www.liveyoursport.com//products?category=step-board",
"http://www.liveyoursport.com//products?category=steppers",
"http://www.liveyoursport.com//products?category=more-fitness-accessories",
"http://www.liveyoursport.com//products?category=yoga-and-pilates",
"http://www.liveyoursport.com//products?category=mats",
"http://www.liveyoursport.com//products?category=Stability+Balls",
"http://www.liveyoursport.com//products?category=apparel--5",
"http://www.liveyoursport.com//products?category=more-yoga-and-pilates-equipment",]


  rules = (Rule (SgmlLinkExtractor(allow=(),
                                   restrict_xpaths=('//div[@class="pagination pagination-right"]',)),
                 follow= True),
    Rule (SgmlLinkExtractor(restrict_xpaths=
                            ('//div[@class="product-list-container"]',))
    , callback="parse_items", follow= True),)  

           
  def parse_items(self, response):
    sel = Selector(response)
    
    
    item = LYSPriceItem()
    
    item ["productname"] = sel.xpath("//h1[@style='text-transform: none;']/text()").extract()    
    item ["SKU"] = sel.xpath("//div[@class='small-sub']/text()").extract()
    item ["URL"] = sel.xpath("//div[@class='fb-like']/@data-href").extract()
    yield item
    
    reviews = sel.xpath("//div[@class='feedback-text']/text()")
    
    

    for review in reviews:
      
      item ["SP"] = review.extract()
      
      item ["productname"] = ''
      item ["SKU"] = 'Review'
      item ["URL"] = ''
    

      yield item
      
    


    

