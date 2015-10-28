from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from starkenn.items import BigCItem
import urlparse
from scrapy import log
import re
import csv

f = open("categories.csv")
csv_file = csv.reader(f)
starkenncat = []
LYScat = []

for row in csv_file:
  starkenncat.append(row[0])
  LYScat.append(row[1])

for i in range(len(starkenncat)):
  print starkenncat[i]
            
