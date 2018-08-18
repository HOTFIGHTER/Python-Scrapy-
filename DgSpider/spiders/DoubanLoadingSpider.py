# coding=utf-8
import scrapy
import urllib
import urllib.parse as urlparse
import io
from PIL import Image
from DgSpider.items import DoubanMovieCommentItem
from faker import Factory

f = Factory.create()


class DoubanLoadingSpider(scrapy.Spider):
    name = 'DoubanLoadingSpider'
    allowed_domains = ['accounts.douban.com', 'douban.com']
    start_urls = ['https://www.douban.com/']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'accounts.douban.com',
        'User-Agent': f.user_agent()
    }

    formdata = {
        'form_email': '1848084079@qq.com',
        'form_password': '10113397',
        'captcha-solution': '',
        'captcha-id': '',
        'login': '登录',
        'redir': 'https://www.douban.com/',
        'source': 'None'
    }

    def start_requests(self):
        return [scrapy.Request(url='https://www.douban.com/accounts/login',
                               headers=self.headers,
                               meta={'cookiejar': 1},
                               callback=self.parse_login)]

    def parse_login(self, response):
            # 如果有验证码要人为处理
      if b'captcha_image' in response.body:
        print('Copy the link:')
        link = response.xpath('//img[@class="captcha_image"]/@src').extract()[0]
        print(link)
        file = io.StringIO(urllib.urlopen(link).read())
        img = Image.open(file)
        img.show()
        captcha_solution = input('captcha-solution:')
        captcha_id = urlparse.parse_qs(urlparse.urlparse(link).query, True)['id']
        self.formdata['captcha-solution'] = captcha_solution
        self.formdata['captcha-id'] = captcha_id
        return [scrapy.FormRequest.from_response(response,
                                                 formdata=self.formdata,
                                                 headers=self.headers,
                                                 meta={'cookiejar': response.meta['cookiejar']},
                                                 callback=self.after_login
                                                 )]


    def after_login(self, response):
        print(response.status)
        self.headers['Host'] = "www.douban.com"
        yield scrapy.Request(url='https://movie.douban.com/subject/22266320/reviews',
                             meta={'cookiejar': response.meta['cookiejar']},
                             headers=self.headers,
                             callback=self.parse_comment_url)
        yield scrapy.Request(url='https://movie.douban.com/subject/22266320/reviews',
                             meta={'cookiejar': response.meta['cookiejar']},
                             headers=self.headers,
                             callback=self.parse_next_page,
                             dont_filter=True)  # 不去重


    def parse_next_page(self, response):
        print(response.status)
        try:
            next_url = response.urljoin(response.xpath('//span[@class="next"]/a/@href').extract()[0])
            print("下一页")
            print(next_url)
            yield scrapy.Request(url=next_url,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 headers=self.headers,
                                 callback=self.parse_comment_url,
                                 dont_filter=True)
            yield scrapy.Request(url=next_url,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 headers=self.headers,
                                 callback=self.parse_next_page,
                                 dont_filter=True)
        except:
            print("Next page Error")
            return


    def parse_comment_url(self, response):
        print(response.status)
        for item in response.xpath('//div[@class="main review-item"]'):
            comment_url = item.xpath('header/h3[@class="title"]/a/@href').extract()[0]
            comment_title = item.xpath('header/h3[@class="title"]/a/text()').extract()[0]
            print(comment_title)
            print(comment_url)
            yield scrapy.Request(url=comment_url,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 headers=self.headers,
                                 callback=self.parse_comment)


    def parse_comment(self, response):
        print(response.status)
        for item in response.xpath('//div[@id="content"]'):
            comment = DoubanMovieCommentItem()
            comment['useful_num'] = item.xpath('//div[@class="main-panel-useful"]/button[1]/text()').extract()[0].strip()
            comment['no_help_num'] = item.xpath('//div[@class="main-panel-useful"]/button[2]/text()').extract()[0].strip()
            comment['people'] = item.xpath('//span[@property="v:reviewer"]/text()').extract()[0]
            comment['people_url'] = item.xpath('//header[@class="main-hd"]/a[1]/@href').extract()[0]
            comment['star'] = item.xpath('//header[@class="main-hd"]/span[1]/@title').extract()[0]
            data_type = item.xpath('//div[@id="link-report"]/div/@data-original').extract()[0]
            print("data_type: " + data_type)
            if data_type == '0':
                comment['comment'] = "\t#####\t".join(
                    map(lambda x: x.strip(), item.xpath('//div[@id="link-report"]/div/p/text()').extract()))
            elif data_type == '1':
                comment['comment'] = "\t#####\t".join(
                    map(lambda x: x.strip(), item.xpath('//div[@id="link-report"]/div[1]/text()').extract()))
            comment['title'] = item.xpath('//span[@property="v:summary"]/text()').extract()[0]
            comment['comment_page_url'] = response.url
            # print comment
            yield comment
