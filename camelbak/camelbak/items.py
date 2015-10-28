# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CamelbakItem(Item):
    productname = Field()
    imgurl = Field()
    imgurl2 = Field()
    stock = Field()
    description = Field()
    SP = Field()
    Video = Field()
    
    pass
