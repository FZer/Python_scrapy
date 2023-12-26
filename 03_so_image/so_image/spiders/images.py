# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json

class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['image.so.com']
    BASE_URL='http://image.so.com/zjl?ch=beauty&sn=%s&listtype=new&temp=1'
    #'http://image.so.com/zjl?ch=beauty&sn=30&listtype=new&temp=1'
    start_urls = [BASE_URL % 0]
    start_index = 0
    MAX_DOWNLOAD_NUM = 28           #因为页面加载是30的倍数，所以获取的图片也是30的倍数（虽然写的28，实际是30张图片；31张，实际是60张）。
    
    def parse(self, response):
        infos=json.loads(response.body.decode('utf-8'))
        yield{'image_urls':[info['qhimg_url'] for info in infos['list']]}
        self.start_index += infos['count']
        if infos['count'] > 0 and self.start_index < self.MAX_DOWNLOAD_NUM:
            yield Request(self.BASE_URL%self.start_index)
            