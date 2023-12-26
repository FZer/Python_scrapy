# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import openpyxl
from itemadapter import ItemAdapter


class XiaohongPipeline:

    def __init__(self):
        print("===========开始写入数据============")
        self.excel = openpyxl.Workbook()
        self.excel_sheet = self.excel.active
        self.excel_sheet.append([
            '文章标题', '文章点赞', '作者', '小红书号', 'IP地', '文章内容', '热门评论', '文章链接',
            '作者链接'
        ])

    def process_item(self, item, spider):
        print(f'正在保存：{item["title"]}')
        line = [
            item['title'], item['article_likes'], item['author'], item['userID'],
            item['userIP'], item['content'], item['review'], item['article_url'],
            item['author_url']
        ]
        self.excel_sheet.append(line)
        return item

    def close_spider(self, spider):
        self.excel.save('xiaohongshu.xlsx')
        self.excel.close()
        print("==============数据保存完毕=============")
