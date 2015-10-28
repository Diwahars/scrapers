# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class LYSPriceItem(Item):
    # define the fields for your item here like:
    # name = Field()
    productname = Field()
    MRP = Field()
    SKU = Field()
    SP = Field()
    stock = Field()
    URL = Field()
    imgurl = Field()
    variant = Field()
    varname = Field()
    description = Field()
    pass
