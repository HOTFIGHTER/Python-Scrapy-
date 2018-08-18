# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
class DgspiderPipeline(object):
    def __init__(self):
        self.filename = open("tencent.json", "w",encoding='utf-8')

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.filename.write(text)
        return item

    def close_spider(self, spider):
        self.filename.close()

class DoubanPipeline(object):
    def __init__(self):
        self.filename = open("douban.json", "w",encoding='utf-8')

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.filename.write(text)
        return item

    def close_spider(self, spider):
        self.filename.close()
