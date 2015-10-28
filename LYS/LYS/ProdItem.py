# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ProdItem(Item):
    ProductName = Field()    
    ProductCodeSKU = Field()
    SP = Field()
    ItemType = Field()
    vendorname = Field()
    vendorcode = Field()
    
    pass
