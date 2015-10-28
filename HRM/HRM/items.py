# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class HrmItem(Item):
    productname = Field()
    MRP = Field()
    stock = Field()
    imgurl = Field()
    Description = Field()
    Size = Field()

    
   
    pass
