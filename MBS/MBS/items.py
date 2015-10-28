# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MbsItem(Item):
    productname = Field()
    imgurl1 = Field()
    imgurl2 = Field()
    imgurl3 = Field()
    MRP = Field()
    SP = Field()
    stock = Field()
    Description = Field()
    SubCategory = Field()
    Category = Field()
    Size = Field()
    SKU = Field()
    Review = Field()
    
   
    pass
