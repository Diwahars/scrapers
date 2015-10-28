# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class GolfessentialsItem(Item):
    productname = Field()
    MRP = Field()
    SP = Field()
    imgurl = Field()
    Description = Field()
    Variant =  Field()
    pass
