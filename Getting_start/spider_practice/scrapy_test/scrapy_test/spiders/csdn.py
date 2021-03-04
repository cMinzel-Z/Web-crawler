# -*- coding: utf-8 -*-
from urllib import parse
from datetime import datetime
import re
import time
from selenium import webdriver

import scrapy



class CsdnSpider(scrapy.Spider):
    name = 'csdn'

    browser = webdriver.Chrome(executable_path="C:\Z_TOOL\Chrome_Webdriver\chromedriver.exe")
    browser.get("https://bbs.csdn.net/")
    
    cookies = browser.get_cookies()
    global cookie_dict
    cookie_dict = {}
    
    for item in cookies:
        cookie_dict[item['name']] = item['value']
    
    def start_requests(self):
        urls = [
            'https://bbs.csdn.net/forums/ios',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, cookies=cookie_dict)
    
    def parse(self, response):
        for topic in response.css('tbody > tr'):
            yield {
                'title': topic.css('.forums_topic > a::text').get(),
                'author': topic.css('.forums_author > a::text').get(),
                'time': topic.css('.forums_author > em::text').get(),
                'reply_num': topic.css('.forums_reply > span::text').getall(),
            }
            
        next_page = response.css('thead > tr:nth-child(1) > td > div > div > a::attr(href)')[-1].get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, cookies=cookie_dict)
