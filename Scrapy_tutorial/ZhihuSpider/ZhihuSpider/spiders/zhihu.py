# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# 使用第三方的库来模拟鼠标点击验证码
#from mouse import move, click
import time

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def start_requests(self):
        """     
        webdriver被知乎识别，需要手动启动chrome
        cd到chrome.exe位置
        run: chrome.exe --remote-debugging-port=9222
        启动之前确保所有的chrome实例已经关闭
        """
        chrome_option = Options()
        chrome_option.add_argument("--disable-extensions")
#        chrome_option.add_experimental_option('excludeSwitches', ['load-extension', 'enable-automation'])
        chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        # selenium打开chrome
        browser = webdriver.Chrome(executable_path="C:\Z_TOOL\Chrome_Webdriver\chromedriver.exe",
                                   chrome_options=chrome_option)
        browser.get("https://www.zhihu.com/signin")
        
        # 通过CSS选择器输入登陆信息
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(Keys.CONTROL + "a")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
            "#")

        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
            "#")
        
        """
#        使用第三方的库来模拟鼠标点击验证码
#        move方法中的两个参数是鼠标坐标
#        move(954, 654)
#        click()
        """
        # .click()并不能完成点击, 使用.send_keys(Keys.ENTER)
        browser.find_element_by_css_selector(
            ".Button.SignFlow-submitButton.Button--primary.Button--blue").send_keys(Keys.ENTER)
  
        time.sleep(60)
    