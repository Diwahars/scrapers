from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from flipkart.itemsPrice import FlipkartPriceItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "price"
  allowed_domains = ["flipkart.com"]
  start_urls = ["http://www.flipkart.com/babolat-aeropro-drive-gt-2013-unstrung-4-3-8-tennis-racquet/p/itmdg5etbruyzkkk",
                "http://www.flipkart.com/babolat-aeropro-drive-gt-2013-unstrung-4-3-8-tennis-racquet/p/itmdg5etbruyzkkk",
                "http://www.flipkart.com/babolat-aeropro-lite-gt-2013-unstrung-4-3-8-tennis-racquet/p/itmdg5et5ryhgxzh",
                "http://www.flipkart.com/babolat-aeropro-team-gt-2013-unstrung-4-3-8-tennis-racquet/p/itmdg5eta3sj3ypy",
                "http://www.flipkart.com/babolat-pure-drive-lite-gt-2013-4-3-8-unstrung-tennis-racquet/p/itmdj3x3qhzwazjs",
                "http://www.flipkart.com/babolat-pure-drive-lite-gt-2013-4-3-8-unstrung-tennis-racquet/p/itmdj3x3qhzwazjs",
                "http://www.flipkart.com/babolat-pure-drive-roddick-gt-2013-4-3-8-unstrung-tennis-racquet/p/itmdj3x3kxufhbne",
                "http://www.flipkart.com/babolat-pure-drive-roddick-gt-2013-4-3-8-unstrung-tennis-racquet/p/itmdj3x3kxufhbne",
                "http://www.flipkart.com/babolat-pure-drive-roddick-gt-unstrung-tennis-racquet/p/itmdenvcbzz5zat5",
                "http://www.flipkart.com/butterfly-amultart-zl-carbon-fl-blade-table-tennis/p/itmdewsmswhbh4j7",
                "http://www.flipkart.com/butterfly-spin-art-table-tennis-rubber/p/itmdtaffsfjmmrpq",
                "http://www.flipkart.com/butterfly-timo-boll-zlf-fl-blade-table-tennis/p/itmdewsnhgzttrrh",
                "http://www.flipkart.com/donic-waldner-black-devil-table-tennis-blade/p/itmdgn6egwnurbrc",
                "http://www.flipkart.com/head-115-ct-strung-squash-racquet/p/itmdcz7j5k3gwrgp",
                "http://www.flipkart.com/head-aft-blast-strung-squash-racquet/p/itmdzbwpyu97h3p3",
                "http://www.flipkart.com/head-aft-flash-strung-squash-racquet/p/itmdcnwa5fxuthun",
                "http://www.flipkart.com/head-microgel-power-laser-strung-squash-racquet/p/itmdcz7jxrzqgsf9",
                "http://www.flipkart.com/head-neon-130-strung-squash-racquet/p/itmdcnwarwgfgemb",
                "http://www.flipkart.com/head-youtek-graphene-speed-mp-g3-unstrung-tennis-racquet/p/itmdku4ndkgycquu",
                "http://www.flipkart.com/head-youtek-graphene-speed-pro-g3-unstrung-tennis-racquet/p/itmdku4n4yapkxhh",
                "http://www.flipkart.com/joola-5005-energy-max-table-tennis-rubber/p/itmdcgefbhrhjdzg",
                "http://www.flipkart.com/prince-tf-storm-strung-squash-racquet/p/itmdcnwahncbgejd",
                "http://www.flipkart.com/tecnifibre-carboflex-130-2008-textalium-squash-racquet/p/itmdt69s6sbjh646",
                "http://www.flipkart.com/tecnifibre-carboflex-140-basal-tex-squash-racquet/p/itmdt69smggxdaww",
                "http://www.flipkart.com/tecnifibre-carboflex-speed-squash-racquet/p/itmdt69saq3zhaee",
                "http://www.flipkart.com/tecnifibre-supreme-caliber-135-squash-racquet/p/itmdt69szp5fhz9j",
                "http://www.flipkart.com/wilson-ps-6-1-100-blx2-frm3-unstrung-tennis-racquet/p/itmdg8wynsuynrzd",
                "http://www.flipkart.com/wilson-six-one-team-95-blx-unstrung-tennis-racquet/p/itmdcnwaw2azs8ux",
                "http://www.flipkart.com/wilson-steam-99s-g3-unstrung-tennis-racquet/p/itmdg8wy7tyzvada",
                "http://www.flipkart.com/yonex-arcsaber-7-g4-unstrung-badminton-racquet/p/itmdfyr9pqznrcjk",
                "http://www.flipkart.com/yonex-arcsaber-7-g4-unstrung-badminton-racquet/p/itmdfyr9pqznrcjk",
                "http://www.flipkart.com/yonex-arcsaber-i-slash-g4-strung-badminton-racquet/p/itmdmkjcvzp77awc",
                "http://www.flipkart.com/yonex-nanospeed-9900-g4-strung-badminton-racquet/p/itmdrubwft97qfhs",
                "http://www.flipkart.com/yonex-nanospeed-9900-g4-strung-badminton-racquet/p/itmdrubwft97qfhs?semcmpid=sem_6332071087_sf_goog&tgi=sem,1,G,6332071087,g,search,,31744812134,1t1,b,%2Byonex%20%2Bnanospeed%20%2B9900,c,,,,,,,",
                "http://www.flipkart.com/yonex-voltric-5-g4-strung-badminton-racquet/p/itmdcnwahu966mug",
                ] 
     
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//head")
    items = []
    for titles in titles:
      item = FlipkartPriceItem()
      item ["productname"] = titles.select("//h1[@itemprop='name']/text()").extract()
      item ["MRP"] = titles.select("//span[@class='price list old-price']/text()").extract()
      item ["SP"] = titles.select("//span[@class='fk-font-verybig pprice fk-bold']/text()").extract()
      item ["stock"] = titles.select("//div[@class='stock-status instock']/text()").extract()
      item ["SKU"] = titles.select("//meta[@name='og_url']/@content").extract()
      item ["URL"] = titles.select("//link[1]/@href").extract()
           
      items.append(item)
      return(items)


