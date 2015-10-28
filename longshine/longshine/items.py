# Define here the models for your scraped s
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/s.html

from scrapy.item import Item, Field

class longshineItem(Item):

    productname = Field()
    MRP = Field()
    brand = Field()   
    sku = Field()
    imgurl = Field()
    imgurl1 = Field()
    Description = Field()
    Specification = Field()
    Color = Field()
    Size = Field()
    category = Field()
    category1 = Field()
    
    pass
