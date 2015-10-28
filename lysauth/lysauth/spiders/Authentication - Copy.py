from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from lysauth.CustItem import CustItem
import urlparse 
from scrapy.http import FormRequest, Request


class MySpider(CrawlSpider):
    name = 'auth'
    allowed_domains = ['liveyoursport.com']
    login_page = 'http://www.liveyoursport.com/administration'
    start_urls = ['http://www.liveyoursport.com/administration/customers?page=1',]   
                 

    rules = (Rule (SgmlLinkExtractor(allow=(),
                                   restrict_xpaths=('//div[@class="pagination pagination-right"][1]/ul/li',)),
                 follow= True),
    Rule (SgmlLinkExtractor(restrict_xpaths=
                            ('//table[@class="table table-striped table-bordered"]/tbody',))
    , callback="parse_item", follow= True),)  

    
    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        return FormRequest.from_response(response,
                    formdata={'employee[email]': 'siddharth@liveyoursport.com', 'employee[password]': 'liveyoursport!@#'},
                    formxpath='//form[@id="new_employee"]',
                    callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "Orders" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            return Request(url='http://www.liveyoursport.com/administration/customers?page=2',)                                  
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//head")
        items = []
        for titles in titles:
            item = CustItem()
            item ["Name"] = titles.select("//div[@id='info']/table/tr[1]/td[2]/text()").extract()
            item ["Email"] = titles.select("//div[@id='info']/table/tr[2]/td[2]/text()").extract()
            item ["Mobile"] = titles.select("//div[@id='info']/table/tr[4]/td[2]/text()").extract()
            item ["KL"] = titles.select("//div[@id='addresses']/table/tr[2]/td[1]/text()").extract()   #Name that appears in the saved address
            item ["N"] = titles.select("//div[@id='addresses']/table/tr[2]/td[3]/text()").extract()  #The first address line in the saved address
            item ["O"] = titles.select("//div[@id='addresses']/table/tr[2]/td[4]/text()").extract()   #The second address line in the saved address
            item ["P"] = titles.select("//div[@id='addresses']/table/tr[2]/td[6]/text()").extract()  #The city in the saved address
            item ["Q"] = titles.select("//div[@id='addresses']/table/tr[2]/td[7]/text()").extract()   #The state in the saved address
            item ["R"] = titles.select("//div[@id='addresses']/table/tr[2]/td[8]/text()").extract()   #The zip or postal code in the saved address
            item ["S"] = titles.select("//div[@id='addresses']/table/tr[2]/td[5]/text()").extract()   #The country in the saved address
            item ["T"] = titles.select("//div[@id='addresses']/table/tr[2]/td[2]/text()").extract()  #The phone number associated with the saved address
            item ["G"] = titles.select("//div[@id='orders']/table/tr[2]/td[1]/a/text()").extract()   #OrderNumber
            items.append(item)
            return(items)
