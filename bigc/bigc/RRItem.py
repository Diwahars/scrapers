# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RoadrunnersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    productname     = scrapy.Field()
    mrp             = scrapy.Field()
    brand           = scrapy.Field()
    description     = scrapy.Field()
    description2     = scrapy.Field()
    sp              = scrapy.Field()
    vp              = scrapy.Field()
    img_url         = scrapy.Field()
    variant         = scrapy.Field()
    description     = scrapy.Field()
    sku             = scrapy.Field()
    image           = scrapy.Field()
    size_width_list = scrapy.Field()
    imageSetUrls    = scrapy.Field()
    imageSetUrls2   = scrapy.Field()
    color           = scrapy.Field()
    category           = scrapy.Field()
