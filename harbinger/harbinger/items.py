# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class HarbingerItem(Item):
    productname = Field()
    imgurl = Field()
    imgurl1 = Field()
    Price = Field()
    description = Field()
    category = Field()
    pass
