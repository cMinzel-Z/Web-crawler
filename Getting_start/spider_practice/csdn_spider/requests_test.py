# -*- coding: utf-8 -*-

import time
import requests

from selenium import webdriver


browser = webdriver.Chrome(executable_path="C:\Z_TOOL\Chrome_Webdriver\chromedriver.exe")
browser.get("https://bbs.csdn.net/")

time.sleep(5)
cookies = browser.get_cookies()
cookie_dict = {}

for item in cookies:
    cookie_dict[item['name']] = item['value']
    
print(requests.get("https://bbs.csdn.net/forums/ios", cookies=cookie_dict).text)
