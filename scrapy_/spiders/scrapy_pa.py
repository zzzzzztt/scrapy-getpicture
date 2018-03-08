# -*- coding:utf-8 -*-
from scrapy_.items import Girl
import scrapy,urllib,threading
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#设置最大线程锁
thread_lock=threading.BoundedSemaphore(value=10)


def download(url,name):
    urllib.urlretrieve(url, 'D:\\1\\1\\' + '%s.jpg' % name)

class Girl_spider(scrapy.Spider):
    # 必须定义
    name = 'girl'
    download_delay=1
    # 初始urls
    start_urls = ["http://www.lesmao.cc/plugin.php?id=group&page=1"]
    allow_urls=['lesmao.cc']
    # 默认response处理函数

    def parse(self, response):
        # print response.text
        for i in response.xpath("//div[@id = 'index-pic']/div/div/a/@href").extract():
            yield scrapy.Request(i, callback=self.parse_pic)

    def parse_pic(self, response):
        item = Girl()
        item['pic_url'] = response.selector.xpath("//li/img/@src").extract()
        item['pic_name'] = response.selector.xpath("//li/img/@alt").extract()
        pages_link = response.xpath("//div[@id = 'thread-page']/a/@href").extract()    #下一页
        if len(pages_link):
            yield scrapy.Request(pages_link[0], callback=self.parse_pic)
        else :
            print"end"
        yield item

        num_pic=0
        for i in item['pic_url']:
            download(i,item['pic_name'][0]+i[-19:-16]+str(num_pic))
            num_pic += 1


