# -*- coding: utf-8 -*-
import os
import scrapy
import pickle
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import LagouJobItem, LagouJobItemLoader
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from settings import BASE_DIR
import time

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    # 对传入的link进行预处理
    # restrict_css参数可以选择提取的区域
    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),
        Rule(LinkExtractor(allow=("gongsi/.*",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )
    
    """
    CrawlSpider中不能覆盖parse函数
    如果要覆盖，则选择parse_start_url和process_results函数
    """
    
#    def parse_start_url(self, response):
#        return []
#
#    def process_results(self, response, results):
#        return results
    
    def start_requests(self):
        # 如果不是第一次登陆则使用cookie
        cookies = []
        if os.path.exists(BASE_DIR+"/cookies/lagou.cookie"):
            cookies = pickle.load(open(BASE_DIR+"/cookies/lagou.cookie", "rb"))
            
        if not cookies:
            # 去使用selenium模拟登陆后，拿到cookie交给scrapy的request使用
            browser = webdriver.Chrome(executable_path="C:\Z_TOOL\Chrome_Webdriver\chromedriver.exe")
            browser.get("https://www.lagou.com/")
            # 登陆
            browser.find_element_by_css_selector(".tab.focus").click()
            browser.find_element_by_css_selector(".lg_tbar_r ul li a.login").click()
            time.sleep(10)
            browser.find_element_by_css_selector(
                    "input.input.login_enter_password.HtoC_JS:nth-child(1)").send_keys(Keys.CONTROL + "a")
            browser.find_element_by_css_selector(
                    "input.input.login_enter_password.HtoC_JS:nth-child(1)").send_keys("#")
            time.sleep(10)
            browser.find_element_by_css_selector(
                    "input[type='password']").send_keys(Keys.CONTROL + "a")
            browser.find_element_by_css_selector(
                    "input[type='password']").send_keys("#")
            time.sleep(10)
            browser.find_element_by_css_selector(
                    ".login-btn.login-password.sense_login_password.btn-green").click()
            
            time.sleep(10)
            cookies = browser.get_cookies()
            print("这是cookies")
            print(cookies)
            # 写入cookie到文件中
            pickle.dump(cookies, open(BASE_DIR+"/cookies/lagou.cookie", "wb"))
        
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]
        
        for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, cookies=cookie_dict)
        
    
    def parse_job(self, response):
        # 解析拉勾网的职位
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css(".job-name h1::text")
        
        job_item = item_loader.load_item()
        
        return job_item
