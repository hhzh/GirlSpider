# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GirlspiderItem(scrapy.Item):
    pass


class MMJPGSpiderItem(scrapy.Item):
    title = scrapy.Field()
    img_url = scrapy.Field()
    path = scrapy.Field()
    tags = scrapy.Field()


class MM131SpiderItem(scrapy.Item):
    title = scrapy.Field()
    tag = scrapy.Field()
    img_url = scrapy.Field()
    path = scrapy.Field()

class ZbjuranSpiderItem(scrapy.Item):
    title = scrapy.Field()
    tag = scrapy.Field()
    img_url = scrapy.Field()
    path = scrapy.Field()