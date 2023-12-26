from typing import Iterable
import scrapy
import re
from scrapy.http import Request
from scrapy.selector import Selector
from ..items import XiaohongItem
import browser_cookie3
import requests


class XiaohongSpSpider(scrapy.Spider):
    name = "xiaohong_sp"
    allowed_domains = ["www.xiaohongshu.com"]

    # start_urls = [
    #     "https://www.xiaohongshu.com/page/topics/5c038e973947d90001ec5504?fullscreen=true"]

    # scrapy原来对于start_urls的处理,只需要重写start_requests()方法即可

    def start_requests(self) -> Iterable[Request]:
        start_urls = "https://www.xiaohongshu.com/page/topics/62b973f05d7a7d00014bbc69?fullscreen=true"
        yield scrapy.Request(
            start_urls,
            method="GET",
            callback=self.parse,
            meta={"middleware": "XiaohongDownloaderMiddleware"})
        # return super().start_requests()

    def parse(self, response, **kwargs):
        selector = Selector(response=response)
        sel = selector.css('.reds-note-body')
        article_urls = selector.xpath(
            '//a[@class="reds-note-trigger"]/@href').getall()
        info = zip(sel, article_urls)
        for elem, article_url in list(info):
            item = XiaohongItem()
            title = elem.css('.note-title::text').getall()[0]
            article_likes = elem.css('.reds-note-like-text::text').getall()[0]
            author = elem.css('.reds-note-user-text::text').getall()[0]
            review_url = re.sub(
                r"/discovery/item/",
                "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id=",
                article_url)
            review_url = review_url + "&image_formats=jpg,webp,avif"
            article_url = article_url.replace(
                "/discovery/item/", "https://www.xiaohongshu.com/explore/")
            author_url = elem.css('.note-footer > a::attr(href)').getall()[0]
            author_url = "https://www.xiaohongshu.com" + author_url
            item['title'] = title
            item['article_likes'] = article_likes
            item['author'] = author
            item['article_url'] = article_url
            item['author_url'] = author_url
            item['review_url'] = review_url
            yield scrapy.Request(meta={'item': item},
                                 url=article_url,
                                 callback=self.parse_article)

    def parse_article(self, response, **kwargs):
        item = response.meta['item']
        selector = Selector(response=response)
        article_content = selector.css(
            '#detail-desc > span:nth-child(1)::text').getall()  # 文章内容
        item['content'] = str(article_content)
        yield scrapy.Request(meta={'item': item},
                             url=item['author_url'],
                             callback=self.parse_author)

    def parse_author(self, response, **kwargs):
        item = response.meta['item']
        selector = Selector(response=response)
        author_id = selector.css('.user-content .user-redId::text').getall()
        author_ip = selector.css('.user-content .user-IP::text').getall()
        # item['userID'] = str(author_id)
        # item['userIP'] = str(author_ip)
        if len(author_id) > 0:
            item['userID'] = re.sub(r'小红书号：', '', author_id[0])
        if len(author_ip) > 0:
            item['userIP'] = re.sub(r' IP属地：', '', author_ip[0])
        else:
            item['userIP'] = '空'
        cookie_jar = browser_cookie3.firefox(domain_name='.xiaohongshu.com')
        cookie_dict = requests.utils.dict_from_cookiejar(cookie_jar)
        yield scrapy.Request(meta={'item': item},
                             url=item['review_url'], cookies=cookie_dict,
                             callback=self.parse_review, dont_filter=True)

    def parse_review(self, response, **kwargs):
        item = response.meta['item']
        print('=============打印item=============\n', item)
        item['review'] = response.text
        yield item
