from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from imagescrapper.items import BigCItem
import urlparse
import re

import pandas as pd
df = pd.read_csv('test.csv')
dict = df.ProductName

for a in dict:
  print str(a)
  
  


    
