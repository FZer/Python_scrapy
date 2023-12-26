# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# ==============FlySky================
from scrapy.exceptions import DropItem
#import MySQLdb

class ToscrapeBookPipeline(object):
    def process_item(self, item, spider):
        return item

# ================FlySky================
class BookPipeline(object):
    review_rating_map = {
    ' One':1,
    ' Two':2,
    ' Three':3,
    ' Four':4,
    ' Five':5,
    }
    def process_item(self,item,spider):
        rating = item.get('review_rating')
        if rating:
            item['review_rating'] = self.review_rating_map[rating]
        return item

#---------------英镑兑换人民币汇率-----------------
class PriceConverterPipeline(object):
    exchange_rate = 8.5309
    def process_item(self,item,spider):
        #提取item的price字段；去掉英镑符号，转换为float类型，乘以汇率
        price = float(item['price'][1:])*self.exchange_rate
        #保留2位小数，赋值回给item的price字段
        item['price'] = '￥%.2f'%price
        return item

# 以书名作为主键，对爬取到信息去重
class DuplicatesPipeline(object):
    # 增加构造器方法，在其中初始化用于对书名去重的集合
    def __init__(self):
        self.book_set = set()
    # process_item方法
    def process_item(self,item,spider):
        name = item['name'] #取出item的name字段
        if name in self.book_set:   #检查书名是否已在集合book_set中
            raise DropItem('Duplicate book found:%s'%item)  #抛出DropItem异常，抛弃Item
        self.book_set.add(name) #将item的name字段存入集合
        return item
"""
#创建MySQLPipeline,将数据入库
class MySQLPipeline():
    def open_spider(self,spider):
        db=spider.settings.get('MYSQL_DB_NAME','scrapy')
        host=spider.settings.get('MYSQL_HOST','localhost')
        #port=spider.settings.get('MYSQL_PORT','3306')
        user=spider.settings.get('MYSQL_USER','root')
        passwd=spider.settings.get('MYSQL_PASSWORD','123456')
        self.db_conn=MySQLdb.connect(host=host,db=db,user=user,passwd=passwd,charset='utf8')
        self.db_cur=self.db_conn.cursor()
    def close_spider(self,spider):
        self.db_conn.commit()
        self.db_conn.close()
    def process_item(self,item,spider):
        self.insert_db(item)
        return item
    def insert_db(self,item):
        values=(
        item['upc'],
        item['name'],
        item['price'],
        item['review_rating'],
        item['review_num'],
        item['stock'],
        )
        sql='INSERT INTO books VALUES (%s,%s,%s,%s,%s,%s)'
        self.db_cur.execute(sql,values)
"""