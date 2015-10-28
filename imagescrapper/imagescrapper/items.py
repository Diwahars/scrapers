# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BigCItem(scrapy.Item):
    LYSProduct_Name                  = scrapy.Field()
    LYSURL                  = scrapy.Field()
    LYSID                  = scrapy.Field()
    LYSMRP                  = scrapy.Field()
    LYSSP                  = scrapy.Field()
    LYSStock                 = scrapy.Field()
    Category = scrapy.Field()
#Snapdeal Items
    SnapdealProductName   = scrapy.Field()
    SnapdealURL             = scrapy.Field()
    SnapdealMRP = scrapy.Field()
    SnapdealSP = scrapy.Field()
    SnapdealStock = scrapy.Field()
    SnapdealMatch = scrapy.Field()
    
    AmazonProductName     = scrapy.Field()
    AmazonURL             = scrapy.Field()
    AmazonMRP = scrapy.Field()
    AmazonSP = scrapy.Field()
    AmazonStock = scrapy.Field()
    AmazonMatch = scrapy.Field()
    

    FlipkartProductName     = scrapy.Field()
    FlipkartURL             = scrapy.Field()
    FlipkartMRP = scrapy.Field()
    FlipkartSP = scrapy.Field()
    FlipkartStock = scrapy.Field()
    FlipkartMatch = scrapy.Field()

    Description = scrapy.Field()
    imgurl = scrapy.Field()
    
    
    
 
    pass

