# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsObj = BeautifulSoup(html, features="lxml")

# 通过css中的class属性获得
# 绿色人物名字
nameList = bsObj.findAll("span", {"class":"green"})
for name in nameList:
    print(name.get_text())
    
nameList_num = bsObj.findAll(text="the prince")
print(len(nameList_num))