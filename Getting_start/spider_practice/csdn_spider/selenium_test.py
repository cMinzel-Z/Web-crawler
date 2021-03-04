# -*- coding: utf-8 -*-

#import time
from selenium import webdriver
from scrapy import Selector
from selenium.common.exceptions import NoSuchElementException


browser = webdriver.Chrome(executable_path="#\chromedriver.exe")
#browser = webdriver.Firefox()

browser.get("https://item.jd.com/7652013.html")

sel = Selector(text=browser.page_source)
#print(browser.page_source)
#with open(r"#\jd.txt","w", encoding='utf-8') as f:
#        f.write(browser.page_source)

try:
    click_ele = browser.find_element_by_xpath("//li[@class='shangpin|keycount|product|shangpinpingjia_1']")
    click_ele.click()
except NoSuchElementException as e:
    pass

print(sel.xpath("//span[@clstag='price J-p-7652013']/text()").extract()[0])
browser.close()