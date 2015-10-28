from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.spider import BaseSpider
import urlparse ,re, json, unicodecsv,csv
from scrapy.http.request import Request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import string

class SquashSpider(CrawlSpider):
		name = 'squash'	 
		allowed_domains = ['liveyoursport.com']
		start_urls = ['http://www.liveyoursport.com']    
		rules = (Rule(SgmlLinkExtractor(restrict_xpaths=('//*[contains(concat(" ", normalize-space(@class), " "), " sf-menu ")]/li[1]//descendant::ul/descendant::ul',))
				, callback='parse_items', follow=True),)
				
				  
		def parse_items(self, response):
			print response.url