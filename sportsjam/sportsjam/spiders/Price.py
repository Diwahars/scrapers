from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from sportsjam.priceitems import priceitem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "price"
  allowed_domains = ["sportsjam.in"]
  start_urls = ["http://www.sportsjam.in/Products/Buy-Sports-Badminton-Badminton-Rackets/Li-ning/Li-Ning-Woods-N90-II-Badminton-Racket-Online-India/pid-1005593.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Badminton-Badminton-Rackets/Yonex/YONEX-ArcSaber%C2%A011-Badminton-Racket-Online-India/pid-2838737.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Badminton-Badminton-Rackets/Yonex/YONEX-ArcSaber%C2%A0FB-Badminton-Racket-Online-India/pid-3022113.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Badminton-Badminton-Rackets/Yonex/YONEX-ArcSaber-I-Slash-Badminton-Racket-Online-India/pid-2143353.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Badminton-Badminton-Rackets/Yonex/YONEX-NanoRay-700RP-Badminton-Racket-Online-India/pid-1030807.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Badminton-Badminton-Rackets/Yonex/YONEX-Nanoray-800-Badminton-Racket-Online-India/pid-2143355.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Badminton-Badminton-Rackets/Yonex/YONEX-Nanoray-800-Badminton-Racket-Online-India/pid-2143355.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Badminton-Badminton-Rackets/Yonex/YONEX-Nanoray-Z-Speed-Badminton-Racket-Online-India/pid-3851115.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Badminton-Badminton-Rackets/Yonex/YONEX-Voltric-80-Badminton-Racket-Online-India/pid-984129.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Squash-Racquet/Prince/Prince-O3-Speedport-Silver-Squash-Racquet-Online-India/pid-1020667.aspx?Rfs=&pgctl=575313&cid=CU00037235",
"http://www.sportsjam.in/Products/Buy-Sports-Squash-Squash-Rackets/Dunlop/Dunlop-Biomimetic-Evolution-120-Squash-Racket-Online-India/pid-3571447.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Squash-Squash-Rackets/Dunlop/Dunlop-Biomimetic-Evolution-130-Squash-Racket-Online-India/pid-1033939.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Squash-Squash-Rackets/Dunlop/Dunlop-Biomimetic-Ultimate-Squash-Racket-Online-India/pid-1033940.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Squash-Squash-Rackets/Head/Head-Neon-130-Squash-Racket-Online-India/pid-1022416.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Squash-Squash-Rackets/Karakal/Karakal-SX-100-Gel-Squash-Racket-Online-India/pid-3571459.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Squash-Squash-Rackets/Karakal/Karakal-Tec-Gel-120-Squash-Racket-Online-India/pid-3571457.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Squash-Squash-Rackets/Prince/Prince-Exo3-Rebel-Squash-Racket-Online-India/pid-1005183.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Squash-Squash-Rackets/Prince/Prince-O3-Speedport-Black-Squash-Racket-Online-India/pid-1020666.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Squash-Squash-Rackets/Tecnifibre/Tecnifibre-Suprem-Calibur-135-Squash-Racket-Online-India/pid-5561366.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Squash-Squash-Rackets/Tecnifibre/Tecnifibre-Suprem-NG-130-Squash-Racket-Online-India/pid-1058454.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Blades/Butterfly/Butterfly-Amultart-ZL-Carbon-Table-Tennis-Blade-Online-India/pid-2152043.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Blades/Butterfly/Butterfly-Amultart-ZL-Carbon-Table-Tennis-Blade-Online-India/pid-2152043.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Blades/Butterfly/Butterfly-Timo-Boll-ZLC-Table-Tennis-Blade-Online-India/pid-2152041.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Blades/Donic/Donic-Waldner-Black-Devil-Table-Tennis-Blade-Online-India/pid-1024057.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Blades/Donic/Donic-Waldner-Legend-Carbon-Table-Tennis-Blade-Online-India/pid-5779344.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Blades/Tibhar/Tibhar-H-3-9-Table-Tennis-Blade-Online-India/pid-3491789.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Blades/Tibhar/Tibhar-Texo-C7-Table-Tennis-Blade-Online-India/pid-3491787.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Rubber/Butterfly/Butterfly-Spin-Art-Table-Tennis-Rubber-Online-India/pid-2152095.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Rubber/Butterfly/Butterfly-Tenergy-05-FX-Table-Tennis-Rubber-India-Online-Butterfly-Rubber/pid-2436980.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Rubber/Butterfly/Butterfly-Tenergy-64-Table-Tennis-Rubber-India-Online-Butterfly-Rubber/pid-2436982.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Rubber/Joola/Joola-Toni-Hold-AntiTopspin-25-Table-Tennis-Rubber-Online-India/pid-1584549.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Rubber/Tibhar/Tibhar-Evolution-EL--P-21-Table-Tennis-Rubber-Online-India/pid-3145729.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Rubber/Tibhar/Tibhar-Evolution-FX--P-21-Table-Tennis-Rubber-Online-India/pid-3145731.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Rubber/Yasaka/Yasaka-Phantom-007-Table-Tennis-Rubber-India-Online-Yasaka-Rubber/pid-4955923.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Tables/Stag/Stag-Center-Fold-Table-Tennis-Table-Online-India/pid-1100628.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Tables/Stag/Stag-Sleek-Table-Tennis-Table-Online-India/pid-1100630.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Tables/Stiga/Stiga-Premium-Roller-Table-Tennis-Table-Online-India/pid-1104612.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Table-Tennis-Table-Tennis-Tables/Stiga/Stiga-Superior-Roller-Table-Tennis-Table-Online-India/pid-1104609.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Babolat/Babolat-Aeropro-Drive-GT-2013-Tennis-Racquet-Online-Shop-India/pid-2217671.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Babolat/Babolat-Aeropro-Drive-GT-2013-Tennis-Racquet-Online-Shop-India/pid-2217671.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Babolat/Babolat-Aeropro-Drive-GT-2013-Tennis-Racquet-Online-Shop-India/pid-2217671.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Babolat/Babolat-Pure-Drive-Roddick-GT-Tennis-Racquet-Online-Shop-India/pid-2492463.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Babolat/Babolat-Pure-Drive-Roddick-GT-Tennis-Racquet-Online-Shop-India/pid-2492463.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Babolat/Babolat-Pure-Drive-Roddick-GT-Tennis-Racquet-Online-Shop-India/pid-2492463.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Head/Head-YOUTEK-Graphene-PWR-Speed-Tennis-Racquet-Online-Shop-India/pid-3030159.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Head/Head-YOUTEK-Graphene-PWR-Speed-Tennis-Racquet-Online-Shop-India/pid-3030159.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Head/Head-YOUTEK-Graphene-Radical-Pro-Tennis-Racquet-Online-Shop-India/pid-5069334.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Head/Head-YOUTEK-Graphene-Speed-Pro-Tennis-Racquet-Online-Shop-India/pid-2631313.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Head/Head-YOUTEK-Graphene-Speed-Pro-Tennis-Racquet-Online-Shop-India/pid-2631313.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Wilson/Wilson-Blade-98-BLX-BLX-Tennis-Racquet-Online-Shop-India/pid-4865703.aspx",
"http://www.sportsjam.in/Products/Buy-Sports-Tennis-Tennis-Racquets/Wilson/Wilson-Pro-Staff-Six-One-95-BLX-Tennis-Racquet-Online-Shop-India/pid-1761305.aspx",]

  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//head")
    items = []
    for titles in titles:
      item = priceitem()
      item ["productname"] = titles.select("//div[@class='container9']/div/h1/text()").extract()
      item ["MRP"] = titles.select("//span[@id='ctl00_ContentPlaceHolder1_Price_ctl00_lblMrp']/text()").extract()
      item ["SP"] = titles.select("//span[@id='ctl00_ContentPlaceHolder1_Price_ctl00_lblOfferPrice']/text()").extract()
      item ["stock"] = titles.select("//div[@class='container_stockavailability']/div/div/text()").extract()
      item ["URL"] = titles.select("//meta[@property='og:url']/@content").extract()
      items.append(item)
      return(items)


