# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, features="lxml")

# 子标签处理
for child in bsObj.find("table",{"id":"giftList"}).children:
    print(child)

print("-"*20)

# 兄弟标签处理
for sibling in bsObj.find("table",{"id":"giftList"}).tr.next_siblings:
    print(sibling)
    
print("-"*20)

# 父标签处理
print(bsObj.find("img",{"src":"../img/gifts/img1.jpg"
}).parent.previous_sibling.get_text())
