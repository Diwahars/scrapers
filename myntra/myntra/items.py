# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MyntraItem(Item):
    # define the fields for your item here like:
    # name = Field()
    Item_Type = Field()
    Product_Code = Field()
    Product_Name = Field()
    Retail_Price = Field()
    Price = Field()
    Sale_Price = Field()
    Brand_Name = Field()
    Category = Field()
    Current_Stock = Field()
    Free_Shipping = Field()
    Product_Availability = Field()
    Product_Description = Field()
    Option_Set = Field()
    Product_Image_File = Field()
    Track_Inventory = Field()
    Product_Image_Description_1 = Field()
    Product_Image_Is_Thumbnail_1 = Field()
    Product_Image_Sort_1 = Field()
    Product_Image_Sort_2 = Field()
    Product_Image_Sort_3 = Field()
    Product_Image_Sort_4 = Field()
    Product_Image_Sort_5 = Field()
    
    
    
    pass
