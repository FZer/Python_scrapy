# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time
from scrapy import signals
from selenium import webdriver
from scrapy import Request
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.downloadermiddlewares import downloadtimeout
from selenium.webdriver.support.wait import WebDriverWait

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

"""
class XiaohongSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)

        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
"""


class XiaohongDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    # def __init__(self):
    #     self.driver = webdriver.Chrome()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        if request.meta.get("middleware") == "XiaohongDownloaderMiddleware":
            self.driver.get(request.url)
            # cookie = self.driver.get_cookies()
        # ============滚动页面=============
            element = WebDriverWait(self.driver, 10, 0.5).until(
                lambda x: x.find_element(By.XPATH, "(//*[@class='dual-row'])[1]/div[1]/section[1]/a"))
            actions = ActionChains(self.driver)
            actions.click_and_hold(element).perform()
            while True:
                start_time = time.time()
                while True:
                    time.sleep(1)
                    actions.key_down(Keys.PAGE_DOWN).key_up(
                        Keys.PAGE_DOWN).perform()
                    elapsed_time = int(time.time() - start_time)
                    time.sleep(1)
                    if elapsed_time >= 10:
                        actions.key_down(Keys.PAGE_UP).key_up(
                            Keys.PAGE_UP).perform()
                        time.sleep(1)
                        actions.key_down(Keys.PAGE_UP).key_up(
                            Keys.PAGE_UP).perform()
                        break
                if self.driver.find_element(By.CSS_SELECTOR, '.swiper-slide-active .indicator > p').text == '没有更多了~':
                    break
        # ============滚动页面END=============
            body = self.driver.page_source
            return HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        self.driver = webdriver.Chrome()
        spider.logger.info("Spider opened: %s" % spider.name)

    def spider_closed(self, spider):
        self.driver.close()
        spider.logger.info("Spider closed: %s" % spider.name)


class RandomDelayMiddleware(object):
    def __init__(self, delay=5) -> None:
        self.delay = delay

    @classmethod
    def from_crawler(cls, crawler):
        return cls(delay=random.randint(3, 20))

    def process_request(self, request, spider):
        if 'download_latency' not in request.meta:
            request.meta['download_latency'] = self.delay
        return None


class RandomUserAgentMiddleware(object):
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class SeleniumType(Request):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)

        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
