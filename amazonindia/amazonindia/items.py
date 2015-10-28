# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class AmazonindiaItem(Item):
    # define the fields for your item here like:
    # name = Field()
    productname = Field()
    MRP = Field()
    SP = Field()
    MarketplaceSP = Field()
    SKU = Field()
    imgurl = Field()
    Stock = Field()
    URL = Field()
    pass
