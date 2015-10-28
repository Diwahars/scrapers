# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class AxisItem(Item):
    # define the fields for your item here like:
    # name = Field()
    productname = Field()
    sku = Field()
    MRP = Field()
    SP = Field()
    Description = Field()
    Specification = Field()
    imgurl = Field()
    imgurl1 = Field()
    category = Field()
    Size = Field()
    Color = Field()
    Stock = Field()
    
    
    pass
