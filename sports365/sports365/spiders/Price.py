from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from sports365.priceitems import priceitem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "price"
  allowed_domains = ["sports365.in"]
  start_urls = ["http://www.sports365.in/Products/Buy-Racket-Sports-Badminton-Rackets/Yonex/Buy-Yonex-ArcSaber-10-Badminton-Racket/pid-1063798.aspx",
"http://www.sports365.in/Products/Buy-Racket-Sports-Badminton-Rackets/Yonex/Buy-Yonex-ArcSaber-10-Badminton-Racket/pid-1063798.aspx",
"http://www.sports365.in/Products/Buy-Racket-Sports-Badminton-Rackets/Yonex/Buy-Yonex-ArcSaber-7-Badminton-Racket/pid-1063799.aspx",
"http://www.sports365.in/Products/Buy-Racket-Sports-Badminton-Rackets/Yonex/Buy-Yonex-ArcSaber-7-Badminton-Racket/pid-1063799.aspx",
"http://www.sports365.in/Products/Buy-Racket-Sports-Badminton-Rackets/Yonex/Buy-Yonex-ArcSaber-Z---Slash-Badminton-Racket/pid-1063797.aspx",
"http://www.sports365.in/Products/Buy-Racket-Sports-Badminton-Rackets/Yonex/Buy-Yonex-Nanoray-700-RP-Badminton-Racket/pid-1172011.aspx",
"http://www.sports365.in/Products/Buy-Racket-Sports-Badminton-Rackets/Yonex/Buy-Yonex-Nanoray-700-RP-Badminton-Racket/pid-1172011.aspx",
"http://www.sports365.in/Products/Buy-Racket-Sports-Badminton-Rackets/Yonex/yonex-arcsaber-11-badminton-racket/pid-3304757.aspx",
"http://www.sports365.in/Products/Buy-Racket-Sports-Badminton-Rackets/Yonex/yonex-arcsaber-11-badminton-racket/pid-3304757.aspx",
"http://www.sports365.in/Products/Buy-Racket-Sports-Badminton-Rackets/Yonex/Yonex-Arc-Saber-FB-Sonic--Badminton-Racket/pid-4177415.aspx",
"http://www.sports365.in/Products/Buy-Racket-Sports-Badminton-Rackets/Yonex/Yonex-Voltric-I-Force-Badminton-Racket---Bright-Pink/pid-4177413.aspx",

                ] 
     

  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//head")
    items = []
    for titles in titles:
      item = priceitem()
      item ["productname"] = titles.select("//div[@class='container9']/div/h1/text()").extract()
      item ["MRP"] = titles.select("//span[@id='ctl00_ContentPlaceHolder1_Price_ctl00_lblMrp']/text()").extract()
      item ["SP"] = titles.select("//span[@id='ctl00_ContentPlaceHolder1_Price_ctl00_lblOfferPrice']/text()").extract()
      item ["stock"] = titles.select("//div[@class='outofstock']/text()").extract()
      item ["SKU"] = titles.select("//div[@class='bucketgroup']/@id").extract()
      item ["URL"] = titles.select("//meta[@property='og:url']/@content").extract()
      items.append(item)
      return(items)


