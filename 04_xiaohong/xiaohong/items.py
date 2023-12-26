# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaohongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    article_likes = scrapy.Field()
    author = scrapy.Field()
    userID = scrapy.Field()
    userIP = scrapy.Field()
    content = scrapy.Field()
    review = scrapy.Field()
    article_url = scrapy.Field()
    author_url = scrapy.Field()
    review_url = scrapy.Field()
