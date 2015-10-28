# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class RbwItem(Item):
    # define the fields for your item here like:
    # name = Field()
    productname = Field()
    MRP = Field()
    MRP1 = Field()
    SP = Field()
    imgurl = Field()
    Description = Field()
    Variant = Field()
    SKU = Field()
    
    pass
