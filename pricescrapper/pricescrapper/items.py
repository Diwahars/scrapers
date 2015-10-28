# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BigCItem(scrapy.Item):

    Product_Name                  = scrapy.Field()
    URL                  = scrapy.Field()   
    MRP                  = scrapy.Field()
    SP                  = scrapy.Field()
    Stock                 = scrapy.Field()
    Category = scrapy.Field()
    sku =  scrapy.Field()
#Snapdeal Items
    Snapdeal__ProductName   = scrapy.Field()
    Snapdeal_URL             = scrapy.Field()
    Snapdeal_MRP = scrapy.Field()
    Snapdeal_SP = scrapy.Field()
    Snapdeal_Stock = scrapy.Field()    
    
    Amazon_ProductName     = scrapy.Field()
    Amazon_URL             = scrapy.Field()
    Amazon_MRP = scrapy.Field()
    Amazon_SP = scrapy.Field()
    Amazon_Stock = scrapy.Field()
    Amazon_Match = scrapy.Field()
    

    Flipkart_ProductName     = scrapy.Field()
    Flipkart_URL             = scrapy.Field()
    Flipkart_MRP = scrapy.Field()
    Flipkart_SP = scrapy.Field()
    Flipkart_Stock = scrapy.Field()
	
    Paytm_ProductName     = scrapy.Field()
    Paytm_URL             = scrapy.Field()
    Paytm_MRP = scrapy.Field()
    Paytm_SP = scrapy.Field()
    Paytm_Stock = scrapy.Field()
    

    Description = scrapy.Field()
    imgurl = scrapy.Field()
    index = scrapy.Field()
    
    
 
    pass

