# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ToscrapeBookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# this is completed of flysky
# 定义封装书籍信息的Item类
class BookItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    review_rating = scrapy.Field()
    review_num = scrapy.Field()
    upc = scrapy.Field()
    stock = scrapy.Field()
    