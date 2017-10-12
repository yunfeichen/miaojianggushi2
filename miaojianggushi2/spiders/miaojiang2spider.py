# -*- coding: utf-8 -*-
import os
import urllib

import scrapy
import re

from scrapy import Selector, Request

from miaojianggushi2.items import Miaojianggushi2Item


class NgaSpider(scrapy.Spider):
    name = "miaojianggushi2"
    host = "http://www.miaojianggushi2.cc/"
    # 这个例子中只指定了一个页面作为爬取的起始url
    # 当然从数据库或者文件或者什么其他地方读取起始url也是可以的
    start_urls = [
        "http://www.miaojianggushi2.cc/",
    ]

    # 爬虫的入口，可以在此进行一些初始化工作，比如从某个文件或者数据库读入起始url
    def start_requests(self):
        for url in self.start_urls:
            # 此处将起始url加入scrapy的待爬取队列，并指定解析函数
            # scrapy会自行调度，并访问该url然后把内容拿回来
            yield Request(url=url, callback=self.parse_url)

    # 版面解析函数，解析一个版面上的帖子的标题和地址
    def parse_url(self, response):
        selectorurl = Selector(response)
        url_list = selectorurl.xpath("//div[@class='booklist clearfix']/span/a['@href']")
        #print type(url_list)
        #exit(0)
        for url in url_list:
            url_true = url.xpath('@href').extract()[0]
            #print url_true
            #exit(0)
            yield Request(url=url_true, callback=self.parse_page)
            #exit(0)
    def parse_page(self, response):
        print response.url
        aaa = response.url
        type(aaa)
        file_name = re.split('\/',aaa)[-1]
        print file_name
        selector = Selector(response)
        content_list = selector.xpath("//div[@id='BookText']/text()").extract()
        content_title = selector.xpath("//div[@class='chaptertitle clearfix']/h1/text()").extract()[0]
        print content_title
        content_all = ""
        for content in content_list:
            #print content
            content_all = content_all + content
        #print content_all
        item = Miaojianggushi2Item()
        item['contect'] = content_all
        print  item['contect']
        absoluteSrc = aaa
        file_path = os.path.join("D:\\novel\\miaojianggushi2", file_name)  # 拼接这个图片的路径，我是放在F盘的pics文件夹下
        urllib.urlretrieve(absoluteSrc, file_path)
        yield item