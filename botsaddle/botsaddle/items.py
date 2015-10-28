# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BotsaddleItem(Item):
    productname = Field()
    MRP = Field()
    Description = Field()
    imgurl = Field()
    Category = Field()
    Subcategory= Field()
    SKU = Field()
    stock = Field()
    Variant = Field()
    
    pass
