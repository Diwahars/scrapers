# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TynorItem(Item):
    productname = Field()
    SKU = Field()
    Description = Field()
    imgurl1 = Field()
    imgurl2 = Field()
    Size = Field()
    pass
