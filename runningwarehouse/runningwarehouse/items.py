# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BigCItem(scrapy.Item):
    
    Item_Type                     = scrapy.Field()
    Product_Name                  = scrapy.Field()
    Retail_Price                  = scrapy.Field()
    Sale_Price                    = scrapy.Field()
    Price                         = scrapy.Field()
    Brand_Name                    = scrapy.Field()
    Product_Code                  = scrapy.Field()    
    Product_Description           = scrapy.Field()
    Product_Image_File1            = scrapy.Field()
    Product_Image_File2           = scrapy.Field()
    Product_Image_File3             = scrapy.Field()
    Product_Image_File4           = scrapy.Field()
    Product_Image_File5           = scrapy.Field()
    Product_Image_File6           = scrapy.Field()
    Category                      = scrapy.Field()
    Category2                     = scrapy.Field()
    Category3                     = scrapy.Field()
    Option_Set                    = scrapy.Field()
    MetaDescription   = scrapy.Field()
    TitleTag  = scrapy.Field()
    Product_Availability          = scrapy.Field()
    Current_Stock                 = scrapy.Field()
    Free_Shipping                 = scrapy.Field()
    Sort_Order                    = scrapy.Field()
    Product_Image_Description_1   = scrapy.Field()
    Product_Image_Is_Thumbnail_1  = scrapy.Field()
    Track_Inventory               = scrapy.Field()
    Product_Image_Sort_1          = scrapy.Field()
    Product_Image_Sort_2          = scrapy.Field()
    Product_Image_Sort_3          = scrapy.Field()
    Product_Image_Sort_4          = scrapy.Field()
    Product_Image_Sort_5          = scrapy.Field()
    Product_Image_Sort_6          = scrapy.Field()
    variants                      = scrapy.Field()
    variant                      = scrapy.Field()
    id1                           = scrapy.Field()
    color                         = scrapy.Field()
    size                         = scrapy.Field()
    model_number =                   scrapy.Field()
    imageSetUrls    = scrapy.Field()
    imageSetUrls2   = scrapy.Field()
    size_width_list = scrapy.Field()
    image           = scrapy.Field()
    sku                  = scrapy.Field()
    Product_ID = scrapy.Field()
    video = scrapy.Field()
    
    pass
