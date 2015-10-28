from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from healthkart.ItemsPrice import HealthkartPriceItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "price"
  allowed_domains = ["healthkart.com"]
  start_urls = ["http://www.healthkart.com/sv/dunlop-biomimetic-ultimate-squash-racket/SP-19839",
                "http://www.healthkart.com/sv/dunlop-rage-25-squash-racket/SP-19838",
                "http://www.healthkart.com/sv/head-aft-flash-squash-racket/SP-13092",
                "http://www.healthkart.com/sv/stag-center-fold-indoor-table-tennis/SP-12835",
                "http://www.healthkart.com/sv/stag-family-model-indoor-outdoor-tt-table-(c.e.n.-certified)/SP-12848",
                "http://www.healthkart.com/sv/stag-international-indoor-tt-table-(i.t.t.f.-approved)/SP-12828",
                "http://www.healthkart.com/sv/stag-sleek-model-indoor-tt-table/SP-12837",
                "http://www.healthkart.com/sv/tecnifibre-dynergy-max-kick-step-squash-racket/SP-13998",
                "http://www.healthkart.com/sv/tecnifibre-master-carboflex-130-basaltex-squash-racket/SP-14022",
                "http://www.healthkart.com/sv/tecnifibre-supreme-ng-130-squash-racket/SP-14000",
                "http://www.healthkart.com/sv/yonex-arcsaber-z-slash-badminton-racket/SP-12484",
                "http://www.healthkart.com/sv/yonex-nanoray-700-fx-badminton-racket/SP-12472",
                "http://www.healthkart.com/sv/yonex-nanoray-700rp-badminton-racket/SP-12471",
                "http://www.healthkart.com/sv/yonex-nanoray-700rp-badminton-racket/SP-12471",
                "http://www.healthkart.com/sv/yonex-nanospeed-9900-badminton-racket/SP-12466",
                "http://www.healthkart.com/sv/yonex-voltric-80-badminton-racket/SP-13525",
                "http://www.healthkart.com/sv/yonex-voltric-z-force-badminton-racket/SP-14203",
                               ] 
                                     
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//head")
    items = []
    for titles in titles:
      item = HealthkartPriceItem()
      item ["productname"] = titles.select("//span[@class='fnt-bold fnt-ttl']/text()").extract()
      item ["MRP"] = titles.select("//span[@class='strikethrough'][1]/text()").extract()
      item ["SP"] = titles.select("//span[@class='sucss-txt']/text()").extract()
      item ["stock"] = titles.select("//div[@class='fnt-caps mrgn-t-5']/text()").extract()      
      item ["URL"] = titles.select("//link[1]/@href").extract()
           
      items.append(item)
      return(items)


