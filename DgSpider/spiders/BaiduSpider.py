# -*- coding: utf-8 -*-
import scrapy
from DgSpider.items import TencentItem

class BaiduspiderSpider(scrapy.Spider):
    name = 'BaiduSpider'
    allowed_domains = ["tencent.com"]
    url = "http://hr.tencent.com/position.php?&start="
    offset = 0
    # 起始url
    start_urls = [url + str(offset)]
    def parse(self, response):
        print('lala')
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            #初始化模型
            item = TencentItem()
            # 职位名称
            item['positionname'] = each.xpath("./td[1]/a/text()").extract()[0]
            # 详情连接
            item['positionlink'] = each.xpath("./td[1]/a/@href").extract()[0]
            # 职位类别
            item['positionType'] = each.xpath("./td[2]/text()").extract()[0]
            # 招聘人数
            item['peopleNum'] = each.xpath("./td[3]/text()").extract()[0]
            # 工作地点
            item['workLocation'] = each.xpath("./td[4]/text()").extract()[0]
            # 发布时间
            item['publishTime'] = each.xpath("./td[5]/text()").extract()[0]
            yield item
        if self.offset < 1680:
            self.offset += 10
        #从新获取信息
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

