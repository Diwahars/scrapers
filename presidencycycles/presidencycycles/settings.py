# -*- coding: utf-8 -*-

# Scrapy settings for presidencycycles project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'presidencycycles'

SPIDER_MODULES = ['presidencycycles.spiders']
NEWSPIDER_MODULE = 'presidencycycles.spiders'
# LOG_STDOUT = True
# LOG_FILE = 'debug_log.txt'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.16 Safari/534.24"
