# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
#---------------解决相对导入-------------
import sys
sys.path.append(r"D:\Code\python\scrapy\toscrape_book")
from toscrape_book.items import BookItem

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    #start_url,起始爬取点，可以有多个
    start_urls = ['http://books.toscrape.com/']
# 书籍列表页面的解析函数.
#当页面下载完成后，Scrapy引擎会回调一个指定的页面解析函数（默认为parse方法）
#页面解析函数通常被实现成一个生成器函数，每一项从页面中提取的数据以及每一个对链接页面的下载请求都由yield语句提交给Scrapy引擎
    def parse(self, response):
        # 提取页面中每个书籍页面的链接，用它们构造Request对象并提交
        # le = LinkExtractor(restrict_css='article.product_pod h3')
        le = LinkExtractor(restrict_xpaths='//*[@id="default"]/div/div/div/div/section/div[2]/ol/li')
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_book, method='GET',encoding='utf-8')
        # 提取页面中‘下一页’的书籍列表页面的链接，用它构造Request对象并提交
        # le = LinkExtractor(restrict_css = 'ul.pager li.next')
        le = LinkExtractor(restrict_css = '#default > div > div > div > div > section > div:nth-child(2) > div > ul > li.next')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse, method='GET',encoding='utf-8')

# 书籍详情页面的解析函数
    def parse_book(self,response):
        # 提取书籍信息存入BookItem对象
        book = BookItem()
        sel = response.css('div.col-sm-6.product_main')
        book['name'] = sel.xpath('./h1/text()').extract_first()
        book['price'] = sel.css('p.price_color::text').extract_first()
        review_ratings = sel.css('p.star-rating::attr(class)').extract_first()
        book['review_rating'] = re.sub(r"star-rating","",review_ratings)
        sel = response.css('#content_inner > article > table ') #sel = response.css('table.table.table-striped')
        book['upc'] = sel.xpath('.//tr[1]/td/text()').extract_first()
        stocks = sel.xpath('./tr[last()-1]/td/text()').extract_first()
        book['stock'] = re.sub("\D","",stocks)
        book['review_num'] = sel.xpath('./tr[7]/td/text()').extract_first()
        yield book
        