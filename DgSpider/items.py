# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DgspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TencentItem(scrapy.Item):
    # 职位名
    positionname = scrapy.Field()
    # 详情连接
    positionlink = scrapy.Field()
    # 职位类别
    positionType = scrapy.Field()
    # 招聘人数
    peopleNum = scrapy.Field()
    # 工作地点
    workLocation = scrapy.Field()
    # 发布时间
    publishTime = scrapy.Field()


class DoubanBookItem(scrapy.Item):
    name = scrapy.Field()  # 书名
    price = scrapy.Field()  # 价格
    edition_year = scrapy.Field()  # 出版年份
    publisher = scrapy.Field()  # 出版社
    ratings = scrapy.Field()  # 评分
    author = scrapy.Field()  # 作者
    content = scrapy.Field()
