from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from LYS.CustItem import CustItem
import urlparse 
from scrapy.http import FormRequest, Request


class MySpider(CrawlSpider):
    name = 'auth1'
    allowed_domains = ['liveyoursport.com']
    login_page = 'http://www.liveyoursport.com/administration'
    start_urls = ['http://www.liveyoursport.com/administration/customers?page=2',]
                  

    rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//table[@class="table table-striped table-bordered"]/tbody',))
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
            return Request(url='http://www.liveyoursport.com/administration/customers?page=2')
            
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse_item(self, response):
        sel = Selector(response)
        item = CustItem()
        item ["Name"] = sel.xpath("//div[@id='info']/table/tbody/tr[1]/td[2]/text()").extract() 
        item ["Email"] = sel.xpath("//div[@id='info']/table/tbody/tr[2]/td[2]/text()").extract() 
        item ["Mobile"] = sel.xpath("//div[@id='info']/table/tbody/tr[4]/td[2]/text()").extract() 
        item ["KL"] = sel.xpath("//div[@id='addresses']/table/tbody/tr[2]/td[1]/text()").extract()   #Name that appears in the saved address
        item ["N"] = sel.xpath("//div[@id='addresses']/table/tbody/tr[2]/td[3]/text()").extract()  #The first address line in the saved address
        item ["O"] = sel.xpath("//div[@id='addresses']/table/tbody/tr[2]/td[4]/text()").extract()   #The second address line in the saved address
        item ["P"] = sel.xpath("//div[@id='addresses']/table/tbody/tr[2]/td[6]/text()").extract()  #The city in the saved address
        item ["Q"] = sel.xpath("//div[@id='addresses']/table/tbody/tr[2]/td[7]/text()").extract()   #The state in the saved address
        item ["R"] = sel.xpath("//div[@id='addresses']/table/tbody/tr[2]/td[8]/text()").extract()   #The zip or postal code in the saved address
        item ["S"] = sel.xpath("//div[@id='addresses']/table/tbody/tr[2]/td[5]/text()").extract()   #The country in the saved address
        item ["T"] = sel.xpath("//div[@id='addresses']/table/tbody/tr[2]/td[2]/text()").extract()  #The phone number associated with the saved address
        item ["G"] = sel.xpath("//div[@id='orders']/table/tbody/tr[2]/td[1]/a/text()").extract()   #OrderNumber
        
        yield item
        
