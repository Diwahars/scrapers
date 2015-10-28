from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from cosco.items import FlipkartPriceItem
import urlparse 
from scrapy.http.request import Request


class MySpider(CrawlSpider):
  name = "mojo"
  allowed_domains = ["cosco.in"]
  start_urls = ["http://cosco.in/sub_prod.php?prodid=1&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=1&from=8&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=263&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=2&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=3&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=102&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=155&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=183&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=4&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=4&from=8&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=180&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=179&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=5&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=10&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=6&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=7&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=11&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=231&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=232&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=233&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=234&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=235&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=14&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=14&from=8&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=177&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=249&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=252&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=290&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=289&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=291&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=292&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=293&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=294&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=295&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=296&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=297&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=298&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=299&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=300&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=301&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=302&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=303&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=304&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=305&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=306&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=307&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=17&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=103&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=158&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=105&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=18&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=75&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=75&from=8&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=73&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=73&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=76&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=76&from=8&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=77&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=63&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=78&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=79&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=79&from=8&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=154&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=265&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=337&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=324&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=323&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=325&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=326&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=338&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=339&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=340&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=342&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=343&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=344&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=345&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=70&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=334&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=335&lv=1&lc=I&catid=22",
                "http://cosco.in/sub_prod.php?prodid=336&lv=1&lc=I&catid=22",      
                "http://cosco.in/sub_prod.php?prodid=265&from=8&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=19&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=72&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=104&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=157&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=153&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=20&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=182&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=20&from=8&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=130&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=130&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=148&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=147&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=142&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=217&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=221&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=228&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=228&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=226&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=230&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=224&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=223&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=146&lv=1&lc=N&catid=21",
                "http://cosco.in/sub_prod.php?prodid=86&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=94&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=94&from=8&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=96&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=87&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=91&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=204&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=257&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=94&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=94&from=8&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=310&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=316&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=309&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=311&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=318&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=287&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=286&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=244&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=245&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=278&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=278&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=240&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=241&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=242&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=266&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=266&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=267&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=268&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=269&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=269&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=98&lv=1&lc=N&catid=23",
                "http://cosco.in/sub_prod.php?prodid=204&from=8&lv=1&lc=N&catid=23"                
                ]                
                
  rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//a[@target="basefrm"]',)),callback="parse_items", follow= True),)
     
  def parse_items(self, response):
    hxs = HtmlXPathSelector(response)
    titles = hxs.select("//html")
    items = []
    for titles in titles:
      item = FlipkartPriceItem()
      item ["productname"] = titles.select("//font[@color='#FFFFFF']/b/text()").extract()
      item ["imageurl"] = titles.select("//td[@align='right']/img/@src").extract()
      item ["description"] = titles.select("//tr").extract()
      
      
           
      items.append(item)
      return(items)


