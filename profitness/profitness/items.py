# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ProfitnessItem(Item):
    productname = Field()
    MRP = Field()
    id = Field()
    URL = Field()
    imgurl = Field()
    description = Field()
    description1 = Field()
    description2 = Field()
    pass
