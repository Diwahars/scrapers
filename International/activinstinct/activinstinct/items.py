# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ActivinstinctItem(Item):
    productname = Field()
    imgurl = Field()
    MRP = Field()
    SP = Field()
    Stock = Field()
    Description = Field()
    Size = Field()
    SKU = Field()
    
    
    
    pass
