# -*- coding: utf-8 -*-

# Scrapy settings for imagescrapper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'imagescrapper'

SPIDER_MODULES = ['imagescrapper.spiders']
NEWSPIDER_MODULE = 'imagescrapper.spiders'
DUPEFILTER_CLASS = 'scrapy.dupefilter.BaseDupeFilter'
##
##LOG_STDOUT = True
##LOG_FILE = 'debug_log.txt'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'imagescrapper (+http://www.yourdomain.com)'
