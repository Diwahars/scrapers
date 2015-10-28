# Scrapy settings for acmefitness project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'acmefitness'

SPIDER_MODULES = ['acmefitness.spiders']
NEWSPIDER_MODULE = 'acmefitness.spiders'

##LOG_STDOUT = True
##LOG_FILE = 'debug_log.txt'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'acmefitness (+http://www.yourdomain.com)'
