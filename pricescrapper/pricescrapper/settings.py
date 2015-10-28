# -*- coding: utf-8 -*-

# Scrapy settings for pricescrapper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'pricescrapper'

SPIDER_MODULES = ['pricescrapper.spiders']
NEWSPIDER_MODULE = 'pricescrapper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13'

# DOWNLOADER_MIDDLEWARES = {
    # 'pricescrapper.middlewares.ProxyMiddleware': 1,
    
# }

DEFAULT_REQUEST_HEADERS = {
    'Referer': 'http://www.google.com'

}